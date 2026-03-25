from flask import Blueprint
from flask import render_template
from flask import request
from services.bmi import BMICalculator
from models.db import Database

homeBp = Blueprint('home',__name__,url_prefix="/")
historyBp = Blueprint('history',__name__,url_prefix="/")
db = Database()   # DB 초기화

@homeBp.route('/', methods=['GET'])
def index():
    return render_template('index.html')
   
@homeBp.route('/calculate', methods=['POST'])
def calculate():
    try:
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        
        # 입력값 유효성 검사
        if weight <= 0 or height <= 0:
            return render_template('index.html', error="체중과 신장은 양수여야 합니다.")
        
        # BMI 계산
        calculator = BMICalculator(weight, height)
        result = calculator.get_result()
        
        # 데이터베이스에 저장
        db.save_bmi_record(weight, height, result["bmi"], result["category"])
        
        return render_template('result.html', 
                              bmi=result["bmi"], 
                              category=result["category"],
                              weight=weight,
                              height=height)
    except ValueError:
        return render_template('index.html', error="유효한 숫자를 입력해주세요.")

@historyBp.route('/history')
def history():
    # 최근 BMI 기록 10개 가져오기
    records = db.get_bmi_records(10)
    return render_template('history.html', records=records)