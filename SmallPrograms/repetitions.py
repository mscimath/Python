# Breaking out of a repetition loop
"""
i = 1 
while (i <= 10):
	print( i )
	if ( i == 5 ):
		print("i is 5; We're 'outta here!")
		break
	i = i + 1

# Skipping code without breaking out of the loop 

i = 1
while ( i <= 10 ):
	if ( i > 3 and i < 8 ):
		i = i + 1
		continue
	print( i )
	i = i + 1
"""

# Skipping code in a for loop

names = [ 'John', 'Roberto', 'Hua', 'Emma' ]
for name in names:
	if not(name == 'Roberto'):
		print(name)