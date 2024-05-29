import uuid


def generator(length=8):
    '''
    *** Internal System Code Generator ***
    This code generator, uses the uuid package.
    '''
    code = f"{uuid.uuid4().hex}"[:length]
    return code