from . import db

from datetime import datetime
from sqlalchemy.types import Numeric
# Bảng Student
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rollno = db.Column(db.String(50), unique=True, nullable=False)  # Mã số sinh viên
    name = db.Column(db.String(100), nullable=False)  # Tên sinh viên
    faculty = db.Column(db.String(100))  # Khoa
    classname = db.Column(db.String(100))  # Lớp học
    email = db.Column(db.String(100))  # Email
    phone = db.Column(db.String(20))  # Số điện thoại
    date_of_birth = db.Column(db.Date)  # Ngày sinh
    address = db.Column(db.String(200))  # Địa chỉ
    gender = db.Column(db.String(10))  # Giới tính
    # Quan hệ với bảng Score
    scores = db.relationship('Score', backref='student', lazy=True)

# Bảng Subject
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Tên môn học
    description = db.Column(db.Text)  # Mô tả môn học
    credit = db.Column(db.Integer, nullable=False)  # Số tín chỉ
    semester = db.Column(db.Integer)  # Học kỳ
    # Quan hệ với bảng Score
    scores = db.relationship('Score', backref='subject', lazy=True)



class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    tx1 = db.Column(Numeric(precision=5, scale=2))  # Tối đa 5 chữ số, 2 chữ số thập phân
    tx2 = db.Column(Numeric(precision=5, scale=2))
    middle = db.Column(Numeric(precision=5, scale=2))
    final = db.Column(Numeric(precision=5, scale=2))
    score = db.Column(Numeric(precision=5, scale=2))  # GPA cũng chỉ 2 chữ số thập phân
    training_point = db.Column(Numeric(precision=5, scale=0))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())



class ScholarshipPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    GPA = db.Column(db.Float, nullable=False)
    training_score = db.Column(db.Float, nullable=False)
    scholarship_A = db.Column(db.Float, nullable=False)
    scholarship_B = db.Column(db.Float, nullable=False)
    scholarship_No = db.Column(db.Float, nullable=False)
    prediction_date = db.Column(db.DateTime, default=db.func.now())
    comments = db.Column(db.Text)

    student = db.relationship('Student', backref=db.backref('scholarship_predictions', lazy=True))
