def nwd(a, b):
   while a != b:
      if a > b:
         a = a - b
      else:
         b = b - a
   return a

a = int(input('a = '))
b = int(input('b = '))

print('NWD =', nwd(a, b))