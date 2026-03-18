"""
=============================================================
  PONG GAME — built with Python's turtle library
  Player (left) vs Computer (right)
  First to 10 points wins. Speed increases every 5 points.

  All on-screen objects inherit from turtle.Turtle so that
  each class owns both its appearance AND its behaviour.
=============================================================
"""

import turtle
import random

# ─────────────────────────────────────────────
# SECTION 1 — CONSTANTS & CONFIGURATION
# All "magic numbers" live here so they're easy to tweak.
# ─────────────────────────────────────────────

WINDOW_WIDTH        = 800       # Total window width in pixels
WINDOW_HEIGHT       = 600       # Total window height in pixels
HALF_WIDTH          = WINDOW_WIDTH  // 2   # 400 — used for boundary maths
HALF_HEIGHT         = WINDOW_HEIGHT // 2   # 300

PADDLE_STRETCH_WID  = 1         # Turtle stretch units along the short axis
PADDLE_STRETCH_LEN  = 3         # Turtle stretch units along the long axis
PADDLE_SPEED        = 20        # Pixels the player paddle moves per key-press
PADDLE_X_OFFSET     = 350       # Distance from centre to each paddle (px)
# Derived pixel half-extents used for collision detection
PADDLE_HALF_TALL_PX = PADDLE_STRETCH_LEN * 5   # ~50 px  (vertical half-height)
PADDLE_HALF_WIDE_PX = PADDLE_STRETCH_WID * 5   # ~20 px  (horizontal half-width)

COMPUTER_AI_SPEED   = 3         # Max px the AI paddle moves per frame (lower = easier)

BALL_SIZE           = 10        # Approximate diameter of the ball in pixels
BALL_INITIAL_DELAY  = 0.01     # Starting delay between frames (seconds)
BALL_SPEED_STEP     = 0.03      # Delay reduction applied every SPEED_UP_EVERY points
BALL_SPEED_MIN      = 0.01      # Minimum delay floor (fastest the ball can go)

WINNING_SCORE       = 10        # First player to reach this score wins
SPEED_UP_EVERY      = 5         # Combined-point milestone that triggers a speed increase

# Colours
BACKGROUND_COLOR    = "black"
PADDLE_COLOR        = "white"
BALL_COLOR          = "white"
SCORE_COLOR         = "white"
DIVIDER_COLOR       = "white"
WIN_COLOR           = "yellow"


# ─────────────────────────────────────────────
# SECTION 2 — WINDOW SETUP
# Creates the 800x600 game window and disables
# automatic screen updates so we control redraws.
# ─────────────────────────────────────────────

game_screen = turtle.Screen()
game_screen.title("Pong — Player vs Computer")
game_screen.bgcolor(BACKGROUND_COLOR)
game_screen.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
game_screen.tracer(0)   # Turn off auto-refresh; we call update() manually


# ─────────────────────────────────────────────
# SECTION 3 — BASE CLASS: GameSprite
#
# All visible game objects inherit from this class.
# It calls turtle.Turtle.__init__() and then applies
# the settings that every sprite shares: pen lifted,
# maximum animation speed, a colour, and an initial
# screen position.  Subclasses call super().__init__()
# to get all of this for free and then customise further.
# ─────────────────────────────────────────────

class GameSprite(turtle.Turtle):
    """
    Base class for every on-screen object in the game.
    Inherits all turtle drawing and movement methods,
    then adds sensible defaults so subclasses stay lean.
    """

    def __init__(self, color=PADDLE_COLOR, x=0, y=0):
        super().__init__()       # Initialise the underlying Turtle
        self.shape("square")     # All sprites start as squares (subclasses may resize)
        self.color(color)
        self.penup()             # Never leave a drawing trail when moving
        self.speed(0)            # Maximum animation speed
        self.goto(x, y)


# ─────────────────────────────────────────────
# SECTION 4 — CLASS: Paddle
#
# Represents one paddle (player or computer).
# Inherits position / colour setup from GameSprite,
# then stretches and rotates itself into a tall
# thin rectangle.  The move_toward() method is used
# by both the player controls and the computer AI.
# ─────────────────────────────────────────────

