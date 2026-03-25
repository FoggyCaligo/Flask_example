from flask import Blueprint, render_template, request
from services.bmi import BMICalculator
from models.db import Database
import atexit

mainBp = Blueprint('main', __name__)

db = Database()
atexit.register(db.close)

@mainBp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@mainBp.route('/calculate', methods=['POST'])
def calculate():
    try:
        weight = float(request.form['weight'])
        height = float(request.form['height'])

        if weight <= 0 or height <= 0:
            return render_template('index.html', error='체중과 신장은 양수여야 합니다.')

        calculator = BMICalculator(weight, height)
        result = calculator.get_result()

        db.save_bmi_record(weight, height, result["bmi"], result["category"])

        return render_template(
            'result.html',
            bmi=result["bmi"],
            category=result["category"],
            weight=weight,
            height=height
        )
    except ValueError:
        return render_template('index.html', error='유효한 숫자를 입력해주세요.')

@mainBp.route('/history', methods=['GET'])
def history():
    records = db.get_bmi_records(10)
    return render_template('history.html', records=records)