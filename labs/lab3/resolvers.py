from ariadne import QueryType, MutationType
import database

query = QueryType()
mutation = MutationType()


# {
#   students(student_id:1238125) {
#     student_id
#     name
#   }
# }
@query.field("students")
def resolve_get_student(_, info, student_id):
    student = database.get_student(student_id=student_id)
    return student


# {
#   classes(class_id:1238125) {
#     class_id
#     name
#   }
# }
@query.field("classes")
def resolve_get_class(_, info, class_id):
    classs = database.get_class(class_id=class_id)
    return classs




@mutation.field("create_student")
def resolve_create_student(_, info, name):
    student = database.create_student(name=name)
    return student


# mutation create_class($name: String!) {
#   create_class(name: $name){
#     class_id
#   	name
#     students
#   }
# }
@mutation.field("create_class")
def resolve_create_class(_, info, name):
    classs = database.create_class(name=name)
    return classs


@mutation.field("add_student_to_class")
def resolve_add_student_to_class(_, info, class_id, student_id):
    classs = database.add_student_to_class(class_id=class_id, student_id=student_id)
    return classs