from random import randint, choice

flag = open("flag.txt", "r").read()

def clear():
    print("\n\n-----------------------------------\n\n")
print("Welcome to the Midterm Review!")
print("This review will test your knowledge of physics formulas we have learned this unit.")
clear()

questions = [("Question 1: A box starts at rest on a frictionless table. It has a constant acceleration of a. How far does it travel in b seconds?", "a*b*b/2")]

while True:
    q = choice(questions)
    print(q[0])
    answer = input("Answer: ")
    print("Running tests...")
    
    for _ in range(10):
        a = randint(0, 100)
        b = randint(0, 100)
        expected = eval(q[1],  {'__builtins__': None}, {'a': a, 'b': b, 'flag': flag}) 
        res = eval(answer, {'__builtins__': None}, {'a': a, 'b': b, 'flag': flag})
        if expected != res:
            print(f"TEST FAILED!")
            break
        if _ == 9:
            print(f"Good job!")
            break
    clear()
