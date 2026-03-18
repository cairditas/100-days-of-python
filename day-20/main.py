import turtle
import random
import time

# --- Constants ---
WINDOW_SIZE = 800
GRID_SIZE = 20
CELL_SIZE = WINDOW_SIZE // GRID_SIZE  # 40px per cell
HALF = WINDOW_SIZE // 2
SPEED = 0.15  # seconds per frame

# --- Setup Screen ---
screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("black")
screen.setup(width=WINDOW_SIZE + 20, height=WINDOW_SIZE + 40)
screen.tracer(0)

# --- Persistent Turtles ---
score_pen = turtle.Turtle()
score_pen.hideturtle()
score_pen.penup()
score_pen.color("white")

snake_pen = turtle.Turtle()
snake_pen.hideturtle()
snake_pen.penup()
snake_pen.speed(0)

food_pen = turtle.Turtle()
food_pen.hideturtle()
food_pen.penup()
food_pen.speed(0)

overlay_pen = turtle.Turtle()
overlay_pen.hideturtle()
overlay_pen.penup()
overlay_pen.color("white")

border_pen = turtle.Turtle()
border_pen.hideturtle()
border_pen.speed(0)

# Button turtles
btn_yes = turtle.Turtle()
btn_yes.hideturtle()
btn_yes.penup()
btn_yes.speed(0)

btn_no = turtle.Turtle()
btn_no.hideturtle()
btn_no.penup()
btn_no.speed(0)

btn_label_yes = turtle.Turtle()
btn_label_yes.hideturtle()
btn_label_yes.penup()
btn_label_yes.color("white")

btn_label_no = turtle.Turtle()
btn_label_no.hideturtle()
btn_label_no.penup()
btn_label_no.color("white")

# --- Button config ---
BTN_W = 140
BTN_H = 55
BTN_YES_X = -100
BTN_NO_X  =  100
BTN_Y     = -100

# --- Draw Border ---
def draw_border():
    border_pen.clear()
    border_pen.penup()
    border_pen.color("white")
    border_pen.goto(-HALF, -HALF)
    border_pen.pendown()
    border_pen.pensize(3)
    for _ in range(4):
        border_pen.forward(WINDOW_SIZE)
        border_pen.left(90)
    border_pen.penup()

# --- Helpers ---
def draw_square(t, x, y, color, size):
    t.goto(x, y)
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(4):
        t.forward(size - 2)
        t.left(90)
    t.end_fill()

def draw_rounded_rect(t, cx, cy, w, h, fill_color, outline_color):
    """Draw a filled rectangle centred on (cx, cy)."""
    t.penup()
    t.color(outline_color, fill_color)
    t.goto(cx - w / 2, cy - h / 2)
    t.pendown()
    t.begin_fill()
    for length in [w, h, w, h]:
        t.forward(length)
        t.left(90)
    t.end_fill()
    t.penup()

def cell_to_pixel(gx, gy):
    px = -HALF + gx * CELL_SIZE
    py = -HALF + gy * CELL_SIZE
    return px, py

def random_food_pos(snake_body):
    while True:
        gx = random.randint(0, GRID_SIZE - 1)
        gy = random.randint(0, GRID_SIZE - 1)
        if (gx, gy) not in snake_body:
            return gx, gy

def draw_game(snake, food_pos):
    snake_pen.clear()
    food_pen.clear()
    for i, (gx, gy) in enumerate(snake):
        px, py = cell_to_pixel(gx, gy)
        color = "#00FF41" if i == 0 else "#007A1E"
        draw_square(snake_pen, px, py, color, CELL_SIZE)
    fx, fy = food_pos
    px, py = cell_to_pixel(fx, fy)
    draw_square(food_pen, px, py, "red", CELL_SIZE)

def update_score(score):
    score_pen.clear()
    score_pen.goto(0, HALF - 30)
    score_pen.write(f"Score: {score}", align="center", font=("Arial", 18, "bold"))

def show_overlay(lines):
    overlay_pen.clear()
    for y_offset, text, font_size in lines:
        overlay_pen.goto(0, y_offset)
        overlay_pen.write(text, align="center", font=("Arial", font_size, "bold"))