class Paddle(GameSprite):
    """
    A tall, thin rectangular paddle that can slide
    up and down within the window boundaries.
    """

    def __init__(self, x=0, y=0):
        super().__init__(color=PADDLE_COLOR, x=x, y=y)
        # Stretch into a vertical paddle shape; outline=1 adds a border
        self.shapesize(
            stretch_wid=PADDLE_STRETCH_LEN,   # tall axis
            stretch_len=PADDLE_STRETCH_WID,   # short (horizontal) axis
            outline=1
        )

    def move_up(self, step=PADDLE_SPEED):
        """
        Slide the paddle upward by `step` pixels,
        stopping before it exits the top of the screen.
        """
        new_y = self.ycor() + step
        max_y = HALF_HEIGHT - PADDLE_HALF_TALL_PX
        if new_y < max_y:
            self.sety(new_y)

    def move_down(self, step=PADDLE_SPEED):
        """
        Slide the paddle downward by `step` pixels,
        stopping before it exits the bottom of the screen.
        """
        new_y = self.ycor() - step
        min_y = -HALF_HEIGHT + PADDLE_HALF_TALL_PX
        if new_y > min_y:
            self.sety(new_y)

    def move_toward(self, target_y, max_step=COMPUTER_AI_SPEED):
        """
        Move the paddle towards `target_y` by at most `max_step`
        pixels per call.  Used by the computer AI every frame.
        Clamping prevents the paddle from leaving the screen.
        """
        diff = target_y - self.ycor()
        step = max(-max_step, min(max_step, diff))
        new_y = self.ycor() + step
        max_y =  HALF_HEIGHT - PADDLE_HALF_TALL_PX
        min_y = -HALF_HEIGHT + PADDLE_HALF_TALL_PX
        self.sety(max(min_y, min(max_y, new_y)))

    def is_hit_by(self, ball):
        """
        Return True if `ball` overlaps this paddle's bounding box.
        Uses simple axis-aligned rectangle overlap maths.
        """
        x_overlap = abs(ball.xcor() - self.xcor()) < PADDLE_HALF_WIDE_PX + BALL_SIZE // 2
        y_overlap = abs(ball.ycor() - self.ycor()) < PADDLE_HALF_TALL_PX + BALL_SIZE // 2
        return x_overlap and y_overlap


# ─────────────────────────────────────────────
# SECTION 5 — CLASS: Ball
#
# The bouncing ball.  dx / dy are instance attributes
# that store the current velocity vector (px per frame).
# reset() re-centres the ball and randomises its direction.
# move() advances the ball by one frame and handles all
# bouncing / scoring logic, returning who scored (if anyone).
# ─────────────────────────────────────────────

class Ball(GameSprite):
    """
    The game ball.  Moves each frame according to its
    velocity (dx, dy) and bounces off walls and paddles.
    """

    def __init__(self):
        super().__init__(color=BALL_COLOR, x=0, y=0)
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        # Velocity components: pixels moved per frame
        self.dx = random.choice([-3, 3])
        self.dy = random.choice([-3, 3])

    def reset(self):
        """
        Return the ball to the centre of the board and
        pick a fresh random velocity for the next rally.
        """
        self.goto(0, 0)
        self.dx = random.choice([-3, 3])
        self.dy = random.choice([-3, 3])

    def move(self, player_paddle, computer_paddle):
        """
        Advance the ball one frame:
          1. Apply velocity to position.
          2. Bounce off the top / bottom walls.
          3. Bounce off either paddle if hit.
          4. Return 'player', 'computer', or None to
             indicate which side (if any) just scored.
        """
        # ── 5a. Advance position ──────────────────────
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

        # ── 5b. Top / bottom wall bounce ─────────────
        if self.ycor() >= HALF_HEIGHT - BALL_SIZE:
            self.sety(HALF_HEIGHT - BALL_SIZE)
            self.dy *= -1

        elif self.ycor() <= -HALF_HEIGHT + BALL_SIZE:
            self.sety(-HALF_HEIGHT + BALL_SIZE)
            self.dy *= -1

        # ── 5c. Paddle collision — player (left side) ─
        # Only test the player paddle when ball is moving left (dx < 0)
        if self.dx < 0 and player_paddle.is_hit_by(self):
            self.setx(player_paddle.xcor() + PADDLE_HALF_WIDE_PX + BALL_SIZE)
            self.dx *= -1

        # ── 5d. Paddle collision — computer (right side)
        if self.dx > 0 and computer_paddle.is_hit_by(self):
            self.setx(computer_paddle.xcor() - PADDLE_HALF_WIDE_PX - BALL_SIZE)
            self.dx *= -1

        # ── 5e. Scoring — ball escapes past a paddle ──
        if self.xcor() < -HALF_WIDTH:
            return "computer"   # Ball passed the left wall -> computer scores

        if self.xcor() > HALF_WIDTH:
            return "player"     # Ball passed the right wall -> player scores

        return None             # No score this frame

    def freeze(self):
        """Stop the ball in place (called when the game ends)."""
        self.dx = 0
        self.dy = 0


