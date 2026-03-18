import turtle
import time
import pandas as pd

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)

# Create map turtle and set it to display the image
map_turtle = turtle.Turtle()
map_turtle.shape(image)
map_turtle.penup()
 
# Create writing turtle
writer = turtle.Turtle()
writer.penup()
writer.hideturtle()

# Game variables
guessed_states = []
game_is_on = True
start_time = time.time()
time_limit = 2  # 120 seconds

states_data = pd.read_csv("50_states.csv")

while game_is_on:
    # Check if time is up
    elapsed_time = time.time() - start_time
    if elapsed_time >= time_limit:
        game_is_on = False
        writer.goto(0, 250)
        writer.write(f"Time's up! You guessed {len(guessed_states)} states.", align="center", font=("Arial", 16, "bold"))
        
        pd.DataFrame([state for state in states_data["state"] if state not in guessed_states]).to_csv("states_to_study.csv")
        break

    if len(guessed_states) == 50:
        game_is_on = False
        writer.goto(0, 250)
        writer.write(f"Congratulations! You guessed all 50 states in {int(elapsed_time)} seconds!", align="center", font=("Arial", 16, "bold"))
        break

    # Get user input
    answer_state = screen.textinput(title=f"Guess the State ({int(time_limit - elapsed_time)}s left)", 
                                   prompt="What's another state's name?").title()

    if answer_state is None:  # User clicked cancel
        break

    if answer_state in states_data['state'].values:
        # Get the row with coordinates
        if answer_state not in guessed_states:
            state_row = states_data[states_data['state'] == answer_state]
            x_coord = state_row['x'].values[0]
            y_coord = state_row['y'].values[0]

            # Use the writer turtle to move and write
            writer.goto(x_coord, y_coord)
            writer.write(answer_state)
            guessed_states.append(answer_state)

screen.exitonclick()