import random

heart = 3
score = 0
lvl = 1
question = ""
choices = []  # Initialize as an empty list at startup
operations = ["+", "-", "*", "/"]

# State variables to hold current problem numbers
num1 = 0
num2 = 0
num3 = 0
rand_operation = ""
second_oper = ""
correct_answer = 0

def question_generator():
    global num1, num2, num3, rand_operation, second_oper, question, correct_answer, lvl, choices
    
    # Recalculate level dynamically based on current score
    lvl = (score // 5) + 1
    max_val = 10 if lvl < 2 else 100

    # Pick operations per turn
    rand_operation = random.choice(operations)
    second_oper = random.choice(operations)
    
    num1 = random.randint(1, max_val)
    num2 = random.randint(1, max_val)
    num3 = random.randint(1, max_val)

    # --- Division Validation Rules ---
    # Rule 1: Validate first operator division
    if rand_operation == "/" and (num2 == 0 or num1 % num2 != 0):
        return question_generator()  # Retry cleanly with 'return'
        
    # Rule 2: Validate second operator division (only matters at Level 3)
    if lvl == 3 and second_oper == "/" and (num3 == 0 or num2 % num3 != 0):
        return question_generator()  # Retry cleanly with 'return'

    # --- Calculate Answers and Format Strings ---
    if lvl == 3:
        expr = f"{num1} {rand_operation} {num2} {second_oper} {num3}"
    else:
        expr = f"{num1} {rand_operation} {num2}"

    # Use int() around eval to cleanly handle division types (e.g., 4 / 2 = 2.0 -> 2)
    correct_answer = int(eval(expr))
    question = f"{expr}"

    # --- Generate Choices fresh for this specific question ---
    choices = [
        correct_answer, 
        correct_answer + random.randint(1, 5), 
        correct_answer - random.randint(1, 5), 
        correct_answer + random.randint(6, 12)
    ]
    random.shuffle(choices)

def check_answer(ans):
    global score, heart
    
    
    try:
        ans = int(ans)
    except (ValueError, TypeError):
        heart -= 1
        return False

    if ans == correct_answer:
        score += 1
        return True
    else:
        heart -= 1
        return False
