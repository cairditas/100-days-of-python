import random
from turtle import Turtle, Screen
from random import randint
import colorgram

t = Turtle()
screen = Screen()

full_circle = 360

t.shape("classic")


def set_random_color():
    screen.colormode(255)
    t.pencolor(randint(0, 255), randint(0, 255), randint(0, 255))


def square():
    for num in range(4):
        t.forward(100)
        t.left(90)


def dashed_square():
    t.speed(10)
    side_length = 50
    dash_length = 3
    t.right(180)
    for num in range(4):
        for n in range(0, side_length, dash_length):
            t.forward(dash_length)
            t.up()
            t.forward(dash_length)
            t.down()
        t.left(90)


def draw_sided_shapes_from_3_to_n(sides: int):
    side_length = 50
    for shape in range(3, sides + 1):
        angle = full_circle / shape
        for side in range(1, shape + 1):
            t.forward(side_length)
            t.right(angle)


def random_walk(steps: int):
    t.speed("fastest")
    set_random_color()
    for _ in range(steps):
        t.pensize(5)
        t.setheading(random.choice([0, 90, 180, -90]))
        t.forward(50)


def spirograph(num_circles: int):
    t.speed("fastest")
    turn_degree = full_circle / num_circles
    for _ in range(num_circles):
        set_random_color()
        t.setheading(t.heading() + turn_degree)
        t.circle(125)


def hirst(row_dots: int, column_dots: int):
    screen.colormode(255)
    colors = colorgram.extract('hirst.jpg', 12)
    t.hideturtle()

    t.up()
    t.goto(-((column_dots - 1) * 30) // 2, ((row_dots - 1) * 30) // 2)

    for i in range(column_dots):  # ← outer loop = rows
        # 1. Draw one full row of dots (moving right)
        for j in range(row_dots):  # ← inner loop = columns/dots in row
            random_color = colors[random.randrange(0, len(colors))].rgb  # fixed index (0-based)
            r, g, b = int(random_color.r), int(random_color.g), int(random_color.b)
            t.dot(15, (r, g, b))
            t.up()

            if j < row_dots - 1:  # don't move after last dot in row
                t.forward(30)

        # 2. After finishing the row → move to start of next row
        if i < column_dots - 1:  # don't do this after the last row
            # Turn around + move down + turn back to face right
            if i % 2 == 0:
                t.right(90)  # was facing right → turn down
                t.forward(30)
                t.right(90)  # now facing left (for next row)
            else:
                t.left(90)  # was facing left → turn down
                t.forward(30)
                t.left(90)  # now facing right again


def orient_before_start(width: int, height: int):
    t.up()
    t.backward(width / 2)
    t.right(90)
    t.forward(height / 2)
    t.left(90)


# square()
# dashed_square()
# draw_sided_shapes_from_3_to_n(10)
# random_walk(200)
# spirograph(100)
hirst(8, 5)

screen.exitonclick()
