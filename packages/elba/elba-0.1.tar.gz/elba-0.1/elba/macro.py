import jax
import jax.numpy as jnp
import numpy as np
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import functools
import os
import time
import shelve
from deepdiff import DeepDiff,DeepHash
import cloudpickle as dill
from termcolor import colored
import networkx as nx
import matplotlib.pylab as plt
import jaxlib
from orderedset import OrderedSet
from .autodiff import *

from .__main__ import get_info as get_info,init_function
#from elba import config as config
from .elba import *

def visualize(G):

     pos = graphviz_layout(G, prog='neato')
     nx.draw(G,with_labels=True,pos=pos)
     plt.show()


def get_channels():

       input_channels      = {}
       output_channels     = {}
       output_channels_map = {}
       input_channels_map = {}
       cache = os.getcwd() + '/.elba/'
       with shelve.open(cache + '/_functions', 'r') as shelf:
           for key,value in shelf.items():
               for channel in value['output_channels']:
                 output_channels[channel] = key
               for channel in value['input_channels']:
                 input_channels_map[channel] = key
               input_channels[key] = value['input_channels']
               output_channels_map[key] = value['output_channels']
  
       return input_channels,output_channels,output_channels_map,input_channels_map         


def import_pipeline(pipeline): 

      if comm.rank == 0:
       cache = os.getcwd() + '/.elba/'
       with shelve.open(cache + '/_pipelines', 'c',writeback=True) as shelf:
          path = shelf[pipeline].split(',') 
      else: path = None    
      return comm.bcast(path)

def macro(outputs,inputs,pipeline=None,state={}):

   if not type(outputs)==list:
       outputs = [outputs]
   if not type(inputs)==list:
       inputs = [inputs]
   original_outputs = outputs.copy()  

   #Augment outputs/inputs if jacobians are needed
   jacs = [] #These are the jacobians we need---
   for i in outputs:
       if ':' in i:
           jacs.append(i)
           v1,v2 = i.split(':')
           inputs.append(v2)
           outputs.append(v1)
   for jac in jacs:        
    outputs.remove(jac)
   #---------------------------- 

   import networkx as nx
   G = nx.DiGraph()

   input_channels,output_channels_map,output_channels,input_channels_map = get_channels()

   inputs_left = inputs + list(state.keys())
   original_inputs_left = inputs_left.copy()

   max_iter = 100
   def tree(channel,head,k):

      if not channel in original_inputs_left:
        
       function = output_channels_map[channel]
       G.add_node(function)  
       if not head == None:     
        G.add_edge(function,head)

       inputs = input_channels[function]
       for channel in inputs:
           if channel in inputs_left:
                  inputs_left.remove(channel)
                  if len(inputs_left) == 0:
                     return
           else: 
                  k +=1
                  if k > max_iter:
                     print('Exceed max iteration')
                     quit()
                  tree(channel,function,k)

   if pipeline == None:
    for channel in outputs:
        tree(channel,None,0)
    forward_path = list(nx.dfs_postorder_nodes(G))[::-1]
   else:
    if type(pipeline) == list:
       forward_path = pipeline
    else:   #Load
      forward_path = import_pipeline(pipeline)
      
      old_node = None   
      for node in forward_path: #We build a simple graph from pipeline
        G.add_node(node)
        if not old_node == None:
          G.add_edge(old_node,node)
        old_node = node  
    #---------------------------

   #visualize(G)

   fnames,ad_jacs = compute_chains(G,forward_path,jacs)
   forward_path += fnames


   print_command('WORKFLOW ',' -> '.join([str(i) for i in forward_path]))
   #Convert states
   ss = {'__elba__':{channel:{'version':get_version(channel,data),'data':data}for channel,data in state.items()}}

   #Init state
   def wrapper(*args):

    #Convert inputs    
    state = {'__elba__':{channel:{'version':get_version(channel,data),'data':data}for channel,data in zip(*(inputs,args))}}

    state['__elba__'].update(ss['__elba__'])

    cache = os.getcwd() + '/.elba/'
    with shelve.open(cache + '/_functions', 'r') as shelf:
      for f in forward_path:
       info  = shelf[f]
       state = elba(dill.loads(info['function']),jacobians=list(ad_jacs[f]),retain_state=True)(state)
    
    #filter only the intended output
    return filter_data(state,original_outputs)

   return wrapper    

