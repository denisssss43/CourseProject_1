
isError = False
isInfo = False
isWarning = False

def INFO(string):
    if isError: print('LOG INF: ', string)
def ERROR(string):
    if isInfo: print('LOG ERR: ', string)
def WARNING(string):
    if isWarning: print('LOG WARNING: ', string)
