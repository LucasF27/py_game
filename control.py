__author__ = 'Lucas'

def control_signal(error):
    p = 5
    i = 1
    c = p*error[-1] + i*sum(error)
    return round(c/10)*10