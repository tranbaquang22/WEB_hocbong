import random
from datetime import datetime, timedelta
from app import db
from app.models import Student, Subject, Score
from app.utils import calculate_score # Import hàm tính GPA

# Xóa dữ liệu cũ
db.session.query(Score).delete()
db.session.query(Subject).delete()
db.session.query(Student).delete()

# Thêm dữ liệu sinh viên
for i in range(1, 101):
    student = Student(
        rollno=f"SV{i:03}",
        name=f"Sinh viên {i}",
        faculty=random.choice(["Công nghệ thông tin", "Kinh tế", "Kỹ thuật", "Y học"]),
        classname=f"Lớp {random.randint(1, 12)}A",
        email=f"sv{i}@example.com",
        phone=f"098{random.randint(1000000, 9999999)}",
        date_of_birth=datetime(2000, 1, 1) + timedelta(days=random.randint(0, 8000)),
        address=f"Địa chỉ {i}",
        gender=random.choice(["Nam", "Nữ"])
    )
    db.session.add(student)

# Thêm dữ liệu môn học
subjects = []
for i in range(1, 11):
    subject = Subject(
        name=f"Môn học {i}",
        description=f"Mô tả môn học {i}",
        credit=random.randint(2, 4),
        semester=random.randint(1, 8)
    )
    db.session.add(subject)
    subjects.append(subject)

# Thêm dữ liệu điểm
students = Student.query.all()
for student in students:
    for subject in random.sample(subjects, k=5):  # Mỗi sinh viên học 5 môn
        tx1 = random.uniform(4.0, 10.0)
        tx2 = random.uniform(4.0, 10.0)
        middle = random.uniform(4.0, 10.0)
        final = random.uniform(4.0, 10.0)
        gpa = calculate_score(tx1, tx2, middle, final)
        training_point = random.uniform(60, 100)

        new_score = Score(
            student_id=student.id,
            subject_id=subject.id,
            tx1=round(tx1, 2),
            tx2=round(tx2, 2),
            middle=round(middle, 2),
            final=round(final, 2),
            score=round(calculate_score(tx1, tx2, middle, final), 2),
            training_point=round(training_point, 0)
        )


        db.session.add(new_score)

# Lưu dữ liệu
db.session.commit()
print("Dữ liệu đã được tạo thành công!")
