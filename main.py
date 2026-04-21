import ast
import json
from typing import Dict, List, Any


import pandas as pd

def load_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Load data about students including required preprocessing, i.e., convert grades into float.
    :param file_path: path to the students data (CSV or JSON)
    :return: list of students.
    """
    is_csv = file_path.endswith(".csv")
    if is_csv:
        df = pd.read_csv(file_path)
        # parse Python string into list of grades
        df['grades'] = df['grades'].apply(lambda x: ast.literal_eval(x))
        students_list = df.to_dict("records")
    else:
        with open(file_path, 'r') as f:
            students_list = json.load(f)
    for student in students_list:
        grades_as_float = []
        for grade in student['grades']:
            try:
                grades_as_float.append(float(grade))
            except ValueError, TypeError:
                # not a number, e.g., Z
                pass
        student['grades'] = grades_as_float
    return students_list

def compute_average_grade(student: Dict[str, Any]) -> float:
    """
    Computes the average grade of a SINGLE student.
    :param student: dictionary with grades key, list of floats as a value.
    :return: average grade.
    """
    return sum(student['grades']) / len(student['grades'])

def determine_scholarship(students: List[Dict[str, Any]]) -> List[str]:
    """
    Students that have 3rd best average grade should have scholarship.
    Therefore, there can be more than 3 students with scholarship if they have equal average grade.
    Moreover, scholarship is granted only if student has average grade higher than 4.
    :param students: list of students with grade nad NIU keys.
    :return: list of NIU numbers with assigned scholarship.
    """
    niu_to_average_grade = {}
    for student in students:
        niu_to_average_grade[student['NIU']] = compute_average_grade(student)
    # sort by 2nd element (values of dictionary)
    sorted_by_grades = sorted(niu_to_average_grade.items(), key=lambda x: x[1], reverse=True)
    last_scholarship_avg = sorted_by_grades[2][1] # 3rd student
    last_scholarship_avg = max(last_scholarship_avg, 4) # average must be higher than 4
    scholarship_student_nius = [student[0] for student in sorted_by_grades if student[1] >= last_scholarship_avg]
    return scholarship_student_nius

if __name__ == "__main__":
    # students = load_data('data/students.csv')
    students = load_data('data/students.json')
    scholarship_student_niu_list = determine_scholarship(students)
    print(scholarship_student_niu_list)
