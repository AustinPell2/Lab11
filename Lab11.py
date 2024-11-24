import os
import matplotlib.pyplot as plt


class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

    def __repr__(self):
        return f"Student(ID={self.student_id}, Name={self.name})"


class Assignment:
    def __init__(self, assignment_id, name, points):
        self.assignment_id = assignment_id
        self.name = name
        self.points = int(points)


class Submission:
    def __init__(self, student_id, assignment_id, percent):
        self.student_id = student_id
        self.assignment_id = assignment_id
        self.percent = float(percent)


def get_students(file_path):
    students = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Extract the first three characters as the student ID and the rest as the name
            student_id = line[:3].strip()  # First 3 characters are the student ID
            name = line[3:].strip()  # The rest is the name
            students[student_id] = Student(student_id, name.lower())  # Normalize the name to lowercase
    print(f"Loaded students: {students}")  # Debugging: Print loaded students
    return students


def get_assignments(file_path):
    assignments = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            name = lines[i].strip()  # Assignment name
            i += 1
            assignment_id = lines[i].strip()  # Assignment ID
            i += 1
            points = lines[i].strip()  # Points
            i += 1
            assignments[assignment_id] = Assignment(assignment_id, name, points)
    return assignments


def get_submissions(directory):
    submissions = []
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as file:
            for line in file:
                student_id, assignment_id, percent = line.strip().split("|")
                submissions.append(Submission(student_id, assignment_id, percent))
    return submissions


def calculate_student_grade(student_name, students, assignments, submissions):
    normalized_name = student_name.strip().lower()  # Normalize input for case and whitespace
    student_id = None

    # Search for the student by normalized name
    for sid, student in students.items():
        if student.name == normalized_name:
            student_id = sid
            break

    if not student_id:
        print("Student not found. Loaded students are:")
        for sid, student in students.items():
            print(f"{sid}: {student.name}")  # Improved debugging to show student names
        return

    # Calculate grades
    total_points_earned = 0
    total_points_possible = 0

    for submission in submissions:
        if submission.student_id == student_id:
            assignment = assignments[submission.assignment_id]
            points_earned = (submission.percent / 100) * assignment.points
            total_points_earned += points_earned
            total_points_possible += assignment.points

    if total_points_possible == 0:
        print("No submissions found for the student")
        return

    grade_percentage = (total_points_earned / total_points_possible) * 100
    print(f"{student_name.title()}: {round(grade_percentage)}%")


def calculate_assignment_statistics(assignment_name, assignments, submissions):
    assignment_id = None
    for aid, assignment in assignments.items():
        if assignment.name == assignment_name:
            assignment_id = aid
            break
    if not assignment_id:
        print("Assignment not found")
        return

    scores = [
        (submission.percent / 100) * assignments[assignment_id].points
        for submission in submissions
        if submission.assignment_id == assignment_id
    ]
    if not scores:
        print("No submissions found for the assignment")
        return

    print(f"Min: {round(min(scores))}%")
    print(f"Avg: {round(sum(scores) / len(scores))}%")
    print(f"Max: {round(max(scores))}%")


def generate_assignment_graph(assignment_name, assignments, submissions):
    assignment_id = None
    for aid, assignment in assignments.items():
        if assignment.name == assignment_name:
            assignment_id = aid
            break
    if not assignment_id:
        print("Assignment not found")
        return

    scores = [
        (submission.percent / 100) * assignments[assignment_id].points
        for submission in submissions
        if submission.assignment_id == assignment_id
    ]
    if not scores:
        print("No submissions found for the assignment")
        return

    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f"Scores Distribution for {assignment_name}")
    plt.xlabel("Scores")
    plt.ylabel("Frequency")
    plt.show()


def main():
    # Load data files
    students = get_students('data/students.txt')
    assignments = get_assignments('data/assignments.txt')
    submissions = get_submissions('data/submissions')

    while True:
        # Display menu
        print("1. Student grade")
        print("2. Assignment statistics")
        print("3. Assignment graph")
        print("Enter your selection:")

        choice = input().strip()

        if choice == "1":
            student_name = input("What is the student's name: ")
            calculate_student_grade(student_name, students, assignments, submissions)
        elif choice == "2":
            assignment_name = input("What is the assignment name: ")
            calculate_assignment_statistics(assignment_name, assignments, submissions)
        elif choice == "3":
            assignment_name = input("What is the assignment name: ")
            generate_assignment_graph(assignment_name, assignments, submissions)
        else:
            print("Invalid choice, exiting program.")
            break


if __name__ == "__main__":
    main()