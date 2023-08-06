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

from .__main__ import get_info as get_info,init_function
#from elba import config as config
from .utils import get

def jacobian(func,variables):
    """ Compute Jacobians for generic input/output variable combinations """

    if not type(variables) == list: variables = [variables]

    x = list(OrderedSet([v.split(':')[1] for v in variables]))  
    y = list(OrderedSet([v.split(':')[0] for v in variables])) 

    info = get_info(func)

    argnums_input  = sorted(list([info['input_channels'].index(i) for i in x]))
    argnums_output = list([info['output_channels'].index(i) for i in y])

    def wrapper(*argv) :

      #Retrieve dat============
      data = get(*argv,channels=info['input_channels'])
      if not type(data) == list:
          data = [data]
      #=========================
      values,jac = jax.value_and_jacrev(func,argnums=argnums_input)(*data)
      
      if not type(values) in (list,tuple): values= [values]

      output = {variable:{'data':values[n],'version':None} for n,variable in enumerate(info['output_channels'])}
      
      #Store gradient 
      for l,(j,t) in enumerate(zip(*(argnums_output,y))):
              for k,(i,r) in enumerate(zip(*(argnums_input,x))):
                    variable = t + ':' + r
                    if variable in variables:
                        if len(argnums_output) > 1:
                          output[t + ':' + r] = {'data':jac[l][k],'version':None}
                        else:  
                          output[t + ':' + r] = {'data':jac[k],'version':None}
                    #else:      
                    # variable = t + ':' + x[0]
                    # 
                    # output[variable] = {'data':jac[l],'version':None}

      return {'__elba__':output}
  
    return wrapper

def make_fun(strc,function_name):
    exec(strc)
    return locals()[function_name]


@jax.jit
def dot_product_4_4(a,b):
    return jnp.einsum('ijlk,lkyt->ijyt',a,b)

@jax.jit
def dot_product_2_4(a,b):
    return jnp.einsum('  lk,lkyt->yt',a,b)

def generalized_dot_product(a,b):

    if a.ndim == 4 and b.ndim == 4:
       return dot_product_4_4(a,b)
    elif a.ndim == 2 and b.ndim == 4:
       return dot_product_2_4(a,b)
    else:
        print('TO be implemented ',a.ndim,b.ndim)
        quit()


def compute_chains(G,forward_path,jacs):

   #Compute jacobian chains:
   diff_workflow = {}
   ad_jacs = {p:set() for p in forward_path}
   for jac in jacs:

         diff_workflow[jac] = {}

         v1,v2 = jac.split(':')
         if len(forward_path) == 1: #Single-node function
             if v1 in output_channels[forward_path[0]] and v2 in input_channels[forward_path[0]]:
                 ad_jacs[path[0]].add(v1 + ':' + v2)
         else:       
                 
          if input_channels_map[v2]==output_channels_map[v1]: #in case of single node
                paths = [[input_channels_map[v2]]]
          else:   
             paths = list(nx.all_simple_paths(G, source=input_channels_map[v2], target=output_channels_map[v1]))
        
          for path in paths:
             index = len(diff_workflow[jac])
             diff_workflow[jac][index] = []
             #------------------------------------------------------
             old_v = v2
             for p in range(len(path)):
                 if p < len(path)-1:   
                   v = list(set(output_channels[path[p]]).intersection(set(input_channels[path[p+1]])))[0]
                   variable= v + ':' + old_v
                   if not variable in output_channels[path[p]]:
                      ad_jacs[path[p]].add(variable)
                      diff_workflow[jac][index].append(variable)
                   old_v = v
             variable= v1 + ':' + old_v
             if not variable in output_channels[path[-1]]:
                 ad_jacs.setdefault(path[-1]).add(variable)
                 diff_workflow[jac][index].append(variable)
             #-------------------------------------------------------      
             #Build Jvp
   
   #Build Jvp----
   #print(diff_workflow)
   fnames = []
   for key,value in diff_workflow.items():
       v1,v2   = key.split(':')
       jac_out = v1 + ':' + v2
       for path_index,var_vec in value.items() :
           for n,jac in enumerate(var_vec):
            if n == 0:
              output_old = jac# + str(path_index)
            else:   
              jac_in      = jac
              output      = jac.split(':')[0] + ':' +  v2 + '_' + str(path_index)

              #Create function
              function_name = 'Jvp_' + output.replace(':','_') 
              strc = 'def ' + function_name +  '(a:"' + jac_in + '",b:"' + output_old + '")->"' + output +'":\n return generalized_dot_product(a,b)'
              init_function(make_fun(strc,function_name))
              fnames.append(function_name)
              ad_jacs[function_name] = set()
              #----------------------
 
              output_old  = output

       #Now sum contributions from jacobians associates to different paths
       if len(var_vec) > 1:
        function_name = 'sum_jacobians_' + jac_out.replace(':','_')
        strc = 'def ' + function_name +  '('
        return_strc = ''
        for k  in range(len(value)):
            strc += 'a_' + str(k) + ':"' + jac_out +  '_' + str(k) + '",'   
            return_strc += 'a_' + str(k) + '+'

        strc = strc[:-1] + ')->"' + jac_out + '":\n return ' + return_strc[:-1]       
        init_function(make_fun(strc,function_name))
        ad_jacs[function_name] = set()
        fnames.append(function_name)

   return fnames,ad_jacs



