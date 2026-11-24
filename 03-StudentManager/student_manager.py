import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# File location
FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "studentMarks.txt")

# Application colours
DARK_BLUE = "#173B70"
BLUE = "#2F65A5"
LIGHT_BLUE = "#EAF1FA"
WHITE = "#FFFFFF"
TEXT_COLOUR = "#263445"
GREY = "#63748A"


def label(parent, text, size=10, bold=False, bg=LIGHT_BLUE, fg=TEXT_COLOUR, **kw):
    """Create a label with the application's standard look."""
    return tk.Label(parent, text=text, font=("Arial", size, "bold" if bold else "normal"),
                    bg=bg, fg=fg, **kw)


def button(parent, text, command, **kw):
    """Create a flat blue button; any option can be overridden."""
    options = dict(bg=BLUE, fg=WHITE, relief="flat", cursor="hand2")
    options.update(kw)
    return tk.Button(parent, text=text, command=command, **options)


def entry(parent, **kw):
    return tk.Entry(parent, relief="solid", bd=1, **kw)


class StudentManager:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1150x780")
        self.root.minsize(950, 650)
        self.root.configure(bg=LIGHT_BLUE)

        self.students = []
        self.search_var = tk.StringVar()

        self.load_students()
        self.create_gui()
        self.show_all_students()

    # File handling

    def load_students(self):
        self.students = []
        try:
            with open(FILE_PATH, "r") as file:
                lines = file.readlines()

            for line in lines[1:]:
                parts = line.strip().split(",")
                if len(parts) != 6:
                    continue
                self.students.append({
                    "code": parts[0], "name": parts[1],
                    "mark1": int(parts[2]), "mark2": int(parts[3]),
                    "mark3": int(parts[4]), "exam": int(parts[5])
                })

        except FileNotFoundError:
            messagebox.showerror(
                "File Error",
                "studentMarks.txt was not found.\n"
                "Keep it in the same folder as this Python file."
            )
        except ValueError:
            messagebox.showerror("Data Error", "Please check the marks in studentMarks.txt.")

    def save_students(self):
        try:
            with open(FILE_PATH, "w") as file:
                file.write(str(len(self.students)) + "\n")
                for s in self.students:
                    file.write(f"{s['code']},{s['name']},{s['mark1']},"
                               f"{s['mark2']},{s['mark3']},{s['exam']}\n")
            return True
        except OSError as error:
            messagebox.showerror("Save Error", f"Could not save the records.\n{error}")
            return False

    # Student calculations

    def coursework_total(self, student):
        return student["mark1"] + student["mark2"] + student["mark3"]

    def overall_total(self, student):
        return self.coursework_total(student) + student["exam"]

    def calculate_percentage(self, student):
        return (self.overall_total(student) / 160) * 100

    def calculate_grade(self, student):
        percentage = self.calculate_percentage(student)
        return next((g for g, limit in zip("ABCD", (70, 60, 50, 40))
                     if percentage >= limit), "F")

    def percentages(self):
        return [self.calculate_percentage(s) for s in self.students]

    # Main GUI

    def create_gui(self):
        header = tk.Frame(self.root, bg=DARK_BLUE, height=75)
        header.pack(fill="x")
        header.pack_propagate(False)

        label(header, "STUDENT MANAGEMENT SYSTEM", 21, True, DARK_BLUE, WHITE).pack(
            side="left", padx=25, pady=20)
        label(header, "Student Records & Performance", 10, False, DARK_BLUE, "#DCE8F7").pack(
            side="right", padx=25)

        content = tk.Frame(self.root, bg=LIGHT_BLUE)
        content.pack(fill="both", expand=True, padx=18, pady=15)

        # Left menu

        menu = tk.Frame(content, bg=DARK_BLUE, width=220)
        menu.pack(side="left", fill="y", padx=(0, 15))
        menu.pack_propagate(False)

        label(menu, "MAIN MENU", 14, True, DARK_BLUE, WHITE).pack(pady=(22, 18))

        menu_buttons = [
            ("View All Students", self.show_all_students),
            ("View Individual Student", self.view_individual),
            ("Highest Scorer", self.show_highest),
            ("Lowest Scorer", self.show_lowest),
            ("Sort Students", self.sort_students),
            ("Add Student", self.add_student),
            ("Update Student", self.update_student),
            ("Delete Student", self.delete_student),
            ("Performance Dashboard", self.show_dashboard)
        ]

        for text, command in menu_buttons:
            button(menu, text, command, font=("Arial", 10, "bold"),
                   activebackground="#477DBB", activeforeground=WHITE,
                   anchor="w", padx=12, pady=10).pack(fill="x", padx=12, pady=4)

        # Right side

        right = tk.Frame(content, bg=LIGHT_BLUE)
        right.pack(side="left", fill="both", expand=True)

        label(right, "Performance Overview", 16, True, fg=DARK_BLUE).pack(anchor="w", pady=(0, 10))

        # Dashboard cards

        dashboard_frame = tk.Frame(right, bg=LIGHT_BLUE)
        dashboard_frame.pack(fill="x", pady=(0, 12))

        self.dashboard_values = {}
        dashboard_items = [("Total Students", "total"), ("Class Average", "average"),
                           ("Highest Score", "highest"), ("Pass Rate", "pass_rate")]

        for index, (text, key) in enumerate(dashboard_items):
            card = tk.Frame(dashboard_frame, bg=WHITE,
                            highlightbackground="#D3DFED", highlightthickness=1)
            card.grid(row=0, column=index, sticky="nsew", padx=4)
            dashboard_frame.grid_columnconfigure(index, weight=1)

            label(card, text, 9, False, WHITE, GREY).pack(pady=(10, 3))
            value_label = label(card, "0", 17, True, WHITE, DARK_BLUE)
            value_label.pack(pady=(0, 10))
            self.dashboard_values[key] = value_label

        # Search bar

        search_frame = tk.Frame(right, bg=LIGHT_BLUE)
        search_frame.pack(fill="x", pady=(0, 12))

        label(search_frame, "Search students:", 10, True).pack(side="left", padx=(0, 8))
        entry(search_frame, textvariable=self.search_var, font=("Arial", 11)).pack(
            side="left", fill="x", expand=True, ipady=7)
        button(search_frame, "Clear", lambda: self.search_var.set(""),
               padx=15, pady=7).pack(side="left", padx=(8, 0))

        self.search_var.trace_add("write", self.search_students)

        # Results heading

        results_heading = tk.Frame(right, bg=LIGHT_BLUE)
        results_heading.pack(fill="x", pady=(0, 7))

        label(results_heading, "Student Records", 16, True, fg=DARK_BLUE).pack(side="left")
        self.result_count = label(results_heading, "", 9, False, fg=GREY)
        self.result_count.pack(side="right")

        # Scrollable results area

        results_frame = tk.Frame(right, bg=WHITE)
        results_frame.pack(fill="both", expand=True)

        self.results = tk.Text(results_frame, font=("Consolas", 10), bg=WHITE, fg=TEXT_COLOUR,
                               wrap="none", padx=12, pady=12, relief="flat", state="disabled")
        vertical = ttk.Scrollbar(results_frame, orient="vertical", command=self.results.yview)
        horizontal = ttk.Scrollbar(results_frame, orient="horizontal", command=self.results.xview)
        self.results.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)

        self.results.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)

        self.results.bind("<MouseWheel>", self.mouse_wheel_scroll)

        # Footer

        label(self.root, "Student Management System | Records are saved automatically",
              9, False, DARK_BLUE, WHITE, pady=8).pack(fill="x")

        self.update_dashboard()

    # Display helpers

    def set_results(self, text, count=None):
        self.results.config(state="normal")
        self.results.delete("1.0", tk.END)
        self.results.insert(tk.END, text)
        self.results.config(state="disabled")
        self.results.yview_moveto(0)
        if count is not None:
            self.result_count.config(text=count)

    def mouse_wheel_scroll(self, event):
        self.results.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def display_record(self, s):
        return (
            f"Student Number  : {s['code']}\n"
            f"Student Name    : {s['name']}\n"
            f"Coursework 1    : {s['mark1']}/20\n"
            f"Coursework 2    : {s['mark2']}/20\n"
            f"Coursework 3    : {s['mark3']}/20\n"
            f"Coursework Total: {self.coursework_total(s)}/60\n"
            f"Exam Mark       : {s['exam']}/100\n"
            f"Overall Total   : {self.overall_total(s)}/160\n"
            f"Percentage      : {self.calculate_percentage(s):.2f}%\n"
            f"Grade           : {self.calculate_grade(s)}\n"
            f"{'-' * 55}\n"
        )

    def render(self, title, records, count, empty=""):
        """Show a heading followed by a list of student records."""
        output = f"{title}\n{'=' * 55}\n\n"
        output += "".join(self.display_record(s) + "\n" for s in records) or empty + "\n"
        self.set_results(output, count)

    def show_all_students(self):
        self.search_var.set("")
        if not self.students:
            self.set_results("No student records found.", "0 students")

    # Search bar (also draws the full list when the search box is empty)

    def search_students(self, *args):
        query = self.search_var.get().strip().lower()

        if not query:
            self.render("ALL STUDENT RECORDS", self.students,
                        f"{len(self.students)} students", "No student records found.")
            return

        matches = [s for s in self.students
                   if query in s["name"].lower() or query in s["code"].lower()]
        self.render(f"SEARCH RESULTS FOR: {query}", matches,
                    f"{len(matches)} matching students", "No matching students found.")

    # Find student using a pop-up

    def ask(self, title, prompt="Enter Student Name or Student Number:"):
        return simpledialog.askstring(title, prompt, parent=self.root)

    def find_student(self, query):
        query = query.strip().lower()
        matches = [s for s in self.students
                   if s["code"] == query or query in s["name"].lower()]

        if not matches:
            messagebox.showinfo("Not Found", "No student matched your search.")
            return None

        if len(matches) == 1:
            return matches[0]

        names = "\n".join(f"{s['code']} - {s['name']}" for s in matches)
        selected = self.ask("Multiple Matches",
                            "More than one student was found.\n"
                            "Enter the student number:\n\n" + names)
        if not selected:
            return None

        for s in matches:
            if s["code"] == selected.strip():
                return s

        messagebox.showerror("Not Found", "That student number is not in the search results.")
        return None

    def ask_student(self, title):
        """Ask for a name/number and return the matching student (or None)."""
        query = self.ask(title)
        return self.find_student(query) if query else None

    # Performance dashboard

    def update_dashboard(self):
        total = len(self.students)
        percentages = self.percentages()
        average = sum(percentages) / total if total else 0
        highest = max(percentages, default=0)
        pass_rate = sum(p >= 40 for p in percentages) / total * 100 if total else 0

        values = {"total": str(total), "average": f"{average:.1f}%",
                  "highest": f"{highest:.1f}%", "pass_rate": f"{pass_rate:.1f}%"}
        for key, text in values.items():
            self.dashboard_values[key].config(text=text)

    def show_dashboard(self):
        self.search_var.set("")
        self.update_dashboard()

        grades = dict.fromkeys("ABCDF", 0)
        for s in self.students:
            grades[self.calculate_grade(s)] += 1

        output = f"STUDENT PERFORMANCE DASHBOARD\n{'=' * 55}\n\n"
        output += f"Total Students: {len(self.students)}\n"

        if self.students:
            percentages = self.percentages()
            passed = sum(p >= 40 for p in percentages)
            output += (
                f"Class Average: {sum(percentages) / len(percentages):.2f}%\n"
                f"Highest Percentage: {max(percentages):.2f}%\n"
                f"Lowest Percentage: {min(percentages):.2f}%\n"
                f"Students Passed: {passed}\n"
                f"Students Failed: {len(percentages) - passed}\n"
                f"Pass Rate: {passed / len(percentages) * 100:.2f}%\n"
            )

        output += f"\nGRADE DISTRIBUTION\n{'-' * 30}\n"
        output += "".join(f"Grade {g}: {n} student(s)\n" for g, n in grades.items())
        output += (
            f"\nGRADE THRESHOLDS\n{'-' * 30}\n"
            "A: 70% and above\n"
            "B: 60% to 69.99%\n"
            "C: 50% to 59.99%\n"
            "D: 40% to 49.99%\n"
            "F: Below 40%\n"
        )
        self.set_results(output, "Class performance summary")

    # View individual student

    def view_individual(self):
        student = self.ask_student("View Individual Student")
        if student:
            self.render("INDIVIDUAL STUDENT RECORD", [student], "1 student")

    # Highest / lowest scorer

    def show_extreme(self, function, title, count):
        if not self.students:
            messagebox.showinfo("No Records", "There are no students to display.")
            return
        student = function(self.students, key=self.calculate_percentage)
        self.render(title, [student], count)

    def show_highest(self):
        self.show_extreme(max, "HIGHEST SCORING STUDENT", "Highest scorer")

    def show_lowest(self):
        self.show_extreme(min, "LOWEST SCORING STUDENT", "Lowest scorer")

    # Sort students

    def sort_students(self):
        if not self.students:
            messagebox.showinfo("No Records", "No students available.")
            return

        choice = self.ask("Sort Students", "Enter A for Ascending or D for Descending:")
        if not choice:
            return

        choice = choice.strip().upper()
        if choice not in ("A", "D"):
            messagebox.showerror("Invalid Choice", "Please enter A or D.")
            return

        sorted_students = sorted(self.students, key=self.calculate_percentage,
                                 reverse=(choice == "D"))
        self.render("SORTED STUDENT RECORDS", sorted_students, "Sorted student records")

    # Validate student information

    def validate_student_data(self, code, first_name, last_name, mark1, mark2, mark3,
                              exam, existing_code=None):

        def fail(title, message):
            messagebox.showerror(title, message)

        if not code.isdigit() or len(code) != 4:
            return fail("Invalid Student Number", "Student number must contain exactly 4 digits.")

        if any(s["code"] == code and s["code"] != existing_code for s in self.students):
            return fail("Duplicate Student", "This student number already exists.")

        if not first_name.strip() or not last_name.strip():
            return fail("Missing Name", "Please enter both first name and last name.")

        for name in (first_name, last_name):
            if not all(c.isalpha() or c in " -'" for c in name.strip()):
                return fail("Invalid Name", "Names should contain letters only.")

        try:
            marks = [int(m) for m in (mark1, mark2, mark3, exam)]
        except ValueError:
            return fail("Invalid Marks", "Please enter whole numbers for all marks.")

        if any(not 0 <= m <= 20 for m in marks[:3]):
            return fail("Invalid Coursework Mark", "Each coursework mark must be between 0 and 20.")

        if not 0 <= marks[3] <= 100:
            return fail("Invalid Exam Mark", "The exam mark must be between 0 and 100.")

        return {
            "code": code,
            "name": first_name.strip().capitalize() + " " + last_name.strip().capitalize(),
            "mark1": marks[0], "mark2": marks[1], "mark3": marks[2], "exam": marks[3]
        }

    # Add / update student

    def add_student(self):
        self.open_student_form("Add Student")

    def update_student(self):
        student = self.ask_student("Update Student")
        if student:
            self.open_student_form("Update Student", student)

    def open_student_form(self, title, student=None):
        is_update = student is not None

        form = tk.Toplevel(self.root)
        form.title(title)
        form.geometry("440x590")
        form.configure(bg=LIGHT_BLUE)
        form.resizable(False, False)
        form.transient(self.root)
        form.grab_set()

        label(form, title.upper(), 17, True, fg=DARK_BLUE).pack(pady=(20, 15))

        fields_frame = tk.Frame(form, bg=LIGHT_BLUE)
        fields_frame.pack(fill="both", expand=True, padx=35)

        first_name = last_name = ""
        if is_update:
            name_parts = student["name"].split(maxsplit=1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""

        def current(key):
            return student[key] if is_update else ""

        field_values = [
            ("Student Number", "code", current("code")),
            ("First Name", "first_name", first_name),
            ("Last Name", "last_name", last_name),
            ("Coursework 1 (out of 20)", "mark1", current("mark1")),
            ("Coursework 2 (out of 20)", "mark2", current("mark2")),
            ("Coursework 3 (out of 20)", "mark3", current("mark3")),
            ("Exam (out of 100)", "exam", current("exam"))
        ]

        entries = {}
        for text, key, value in field_values:
            label(fields_frame, text, 10, True).pack(anchor="w", pady=(5, 3))
            field = entry(fields_frame, font=("Arial", 11))
            field.pack(fill="x", ipady=6)
            field.insert(0, str(value))
            if is_update and key == "code":
                field.config(state="readonly")
            entries[key] = field

        def save_record():
            values = {key: field.get().strip() for key, field in entries.items()}

            new_student = self.validate_student_data(
                values["code"],
                entries["first_name"].get(),
                entries["last_name"].get(),
                values["mark1"], values["mark2"], values["mark3"], values["exam"],
                existing_code=student["code"] if is_update else None
            )
            if new_student is None:
                return

            old_students = [item.copy() for item in self.students]

            if is_update:
                student.update(new_student)
            else:
                self.students.append(new_student)

            if self.save_students():
                form.destroy()
                self.update_dashboard()
                self.show_all_students()
                messagebox.showinfo(
                    "Success",
                    "Student record updated successfully." if is_update
                    else "Student added successfully."
                )
            else:
                self.students = old_students

        button(form, "Save Student", save_record, font=("Arial", 11, "bold"),
               bg=DARK_BLUE, pady=10).pack(fill="x", padx=35, pady=18)

    # Delete student

    def delete_student(self):
        student = self.ask_student("Delete Student")
        if not student:
            return

        if not messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete:\n\n{student['name']} ({student['code']})?"):
            return

        old_students = [item.copy() for item in self.students]
        self.students = [s for s in self.students if s["code"] != student["code"]]

        if self.save_students():
            self.update_dashboard()
            self.show_all_students()
            messagebox.showinfo("Success", "Student deleted successfully.")
        else:
            self.students = old_students


# Start application

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()