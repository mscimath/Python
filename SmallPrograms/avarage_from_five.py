# use a for loop to read exactly five values from the user and then display the avarage

sum = 0

for i in range(5):
   number = float(input("Enter a number: "))
   sum += number

avarage = sum / 5
print("The avarage of the number is", avarage)