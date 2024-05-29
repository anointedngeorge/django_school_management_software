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


def actionparam(
        title='',
        url='',
        has_modal=False,
        is_active=True,
        classicon='',
        query={}
    ):
    return dict({
        'title':title,
        'url':url,
        'has_modal':has_modal,
        'is_active':is_active,
        'classicon':classicon,
        'query':query
    })



def checkIfIsAmongA2Z(string):
    import re
    pattern = r'[A-Z]'
    matches = re.findall(pattern, string)
    print(matches)