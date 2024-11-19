from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import db, Student, Subject, Score, ScholarshipPrediction
from .utils import calculate_score, predict_scholarship_bayesian
from datetime import datetime

main = Blueprint('main', __name__)

# Trang chính
@main.route('/')
def index():
    user = session.get('user', None)
    return render_template('index.html', user=user)

# Quản lý sinh viên
@main.route('/students', methods=['GET', 'POST'])
def manage_students():
    if request.method == 'POST':
        rollno = request.form['rollno']
        name = request.form['name']
        faculty = request.form.get('faculty')
        classname = request.form.get('classname')
        email = request.form.get('email')
        new_student = Student(rollno=rollno, name=name, faculty=faculty, classname=classname, email=email)
        db.session.add(new_student)
        db.session.commit()
        flash('Student added successfully!', 'success')
    students = Student.query.all()
    return render_template('student.html', students=students)

@main.route('/students/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        try:
            student.name = request.form['name']
            student.rollno = request.form['rollno']
            student.faculty = request.form['faculty']
            student.classname = request.form['classname']
            student.email = request.form['email']
            db.session.commit()
            flash('Student updated successfully!', 'success')
            return redirect('/students')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

    return render_template('edit_student.html', student=student)

@main.route('/students/delete/<int:id>', methods=['POST'])
def delete_student(id):
    try:
        # Lấy thông tin sinh viên cần xóa
        student = Student.query.get_or_404(id)

        # Xóa các bản ghi liên quan trong bảng Score
        Score.query.filter_by(student_id=id).delete()

        # Xóa các bản ghi liên quan trong bảng ScholarshipPrediction
        ScholarshipPrediction.query.filter_by(student_id=id).delete()

        # Xóa sinh viên khỏi bảng Student
        db.session.delete(student)

        # Lưu thay đổi vào cơ sở dữ liệu
        db.session.commit()

        flash('Student and related data deleted successfully!', 'success')
    except Exception as e:
        # Xử lý lỗi nếu có
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'danger')

    return redirect(url_for('main.manage_students'))

# Quản lý môn học
@main.route('/subjects', methods=['GET', 'POST'])
def manage_subjects():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        credit = int(request.form['credit'])
        semester = int(request.form['semester'])
        new_subject = Subject(name=name, description=description, credit=credit, semester=semester)
        db.session.add(new_subject)
        db.session.commit()
        flash('Subject added successfully!', 'success')
    subjects = Subject.query.all()
    return render_template('subject.html', subjects=subjects)

@main.route('/subjects/edit/<int:id>', methods=['GET', 'POST'])
def edit_subject(id):
    subject = Subject.query.get(id)  # Tìm môn học với id
    if not subject:
        flash('Subject not found!', 'danger')
        return redirect('/subjects')

    if request.method == 'POST':
        try:
            # Lấy dữ liệu từ form
            subject.name = request.form['name']
            subject.description = request.form.get('description', '')
            subject.credit = int(request.form['credit'])
            subject.semester = int(request.form['semester'])

            # Lưu thay đổi
            db.session.commit()
            flash('Subject updated successfully!', 'success')
            return redirect('/subjects')
        except ValueError as e:
            flash(f'Invalid input: {e}', 'danger')
        except Exception as e:
            flash(f'Error: {e}', 'danger')

    return render_template('edit_subject.html', subject=subject)

@main.route('/subjects/delete/<int:id>', methods=['POST'])
def delete_subject(id):
    try:
        # Lấy thông tin môn học cần xóa
        subject = Subject.query.get_or_404(id)

        # Xóa các bản ghi liên quan trong bảng Score
        Score.query.filter_by(subject_id=id).delete()

        # Xóa môn học
        db.session.delete(subject)

        # Lưu thay đổi
        db.session.commit()

        flash('Subject and related data deleted successfully!', 'success')
    except Exception as e:
        # Rollback nếu có lỗi
        db.session.rollback()
        flash(f'Error deleting subject: {str(e)}', 'danger')

    return redirect(url_for('main.manage_subjects'))


# Quản lý điểm
@main.route('/scores', methods=['GET', 'POST'])
def manage_scores():
    students = Student.query.all()
    subjects = Subject.query.all()
    if request.method == 'POST':
        student_id = int(request.form['student_id'])
        subject_id = int(request.form['subject_id'])
        tx1 = float(request.form.get('tx1', 0))
        tx2 = float(request.form.get('tx2', 0))
        middle = float(request.form.get('middle', 0))
        final = float(request.form.get('final', 0))
        training_point = float(request.form.get('training_point', 0))
        total_score = calculate_score(tx1, tx2, middle, final)
        new_score = Score(
            student_id=student_id,
            subject_id=subject_id,
            tx1=tx1, tx2=tx2, middle=middle, final=final,
            score=total_score,
            training_point=training_point
        )
        db.session.add(new_score)
        db.session.commit()
        flash('Score added successfully!', 'success')

    scores = Score.query.all()
    return render_template('score.html', students=students, subjects=subjects, scores=scores)

