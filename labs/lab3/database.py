import time

students = dict(dict())
classes = dict(dict())


def get_student(student_id):
    student = students.get(student_id)
    return student


def get_class(class_id):
    classs = classes.get(class_id)
    return classs


def create_student(name):
    student_id = int(time.time())
    students[student_id] = {
        "student_id": student_id,
        "name": name,
        "classes": []
    }
    print('Students dict: ' + str(students))
    return students[student_id]


def create_class(name):
    class_id = int(time.time())
    classes[class_id] = {
        "class_id": class_id,
        "name": name,
        "students": []
    }
    print('Classes dict: ' + str(classes))
    return classes[class_id]


def add_student_to_class(class_id, student_id):
    classs = classes.get(class_id)
    if classs is None:
        return None
    classs['students'].append(student_id)
    classes[class_id] = classs
    return classs
