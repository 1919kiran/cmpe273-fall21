from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///university.db")

junction_table = Table('students_classes', Base.metadata,
                       Column('student_id', Integer, ForeignKey('students.id')),
                       Column('class_id', Integer, ForeignKey('classes.id'))
                       )


class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    classes = relationship("Classes",
                           secondary=junction_table,
                           back_populates="students")

    def serialize(self):
        return {"id": self.id, "name": self.name, "classes": self.classes}

    def __repr__(self):
        return f"{self.id}, {self.name}, {self.classes}"


class Classes(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    students = relationship("Students",
                            secondary=junction_table,
                            back_populates="classes")

    def serialize(self):
        return {"id": self.id, "name": self.name, "students": self.students.serialize()}

    def __repr__(self):
        return f"({self.id}, {self.name})"


# will create all tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Session is our Data Mapper
session = Session()


def create_student(name):
    student = Students(name=name)
    session.add(student)
    session.commit()
    student = session.query(Students).filter_by(name=name).first()
    return student.serialize()


def create_class(name):
    classs = Classes(name=name)
    session.add(classs)
    session.commit()
    classs = session.query(Classes).filter_by(name=name).first()
    return classs


def get_student(id):
    student = session.query(Students).filter_by(id=id).first()
    if student is None:
        return {"id": 0, "name": ""}
    else:
        return student.serialize()


def get_class(id):
    classs = session.query(Classes).filter_by(id=id).first()
    if classs is None:
        return {"id": 0, "name": ""}
    else:
        return classs.serialize()


def get_all_students():
    students = session.query(Students).all()
    print(students)