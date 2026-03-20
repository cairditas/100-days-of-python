from tkinter import Tk, Canvas, Button, Label, PhotoImage, TclError
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
FONT = ("Arial", 12, "italic")
BUTTON_FONT = ("Arial", 14, "bold")

class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain
        self.window = None
        self.score_label = None
        self.canvas = None
        self.question_text = None
        self.true_button = None
        self.false_button = None
        self.true_image = None
        self.false_image = None
        
        self._setup_ui()
        self.get_next_question()
        self.window.mainloop()
    
    def _setup_ui(self):
        """Setup complete UI in one method."""
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)
        
        # Create widgets
        self.score_label = Label(
            text="Score: 0", 
            fg="white", 
            bg=THEME_COLOR,
            font=FONT
        )
        self.score_label.grid(row=0, column=0, pady=(0, 20))
        
        self.canvas = Canvas(width=300, height=250, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=2, pady=20)
        
        self.question_text = self.canvas.create_text(
            150, 125, width=280, text="Question text here",
            fill=THEME_COLOR, font=FONT
        )
        
        # Create buttons with commands
        self.true_button = Button(highlightthickness=0, command=self.true_pressed)
        self.false_button = Button(highlightthickness=0, command=self.false_pressed)
        
        # Load images or fallback to text
        self._setup_buttons()
        
        # Layout buttons
        self.true_button.grid(row=2, column=0, padx=20, pady=20)
        self.false_button.grid(row=2, column=1, padx=20, pady=20)
    
    def _setup_buttons(self):
        """Setup button images or text fallback."""
        try:
            self.true_image = PhotoImage(file="images/true.png")
            self.false_image = PhotoImage(file="images/false.png")
            self.true_button.config(image=self.true_image)
            self.false_button.config(image=self.false_image)
        except TclError:
            self.true_button.config(text="True", font=BUTTON_FONT)
            self.false_button.config(text="False", font=BUTTON_FONT)
    
    def true_pressed(self):
        """Handle True button click."""
        self._handle_answer("True")
    
    def false_pressed(self):
        """Handle False button click."""
        self._handle_answer("False")
    
    def _handle_answer(self, user_answer):
        """Handle answer checking and UI updates."""
        correct = self.quiz.check_answer(user_answer)
        
        # Show feedback
        feedback_color = "green" if correct else "red"
        self.canvas.config(bg=feedback_color)
        self.score_label.config(text=f"Score: {self.quiz.score}")
        
        # Load next question after delay
        self.window.after(1500, self.get_next_question)
    
    def get_next_question(self):
        """Load and display next question."""
        self.canvas.config(bg="white")  # Reset background
        
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
            self.score_label.config(text=f"Score: {self.quiz.score}")
        else:
            self.canvas.itemconfig(
                self.question_text, 
                text="You've reached the end of the quiz."
            )
            self._disable_buttons()
    
    def _disable_buttons(self):
        """Disable buttons at end of quiz."""
        self.true_button.config(state="disabled")
        self.false_button.config(state="disabled")