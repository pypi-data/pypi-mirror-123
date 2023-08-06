import os

os.environ['ELBA_DEBUG']='0'
os.environ['BYPASS_ELBA']='0'
os.environ['ELBA_AUTODIFF']='0'

from elba.elba       import elba as elba
from elba.elba       import get as get
from elba.elba       import load_function as load_function