# ─────────────────────────────────────────────
# SECTION 6 — CLASS: Divider
#
# Draws the dotted centre line once on construction.
# Inherits from GameSprite so it lives in the same
# class hierarchy, but its only job is to draw and
# then hide itself.
# ─────────────────────────────────────────────

class Divider(GameSprite):
    """
    Draws a static dotted white line down the centre
    of the board to visually separate the two halves.
    The turtle hides itself after drawing is complete.
    """

    DOT_LENGTH = 10   # Pixels drawn per dash segment
    DOT_GAP    = 20   # Pixels skipped between segments

    def __init__(self):
        super().__init__(color=DIVIDER_COLOR, x=0, y=HALF_HEIGHT)
        self._draw()
        self.hideturtle()   # No sprite needed — just the line

    def _draw(self):
        """
        Walk from the top to the bottom of the screen,
        alternating between drawing a short segment and
        lifting the pen to create the dashed appearance.
        """
        y = HALF_HEIGHT
        while y > -HALF_HEIGHT:
            self.goto(0, y)
            self.pendown()
            self.goto(0, y - self.DOT_LENGTH)
            self.penup()
            y -= self.DOT_LENGTH + self.DOT_GAP


# ─────────────────────────────────────────────
# SECTION 7 — CLASS: ScoreDisplay
#
# Owns both score values and the turtle that
# renders them.  Inherits from GameSprite so
# the turtle is set up the same way as everything
# else; hideturtle() removes the arrow icon.
# ─────────────────────────────────────────────

class ScoreDisplay(GameSprite):
    """
    Tracks the score for both players and renders
    it in the top portion of each half of the board.
    """

    SCORE_Y = HALF_HEIGHT - 50
    FONT    = ("Courier", 20, "bold")

    def __init__(self):
        super().__init__(color=SCORE_COLOR, x=0, y=self.SCORE_Y)
        self.hideturtle()
        self.player_score   = 0
        self.computer_score = 0
        self.refresh()

    def refresh(self):
        """
        Erase the previous score text and redraw both
        values in their respective halves of the screen.
        """
        self.clear()
        self.goto(-200, self.SCORE_Y)
        self.write(f"Player: {self.player_score}",
                   align="center", font=self.FONT)
        self.goto(200, self.SCORE_Y)
        self.write(f"Computer: {self.computer_score}",
                   align="center", font=self.FONT)

    def add_player_point(self):
        """Increment the player's score and refresh the display."""
        self.player_score += 1
        self.refresh()

    def add_computer_point(self):
        """Increment the computer's score and refresh the display."""
        self.computer_score += 1
        self.refresh()

    @property
    def total_points(self):
        """Combined score of both players — used to track speed milestones."""
        return self.player_score + self.computer_score


# ─────────────────────────────────────────────
# SECTION 8 — CLASS: WinDisplay
#
# A hidden text turtle that surfaces a large
# centred message when the game ends.
# ─────────────────────────────────────────────

class WinDisplay(GameSprite):
    """
    Renders a full-screen win/lose announcement.
    Stays invisible until show() is called.
    """

    FONT = ("Courier", 32, "bold")

    def __init__(self):
        super().__init__(color=WIN_COLOR, x=0, y=0)
        self.hideturtle()

    def show(self, message):
        """Write `message` centred on the screen."""
        self.write(message, align="center", font=self.FONT)


# ─────────────────────────────────────────────
# SECTION 9 — CLASS: PongGame
#
# The top-level controller that owns every object,
# wires up keyboard input, and runs the game loop.
# Keeping all of this in one class means there are
# no global variables — state lives in self.
# ─────────────────────────────────────────────

