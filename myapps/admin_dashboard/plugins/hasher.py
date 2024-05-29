import random
import string
from cryptography.fernet import Fernet




def randomCharacter(length):  
    letters = string.ascii_lowercase # define the specific string  
    # define the condition for random.sample() method  
    result = ''.join((random.sample(letters, length)))   
    return result
  




# https://www.geeksforgeeks.org/how-to-encrypt-and-decrypt-strings-in-python/
def hasherGenerator():
    '''
    word hasherGenerator. Can be used for hashing password, create a session pass key.
    '''

    message=randomCharacter(10)
    key = Fernet.generate_key()
    # Instance the Fernet class with the key
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message.encode())
    return {'key':key, 'message':message, 'encoded':encMessage}



def decrypter(key, encoded):
    '''
    data: is passed in as a dictionary. {'key':key, 'message':message, 'encoded':encMessage}
    '''
    fernet = Fernet(key)
    result = fernet.decrypt(encoded).decode()
    return result

# dt =  hasherGenerator()
# print(dt)
# d = decrypter(key=dt.get('key'), encoded=dt.get('encoded'))
# print(d)


def numbershuffler(limit:int=4):
    try:
        import random
        # Generate a list of numbers from 0 to 9
        result = ""
        numbers = list(range(10))
        # Shuffle the numbers randomly
        random.shuffle(numbers)
        # Print the shuffled numbers in groups of 4 digits
        for i in range(0, len(numbers), limit):
            group = numbers[i:i+limit]
            return ''.join(map(str, group))
    except:
        pass
        
