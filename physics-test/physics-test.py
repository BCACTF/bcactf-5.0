from random import randint, choice

flag = open("flag.txt", "r").read()

def clear():
    print("\n\n---------------------------------------------------------------------\n\n")
print("Welcome to the Midterm Review!")
print("This review will test your knowledge of physics formulas we have learned this unit.")
print("Be sure to write all of your answers in terms of x and y!")
clear()

questions = [("Question {}: A box starts at rest on a frictionless table. It has a constant acceleration of x. How far does it travel in y seconds?", "x*y*y/2"),
             ("Question {}: A spring has a spring constant of x. If it is compressed by a distance of y, what is the magnitude of the restoring force? (Your answer should be positive.)", "x*y"),
             ("Question {}: A red ball (with mass 1kg and velocity x) and a blue ball (with mass 2kg and velocity y) collide perfectly inelastically. What is the final velocity of the two balls?", "(x+2*y)/3"),]

i = 0
while True:
    i += 1
    q = choice(questions)
    print(q[0].format(i))
    answer = input("Answer: ")
    for char in ".=_{}'\" \t\n\r\x0b\x0c:;":
        if char in answer:
            print(f"Dangerous character ({char})!")
            exit()
    print("Running tests...")
    
    for _ in range(10):
        x = randint(0, 100)
        y = randint(0, 100)
        expected = eval(q[1], {'__builtins__': None, 'ord': ord, 'len': len}, {'x': x, 'y': y, 'flag': flag}) 
        res = eval(answer, {'__builtins__': None, 'ord': ord, 'len': len}, {'x': x, 'y': y, 'flag': flag})
        if expected != res:
            print(f"TEST FAILED!")
            break
        if _ == 9:
            print(f"Good job!")
            break
    clear()