class PongGame:
    """
    Owns and coordinates all game objects.
    Call .run() to start.
    """

    def __init__(self):
        # ── Create all sprites ───────────────────────
        Divider()   # Drawn once; no reference needed afterwards

        self.player_paddle   = Paddle(x=-PADDLE_X_OFFSET, y=0)
        self.computer_paddle = Paddle(x= PADDLE_X_OFFSET, y=0)
        self.ball            = Ball()
        self.score           = ScoreDisplay()
        self.win_display     = WinDisplay()

        # ── Game-speed state ─────────────────────────
        self.ball_delay = BALL_INITIAL_DELAY   # Seconds between frames

        # ── Wire up keyboard input ───────────────────
        self._bind_keys()

    # ─────────────────────────────────────────────
    # SECTION 9a — KEY BINDINGS
    # Delegates directly to the player paddle's
    # own move_up / move_down methods.
    # ─────────────────────────────────────────────

    def _bind_keys(self):
        """Register W / S (and arrow keys) to move the player paddle."""
        game_screen.listen()
        game_screen.onkeypress(self.player_paddle.move_up,   "w")
        game_screen.onkeypress(self.player_paddle.move_up,   "Up")
        game_screen.onkeypress(self.player_paddle.move_down, "s")
        game_screen.onkeypress(self.player_paddle.move_down, "Down")

    # ─────────────────────────────────────────────
    # SECTION 9b — SPEED SCALING
    # Called after every point.  Every SPEED_UP_EVERY
    # combined points, the inter-frame delay shrinks.
    # ─────────────────────────────────────────────

    def _maybe_increase_speed(self):
        """
        Reduce the frame delay (speeding up the ball) whenever
        the combined score hits a new multiple of SPEED_UP_EVERY.
        The delay never drops below BALL_SPEED_MIN.
        """
        total = self.score.total_points
        if total > 0 and total % SPEED_UP_EVERY == 0:
            self.ball_delay = max(
                self.ball_delay - BALL_SPEED_STEP,
                BALL_SPEED_MIN
            )

    # ─────────────────────────────────────────────
    # SECTION 9c — MAIN GAME LOOP
    # Scheduled repeatedly via turtle.ontimer() so
    # it never blocks the event loop.  Each call:
    #   1. Moves the ball (and checks for scores).
    #   2. Moves the computer AI paddle.
    #   3. Handles any points that were scored.
    #   4. Redraws the screen.
    #   5. Reschedules itself for the next frame.
    # ─────────────────────────────────────────────

    def _game_loop(self):
        """One frame of gameplay."""

        # ── Move the ball; find out if anyone scored ─
        scorer = self.ball.move(self.player_paddle, self.computer_paddle)

        # ── Handle scoring ───────────────────────────
        if scorer == "player":
            self.score.add_player_point()
            self._maybe_increase_speed()
            if self.score.player_score >= WINNING_SCORE:
                self.win_display.show("Player Wins! 🎉")
                game_screen.update()
                return
            self.ball.reset()

        elif scorer == "computer":
            self.score.add_computer_point()
            self._maybe_increase_speed()
            if self.score.computer_score >= WINNING_SCORE:
                self.win_display.show("Computer Wins! 🎉")
                game_screen.update()
                return
            self.ball.reset()

        # ── Move the computer AI toward the ball ─────
        self.computer_paddle.move_toward(self.ball.ycor())

        # ── Redraw everything ────────────────────────
        game_screen.update()

        # ── Schedule the next frame ──────────────────
        delay_ms = int(self.ball_delay * 1000)
        turtle.ontimer(self._game_loop, delay_ms)

    # ─────────────────────────────────────────────
    # SECTION 9d — RUN
    # Public entry point.  Kicks off the loop then
    # hands control to turtle's own event loop so
    # keyboard events keep firing.
    # ─────────────────────────────────────────────

    def run(self):
        """Start the game loop and enter turtle's event loop."""
        self._game_loop()
        turtle.mainloop()


# ─────────────────────────────────────────────
# SECTION 10 — ENTRY POINT
# Only runs when the script is executed directly
# (not when imported as a module).
# ─────────────────────────────────────────────

if __name__ == "__main__":
    game = PongGame()
    game.run()