
import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
from pathlib import Path


class MathsQuizApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz Challenge")
        self.root.geometry("550x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#F3F6FF")

        # Design colours
        self.background = "#F3F6FF"
        self.card_colour = "#FFFFFF"
        self.primary_colour = "#536DFE"
        self.secondary_colour = "#7C4DFF"
        self.text_colour = "#263238"
        self.green = "#2EAD67"
        self.red = "#E53935"
        self.orange = "#F5A623"

        # Quiz settings
        self.total_questions = 10
        self.time_limit = 30
        self.difficulty = "Easy"

        # Score and results
        self.score = 0
        self.question_number = 0
        self.first_try_correct = 0
        self.second_try_correct = 0
        self.incorrect_answers = 0
        self.timed_out_answers = 0

        # Question variables
        self.num1 = 0
        self.num2 = 0
        self.operation = "+"
        self.correct_answer = 0
        self.attempts = 0
        self.question_finished = False

        # Timer variables
        self.time_left = self.time_limit
        self.timer_id = None
        self.next_question_id = None

        # High score storage
        self.high_score_file = (
            Path(__file__).resolve().parent / "high_scores.json"
        )
        self.high_scores = self.loadHighScores()

        # Main screen
        self.main_frame = tk.Frame(
            self.root,
            bg=self.background
        )
        self.main_frame.pack(fill="both", expand=True)

        # Progress bar style
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Quiz.Horizontal.TProgressbar",
            troughcolor="#DCE3FF",
            background=self.primary_colour,
            thickness=16
        )

        self.displayMenu()

    # SCREEN MANAGEMENT
     

    def clearScreen(self):
        self.cancelTimer()

        if self.next_question_id is not None:
            try:
                self.root.after_cancel(self.next_question_id)
            except tk.TclError:
                pass

            self.next_question_id = None

        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def createTitle(self, title, subtitle=None):
        tk.Label(
            self.main_frame,
            text=title,
            font=("Arial", 25, "bold"),
            bg=self.background,
            fg=self.primary_colour
        ).pack(pady=(20, 5))

        if subtitle:
            tk.Label(
                self.main_frame,
                text=subtitle,
                font=("Arial", 11),
                bg=self.background,
                fg="#667085"
            ).pack(pady=(0, 15))

    def createButton(self, text, command, colour=None):
        if colour is None:
            colour = self.primary_colour

        return tk.Button(
            self.main_frame,
            text=text,
            command=command,
            font=("Arial", 12, "bold"),
            bg=colour,
            fg="white",
            activebackground=self.secondary_colour,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=25,
            pady=9
        )

    # HIGH SCORE SETTINGS
   
    def loadHighScores(self):
        try:
            if self.high_score_file.exists():
                with open(self.high_score_file, "r") as file:
                    data = json.load(file)

                    if isinstance(data, dict):
                        return data

        except (json.JSONDecodeError, OSError):
            return {}

        return {}

    def saveHighScore(self):
        current_best = self.high_scores.get(
            self.difficulty, 0
        )

        if self.score > current_best:
            self.high_scores[self.difficulty] = self.score

            try:
                with open(self.high_score_file, "w") as file:
                    json.dump(
                        self.high_scores,
                        file,
                        indent=4
                    )

            except OSError:
                messagebox.showerror(
                    "Saving Error",
                    "Your high score could not be saved."
                )
    
    #FUNCTION 1: DISPLAY MENU

    def displayMenu(self):
        self.clearScreen()

        self.createTitle(
            "MATHS QUIZ",
            "Test your maths skills and challenge yourself!"
        )

        # Welcome card
        welcome_card = tk.Frame(
            self.main_frame,
            bg=self.card_colour,
            padx=20,
            pady=15
        )
        welcome_card.pack(padx=35, fill="x", pady=10)

        tk.Label(
            welcome_card,
            text="Welcome!",
            font=("Arial", 17, "bold"),
            bg=self.card_colour,
            fg=self.text_colour
        ).pack(pady=5)

        tk.Label(
            welcome_card,
            text=(
                "Answer 10 maths questions.\n"
                "You get two attempts for each question.\n"
                "Earn 10 points on your first try\n"
                "and 5 points on your second try!"
            ),
            font=("Arial", 11),
            bg=self.card_colour,
            fg="#667085",
            justify="center"
        ).pack(pady=5)

        tk.Label(
            self.main_frame,
            text="CHOOSE YOUR LEVEL",
            font=("Arial", 13, "bold"),
            bg=self.background,
            fg=self.text_colour
        ).pack(pady=10)

        self.createButton(
            "Easy - Single Digit",
            lambda: self.startQuiz("Easy"),
            "#42A5F5"
        ).pack(pady=5)

        self.createButton(
            "Moderate - Double Digit",
            lambda: self.startQuiz("Moderate"),
            "#7E57C2"
        ).pack(pady=5)

        self.createButton(
            "Advanced - Four Digit",
            lambda: self.startQuiz("Advanced"),
            "#EC407A"
        ).pack(pady=5)

        # Personal best scores
        tk.Label(
            self.main_frame,
            text="YOUR PERSONAL BEST",
            font=("Arial", 12, "bold"),
            bg=self.background,
            fg=self.text_colour
        ).pack(pady=(18, 5))

        for level in ("Easy", "Moderate", "Advanced"):
            best = self.high_scores.get(level, 0)

            tk.Label(
                self.main_frame,
                text=f"{level}: {best}/100",
                font=("Arial", 10),
                bg=self.background,
                fg="#667085"
            ).pack(pady=1)

    # START QUIZ

    def startQuiz(self, difficulty):
        self.difficulty = difficulty

        self.score = 0
        self.question_number = 0

        self.first_try_correct = 0
        self.second_try_correct = 0
        self.incorrect_answers = 0
        self.timed_out_answers = 0

        self.displayProblem()

    # REQUIRED FUNCTION 2: RANDOM NUMBER

    def randomInt(self):
        if self.difficulty == "Easy":
            return random.randint(1, 9)

        elif self.difficulty == "Moderate":
            return random.randint(10, 99)

        else:
            return random.randint(1000, 9999)

    # REQUIRED FUNCTION 3: DECIDE OPERATION
   
    def decideOperation(self):
        return random.choice(["+", "-"])

    # REQUIRED FUNCTION 4: DISPLAY PROBLEM
    

    def displayProblem(self):
        self.clearScreen()

        if self.question_number >= self.total_questions:
            self.displayResults()
            return

        self.question_number += 1
        self.attempts = 0
        self.question_finished = False
        self.time_left = self.time_limit

        # Generate question
        self.num1 = self.randomInt()
        self.num2 = self.randomInt()
        self.operation = self.decideOperation()

        # Prevent negative subtraction answers
        if self.operation == "-" and self.num2 > self.num1:
            self.num1, self.num2 = self.num2, self.num1

        if self.operation == "+":
            self.correct_answer = self.num1 + self.num2
        else:
            self.correct_answer = self.num1 - self.num2

        # Heading
        self.createTitle(
            "MATHS QUIZ",
            f"Difficulty: {self.difficulty}"
        )

        # Question counter
        self.progress_label = tk.Label(
            self.main_frame,
            text=(
                f"Question {self.question_number} "
                f"of {self.total_questions}"
            ),
            font=("Arial", 12, "bold"),
            bg=self.background,
            fg=self.text_colour
        )
        self.progress_label.pack(pady=5)

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self.main_frame,
            style="Quiz.Horizontal.TProgressbar",
            maximum=self.total_questions,
            value=self.question_number,
            length=350
        )
        self.progress_bar.pack(pady=8)

        # Current score
        tk.Label(
            self.main_frame,
            text=f"Score: {self.score}/100",
            font=("Arial", 13, "bold"),
            bg=self.background,
            fg=self.secondary_colour
        ).pack(pady=8)

        # Timer
        self.timer_label = tk.Label(
            self.main_frame,
            text=f"Time left: {self.time_left} seconds",
            font=("Arial", 13, "bold"),
            bg=self.background,
            fg=self.primary_colour
        )
        self.timer_label.pack(pady=8)

        # Question card
        question_card = tk.Frame(
            self.main_frame,
            bg=self.card_colour,
            padx=25,
            pady=25
        )
        question_card.pack(padx=35, pady=12, fill="x")

        tk.Label(
            question_card,
            text="SOLVE THIS QUESTION",
            font=("Arial", 11, "bold"),
            bg=self.card_colour,
            fg="#667085"
        ).pack(pady=5)

        tk.Label(
            question_card,
            text=f"{self.num1} {self.operation} {self.num2} = ?",
            font=("Arial", 28, "bold"),
            bg=self.card_colour,
            fg=self.text_colour
        ).pack(pady=10)

        # Answer entry
        self.answer_entry = tk.Entry(
            self.main_frame,
            font=("Arial", 18),
            justify="center",
            width=15,
            relief="solid",
            bd=1
        )
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus_set()

        self.answer_entry.bind(
            "<Return>",
            lambda event: self.isCorrect()
        )

        # Submit button
        self.submit_button = self.createButton(
            "SUBMIT ANSWER",
            self.isCorrect
        )
        self.submit_button.pack(pady=8)

        # Feedback label
        self.feedback_label = tk.Label(
            self.main_frame,
            text="You have two attempts. Good luck!",
            font=("Arial", 11, "bold"),
            bg=self.background,
            fg=self.text_colour
        )
        self.feedback_label.pack(pady=10)

        # Start timer
        self.updateTimer()

  
    # COUNTDOWN TIMER
  

    def cancelTimer(self):
        if self.timer_id is not None:
            try:
                self.root.after_cancel(self.timer_id)
            except tk.TclError:
                pass

            self.timer_id = None

    def updateTimer(self):
        if self.question_finished:
            return

        self.timer_label.config(
            text=f"Time left: {self.time_left} seconds"
        )

        if self.time_left <= 0:
            self.handleTimeout()
            return

        self.time_left -= 1

        self.timer_id = self.root.after(
            1000,
            self.updateTimer
        )

    def handleTimeout(self):
        if self.question_finished:
            return

        self.question_finished = True
        self.cancelTimer()

        self.incorrect_answers += 1
        self.timed_out_answers += 1

        self.feedback_label.config(
            text=(
                f"Time is up! The answer was "
                f"{self.correct_answer}."
            ),
            fg=self.red
        )

        self.answer_entry.config(state="disabled")
        self.submit_button.config(state="disabled")

        self.scheduleNextQuestion()

    # REQUIRED FUNCTION 5: CHECK ANSWER

    def isCorrect(self):
        if self.question_finished:
            return

        answer_text = self.answer_entry.get().strip()

        if not answer_text:
            self.feedback_label.config(
                text="Please enter an answer.",
                fg=self.orange
            )
            return

        try:
            user_answer = int(answer_text)

        except ValueError:
            self.feedback_label.config(
                text="Please enter a whole number.",
                fg=self.orange
            )
            return

        self.attempts += 1

        if user_answer == self.correct_answer:
            self.question_finished = True
            self.cancelTimer()

            if self.attempts == 1:
                self.score += 10
                self.first_try_correct += 1

                feedback = "Correct! You earned 10 points."

            else:
                self.score += 5
                self.second_try_correct += 1

                feedback = (
                    "Correct on your second attempt! "
                    "You earned 5 points."
                )

            self.feedback_label.config(
                text=feedback,
                fg=self.green
            )

            self.answer_entry.config(state="disabled")
            self.submit_button.config(state="disabled")

            self.scheduleNextQuestion()

        else:
            if self.attempts == 1:
                self.feedback_label.config(
                    text="Not quite! Try one more time.",
                    fg=self.orange
                )

                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus_set()

            else:
                self.question_finished = True
                self.cancelTimer()

                self.incorrect_answers += 1

                self.feedback_label.config(
                    text=(
                        f"Incorrect! The correct answer "
                        f"was {self.correct_answer}."
                    ),
                    fg=self.red
                )

                self.answer_entry.config(state="disabled")
                self.submit_button.config(state="disabled")

                self.scheduleNextQuestion()

    # NEXT QUESTION
    

    def scheduleNextQuestion(self):
        self.cancelTimer()

        self.next_question_id = self.root.after(
            1500,
            self.displayProblem
        )

    # GRADE AND STAR RATING


    def calculateGrade(self):
        if self.score >= 90:
            return "A+"

        elif self.score >= 80:
            return "A"

        elif self.score >= 70:
            return "B"

        elif self.score >= 60:
            return "C"

        elif self.score >= 50:
            return "D"

        else:
            return "Needs Improvement"

    def calculateStars(self):
        if self.score >= 90:
            return "★★★★★"

        elif self.score >= 75:
            return "★★★★☆"

        elif self.score >= 60:
            return "★★★☆☆"

        elif self.score >= 40:
            return "★★☆☆☆"

        else:
            return "★☆☆☆☆"

    # REQUIRED FUNCTION 6: DISPLAY RESULTS

    def displayResults(self):
        self.clearScreen()

        old_best = self.high_scores.get(
            self.difficulty, 0
        )

        new_record = self.score > old_best

        self.saveHighScore()

        self.createTitle(
            "QUIZ COMPLETED!",
            "Here is how you performed."
        )

        # Results card
        results_card = tk.Frame(
            self.main_frame,
            bg=self.card_colour,
            padx=20,
            pady=15
        )
        results_card.pack(padx=35, pady=8, fill="x")

        tk.Label(
            results_card,
            text=f"{self.score}/100",
            font=("Arial", 30, "bold"),
            bg=self.card_colour,
            fg=self.primary_colour
        ).pack(pady=5)

        tk.Label(
            results_card,
            text=f"Grade: {self.calculateGrade()}",
            font=("Arial", 16, "bold"),
            bg=self.card_colour,
            fg=self.text_colour
        ).pack(pady=4)

        tk.Label(
            results_card,
            text=self.calculateStars(),
            font=("Arial", 24, "bold"),
            bg=self.card_colour,
            fg="#F5B400"
        ).pack(pady=4)

        if new_record:
            tk.Label(
                results_card,
                text="NEW PERSONAL BEST!",
                font=("Arial", 12, "bold"),
                bg=self.card_colour,
                fg=self.green
            ).pack(pady=5)

        # Detailed results
        tk.Label(
            self.main_frame,
            text="YOUR RESULTS",
            font=("Arial", 13, "bold"),
            bg=self.background,
            fg=self.text_colour
        ).pack(pady=8)

        results_text = (
            f"Correct on first attempt: {self.first_try_correct}\n"
            f"Correct on second attempt: {self.second_try_correct}\n"
            f"Incorrect answers: {self.incorrect_answers}\n"
            f"Timed-out questions: {self.timed_out_answers}\n"
            f"Personal best: "
            f"{self.high_scores.get(self.difficulty, 0)}/100"
        )

        tk.Label(
            self.main_frame,
            text=results_text,
            font=("Arial", 10),
            bg=self.background,
            fg="#52606D",
            justify="left"
        ).pack(pady=5)

        # Replay and menu buttons
        self.createButton(
            "PLAY AGAIN",
            lambda: self.startQuiz(self.difficulty),
            self.green
        ).pack(pady=(12, 5))

        self.createButton(
            "BACK TO MENU",
            self.displayMenu,
            self.primary_colour
        ).pack(pady=5)

        self.createButton(
            "EXIT",
            self.root.destroy,
            "#78909C"
        ).pack(pady=5)

# RUN PROGRAM

if __name__ == "__main__":
    root = tk.Tk()
    app = MathsQuizApp(root)
    root.mainloop()
