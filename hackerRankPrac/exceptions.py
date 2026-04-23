# 1. write code that asks for a number and prints 100/number
# handle: invalid integer input, division by zero
def division():
    try:
        num = int(input("enter a number: "))
        result = 100/num
        print(result)
    except ValueError:
        print("invalid integer input")
    except ZeroDivisionError:
        print("cant divide by zero")

# 2. write a function get_item(list,index) that safely returns a list item
# if the index is out of range, return "invalid index"
def get_item(lst, index):
    try:
        return lst[index]
    except IndexError:
        return "invalid index"

# 3. write a function that raises a ValueError if a password is shorter than 8 characters
def password_check(password):
    if len(password) < 8:
        raise ValueError("your password must be more than 8 characters")