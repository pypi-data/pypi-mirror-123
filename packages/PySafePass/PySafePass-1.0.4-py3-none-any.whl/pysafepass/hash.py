import hashlib


def hashdata(data:str)->str:
    '''
    Generates hash of data passed as parameter and returns hashed str
    '''
    data = data.encode('utf-8')
    hashed_data = hashlib.md5(data).hexdigest()
    return hashed_data
