from turtle import Turtle, Screen
import time
import random

WHITE = "white"

# ====================== 1. BASE CLASS FOR ALL GAME TURTLES ======================
# All visual elements inherit from this base class for consistent setup (speed, penup)
class GameTurtle(Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)               # Fastest drawing speed
        self.penup()                # No drawing lines when moving

# ====================== 2. SCORE DISPLAY CLASS ======================
# Handles displaying and updating scores at specific positions
# Used for both player and computer scores
class ScoreDisplay(GameTurtle):
    def __init__(self, x, y, label):
        super().__init__()
        self.goto(x, y)
        self.color(WHITE)
        self.hideturtle()           # Invisible turtle, only text visible
        self.label = label

    def update(self, score):
        """Clear and rewrite the score text"""
        self.clear()
        self.write(f"{self.label}: {score}", align="center", font=("Courier", 24, "normal"))

# ====================== 3. CENTER LINE CLASS ======================
# Draws the static dotted dividing line once
class CenterLine(GameTurtle):
    def __init__(self):
        super().__init__()
        self.color(WHITE)
        self.goto(0, 290)
        self.setheading(270)        # Point downward
        # Draw 25 dotted segments
        for _ in range(25):
            self.pendown()
            self.forward(15)
            self.penup()
            self.forward(15)
        self.hideturtle()           # Hide after drawing

# ====================== 4. BASE PADDLE CLASS ======================
# Common functionality for both paddles (movement, collision shape)
class Paddle(GameTurtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("square")
        self.color(WHITE)
        self.speed(0)
        self.shapesize(stretch_wid=5, stretch_len=1)  # Tall thin rectangle
        self.goto(x, y)

    def move_up(self):
        """Move up, clamped to top edge"""
        y = self.ycor()
        if y < 250:
            self.sety(y + 25)

    def move_down(self):
        """Move down, clamped to bottom edge"""
        y = self.ycor()
        if y > -250:
            self.sety(y - 25)

# ====================== 5. COMPUTER PADDLE SUBCLASS (inherits from Paddle) ======================
# Adds AI movement logic - chases ball with slight delay for beatable difficulty
class ComputerPaddle(Paddle):
    def ai_move(self, ball):
        """AI: incrementally follow ball's Y position"""
        if self.ycor() < ball.ycor() - 15:
            self.sety(self.ycor() + 7.5)
        elif self.ycor() > ball.ycor() + 15:
            self.sety(self.ycor() - 7.5)

# ====================== 6. BALL CLASS ======================
# Handles all ball movement, bounces, resets, and speed increases
class Ball(GameTurtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color(WHITE)
        self.goto(0, 0)
        self.base_speed = 0.28
        self.dx = self.base_speed      # Initial direction: rightward
        self.dy = self.base_speed      # Initial vertical speed
        self.last_speed_increase = 0   # Tracks speed milestones

    def move(self):
        """Update position based on velocity"""
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

    def bounce_y(self):
        """Reverse vertical direction (top/bottom wall)"""
        self.dy *= -1

    def bounce_x(self):
        """Reverse horizontal direction (paddle hit)"""
        self.dx *= -1

    def reset(self):
        """Reset to center with fresh random direction"""
        self.goto(0, 0)
        self.dx = self.base_speed * random.choice([1, -1])
        self.dy = random.uniform(-0.3, 0.3)

    def increase_speed(self):
        """Increase speed every 5 total points (gradual + cap)"""
        self.base_speed += 0.04
        if self.base_speed > 0.60:
            self.base_speed = 0.60
        # Preserve direction, amplify
        self.dx = self.base_speed * (1 if self.dx > 0 else -1)
        self.dy *= 1.05

# ====================== 7. GAME OVER DISPLAY CLASS ======================
# One-time winner announcement
class GameOverDisplay(GameTurtle):
    def __init__(self, is_player_win):
        super().__init__()
        self.color("yellow")
        self.hideturtle()
        self.goto(0, 0)
        text = "GAME OVER\nYOU WIN!" if is_player_win else "GAME OVER\nCOMPUTER WINS!"
        self.write(text, align="center", font=("Courier", 36, "bold"))

# ====================== 8. SCREEN & INITIALIZATION ======================
screen = Screen()
screen.title("Pong - Player (Left) vs Computer (Right)")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)                    # Manual updates for smooth animation

# Score tracking
player_score = 0
computer_score = 0

# ====================== 9. CREATE ALL GAME OBJECTS ======================
# Instantiate classes - positions match specs (paddles on outer edges)
player_display = ScoreDisplay(-150, 240, "Player")      # Top-left half
computer_display = ScoreDisplay(150, 240, "Computer")   # Top-right half
center_line = CenterLine()
player_paddle = Paddle(-350, 0)                         # Left outer side
computer_paddle = ComputerPaddle(350, 0)                # Right outer side
ball = Ball()

def update_scores():
    """Update both score displays"""
    player_display.update(player_score)
    computer_display.update(computer_score)

update_scores()  # Initial display

# ====================== 10. PLAYER INPUT FUNCTIONS ======================
def player_move_up():
    player_paddle.move_up()

def player_move_down():
    player_paddle.move_down()

# ====================== 11. KEYBOARD BINDINGS ======================
screen.listen()
screen.onkeypress(player_move_up, "w")
screen.onkeypress(player_move_down, "s")
screen.onkeypress(player_move_up, "Up")
screen.onkeypress(player_move_down, "Down")

# ====================== 12. MAIN GAME LOOP ======================
game_running = True
while game_running:
    screen.update()

    # Ball movement & wall bounces
    ball.move()
    if ball.ycor() > 290 or ball.ycor() < -290:
        ball.bounce_y()

    # Player paddle collision + angled bounce
    if ball.xcor() < -340 and abs(ball.ycor() - player_paddle.ycor()) < 55:
        ball.bounce_x()
        hit_pos = (ball.ycor() - player_paddle.ycor()) / 50
        ball.dy = hit_pos * 0.45

    # Computer paddle collision + angled bounce
    if ball.xcor() > 340 and abs(ball.ycor() - computer_paddle.ycor()) < 55:
        ball.bounce_x()
        hit_pos = (ball.ycor() - computer_paddle.ycor()) / 50
        ball.dy = hit_pos * 0.45

    # Scoring
    if ball.xcor() > 390:  # Past right paddle → Player scores
        player_score += 1
        update_scores()
        ball.reset()
        time.sleep(0.4)

    if ball.xcor() < -390:  # Past left paddle → Computer scores
        computer_score += 1
        update_scores()
        ball.reset()
        time.sleep(0.4)

    # Computer AI
    computer_paddle.ai_move(ball)

    # Speed increase every 5 total points
    total_points = player_score + computer_score
    if total_points > 0 and (total_points // 5) > ball.last_speed_increase:
        ball.increase_speed()
        ball.last_speed_increase += 1

    # Win condition
    if player_score >= 10 or computer_score >= 10:
        game_running = False

# ====================== 13. GAME OVER ======================
# Clear scores and show winner
player_display.clear()
computer_display.clear()
game_over = GameOverDisplay(player_score >= 10)
screen.mainloop()  # Keep window open