def clear_overlay():
    overlay_pen.clear()

# --- Play Again Buttons ---
def show_play_again_buttons(score):
    # Dim overlay text
    show_overlay([
        (80,  "GAME OVER",        40),
        (10,  f"Final Score: {score}", 26),
        (-50, "Play Again?",      22),
    ])

    # YES button (green)
    draw_rounded_rect(btn_yes, BTN_YES_X, BTN_Y, BTN_W, BTN_H, "#1a7a1a", "#00FF41")
    btn_label_yes.goto(BTN_YES_X, BTN_Y - 14)
    btn_label_yes.write("YES", align="center", font=("Arial", 22, "bold"))

    # NO button (red)
    draw_rounded_rect(btn_no, BTN_NO_X, BTN_Y, BTN_W, BTN_H, "#7a1a1a", "#FF4141")
    btn_label_no.goto(BTN_NO_X, BTN_Y - 14)
    btn_label_no.write("NO", align="center", font=("Arial", 22, "bold"))

    screen.update()

def hide_play_again_buttons():
    btn_yes.clear()
    btn_no.clear()
    btn_label_yes.clear()
    btn_label_no.clear()

def in_button(mx, my, cx, cy):
    return (cx - BTN_W / 2 <= mx <= cx + BTN_W / 2 and
            cy - BTN_H / 2 <= my <= cy + BTN_H / 2)

def wait_for_button_click():
    """Block until the user clicks YES or NO. Returns True for YES, False for NO."""
    result = [None]

    def on_click(x, y):
        if result[0] is not None:
            return
        if in_button(x, y, BTN_YES_X, BTN_Y):
            result[0] = True
        elif in_button(x, y, BTN_NO_X, BTN_Y):
            result[0] = False

    screen.onclick(on_click)

    while result[0] is None:
        screen.update()
        time.sleep(0.05)

    screen.onclick(None)
    return result[0]

# --- Countdown ---
def show_countdown():
    for i in range(3, 0, -1):
        show_overlay([(20, "Get Ready!", 30), (-40, str(i), 60)])
        screen.update()
        time.sleep(1)
    clear_overlay()
    screen.update()

# --- Key state ---
direction = (1, 0)
next_direction = (1, 0)

def go_up():
    global next_direction
    if direction != (0, -1):
        next_direction = (0, 1)

def go_down():
    global next_direction
    if direction != (0, 1):
        next_direction = (0, -1)

def go_left():
    global next_direction
    if direction != (1, 0):
        next_direction = (-1, 0)

def go_right():
    global next_direction
    if direction != (-1, 0):
        next_direction = (1, 0)

screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(go_right, "Right")

# --- Main Game Function ---
def run_game():
    global direction, next_direction

    start_x = GRID_SIZE // 2
    start_y = GRID_SIZE // 2
    snake = [(start_x - i, start_y) for i in range(3)]
    direction = (1, 0)
    next_direction = (1, 0)
    score = 0
    food_pos = random_food_pos(set(snake))

    draw_border()
    update_score(score)
    draw_game(snake, food_pos)
    screen.update()

    current_speed = SPEED

    while True:
        time.sleep(current_speed)

        direction = next_direction
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
            break
        if new_head in snake[1:]:
            break

        snake.insert(0, new_head)

        if new_head == food_pos:
            score += 1
            update_score(score)
            food_pos = random_food_pos(set(snake))
            # Speed up every 3 points (min delay of 0.05s)
            current_speed = max(0.05, SPEED - (score // 3) * 0.015)
        else:
            snake.pop()

        draw_game(snake, food_pos)
        screen.update()

    return score

# --- Main Program Loop ---
while True:
    score = run_game()

    show_play_again_buttons(score)
    play_again = wait_for_button_click()

    hide_play_again_buttons()
    clear_overlay()
    snake_pen.clear()
    food_pen.clear()
    score_pen.clear()
    screen.update()

    if not play_again:
        show_overlay([(0, "Thanks for playing! Goodbye :)", 22)])
        screen.update()
        time.sleep(2)
        break

    show_countdown()

screen.bye()