import re

def is_camel_or_pascal_case(word):
    # Check if the word is in camel-case or Pascal-case
    return re.match(r'^[a-z]+(?:[A-Z][a-z]*)*$', word) is not None



# for word in words:
#     if is_camel_or_pascal_case(word):
#         print(f"'{word}' is in camel-case or Pascal-case")
#     else:
#         print(f"'{word}' is not in camel-case or Pascal-case")

