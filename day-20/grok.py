import turtle
import random

# Global variables
dx = 20
dy = 0
score = 0
delay = 130
game_is_on = True
segments = []
food = None
pen = None
wn = None

def update_delay():
    global delay
    levels = score // 3
    delay = max(50, 130 - levels * 10)

def go_up():
    global dx, dy
    if dy != -20:
        dx = 0
        dy = 20

def go_down():
    global dx, dy
    if dy != 20:
        dx = 0
        dy = -20

def go_left():
    global dx, dy
    if dx != 20:
        dx = -20
        dy = 0

def go_right():
    global dx, dy
    if dx != -20:
        dx = 20
        dy = 0

def spawn_food():
    global food
    while True:
        x = random.randrange(-380, 381, 20)
        y = random.randrange(-380, 381, 20)
        food_pos = (x, y)
        if food_pos not in [seg.pos() for seg in segments]:
            break
    food.goto(x, y)

def move_snake():
    global score, game_is_on
    head = segments[0]
    new_x = head.xcor() + dx
    new_y = head.ycor() + dy

    # Check wall collision
    if new_x > 380 or new_x < -380 or new_y > 380 or new_y < -380:
        game_over()
        return

    # Check body collision (skip tail as it will move)
    for seg in segments[1:-1]:
        if seg.xcor() == new_x and seg.ycor() == new_y:
            game_over()
            return

    # Record old tail position
    old_tail_pos = segments[-1].pos()

    # Move body segments (shift)
    for i in range(len(segments) - 1, 0, -1):
        segments[i].setpos(segments[i - 1].pos())

    # Move head
    segments[0].setpos(new_x, new_y)

    # Check if ate food
    if segments[0].distance(food) < 15:
        score += 1
        update_delay()
        pen.clear()
        pen.write(f"Score: {score}", align="center", font=("Arial", 24, "normal"))
        spawn_food()

        # Grow snake
        new_tail = turtle.Turtle()
        new_tail.speed(0)
        new_tail.shape("square")
        new_tail.color("lime")
        new_tail.penup()
        new_tail.setpos(old_tail_pos)
        segments.append(new_tail)

def game_over():
    global game_is_on
    game_is_on = False
    pen.goto(0, 0)
    pen.write("GAME OVER", align="center", font=("Arial", 36, "bold"))
    pen.goto(0, -40)
    pen.write(f"Final Score: {score}", align="center", font=("Arial", 24, "normal"))
    wn.exitonclick()

def move():
    global game_is_on
    if game_is_on:
        move_snake()
    wn.update()
    wn.ontimer(move, delay)

# Set up the screen
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("black")
wn.setup(800, 800)
wn.tracer(0)
wn.listen()
wn.onkey(go_up, "Up")
wn.onkey(go_down, "Down")
wn.onkey(go_left, "Left")
wn.onkey(go_right, "Right")

# Create pen for score
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 370)
pen.write("Score: 0", align="center", font=("Arial", 24, "normal"))

# Create snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)
segments.append(head)

# Create initial body segments (3 total)
for pos in [(-20, 0), (-40, 0)]:
    seg = turtle.Turtle()
    seg.speed(0)
    seg.shape("square")
    seg.color("lime")
    seg.penup()
    seg.goto(pos)
    segments.append(seg)

# Create food
food = turtle.Turtle()
food.speed(0)
food.shape("square")
food.color("red")
food.penup()
food.shapesize(0.8, 0.8)  # Tiny square
spawn_food()

# Start the game
wn.update()
move()
wn.mainloop()