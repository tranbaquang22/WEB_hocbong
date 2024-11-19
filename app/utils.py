from sklearn.naive_bayes import GaussianNB
import numpy as np


def calculate_score(tx1, tx2, middle, final):
    """
    Tính điểm tổng kết dựa trên các thành phần điểm.
    - tx1, tx2: Điểm thường xuyên (hệ số 0.1)
    - middle: Điểm giữa kỳ (hệ số 0.2)
    - final: Điểm cuối kỳ (hệ số 0.6)

    """
    # Tính tổng điểm
    total_score = tx1 * 0.1 + tx2 * 0.1 + middle * 0.2 + final * 0.6
    
    # Quy đổi tổng điểm từ hệ số 10 sang hệ số 4
    GPA = total_score * 4 / 10  # Điều chỉnh điểm tổng kết cho đúng chuẩn hệ số 4
    
    return round(GPA, 2)  # Trả về GPA trong khoảng [0, 4]


def train_scholarship_model():
    """
    Huấn luyện mô hình Naive Bayes dự đoán xác suất nhận học bổng.
    - Sử dụng dữ liệu huấn luyện mẫu.
    """
    # Dữ liệu huấn luyện: GPA và điểm rèn luyện
    X_train = np.array([
        [3.5, 85], [3.8, 90], [2.9, 70], [3.0, 60], [3.7, 80],
        [2.8, 50], [3.1, 65], [3.9, 95], [2.5, 55], [3.2, 75]
    ])
    # Nhãn mục tiêu: 1 (Được học bổng), 0 (Không được học bổng)
    y_train = np.array([1, 1, 0, 0, 1, 0, 0, 1, 0, 1])

    # Tạo và huấn luyện mô hình
    model = GaussianNB()
    model.fit(X_train, y_train)
    return model


def predict_scholarship_bayesian(GPA, training_score, prior_A, prior_B, prior_No):
    """
    Dự đoán xác suất nhận học bổng loại A, B, hoặc không nhận học bổng dựa trên Định lý Bayes.

    Args:
        GPA: Điểm trung bình học kỳ (hệ số 4).
        training_score: Điểm rèn luyện (0-100).
        prior_A: Xác suất ban đầu của học bổng loại A.
        prior_B: Xác suất ban đầu của học bổng loại B.
        prior_No: Xác suất ban đầu không nhận học bổng.

    Returns:
        A dictionary with probabilities for each type of scholarship.
    """

    # Xác suất có điều kiện P(GPA|Học bổng)
    P_GPA_given_A = 0.9 if GPA >= 3.8 else 0.7 if GPA >= 3.5 else 0.4
    P_GPA_given_B = 0.7 if GPA >= 3.2 else 0.5
    P_GPA_given_No = 0.3 if GPA >= 2.5 else 0.1

    # Xác suất có điều kiện P(ĐRL|Học bổng)
    P_training_given_A = 0.8 if training_score >= 90 else 0.6 if training_score >= 80 else 0.4
    P_training_given_B = 0.6 if training_score >= 75 else 0.4
    P_training_given_No = 0.2 if training_score >= 50 else 0.1

    # Tính P(GPA) và P(ĐRL) giả định phân phối đều
    P_GPA = 0.3 if GPA >= 3.5 else 0.5 if GPA >= 2.5 else 0.2
    P_training = 0.4 if training_score >= 80 else 0.4 if training_score >= 50 else 0.2

    # Tính xác suất ngược P(Học bổng|GPA, ĐRL)
    P_X_given_A = P_GPA_given_A * P_training_given_A
    P_X_given_B = P_GPA_given_B * P_training_given_B
    P_X_given_No = P_GPA_given_No * P_training_given_No

    P_X = (P_X_given_A * prior_A) + (P_X_given_B * prior_B) + (P_X_given_No * prior_No)

    P_A_given_X = (P_X_given_A * prior_A) / P_X
    P_B_given_X = (P_X_given_B * prior_B) / P_X
    P_No_given_X = (P_X_given_No * prior_No) / P_X

    return {
        "A": round(P_A_given_X * 100, 2),  # Xác suất nhận học bổng loại A (%)
        "B": round(P_B_given_X * 100, 2),  # Xác suất nhận học bổng loại B (%)
        "No": round(P_No_given_X * 100, 2),  # Xác suất không nhận học bổng (%)
    }




def validate_inputs(inputs, required_fields):
    """
    Kiểm tra các trường input có bị thiếu không.
    - inputs: dict chứa dữ liệu input từ form
    - required_fields: list các trường bắt buộc
    """
    missing_fields = [field for field in required_fields if field not in inputs or not inputs[field]]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")


def is_valid_gpa(gpa):
    """
    Kiểm tra tính hợp lệ của GPA.
    - GPA phải nằm trong khoảng 0.0 đến 4.0
    """
    return 0.0 <= gpa <= 4.0


def is_valid_training_score(score):
    """
    Kiểm tra tính hợp lệ của điểm rèn luyện.
    - Điểm rèn luyện phải nằm trong khoảng 0 đến 100
    """
    return 0 <= score <= 100
