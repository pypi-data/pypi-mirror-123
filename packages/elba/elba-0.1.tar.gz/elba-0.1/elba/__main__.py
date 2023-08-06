import sys
import os
import cloudpickle as dill
from termcolor import colored, cprint 
import inspect
import os
import shutil
import shelve
from termcolor import colored
import importlib,yaml

#from .registry import *
#from .elba import *
from mpi4py import MPI
comm = MPI.COMM_WORLD


def init_function(func):

    info = get_info(func)
    if comm.rank == 0:
     #Init state
     cache = os.getcwd() + '/.elba/'
     with shelve.open(cache + '/_state', 'c',writeback=True) as shelf:
      shelf.setdefault(func.__name__,{})  
    #------------------------------------------    

     #Init function--
     cache = os.getcwd() + '/.elba/'
     with shelve.open(cache + '/_functions', 'c',writeback=True) as shelf:
         shelf[info['name']] = info

    return info


def get_info(func):

    data = func.__annotations__

    input_variables = []
    output_variables = []
    for key,value in data.items():
      if not key == 'return':
         input_variables.append(value.replace("'",''))
      else:
         value = value.replace('(','')
         value = value.replace(')','')
         value = value.split(',')
         output_variables  = value
         output_variables = [tmp.replace("'",'') for tmp in output_variables]

    #In this case we take the parameters
    if len(input_variables) == 0:
        input_variables = list(inspect.signature(func).parameters.keys())

    #Make a function a leaf so it runs
    leaf = False
    if len(output_variables) == 0:
       output_variables = [func.__name__]
       leaf = True

    try : 
        code = inspect.getsource(func)
      
    except OSError as error : 
        code = None 

    return  {'name':func.__name__,'input_channels':input_variables,'output_channels':output_variables,'leaf':leaf,'code':code,'function':dill.dumps(func)}
    


def load_file(filename,module_name,project):


   with open(filename, 'r') as stream:
      #stream = open(filename, 'r')
      main = yaml.safe_load(stream)[project]

      #Load dependences (project can't be specified)
      if 'dependences' in main.keys():
          for dep in main['dependences']:
              load_module(dep.split(':')[0],dep.split(':')[1]) 
      #-------------------------------
      funcs = main['functions']
      for function in funcs:
       
          function_name    = function.split(':')[-1]
          suffix           = function.split(':')[0] 
          full_module_name = module_name + '.' + suffix

          module = importlib.import_module(full_module_name)
          func   = getattr(module,function_name)   
          init_function(func)

      pipelines = main['pipelines']

      #Init function--
      cache = os.getcwd() + '/.elba/'
      with shelve.open(cache + '/_pipelines', 'c',writeback=True) as shelf:
        for pipeline in pipelines:    
         shelf.update(pipeline)
          

def load_module(module_name,project=None):
    """Loads a pip-installed module"""
    if comm.rank == 0:
        
     print(colored('Loading module ','green') + module_name + colored(' project ','green')+  module_name)

     module = importlib.import_module(module_name)
     filename = '/'.join(module.__file__.split('/')[:-1]) + '/elba.yaml'
     if not os.path.isfile(filename):
        print('No filename found')
        quit()

     load_file(filename,module_name,module_name)



def clear_cache():

      cache = os.getcwd() + '/.elba/'
      basename = cache + '/_data'
      with shelve.open(basename, 'c',writeback=True) as shelf:
            shelf.clear()

      basename = cache + '/_state'
      with shelve.open(basename, 'c',writeback=True) as shelf:
            shelf.clear()


def start_project():

      folder = os.getcwd() + '/.elba'

      if os.path.exists(folder):
          shutil.rmtree(folder)
      os.makedirs(folder)


      basename = folder + '/_functions'
      with shelve.open(basename, 'c',writeback=True) as shelf:
          shelf = {}


      basename = folder + '/_data'
      with shelve.open(basename, 'c',writeback=True) as shelf:
            shelf = {}

      basename = folder + '/_state'
      with shelve.open(basename, 'c',writeback=True) as shelf:
            shelf = {}


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]


    if args[0] == 'clear':

       clear_cache() 


    if args[0] == 'inspect':

      inspect_data()  
      #INIT REGISTRY LOCALLY  

    if args[0] == 'init':
      #INIT REGISTRY LOCALLY  

      folder = os.getcwd() + '/.elba'
      if os.path.exists(folder):
          shutil.rmtree(folder)
      os.makedirs(folder)

      #Start global project
      start_project()
      print(" ")
      print(colored('Init Efunx','blue'))
      print(" ")


    if args[0] == 'load':
       load_module(args[1]) 

    if args[0] == 'load_file':
       load_file(args[1]) 

    if args[0] == 'list':

      #Show functions 
      print(' ')
      print(colored('FUNCTIONS','blue'))
      cache = os.getcwd() + '/.elba/'
      with shelve.open(cache + '/_functions', 'r') as shelf:
        for key,values in shelf.items():
            print(colored(key,'green'),': ',values['input_channels'],'->',values['output_channels']) 

      print(colored('PIPELINES','blue'))
      with shelve.open(cache + '/_pipelines', 'r') as shelf:
        for key,values in shelf.items():
            print(colored(key,'green'),': ',values) 


#if __name__ == "__main__":
#    sys.exit(main())
