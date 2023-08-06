import os


def set_debug(a):

     if a:
      os.environ['EFUNX_DEBUG'] = '1'
     else: 
      os.environ['EFUNX_DEBUG'] = '0'

def set_bypass(a):

     if a:
      os.environ['BYPASS_EFUNX'] = '1'
     else: 
      os.environ['BYPASS_EFUNX'] = '0'

def set_autodiff(a):

     if a:
      os.environ['ELBA_AUTODIFF'] = '1'
     else: 
      os.environ['ELBA_AUTODIFF'] = '0'

