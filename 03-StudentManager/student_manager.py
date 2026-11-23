
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# File location
FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "studentMarks.txt"
)

# Application colours
DARK_BLUE = "#173B70"
BLUE = "#2F65A5"
LIGHT_BLUE = "#EAF1FA"
WHITE = "#FFFFFF"
TEXT_COLOUR = "#263445"


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
                line = line.strip()

                if not line:
                    continue

                parts = line.split(",")

                if len(parts) != 6:
                    continue

                student = {
                    "code": parts[0],
                    "name": parts[1],
                    "mark1": int(parts[2]),
                    "mark2": int(parts[3]),
                    "mark3": int(parts[4]),
                    "exam": int(parts[5])
                }

                self.students.append(student)

        except FileNotFoundError:
            messagebox.showerror(
                "File Error",
                "studentMarks.txt was not found.\n"
                "Keep it in the same folder as this Python file."
            )

        except ValueError:
            messagebox.showerror(
                "Data Error",
                "Please check the marks in studentMarks.txt."
            )

    def save_students(self):
        try:
            with open(FILE_PATH, "w") as file:
                file.write(str(len(self.students)) + "\n")

                for student in self.students:
                    file.write(
                        f"{student['code']},{student['name']},"
                        f"{student['mark1']},{student['mark2']},"
                        f"{student['mark3']},{student['exam']}\n"
                    )

            return True

        except OSError as error:
            messagebox.showerror(
                "Save Error",
                f"Could not save the records.\n{error}"
            )
            return False

    # Student calculations

    def coursework_total(self, student):
        return (
            student["mark1"]
            + student["mark2"]
            + student["mark3"]
        )

    def overall_total(self, student):
        return self.coursework_total(student) + student["exam"]

    def calculate_percentage(self, student):
        return (self.overall_total(student) / 160) * 100

    def calculate_grade(self, student):
        percentage = self.calculate_percentage(student)

        if percentage >= 70:
            return "A"
        elif percentage >= 60:
            return "B"
        elif percentage >= 50:
            return "C"
        elif percentage >= 40:
            return "D"
        else:
            return "F"

    # Main GUI

    def create_gui(self):
        header = tk.Frame(self.root, bg=DARK_BLUE, height=75)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="STUDENT MANAGEMENT SYSTEM",
            font=("Arial", 21, "bold"),
            bg=DARK_BLUE,
            fg=WHITE
        ).pack(side="left", padx=25, pady=20)

        tk.Label(
            header,
            text="Student Records & Performance",
            font=("Arial", 10),
            bg=DARK_BLUE,
            fg="#DCE8F7"
        ).pack(side="right", padx=25)

        content = tk.Frame(self.root, bg=LIGHT_BLUE)
        content.pack(fill="both", expand=True, padx=18, pady=15)

        # Left menu

        menu = tk.Frame(content, bg=DARK_BLUE, width=220)
        menu.pack(side="left", fill="y", padx=(0, 15))
        menu.pack_propagate(False)

        tk.Label(
            menu,
            text="MAIN MENU",
            font=("Arial", 14, "bold"),
            bg=DARK_BLUE,
            fg=WHITE
        ).pack(pady=(22, 18))

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

        for label, command in menu_buttons:
            tk.Button(
                menu,
                text=label,
                command=command,
                font=("Arial", 10, "bold"),
                bg=BLUE,
                fg=WHITE,
                activebackground="#477DBB",
                activeforeground=WHITE,
                relief="flat",
                cursor="hand2",
                anchor="w",
                padx=12,
                pady=10
            ).pack(fill="x", padx=12, pady=4)

        # Right side

        right = tk.Frame(content, bg=LIGHT_BLUE)
        right.pack(side="left", fill="both", expand=True)

        tk.Label(
            right,
            text="Performance Overview",
            font=("Arial", 16, "bold"),
            bg=LIGHT_BLUE,
            fg=DARK_BLUE
        ).pack(anchor="w", pady=(0, 10))

        # Dashboard cards

        self.dashboard_frame = tk.Frame(
            right,
            bg=LIGHT_BLUE
        )
        self.dashboard_frame.pack(fill="x", pady=(0, 12))

        self.dashboard_values = {}

        dashboard_items = [
            ("Total Students", "total"),
            ("Class Average", "average"),
            ("Highest Score", "highest"),
            ("Pass Rate", "pass_rate")
        ]

        for index, (label, key) in enumerate(dashboard_items):
            card = tk.Frame(
                self.dashboard_frame,
                bg=WHITE,
                highlightbackground="#D3DFED",
                highlightthickness=1
            )

            card.grid(
                row=0,
                column=index,
                sticky="nsew",
                padx=4
            )

            self.dashboard_frame.grid_columnconfigure(
                index,
                weight=1
            )

            tk.Label(
                card,
                text=label,
                font=("Arial", 9),
                bg=WHITE,
                fg="#63748A"
            ).pack(pady=(10, 3))

            value_label = tk.Label(
                card,
                text="0",
                font=("Arial", 17, "bold"),
                bg=WHITE,
                fg=DARK_BLUE
            )

            value_label.pack(pady=(0, 10))
            self.dashboard_values[key] = value_label

        # Search bar

        search_frame = tk.Frame(right, bg=LIGHT_BLUE)
        search_frame.pack(fill="x", pady=(0, 12))

        tk.Label(
            search_frame,
            text="Search students:",
            font=("Arial", 10, "bold"),
            bg=LIGHT_BLUE,
            fg=TEXT_COLOUR
        ).pack(side="left", padx=(0, 8))

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=7
        )

        tk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search,
            bg=BLUE,
            fg=WHITE,
            relief="flat",
            padx=15,
            pady=7,
            cursor="hand2"
        ).pack(side="left", padx=(8, 0))

        self.search_var.trace_add(
            "write",
            self.search_students
        )

        # Results heading

        results_heading = tk.Frame(right, bg=LIGHT_BLUE)
        results_heading.pack(fill="x", pady=(0, 7))

        tk.Label(
            results_heading,
            text="Student Records",
            font=("Arial", 16, "bold"),
            bg=LIGHT_BLUE,
            fg=DARK_BLUE
        ).pack(side="left")

        self.result_count = tk.Label(
            results_heading,
            text="",
            font=("Arial", 9),
            bg=LIGHT_BLUE,
            fg="#63748A"
        )

        self.result_count.pack(side="right")

        # Scrollable results area

        results_frame = tk.Frame(right, bg=WHITE)
        results_frame.pack(fill="both", expand=True)

        self.results = tk.Text(
            results_frame,
            font=("Consolas", 10),
            bg=WHITE,
            fg=TEXT_COLOUR,
            wrap="none",
            padx=12,
            pady=12,
            relief="flat",
            state="disabled"
        )

        vertical_scrollbar = ttk.Scrollbar(
            results_frame,
            orient="vertical",
            command=self.results.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            results_frame,
            orient="horizontal",
            command=self.results.xview
        )

        self.results.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.results.grid(row=0, column=0, sticky="nsew")
        vertical_scrollbar.grid(row=0, column=1, sticky="ns")
        horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)

        self.results.bind(
            "<MouseWheel>",
            self.mouse_wheel_scroll
        )

        # Footer

        tk.Label(
            self.root,
            text="Student Management System | Records are saved automatically",
            font=("Arial", 9),
            bg=DARK_BLUE,
            fg=WHITE,
            pady=8
        ).pack(fill="x")

        self.update_dashboard()

    # Display helpers

    def set_results(self, text):
        self.results.config(state="normal")
        self.results.delete("1.0", tk.END)
        self.results.insert(tk.END, text)
        self.results.config(state="disabled")
        self.results.yview_moveto(0)

    def mouse_wheel_scroll(self, event):
        self.results.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )
        return "break"

    def display_record(self, student):
        return (
            f"Student Number  : {student['code']}\n"
            f"Student Name    : {student['name']}\n"
            f"Coursework 1    : {student['mark1']}/20\n"
            f"Coursework 2    : {student['mark2']}/20\n"
            f"Coursework 3    : {student['mark3']}/20\n"
            f"Coursework Total: {self.coursework_total(student)}/60\n"
            f"Exam Mark       : {student['exam']}/100\n"
            f"Overall Total   : {self.overall_total(student)}/160\n"
            f"Percentage      : {self.calculate_percentage(student):.2f}%\n"
            f"Grade           : {self.calculate_grade(student)}\n"
            f"{'-' * 55}\n"
        )

    def show_all_students(self):
        self.search_var.set("")

        if not self.students:
            self.set_results("No student records found.")
            self.result_count.config(text="0 students")
            return

        output = "ALL STUDENT RECORDS\n"
        output += "=" * 55 + "\n\n"

        for student in self.students:
            output += self.display_record(student) + "\n"

        self.set_results(output)
        self.result_count.config(
            text=f"{len(self.students)} students"
        )

    # Search bar

    def search_students(self, *args):
        query = self.search_var.get().strip().lower()

        if not query:
            self.show_all_students_without_clearing_search()
            return

        matches = [
            student for student in self.students
            if query in student["name"].lower()
            or query in student["code"].lower()
        ]

        output = f"SEARCH RESULTS FOR: {query}\n"
        output += "=" * 55 + "\n\n"

        if matches:
            for student in matches:
                output += self.display_record(student) + "\n"
        else:
            output += "No matching students found.\n"

        self.set_results(output)
        self.result_count.config(
            text=f"{len(matches)} matching students"
        )

    def show_all_students_without_clearing_search(self):
        output = "ALL STUDENT RECORDS\n"
        output += "=" * 55 + "\n\n"

        if not self.students:
            output += "No student records found."
        else:
            for student in self.students:
                output += self.display_record(student) + "\n"

        self.set_results(output)
        self.result_count.config(
            text=f"{len(self.students)} students"
        )

    def clear_search(self):
        self.search_var.set("")

    # Find student using a pop-up

    def find_student(self, query):
        query = query.strip().lower()

        matches = [
            student for student in self.students
            if student["code"] == query
            or query in student["name"].lower()
        ]

        if not matches:
            messagebox.showinfo(
                "Not Found",
                "No student matched your search."
            )
            return None

        if len(matches) == 1:
            return matches[0]

        names = "\n".join(
            f"{student['code']} - {student['name']}"
            for student in matches
        )

        selected_code = simpledialog.askstring(
            "Multiple Matches",
            "More than one student was found.\n"
            "Enter the student number:\n\n" + names,
            parent=self.root
        )

        if not selected_code:
            return None

        for student in matches:
            if student["code"] == selected_code.strip():
                return student

        messagebox.showerror(
            "Not Found",
            "That student number is not in the search results."
        )
        return None

    # Performance dashboard

    def update_dashboard(self):
        total = len(self.students)

        if total == 0:
            average = 0
            highest = 0
            pass_rate = 0
        else:
            percentages = [
                self.calculate_percentage(student)
                for student in self.students
            ]

            average = sum(percentages) / total
            highest = max(percentages)

            passed = sum(
                1 for value in percentages if value >= 40
            )

            pass_rate = (passed / total) * 100

        self.dashboard_values["total"].config(text=str(total))
        self.dashboard_values["average"].config(
            text=f"{average:.1f}%"
        )
        self.dashboard_values["highest"].config(
            text=f"{highest:.1f}%"
        )
        self.dashboard_values["pass_rate"].config(
            text=f"{pass_rate:.1f}%"
        )

    def show_dashboard(self):
        self.search_var.set("")
        self.update_dashboard()

        grades = {
            "A": 0,
            "B": 0,
            "C": 0,
            "D": 0,
            "F": 0
        }

        for student in self.students:
            grade = self.calculate_grade(student)
            grades[grade] += 1

        output = "STUDENT PERFORMANCE DASHBOARD\n"
        output += "=" * 55 + "\n\n"

        output += f"Total Students: {len(self.students)}\n"

        if self.students:
            percentages = [
                self.calculate_percentage(student)
                for student in self.students
            ]

            average = sum(percentages) / len(percentages)
            highest = max(percentages)
            lowest = min(percentages)

            passed = sum(
                1 for value in percentages if value >= 40
            )

            failed = len(self.students) - passed

            output += f"Class Average: {average:.2f}%\n"
            output += f"Highest Percentage: {highest:.2f}%\n"
            output += f"Lowest Percentage: {lowest:.2f}%\n"
            output += f"Students Passed: {passed}\n"
            output += f"Students Failed: {failed}\n"
            output += (
                f"Pass Rate: "
                f"{(passed / len(self.students)) * 100:.2f}%\n"
            )

        output += "\nGRADE DISTRIBUTION\n"
        output += "-" * 30 + "\n"

        for grade, count in grades.items():
            output += f"Grade {grade}: {count} student(s)\n"

        output += "\nGRADE THRESHOLDS\n"
        output += "-" * 30 + "\n"
        output += "A: 70% and above\n"
        output += "B: 60% to 69.99%\n"
        output += "C: 50% to 59.99%\n"
        output += "D: 40% to 49.99%\n"
        output += "F: Below 40%\n"

        self.set_results(output)
        self.result_count.config(text="Class performance summary")

    # View individual student

    def view_individual(self):
        query = simpledialog.askstring(
            "View Individual Student",
            "Enter Student Name or Student Number:",
            parent=self.root
        )

        if not query:
            return

        student = self.find_student(query)

        if student:
            output = "INDIVIDUAL STUDENT RECORD\n"
            output += "=" * 55 + "\n\n"
            output += self.display_record(student)

            self.set_results(output)
            self.result_count.config(text="1 student")

    # Highest scorer

    def show_highest(self):
        if not self.students:
            messagebox.showinfo(
                "No Records",
                "There are no students to display."
            )
            return

        student = max(
            self.students,
            key=self.calculate_percentage
        )

        self.set_results(
            "HIGHEST SCORING STUDENT\n"
            + "=" * 55 + "\n\n"
            + self.display_record(student)
        )

        self.result_count.config(text="Highest scorer")

    # Lowest scorer

    def show_lowest(self):
        if not self.students:
            messagebox.showinfo(
                "No Records",
                "There are no students to display."
            )
            return

        student = min(
            self.students,
            key=self.calculate_percentage
        )

        self.set_results(
            "LOWEST SCORING STUDENT\n"
            + "=" * 55 + "\n\n"
            + self.display_record(student)
        )

        self.result_count.config(text="Lowest scorer")

    # Sort students

    def sort_students(self):
        if not self.students:
            messagebox.showinfo(
                "No Records",
                "No students available."
            )
            return

        choice = simpledialog.askstring(
            "Sort Students",
            "Enter A for Ascending or D for Descending:",
            parent=self.root
        )

        if not choice:
            return

        choice = choice.strip().upper()

        if choice not in ["A", "D"]:
            messagebox.showerror(
                "Invalid Choice",
                "Please enter A or D."
            )
            return

        sorted_students = sorted(
            self.students,
            key=self.calculate_percentage,
            reverse=(choice == "D")
        )

        output = "SORTED STUDENT RECORDS\n"
        output += "=" * 55 + "\n\n"

        for student in sorted_students:
            output += self.display_record(student) + "\n"

        self.set_results(output)
        self.result_count.config(text="Sorted student records")

    # Validate student information

    def validate_student_data(
        self,
        code,
        first_name,
        last_name,
        mark1,
        mark2,
        mark3,
        exam,
        existing_code=None
    ):

        if not code.isdigit() or len(code) != 4:
            messagebox.showerror(
                "Invalid Student Number",
                "Student number must contain exactly 4 digits."
            )
            return None

        if any(
            student["code"] == code
            and student["code"] != existing_code
            for student in self.students
        ):
            messagebox.showerror(
                "Duplicate Student",
                "This student number already exists."
            )
            return None

        if not first_name.strip() or not last_name.strip():
            messagebox.showerror(
                "Missing Name",
                "Please enter both first name and last name."
            )
            return None

        allowed_characters = " -'"

        for name in [first_name, last_name]:
            if not all(
                character.isalpha()
                or character in allowed_characters
                for character in name.strip()
            ):
                messagebox.showerror(
                    "Invalid Name",
                    "Names should contain letters only."
                )
                return None

        try:
            marks = [
                int(mark1),
                int(mark2),
                int(mark3),
                int(exam)
            ]
        except ValueError:
            messagebox.showerror(
                "Invalid Marks",
                "Please enter whole numbers for all marks."
            )
            return None

        if any(mark < 0 or mark > 20 for mark in marks[:3]):
            messagebox.showerror(
                "Invalid Coursework Mark",
                "Each coursework mark must be between 0 and 20."
            )
            return None

        if marks[3] < 0 or marks[3] > 100:
            messagebox.showerror(
                "Invalid Exam Mark",
                "The exam mark must be between 0 and 100."
            )
            return None

        return {
            "code": code,
            "name": (
                first_name.strip().capitalize()
                + " "
                + last_name.strip().capitalize()
            ),
            "mark1": marks[0],
            "mark2": marks[1],
            "mark3": marks[2],
            "exam": marks[3]
        }

    # Add student

    def add_student(self):
        self.open_student_form("Add Student")

    # Update student

    def update_student(self):
        query = simpledialog.askstring(
            "Update Student",
            "Enter Student Name or Student Number:",
            parent=self.root
        )

        if not query:
            return

        student = self.find_student(query)

        if student:
            self.open_student_form("Update Student", student)

    # Add and update form

    def open_student_form(self, title, student=None):
        is_update = student is not None

        form = tk.Toplevel(self.root)
        form.title(title)
        form.geometry("440x590")
        form.configure(bg=LIGHT_BLUE)
        form.resizable(False, False)
        form.transient(self.root)
        form.grab_set()

        tk.Label(
            form,
            text=title.upper(),
            font=("Arial", 17, "bold"),
            bg=LIGHT_BLUE,
            fg=DARK_BLUE
        ).pack(pady=(20, 15))

        fields_frame = tk.Frame(form, bg=LIGHT_BLUE)
        fields_frame.pack(fill="both", expand=True, padx=35)

        entries = {}

        first_name = ""
        last_name = ""

        if is_update:
            name_parts = student["name"].split(maxsplit=1)
            first_name = name_parts[0]
            last_name = (
                name_parts[1] if len(name_parts) > 1 else ""
            )

        field_values = [
            ("Student Number", "code",
             student["code"] if is_update else ""),
            ("First Name", "first_name", first_name),
            ("Last Name", "last_name", last_name),
            ("Coursework 1 (out of 20)", "mark1",
             student["mark1"] if is_update else ""),
            ("Coursework 2 (out of 20)", "mark2",
             student["mark2"] if is_update else ""),
            ("Coursework 3 (out of 20)", "mark3",
             student["mark3"] if is_update else ""),
            ("Exam (out of 100)", "exam",
             student["exam"] if is_update else "")
        ]

        for label_text, key, value in field_values:
            tk.Label(
                fields_frame,
                text=label_text,
                font=("Arial", 10, "bold"),
                bg=LIGHT_BLUE,
                fg=TEXT_COLOUR
            ).pack(anchor="w", pady=(5, 3))

            entry = tk.Entry(
                fields_frame,
                font=("Arial", 11),
                relief="solid",
                bd=1
            )

            entry.pack(fill="x", ipady=6)
            entry.insert(0, str(value))

            if is_update and key == "code":
                entry.config(state="readonly")

            entries[key] = entry

        def save_record():
            code = entries["code"].get().strip()
            first = entries["first_name"].get()
            last = entries["last_name"].get()

            new_student = self.validate_student_data(
                code,
                first,
                last,
                entries["mark1"].get().strip(),
                entries["mark2"].get().strip(),
                entries["mark3"].get().strip(),
                entries["exam"].get().strip(),
                existing_code=student["code"] if is_update else None
            )

            if new_student is None:
                return

            old_students = [
                item.copy() for item in self.students
            ]

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
                    "Student record updated successfully."
                    if is_update
                    else "Student added successfully."
                )
            else:
                self.students = old_students

        tk.Button(
            form,
            text="Save Student",
            command=save_record,
            font=("Arial", 11, "bold"),
            bg=DARK_BLUE,
            fg=WHITE,
            relief="flat",
            cursor="hand2",
            pady=10
        ).pack(fill="x", padx=35, pady=18)

    # Delete student

    def delete_student(self):
        query = simpledialog.askstring(
            "Delete Student",
            "Enter Student Name or Student Number:",
            parent=self.root
        )

        if not query:
            return

        student = self.find_student(query)

        if not student:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete:\n\n"
            f"{student['name']} ({student['code']})?"
        )

        if not confirm:
            return

        old_students = [
            item.copy() for item in self.students
        ]

        self.students = [
            item for item in self.students
            if item["code"] != student["code"]
        ]

        if self.save_students():
            self.update_dashboard()
            self.show_all_students()

            messagebox.showinfo(
                "Success",
                "Student deleted successfully."
            )
        else:
            self.students = old_students


# Start application

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()
