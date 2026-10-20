import json
from pathlib import Path


class StudentManagementSystem:
    """Manage student records using JSON file storage."""

    def __init__(self, storage_file="students.json"):
        self.storage_file = Path(storage_file)
        self.students = {}
        self._load_students()

    def _load_students(self):
        """Load student records from the JSON file."""
        if not self.storage_file.exists():
            self.students = {}
            return

        try:
            with self.storage_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("Student data must be a JSON object.")

            self.students = data

        except json.JSONDecodeError as error:
            raise ValueError("The student data file contains invalid JSON.") from error

    def _save_students(self):
        """Save student records to the JSON file."""
        with self.storage_file.open("w", encoding="utf-8") as file:
            json.dump(self.students, file, indent=4)

    @staticmethod
    def _validate_student(student_id, name, age, course):
        """Validate the supplied student details."""
        if not isinstance(student_id, str) or not student_id.strip():
            raise ValueError("Student ID cannot be empty.")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Student name cannot be empty.")

        if not isinstance(age, int) or isinstance(age, bool) or age <= 0:
            raise ValueError("Age must be a positive integer.")

        if not isinstance(course, str) or not course.strip():
            raise ValueError("Course cannot be empty.")

    def add_student(self, student_id, name, age, course):
        """Add a new student record."""
        self._validate_student(student_id, name, age, course)
        student_id = student_id.strip()

        if student_id in self.students:
            raise ValueError(f"Student ID '{student_id}' already exists.")

        self.students[student_id] = {
            "student_id": student_id,
            "name": name.strip(),
            "age": age,
            "course": course.strip(),
        }

        self._save_students()
        return self.students[student_id].copy()

    def get_student(self, student_id):
        """Find a student by ID."""
        if not isinstance(student_id, str) or not student_id.strip():
            raise ValueError("Student ID cannot be empty.")

        student = self.students.get(student_id.strip())

        if student is None:
            raise KeyError(f"Student ID '{student_id}' was not found.")

        return student.copy()

    def get_all_students(self):
        """Return all student records."""
        return [student.copy() for student in self.students.values()]

    def update_student(self, student_id, name=None, age=None, course=None):
        """Update the supplied fields of an existing student."""
        student = self.get_student(student_id)
        student_id = student_id.strip()

        new_name = student["name"] if name is None else name
        new_age = student["age"] if age is None else age
        new_course = student["course"] if course is None else course

        self._validate_student(student_id, new_name, new_age, new_course)

        self.students[student_id] = {
            "student_id": student_id,
            "name": new_name.strip(),
            "age": new_age,
            "course": new_course.strip(),
        }

        self._save_students()
        return self.students[student_id].copy()

    def delete_student(self, student_id):
        """Delete a student record."""
        self.get_student(student_id)
        del self.students[student_id.strip()]
        self._save_students()
        return True


def main():
    system = StudentManagementSystem()

    while True:
        print("\n========== STUDENT MANAGEMENT SYSTEM ==========")
        print("1. Add student")
        print("2. View all students")
        print("3. Search student")
        print("4. Update student")
        print("5. Delete student")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                student_id = input("Student ID: ").strip()
                name = input("Student name: ").strip()
                age = int(input("Age: ").strip())
                course = input("Course: ").strip()

                student = system.add_student(student_id, name, age, course)
                print(f"Student '{student['name']}' added successfully.")

            elif choice == "2":
                students = system.get_all_students()

                if not students:
                    print("No student records found.")
                else:
                    for student in students:
                        print(
                            f"ID: {student['student_id']} | "
                            f"Name: {student['name']} | "
                            f"Age: {student['age']} | "
                            f"Course: {student['course']}"
                        )

            elif choice == "3":
                student_id = input("Enter student ID: ").strip()
                print(system.get_student(student_id))

            elif choice == "4":
                student_id = input("Enter student ID to update: ").strip()
                existing = system.get_student(student_id)

                name = input(
                    f"Name [{existing['name']}] (Enter to keep): "
                ).strip()
                age_text = input(
                    f"Age [{existing['age']}] (Enter to keep): "
                ).strip()
                course = input(
                    f"Course [{existing['course']}] (Enter to keep): "
                ).strip()

                updated = system.update_student(
                    student_id,
                    name=name if name else None,
                    age=int(age_text) if age_text else None,
                    course=course if course else None,
                )
                print(f"Updated student: {updated}")

            elif choice == "5":
                student_id = input("Enter student ID to delete: ").strip()
                system.delete_student(student_id)
                print("Student deleted successfully.")

            elif choice == "0":
                print("Student Management System closed.")
                break

            else:
                print("Invalid option. Choose from 0 to 5.")

        except (ValueError, KeyError, OSError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
