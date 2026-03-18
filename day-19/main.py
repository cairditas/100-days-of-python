import turtle
import random

# Setup screen
screen = turtle.Screen()
screen.title("Turtle Race!")
screen.bgcolor("white")
screen.setup(width=800, height=500)

COLORS = ["red", "orange", "green", "blue", "purple", "pink"]
START_X = -350
FINISH_X = 350
Y_POSITIONS = [-200, -120, -40, 40, 120, 200]

turtles = []

# Create turtles
for i, color in enumerate(COLORS):
    t = turtle.Turtle()
    t.shape("turtle")
    t.color(color)
    t.penup()
    t.goto(START_X, Y_POSITIONS[i])
    turtles.append(t)

# Draw finish line
finish = turtle.Turtle()
finish.hideturtle()
finish.penup()
finish.goto(FINISH_X, -250)
finish.pendown()
finish.pensize(3)
finish.color("black")
finish.goto(FINISH_X, 250)

# Label turtles
label_writer = turtle.Turtle()
label_writer.hideturtle()
label_writer.penup()
for i, color in enumerate(COLORS):
    label_writer.goto(START_X - 60, Y_POSITIONS[i] - 10)
    label_writer.color(color)
    label_writer.write(color, font=("Arial", 11, "bold"))

# Ask user for their pick
user_choice = screen.textinput(
    "Place your bet!",
    f"Which turtle will win?\nColors: {', '.join(COLORS)}\n\nEnter color:"
)

if user_choice:
    user_choice = user_choice.strip().lower()

# Race!
winner = None
while winner is None:
    for t in turtles:
        t.forward(random.randint(5, 15))
        if t.xcor() >= FINISH_X:
            winner = t
            break

# Announce result
winner_color = winner.pencolor()
result_writer = turtle.Turtle()
result_writer.hideturtle()
result_writer.penup()
result_writer.goto(0, 0)

if user_choice == winner_color:
    msg = f"🎉 {winner_color.upper()} wins!\nYou guessed right — YOU WIN!"
    result_writer.color("green")
else:
    msg = f"{winner_color.upper()} wins!\nYou picked {user_choice} — Better luck next time!"
    result_writer.color("red")

result_writer.write(msg, align="center", font=("Arial", 18, "bold"))

screen.exitonclick()