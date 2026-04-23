# 1. a student class with name, grade.
# add a method passed() that returns true if grade >= 60
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    def passed(self):
        return self.grade >= 60

# 2. make a rectangle class with width, height.
# add methods area() and perimeter()
class Rectangle:
    def __init__ (self, width, height):
        self.width = width
        self.height = height
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
    
# 3. create a parent class employee with name, salary
# then create a child class manager with extra attribute: department
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    
class Manager(Employee):
    def __init__ (self, department, name, salary):
        super().__init__(name,salary)
        self.department = department