@main.route('/scores/edit/<int:id>', methods=['GET', 'POST'])
def edit_score(id):
    score = Score.query.get_or_404(id)
    if request.method == 'POST':
        try:
            score.tx1 = float(request.form['tx1'])
            score.tx2 = float(request.form['tx2'])
            score.middle = float(request.form['middle'])
            score.final = float(request.form['final'])
            score.training_point = float(request.form['training_point'])
            score.score = calculate_score(score.tx1, score.tx2, score.middle, score.final)
            db.session.commit()
            flash('Score updated successfully!', 'success')
            return redirect('/scores')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

    return render_template('edit_score.html', score=score)

@main.route('/scores/delete/<int:id>', methods=['POST'])
def delete_score(id):
    score = Score.query.get_or_404(id)
    db.session.delete(score)
    db.session.commit()
    flash('Score deleted successfully!', 'success')
    return redirect(url_for('main.manage_scores'))

# Trang dự đoán học bổng


@main.route('/predict', methods=['GET', 'POST'])
def predict():
    students = Student.query.all()  # Lấy danh sách sinh viên
    selected_student = None  # Sinh viên được chọn
    result = None  # Kết quả dự đoán

    if request.method == 'POST':
        try:
            # Lấy ID sinh viên từ form
            student_id = int(request.form['student_id'])

            # Truy xuất sinh viên được chọn
            selected_student = Student.query.get_or_404(student_id)

            # Lấy danh sách điểm và thông tin tín chỉ
            scores = Score.query.filter_by(student_id=student_id).all()
            if not scores:
                raise ValueError("Không tìm thấy điểm của sinh viên này.")

            # Tính GPA tổng dựa trên tín chỉ
            total_credits = sum(score.subject.credit for score in scores)  # Tổng số tín chỉ
            weighted_gpa_sum = sum(score.score * score.subject.credit for score in scores)  # Tổng điểm GPA * tín chỉ
            total_gpa = round(weighted_gpa_sum / total_credits, 2) if total_credits > 0 else 0.0  # GPA tổng

            # Tính điểm rèn luyện trung bình
            training_score = round(sum(score.training_point for score in scores) / len(scores), 2)

            # Các xác suất ban đầu (prior probabilities)
            prior_A = 0.1  # Xác suất nhận học bổng loại A
            prior_B = 0.2  # Xác suất nhận học bổng loại B
            prior_No = 0.7  # Xác suất không nhận học bổng

            # Sử dụng định lý Bayes để dự đoán
            result = predict_scholarship_bayesian(total_gpa, training_score, prior_A, prior_B, prior_No)

            # Kiểm tra bảng ScholarshipPrediction
            prediction_data = ScholarshipPrediction.query.filter_by(student_id=student_id).first()
            if prediction_data:
                # Cập nhật dữ liệu dự đoán
                prediction_data.GPA = total_gpa
                prediction_data.training_score = training_score
                prediction_data.scholarship_A = result["A"]
                prediction_data.scholarship_B = result["B"]
                prediction_data.scholarship_No = result["No"]
                prediction_data.prediction_date = datetime.now()
            else:
                # Tạo bản ghi mới nếu chưa tồn tại
                new_prediction = ScholarshipPrediction(
                    student_id=student_id,
                    GPA=total_gpa,
                    training_score=training_score,
                    scholarship_A=result["A"],
                    scholarship_B=result["B"],
                    scholarship_No=result["No"],
                    prediction_date=datetime.now()
                )
                db.session.add(new_prediction)

            # Lưu thay đổi
            db.session.commit()

            flash("Dự đoán hoàn tất và đã cập nhật!", "success")

        except ValueError as e:
            flash(str(e), "danger")
        except Exception as e:
            flash("Đã xảy ra lỗi: " + str(e), "danger")

    # Hiển thị dữ liệu dự đoán nếu có sinh viên được chọn
    if selected_student:
        prediction_data = ScholarshipPrediction.query.filter_by(student_id=selected_student.id).first()
        if prediction_data:
            result = {
                "A": prediction_data.scholarship_A,
                "B": prediction_data.scholarship_B,
                "No": prediction_data.scholarship_No,
                "GPA": prediction_data.GPA,
                "training_score": prediction_data.training_score,
                "prediction_date": prediction_data.prediction_date
            }

    return render_template('predict.html', students=students, result=result, selected_student=selected_student)






