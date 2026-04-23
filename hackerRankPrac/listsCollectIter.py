# 1. given [1,2,3,4,5], create a new list with each number doubled
numbers = [1,2,3,4,5]
doubled = [num * 2 for num in numbers]
print(doubled)

# 2. count how many times each letter appears in "banana" using a dictionary
word = "banana"
count = {}
for letter in word:
    if letter in count:
        count[letter] += 1
    else:
        count[letter] =1
print(count)

# 3. remove duplicate from a list using a set
list = [1,2,3,4,5]
unique = set(list)
print(unique)

# 4. loop through a dictionary and print each key and value
my_dict = {
    'a': 1, 
    'b': 2, 
    'c': 3
}
for key,value in my_dict.items():
    print(f"{key}: {value}")