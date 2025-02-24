# dictionary to store everything
students = {}

# function- adds student + grades
def add_student():
    name = input("Enter student name: ")
    subjects = {}
    while True:
        subject = input("Enter subject (or 'done' to finish): ")
        if subject.lower() == 'done':
            break
        try:
            grade = float(input(f"Enter grade for {subject}: "))
            if 0 <= grade <= 100:
                subjects[subject] = grade
            else:
                print("Grade must be between 0 and 100. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    students[name] = subjects
    print(f"Student {name} added successfully!")

# retrieves grades
def retrieve_grades():
    name = input("Enter student name: ")
    if name in students:
        print(f"Grades for {name}: {students[name]}")
    else:
        print(f"Student {name} not found.")

# calculate average
def calculate_average():
    name = input("Enter student name: ")
    if name in students:
        grades = students[name].values()
        average = sum(grades) / len(grades)
        print(f"{name}'s average grade: {average:.2f}")
    else:
        print(f"Student {name} not found.")

# display all students and avg grades
def display_all_students():
    if not students:
        print("No students found.")
    else:
        for name, subjects in students.items():
            grades = subjects.values()
            average = sum(grades) / len(grades)
            print(f"{name}: Average Grade = {average:.2f}")

# terminal stuff so u can use program
def main():
    while True:
        print("\n1. Add Student Grades")
        print("2. Retrieve Student Grades")
        print("3. Calculate Student Average")
        print("4. Display All Students")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_student()
        elif choice == '2':
            retrieve_grades()
        elif choice == '3':
            calculate_average()
        elif choice == '4':
            display_all_students()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# and we're done!
if __name__ == "__main__":
    main()