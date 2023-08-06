import os,shelve
import jax.numpy as jnp
import numpy as np
from termcolor import colored
from mpi4py import MPI

comm = MPI.COMM_WORLD

def print_command(cmd,text):
    if int(os.environ['EFUNX_DEBUG']) == 1:
      if comm.rank == 0:    
       print(colored(cmd,'green') + text)



def isnan(data):

    if type(data) == np.ndarray:
        return jnp.any(jnp.isnan(data))
    else:
        return data == None



def load_variable(channel,variable):
    print_command('LOAD ',channel + ' version: ' + str(variable['version']))
    cache = os.getcwd() + '/.elba/'

    with shelve.open(cache + '/_data', 'r') as shelf:
        if not channel in shelf.keys():
           with shelve.open(cache + '/_translator', 'r') as translator:
             input_channel = channel  
             channel = translator[channel]
             print_command('TRANSLATE ',channel + ' -> ' + input_channel)
        return shelf[channel][variable['version']]


def translate(key_1,key_2):
 
     if not key_1 == key_2:
       cache = os.getcwd() + '/.elba/'
       with shelve.open(cache + '/_translator', 'c',writeback=True) as shelf:
            shelf[key_2] = key_1
     

def get(data,channels='all'):

    def get_data(value,channel):

            if isnan(value['data']):
                return load_variable(channel,value)
            else:
                return value['data']

    output = []
    if channels == 'all':
        for channel,value in data['__elba__'].items():
            output.append(get_data(value,channel))
    else:

        if not type(channels) == list: channels = [channels]
        for channel in channels:
                
            output.append(get_data(data['__elba__'][channel],channel))

    if len(output) == 1: output = output[0]

    return output
