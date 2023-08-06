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
import networkx as nx
import matplotlib.pylab as plt
import jaxlib
from orderedset import OrderedSet

from .__main__ import get_info as get_info,init_function

from .autodiff import *
from .utils import *
from mpi4py import MPI

comm = MPI.COMM_WORLD

def run(func,jacobians = []):

    #Compute the actual Jacobians to be computed via AD 
    info =  get_info(func)
    output_channels = info['output_channels']
    input_channels  = info['input_channels']

    AD_jacobians = []
    for jac in jacobians:
        if not jac in output_channels:
           AD_jacobians.append(jac)
    #--------       
    

    if len(AD_jacobians) == 0:

        #print('Function')  
        def wrapper(*args):
            args = get(args[0],channels=input_channels)
            if not type(args) == list: args = [args]
            value = func(*args)
            if not type(value) in (list,tuple): value = [value]
            value = {channel:{'data':value[n],'version':None}  for n,channel in enumerate(get_info(func)['output_channels'])}

            return {'__elba__':value} 

        return wrapper

    else:
      return jacobian(func,AD_jacobians)  



def compare_data(var1,var2):
         """compare hashable data for caching"""
         if hasattr(var1,'ndim'):
            if var1.ndim == 0: #in case of 0-d arrays
                  return var1 == var2
         if isinstance(var2,jaxlib.xla_extension.DeviceArray):
            var2 = np.array(var2) 
              
         return DeepHash(var1)[var1] == DeepHash(var2)[var2]



def get_version(channel,data):


    version = None
    if comm.rank == 0: 
     cache = os.getcwd() + '/.elba/'
     with shelve.open(cache + '/_data', 'c',writeback=True) as shelf:
            if not channel in shelf.keys():
                shelf[channel] = {0:data} #Init data
                version = 0
            else:
                for key,value in shelf[channel].items():
                    if compare_data(value,data):
                        version =  key #It is already stored
                        break
                if version == None:    
                 version = len(shelf[channel])    
                 shelf[channel].update({version:data}) 
    comm.Barrier()    
    return comm.bcast(version,root=0)


def save_state(func,inputs,outputs,jacobians=[]):
  
       """save the function state"""

       info = get_info(func)
       output_versions = None
       if comm.rank == 0:
        input_versions = [inputs['__elba__'][channel]['version'] for channel in info['input_channels'] ]
        input_versions.append(info['code'])

        cache = os.getcwd() + '/.elba/'

        with shelve.open(cache + '/_state', 'c',writeback=True) as shelf:
             output_versions = [len(shelf[info['name']])]*len(info['output_channels']+jacobians)
             shelf[info['name']].update({dill.dumps(input_versions):output_versions})
     
        with shelve.open(cache + '/_data', 'c',writeback=True) as shelf:
           for n,channel in enumerate(info['output_channels']+jacobians):
             shelf.setdefault(channel,{})[output_versions[n]] = outputs['__elba__'][channel]['data']        

       output_versions = comm.bcast(output_versions,root=0)


       for n,name in enumerate(info['output_channels']+jacobians): outputs['__elba__'][name]['version'] = output_versions[n]

       return outputs


def convert_to_elba(func,retain_state,*args):

    input_channels = get_info(func)['input_channels']

    def is_elba(x):
      if type(x) == dict:
        if '__elba__' in x.keys():
            return True
      return False  

    output = {}

    for n,arg in enumerate(args):
        if is_elba(arg):
            if retain_state:
             output.update(arg['__elba__'])
            else: 
             item = arg['__elba__']   
             output.update({input_channels[n]:list(item.values())[0]})
             translate(list(item.keys())[0],input_channels[n])

        else:
            version = get_version(input_channels[n],arg)
            output.update({input_channels[n]:{'data':arg,'version':version}})

    #Default to empty dictionaries if a channel is missing           
    for channel in input_channels:
       if not channel in output.keys():
            version = get_version(channel,{})
            print_command('Default ',channel)
            output.update({channel:{'data':{},'version':version}})

    return {'__elba__':output}

def load_state(func,inputs,jacobians=[]):

    info = get_info(func)

    input_versions = [inputs['__elba__'][channel]['version']  for channel in info['input_channels'] ]

    for version in input_versions:
        if version == None:
            return {'__elba__':{}}

    #TODO: if the data being passed is new there is not need to check for the state. We need a flag to indicate that this is new data

    input_versions.append(info['code'])

    if comm.rank == 0:
     cache = os.getcwd() + '/.elba/'
     with shelve.open(cache + '/_state', 'r') as shelf:
           if dill.dumps(input_versions) in shelf[info['name']].keys():

               output_versions =  shelf[info['name']][dill.dumps(input_versions)]

               output = {(info['output_channels']+jacobians)[n]:{'version':version,'data':None} for n,version in enumerate(output_versions)} #There is no need to retrieve data at this point
           else: output = {}
    else: output = None

   
    output = comm.bcast(output,root=0)

    return {'__elba__':output}


def elba(_func=None, *,jacobians=[],retain_state=False):
    def decorator(func):
        if int(os.environ['BYPASS_ELBA']) == 1:
          def wrapper(*args, **kwargs): return func(*args,**kwargs)
          return wrapper

        else:
         init_function(func)
         @functools.wraps(func)
         def wrapper(*args, **kwargs):
            args  = convert_to_elba(func,retain_state,*args)
            state = load_state(func,args,jacobians=jacobians)
            if len(state['__elba__']) == 0:
               
             print_command('RUN ',get_info(func)['name'])
             
             outputs = run(func,jacobians = jacobians)(args) 
             if retain_state:
              args['__elba__'].update(save_state(func,args,outputs,jacobians=jacobians)['__elba__'])
             else: 
              args = save_state(func,args,outputs,jacobians=jacobians)

            else:
             if retain_state:
              args['__elba__'].update(state['__elba__']) #for now store all the variables on the graph (gargabe will be needed)
             else: 
              args=state   

            return args

         return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)

def filter_data(data,channels):

    output = {channel: data['__elba__'][channel] for channel in channels}

    return {'__elba__':output}






def load_function(function):

    cache = os.getcwd() + '/.elba/'
    with shelve.open(cache + '/_functions', 'r') as shelf:
        return dill.loads(shelf[function]['function'])
