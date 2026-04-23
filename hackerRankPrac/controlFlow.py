# 1. print all even numbers from 1 to 20
for i in range(1,21):
    if i % 2 == 0:
        print(i)

# 2. write a program that prints:
# fizz for multiples of 3
# buzz for multiples of 5
# fizzbuzz for both
# otherwise the number
for i in range(1,101):
    if i % 3 == 0 and i % 5 == 0:
        print("fizzbuzz")
    elif i % 3 == 0:
        print("fizz")
    elif i % 5 == 0:
        print("buzz")
    else:
        print(i)

# 3. write a while loop to count down from 5 to 1
num = 5
while num > 1:
    print(num)
    num -= 1