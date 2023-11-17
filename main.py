import random


def get_question():
    with open('questions.txt', 'r', encoding='utf-8') as f:
        question_list = f.read().splitlines()
    number_question = random.randrange(0, len(question_list))
    question_answer = str(question_list[number_question])
    for i in range(len(question_answer)):
        if question_answer[i] == ';':
            question = question_answer[:i]
            answer = question_answer[i + 1:len(question_answer)]
    return answer, question


answer, question = get_question()
print(question)
print(answer)
