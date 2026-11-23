
import tkinter as tk
from tkinter import messagebox
import random
import json
from pathlib import Path


class JokeAssistant:

    def __init__(self, root):

        self.root = root
        self.root.title("Alexa - Joke Assistant")
        self.root.geometry("680x700")
        self.root.configure(bg="#F3F0FF")
        self.root.resizable(False, False)

        # File locations
        self.joke_file = Path(__file__).with_name("randomJokes.txt")
        self.favourite_file = Path(__file__).with_name(
            "favourite_jokes.json"
        )

        # Application data
        self.jokes = self.load_jokes()
        self.favourites = self.load_favourites()
        self.remaining_jokes = []
        self.current_joke = None
        self.previous_joke_index = None
        self.viewed_count = 0

        self.reset_joke_list()

        # Create the interface
        self.create_interface()

        # Keyboard shortcuts
        self.root.bind("<Return>", self.keyboard_next_joke)
        self.root.bind("<space>", self.keyboard_punchline)
        self.root.bind("<Control-f>", self.keyboard_favourite)
        self.root.bind("<Control-l>", self.keyboard_favourites)
        self.root.bind("<Escape>", self.quit_app)

        self.update_counter()

    # Load jokes from text file
    def load_jokes(self):

        jokes = []

        try:
            with open(
                self.joke_file, "r", encoding="utf-8"
            ) as file:

                for line in file:
                    line = line.strip()

                    if line.startswith("- "):
                        line = line[2:]

                    if "?" in line:
                        setup, punchline = line.split("?", 1)

                        setup = setup.strip() + "?"
                        punchline = punchline.strip()

                        if setup and punchline:
                            jokes.append((setup, punchline))

        except FileNotFoundError:
            messagebox.showerror(
                "File Error",
                "randomJokes.txt could not be found!"
            )

        return jokes

    # Load saved favourites
    def load_favourites(self):

        try:
            with open(
                self.favourite_file, "r", encoding="utf-8"
            ) as file:

                saved_data = json.load(file)

                return [
                    (item["setup"], item["punchline"])
                    for item in saved_data
                    if "setup" in item and "punchline" in item
                ]

        except (FileNotFoundError, json.JSONDecodeError,
                TypeError, KeyError):
            return []

    # Save favourites to JSON file
    def save_favourites(self):

        saved_data = [
            {"setup": joke[0], "punchline": joke[1]}
            for joke in self.favourites
        ]

        with open(
            self.favourite_file, "w", encoding="utf-8"
        ) as file:

            json.dump(saved_data, file, indent=4)

    # Shuffle jokes to prevent repetition
    def reset_joke_list(self):

        self.remaining_jokes = list(range(len(self.jokes)))
        random.shuffle(self.remaining_jokes)

        if (
            len(self.remaining_jokes) > 1
            and self.previous_joke_index is not None
            and self.remaining_jokes[0] == self.previous_joke_index
        ):

            self.remaining_jokes[0], self.remaining_jokes[1] = (
                self.remaining_jokes[1],
                self.remaining_jokes[0]
            )

    # Create the main interface
    def create_interface(self):

        title = tk.Label(
            self.root,
            text="😂 Alexa, Joke Time!",
            font=("Arial", 25, "bold"),
            bg="#F3F0FF",
            fg="#59418C"
        )
        title.pack(pady=(20, 5))

        subtitle = tk.Label(
            self.root,
            text="Your daily dose of laughter!",
            font=("Arial", 12),
            bg="#F3F0FF",
            fg="#77708A"
        )
        subtitle.pack(pady=5)

        # Joke counter
        self.counter_label = tk.Label(
            self.root,
            text="Jokes viewed: 0",
            font=("Arial", 11, "bold"),
            bg="#E4DCF9",
            fg="#59418C",
            padx=15,
            pady=8
        )
        self.counter_label.pack(pady=12)

        # White joke card
        self.joke_card = tk.Frame(
            self.root,
            bg="white",
            padx=20,
            pady=15,
            highlightbackground="#D9CFF2",
            highlightthickness=2
        )
        self.joke_card.pack(
            padx=35,
            pady=10,
            fill="x"
        )

        # Joke setup
        self.setup_label = tk.Label(
            self.joke_card,
            text="Click the button below to get your first joke!",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#40345E",
            wraplength=530,
            justify="center",
            height=3
        )
        self.setup_label.pack(fill="x", pady=8)

        # Joke punchline
        self.punchline_label = tk.Label(
            self.joke_card,
            text="",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#D65A8A",
            wraplength=530,
            justify="center",
            height=2
        )
        self.punchline_label.pack(fill="x", pady=5)

        # Favourite button INSIDE the joke card
        self.favourite_button = self.create_button(
            self.joke_card,
            "♡ Add to Favourites",
            "#F8C6D8",
            "#703A54",
            self.toggle_favourite,
            25
        )
        self.favourite_button.pack(pady=10)
        self.favourite_button.config(state="disabled")

        # Status message
        self.status_label = tk.Label(
            self.root,
            text="Ready for a laugh?",
            font=("Arial", 10),
            bg="#F3F0FF",
            fg="#77708A"
        )
        self.status_label.pack(pady=5)

        # Main buttons
        button_frame = tk.Frame(
            self.root,
            bg="#F3F0FF"
        )
        button_frame.pack(pady=8)

        self.create_button(
            button_frame,
            "Alexa tell me a Joke",
            "#8064C7",
            "white",
            self.display_joke,
            28
        ).pack(pady=5)

        self.punchline_button = self.create_button(
            button_frame,
            "Show Punchline",
            "#F4A6C1",
            "#40345E",
            self.show_punchline,
            22
        )
        self.punchline_button.pack(pady=4)
        self.punchline_button.config(state="disabled")

        self.create_button(
            button_frame,
            "Next Joke",
            "#A7D8C9",
            "#263F39",
            self.display_joke,
            22
        ).pack(pady=4)

        self.create_button(
            button_frame,
            "View Favourite Jokes",
            "#C9B9ED",
            "#40345E",
            self.show_favourites,
            22
        ).pack(pady=4)

        self.create_button(
            button_frame,
            "Quit",
            "#E58B8B",
            "white",
            self.quit_app,
            22
        ).pack(pady=6)

        # Keyboard shortcut information
        shortcut_text = (
            "Enter = Next Joke | Space = Punchline | "
            "Ctrl + F = Favourite | "
            "Ctrl + L = View Favourites | Esc = Quit"
        )

        shortcut_label = tk.Label(
            self.root,
            text=shortcut_text,
            font=("Arial", 8),
            bg="#F3F0FF",
            fg="#77708A",
            wraplength=630
        )
        shortcut_label.pack(pady=5)

    # Create consistent buttons
    def create_button(
        self, parent, text, background, foreground, command, width
    ):

        return tk.Button(
            parent,
            text=text,
            font=("Arial", 11, "bold"),
            bg=background,
            fg=foreground,
            activebackground="#E2D8F5",
            activeforeground="#40345E",
            width=width,
            relief="flat",
            cursor="hand2",
            command=command,
            padx=8,
            pady=7
        )

    # Display a random joke
    def display_joke(self):

        if not self.jokes:
            messagebox.showwarning(
                "No Jokes",
                "There are no valid jokes in randomJokes.txt."
            )
            return

        if not self.remaining_jokes:
            self.reset_joke_list()

            self.status_label.config(
                text="New round! All jokes have been shown."
            )

        joke_index = self.remaining_jokes.pop()

        self.previous_joke_index = joke_index
        self.current_joke = self.jokes[joke_index]

        self.setup_label.config(
            text=self.current_joke[0],
            fg="#40345E"
        )

        self.punchline_label.config(text="")

        self.viewed_count += 1
        self.update_counter()

        self.punchline_button.config(state="normal")
        self.favourite_button.config(state="normal")

        self.update_favourite_button()

        self.status_label.config(
            text="Can you guess the punchline?"
        )

    # Show the punchline
    def show_punchline(self):

        if self.current_joke is None:
            return

        self.punchline_label.config(
            text="😂 " + self.current_joke[1],
            fg="#D65A8A"
        )

        self.status_label.config(
            text="Hope that made you laugh!"
        )

    # Update joke counter
    def update_counter(self):

        self.counter_label.config(
            text=f"Jokes viewed: {self.viewed_count} | "
                 f"Total jokes: {len(self.jokes)}"
        )

    # Add or remove a favourite
    def toggle_favourite(self):

        if self.current_joke is None:
            return

        if self.current_joke in self.favourites:

            self.favourites.remove(self.current_joke)

            self.status_label.config(
                text="Removed from favourites."
            )

        else:

            self.favourites.append(self.current_joke)

            self.status_label.config(
                text="Added to your favourites! ❤️"
            )

        self.save_favourites()
        self.update_favourite_button()

    # Change favourite button text
    def update_favourite_button(self):

        if self.current_joke in self.favourites:

            self.favourite_button.config(
                text="♥ Remove from Favourites"
            )

        else:

            self.favourite_button.config(
                text="♡ Add to Favourites"
            )

    # View favourite jokes
    def show_favourites(self):

        favourite_window = tk.Toplevel(self.root)
        favourite_window.title("My Favourite Jokes")
        favourite_window.geometry("520x430")
        favourite_window.configure(bg="#F3F0FF")

        heading = tk.Label(
            favourite_window,
            text="❤️ My Favourite Jokes",
            font=("Arial", 20, "bold"),
            bg="#F3F0FF",
            fg="#59418C"
        )
        heading.pack(pady=15)

        listbox = tk.Listbox(
            favourite_window,
            font=("Arial", 11),
            width=55,
            height=12,
            bg="white",
            fg="#40345E",
            selectbackground="#8064C7",
            activestyle="none"
        )
        listbox.pack(padx=15, pady=10)

        def refresh_list():

            listbox.delete(0, tk.END)

            for number, joke in enumerate(
                self.favourites, start=1
            ):
                listbox.insert(
                    tk.END,
                    f"{number}. {joke[0]}"
                )

        def show_selected_punchline():

            selection = listbox.curselection()

            if not selection:
                messagebox.showinfo(
                    "Select a Joke",
                    "Please select a favourite joke first."
                )
                return

            joke = self.favourites[selection[0]]

            messagebox.showinfo(
                "Punchline",
                joke[1],
                parent=favourite_window
            )

        def remove_selected_favourite():

            selection = listbox.curselection()

            if not selection:
                messagebox.showinfo(
                    "Select a Joke",
                    "Please select a joke to remove."
                )
                return

            del self.favourites[selection[0]]

            self.save_favourites()
            refresh_list()

            self.update_favourite_button()

        refresh_list()

        self.create_button(
            favourite_window,
            "Show Selected Punchline",
            "#F4A6C1",
            "#40345E",
            show_selected_punchline,
            25
        ).pack(pady=5)

        self.create_button(
            favourite_window,
            "Remove Selected Favourite",
            "#E58B8B",
            "white",
            remove_selected_favourite,
            25
        ).pack(pady=5)

        self.create_button(
            favourite_window,
            "Close",
            "#8064C7",
            "white",
            favourite_window.destroy,
            25
        ).pack(pady=8)

    # Keyboard shortcuts
    def keyboard_next_joke(self, event):
        self.display_joke()
        return "break"

    def keyboard_punchline(self, event):
        self.show_punchline()
        return "break"

    def keyboard_favourite(self, event):
        self.toggle_favourite()
        return "break"

    def keyboard_favourites(self, event):
        self.show_favourites()
        return "break"

    # Quit application
    def quit_app(self, event=None):
        self.root.destroy()


# Start the application
if __name__ == "__main__":

    root = tk.Tk()
    app = JokeAssistant(root)

    root.mainloop()
  