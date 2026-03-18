from tkinter import *


# ---------------------------- CONSTANTS ------------------------------- #

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

RESET_COUNT = 0
COMPLETIONS = 0
TIMER_ID = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset():
    global TIMER_ID, RESET_COUNT, COMPLETIONS
    RESET_COUNT += 1
    COMPLETIONS = 0

    start_button.config(state="normal")
    canvas.itemconfig(timer_text, text="00:00")
    title.config(text="Timer", fg=GREEN)
    checkmark_label.config(text="")

    if TIMER_ID:
        window.after_cancel(TIMER_ID)
        TIMER_ID = None

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global COMPLETIONS
    start_button.config(state="disabled")

    if COMPLETIONS % 8 == 0 and COMPLETIONS > 0:
        title.config(text="Long Break", fg=GREEN)
        count_down(LONG_BREAK_MIN * 60)
    elif COMPLETIONS % 2 != 0 and COMPLETIONS > 0:
        title.config(text="Short Break", fg=GREEN)
        count_down(SHORT_BREAK_MIN * 60)
    else:
        title.config(text="Work", fg=RED)
        count_down(WORK_MIN * 60)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global TIMER_ID, COMPLETIONS
    minutes = count // 60
    seconds = count % 60
    canvas.itemconfig(timer_text, text=f"{minutes:02d}:{seconds:02d}")

    if count > 0:
        TIMER_ID = window.after(1000, count_down, count - 1)
    elif RESET_COUNT == 0:
        COMPLETIONS += 1
        checkmark_label.config(text=checkmark_label.cget("text") + "✔ ")
        window.lift()  
        window.attributes('-topmost', True)  # Keep on top temporarily
        window.after(60000, lambda: window.attributes('-topmost', False))  # Remove after 1 minute
        
        start_timer()
        # start_button.config(state="normal")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

title = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="0:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", command=start_timer)
start_button.config(
    highlightthickness=10, 
    borderwidth=0, 
    relief="flat", 
    bd=0, 
    bg=YELLOW, 
    activebackground=YELLOW, 
    highlightbackground=YELLOW)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", command=reset)
reset_button.config(
    highlightthickness=10, 
    borderwidth=0, 
    relief="flat", 
    bd=0, 
    bg=YELLOW, 
    activebackground=YELLOW, 
    highlightbackground=YELLOW)
reset_button.grid(column=2, row=2)

checkmark_label = Label(text="", fg=GREEN, bg=YELLOW)
checkmark_label.grid(column=1, row=3)




window.mainloop()