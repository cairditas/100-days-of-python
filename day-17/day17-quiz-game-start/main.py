from question_model import Question
from quiz_brain import QuizBrain
from data import question_data

questions = [Question(q["question"], q["correct_answer"]) for q in question_data]

# a = [print(q.answer) for q in questions]

quiz_brain = QuizBrain(questions)

while quiz_brain.still_has_question():
    quiz_brain.next_question()

print(f"You've completed the quiz. Your final score was: {quiz_brain.score}/{quiz_brain.question_number}.\n")