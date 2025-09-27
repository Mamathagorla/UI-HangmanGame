import tkinter as tk
import random

WORDS = ["kai", "barron", "chloe", "tim", "maira"]

class HangmanGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman Game")
        self.geometry("400x500")
        self.configure(bg="#22223B")  # Set a dark background
        self.encouragements = [
            "Keep going!",
            "You're getting closer!",
            "Nice try!",
            "Don't give up!",
            "You can do it!",
            "Almost there!",
            "Great guess!"
        ]
        self.attempts = 0
        self.max_attempts = 6
        self.goal = random.choice(WORDS)
        self.guesslist = ["_"] * len(self.goal)
        # UI Elements
        # Trophy drawing canvas
        self.trophy_stage = 0
        self.canvas = tk.Canvas(self, width=200, height=250, bg='#BE5985', highlightthickness=0)
        self.canvas.pack(pady=20)
        # Hint button
        self.hint_btn = tk.Button(self, text="Hint", command=self.show_hint, font=("Arial", 12), bg="#FFFACD")
        self.hint_btn.pack(pady=5)
        self.hint_used = False
        self.status_label = tk.Label(self, text="Attempts left: 6", font=("Arial", 14), fg="blue")
        self.status_label.pack()
        self.word_label = tk.Label(self, text=" ".join(self.guesslist), font=("Arial", 18), fg="darkgreen")
        self.word_label.pack(pady=10)
        self.input_entry = tk.Entry(self, font=("Arial", 14), width=5)
        self.input_entry.pack()
        self.input_entry.bind("<Return>", self.guess_letter)
        self.feedback_label = tk.Label(self, text="", font=("Arial", 12), fg="black")
        self.feedback_label.pack()
        self.restart_btn = tk.Button(self, text="Restart", command=self.restart)
        self.restart_btn.pack(pady=10)
        self.draw_trophy(0)
    
    def guess_letter(self, event):
        guess = self.input_entry.get().lower()
        self.input_entry.delete(0, tk.END)
        if not guess or len(guess) != 1 or not guess.isalpha():
            self.feedback_label.config(text="Enter a single letter (a-z).", fg="orange")
            return
        found = False
        for idx, char in enumerate(self.goal):
            if guess == char:
                self.guesslist[idx] = guess
                found = True
        self.word_label.config(text=" ".join(self.guesslist))
        if found:
            import random
            msg = random.choice(self.encouragements)
            self.feedback_label.config(text=msg, fg="green")
            self.trophy_stage += 1
            self.draw_trophy(self.trophy_stage, won=("".join(self.guesslist) == self.goal))
            if "".join(self.guesslist) == self.goal:
                self.status_label.config(text="You won! 🎉", fg="purple")
                self.feedback_label.config(text="Congratulations!", fg="purple")
                self.confetti_blast()
                self.play_win_sound()
                self.animate_trophy_shine()
        else:
            self.attempts += 1
            self.feedback_label.config(text="Wrong guess!", fg="red")
            self.status_label.config(text=f"Attempts left: {self.max_attempts - self.attempts}", fg="blue")
            # Trophy remains at current stage
            if self.attempts == self.max_attempts:
                self.status_label.config(text="Game Over!", fg="red")
                self.feedback_label.config(text=f"The word was: {self.goal}", fg="red")
    def play_win_sound(self):
        try:
            import winsound
            winsound.Beep(1200, 200)
            winsound.Beep(1500, 200)
            winsound.Beep(1800, 200)
        except Exception:
            pass

    def animate_trophy_shine(self):
        # Simple shine animation on trophy
        for i in range(3):
            self.canvas.create_line(70, 130, 130, 130, fill="#FFFACD", width=2)
            self.canvas.update()
            self.after(150)
            self.draw_trophy(self.trophy_stage, won=True)
    
    def restart(self):
        self.attempts = 0
        self.goal = random.choice(WORDS)
        self.guesslist = ["_"] * len(self.goal)
        self.word_label.config(text=" ".join(self.guesslist))
        self.status_label.config(text=f"Attempts left: {self.max_attempts}")
        self.feedback_label.config(text="")
        self.trophy_stage = 0
        self.canvas.delete("all")
        self.draw_trophy(0)
        self.hint_used = False
    def draw_trophy(self, stage, won=False):
        self.canvas.delete("all")
        trophy_color = "#FFD700"  # gold/yellow
        inside_color = "#EC7FA9"
        # Draw the box behind the trophy
        self.canvas.create_rectangle(60, 90, 140, 230, fill=inside_color, outline=inside_color)
        # Draw trophy step by step
        if stage > 0:
            # Base
            self.canvas.create_rectangle(80, 200, 120, 220, fill=trophy_color, outline=trophy_color)
        if stage > 1:
            # Stem
            self.canvas.create_rectangle(95, 150, 105, 200, fill=trophy_color, outline=trophy_color)
        if stage > 2:
            # Cup (outer)
            self.canvas.create_oval(70, 100, 130, 170, fill=trophy_color, outline=trophy_color)
        if stage > 3:
            # Cup (inner)
            self.canvas.create_oval(80, 115, 120, 165, fill=inside_color, outline=inside_color)
        if stage > 4:
            # Left handle
            self.canvas.create_arc(40, 120, 90, 170, start=90, extent=180, style=tk.ARC, outline=trophy_color, width=4)
        if stage > 5:
            # Right handle
            self.canvas.create_arc(110, 120, 160, 170, start=270, extent=180, style=tk.ARC, outline=trophy_color, width=4)
        if won:
            self.canvas.create_text(100, 80, text="WON", font=("Arial", 18, "bold"), fill="purple")
    def show_hint(self):
        if self.hint_used:
            self.feedback_label.config(text="Hint already used!", fg="orange")
            return
        # Find a letter not yet guessed
        for idx, char in enumerate(self.goal):
            if self.guesslist[idx] == "_":
                clue = self.get_letter_clue(char)
                self.feedback_label.config(text=f"Hint: {clue}", fg="#6A89CC")
                self.hint_used = True
                return
        self.feedback_label.config(text="No hints available!", fg="orange")

    def get_letter_clue(self, letter):
        clues = {
            'a': "First letter of the alphabet.",
            'b': "A buzzing insect starts with this.",
            'c': "A letter that defines a meow animal.",
            'd': "Starts the word for a loyal pet.",
            'e': "Most common vowel in English.",
            'f': "Starts the word for a flying animal.",
            'k': "Starts the word for a martial art and a bird.",
            'm': "Starts the word for a musical genre and a month.",
            't': "Starts the word for a hot beverage.",
            's': "Starts the word for a slithering animal.",
            'p': "Starts the word for a popular programming language.",
            'l': "Starts the word for a king of the jungle.",
            'r': "Starts the word for a hopping animal.",
            'o': "A round fruit starts with this.",
            'g': "Starts the word for a leafy vegetable.",
            'h': "Starts the word for a greeting.",
            'n': "Starts the word for a nocturnal animal.",
            'q': "A rare letter, starts the word for a royal title.",
            'z': "Starts the word for a striped animal.",
        }
        return clues.get(letter, f"It's the letter '{letter.upper()}' in the word.")

    def confetti_blast(self):
        import random
        # Mesmerizing colors
        colors = ["#FF61A6", "#6A89CC", "#F6D365", "#FFB86F", "#43E97B", "#38F9D7", "#A770EF", "#FDB99B", "#F5576C", "#4ECDC4"]
        confetti = []
        for _ in range(40):
            x = random.randint(10, 190)
            y = random.randint(10, 90)
            color = random.choice(colors)
            oval = self.canvas.create_oval(x, y, x+8, y+8, fill=color, outline=color)
            confetti.append((oval, x, y, color))
        # Animate falling confetti
        for step in range(30):
            for idx, (oval, x, y, color) in enumerate(confetti):
                dy = random.randint(2, 6)
                self.canvas.move(oval, 0, dy)
            self.canvas.update()
            self.after(50)
    

if __name__ == "__main__":
    app = HangmanGame()
    app.mainloop()