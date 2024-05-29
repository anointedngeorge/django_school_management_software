import random
import string
from datetime import date



def shuffler(w1,w2,size=6,step=1):
    import math
    import random
    try:
        """
        This function requires 
        w1 = "myfirst leter"
        w2 = "second letter"
        size = "The length of the code generated"
        """
        full_word = f"{w1}{w2}"
        mt = math.pow(len(full_word), len(w1)) * 1000
        rd =  random.randint(a=0, b=mt)
        code = str(f"{full_word}{rd}").upper()
        f = list(code)
        random.shuffle(f)
        reshuffled = ''.join(f)
        return reshuffled[:size:step]
    except:
        pass



def generateUniqueId():
    # Generate 6 random numbers
    random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(6))
    # Generate 3 random capital alphabets
    random_alphabets = ''.join(random.choice(string.ascii_uppercase) for _ in range(3))
    # Combine numbers and alphabets with a hyphen
    unique_id = f"{random_numbers}{random_alphabets}"
    return unique_id


def generateUniqueSalesHash():
    random_numbers = ''.join(str(random.randint(1, 9)) for _ in range(6))
    random_numbers2 = ''.join(str(random.randint(0, 9)) for _ in range(6))
    unique_id = f"{random_numbers}{random_numbers2}"
    return unique_id


def generateStaffID():
    year = date.today().year
    brandInitials = "EUS"
    random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(3))
    staff_unique_id = f"{year}/{brandInitials}/{random_numbers}"
    return staff_unique_id




def shufflerWithoutInt(size=6,step=1):
    import random
    import string
    try:
        f = list(string.ascii_letters)
        random.shuffle(f)
        reshuffled = ''.join(f)
        return reshuffled[:size:step]
    except:
        pass