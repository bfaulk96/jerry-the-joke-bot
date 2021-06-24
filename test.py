import random
#

# print("&".join(list(filter(lambda x: (x != ""), ["cat=meow", "", "dog=woof"]))))

mentions = ['@one', '@two', '@three']
print(f'{", ".join(mentions[:-1])}, and {mentions[-1]}')
