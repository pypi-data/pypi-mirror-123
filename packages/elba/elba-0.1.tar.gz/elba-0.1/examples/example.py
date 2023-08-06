from elba import elba,get,config
config.set_debug(True)

@elba
def add(a,b):

    return a+b


@elba
def multiply(c,d):

    return c*d

add(1.0,2.0)

print(get(multiply(add(1.0,2.0),3.0)))












