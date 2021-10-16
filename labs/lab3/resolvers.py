from ariadne import QueryType, MutationType
import database

query = QueryType()
mutation = MutationType()


@mutation.field("create_student")
def resolve_create_student(_, info, name):
    student = database.create_student(name=name)
    return student


@mutation.field("create_class")
def resolve_create_class(_, info, name):
    classs = database.create_class(name=name)
    return classs


@query.field("students")
def resolve_student(_, info, id):
    student = database.get_student(id)
    return student


@query.field("classes")
def resolve_class(_, info, id):
    classs = database.get_class(id)
    return classs



