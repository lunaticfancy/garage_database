from flask import Flask, request, render_template, redirect, url_for, send_file, flash
import io
import os
from werkzeug.utils import secure_filename
from database import Database

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 플래시 메시지를 사용하기 위해 필요
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

database = Database.load_database()

@app.route('/')
def index():
    return render_template('index.html', database=database.show())

@app.route('/insert', methods=['GET', 'POST'])
def insert_item():
    if request.method == 'POST':
        try:
            key = request.form['key']
            value_str = request.form['value']
            location_str = request.form['location']
            
            if not key:
                raise ValueError("아이템의 이름을 입력하지 않았습니다.")
            if not value_str.isdigit():
                raise ValueError("아이템의 개수를 입력하지 않았습니다.")
            value = int(value_str)
            try:
                location = Database.parse_location(location_str)
            except ValueError as e:
                raise ValueError(f"위치 입력이 잘못되었습니다: {e}")
            
            if database.get(key):
                raise ValueError("아이템이 이미 존재합니다.")
            database.insert(key, value, location)
            return redirect(url_for('index'))
        except ValueError as e:
            return str(e)
    return render_template('insert.html')

@app.route('/update/<key>', methods=['GET', 'POST'])
def update_item(key):
    if request.method == 'GET':
        item = database.get(key)
        if item:
            return render_template('update.html', key=key, value=item['count'], location=f"{item['location'].stack},{item['location'].column},{item['location'].shelf}")
        else:
            return "아이템이 존재하지 않습니다.", 404  # 404 상태 코드를 반환하여 아이템이 없음을 알림
    elif request.method == 'POST':
        try:
            value_str = request.form['value']
            location_str = request.form['location']
            
            if not value_str.isdigit():
                raise ValueError("아이템의 개수를 입력하지 않았습니다.")
            value = int(value_str)
            try:
                location = Database.parse_location(location_str)
            except ValueError as e:
                raise ValueError(f"위치 입력이 잘못되었습니다: {e}")
            
            database.update(key, value, location)
            return redirect(url_for('index'))
        except ValueError as e:
            return str(e), 400  # 400 상태 코드를 반환하여 잘못된 요청임을 알림

    return "잘못된 요청입니다.", 400  # GET 또는 POST가 아닌 다른 메서드로 요청이 들어왔을 때

@app.route('/delete', methods=['POST'])
def delete_item():
    key = request.form['key']
    database.delete(key)
    return redirect(url_for('index'))

@app.route('/find', methods=['GET', 'POST'])
def find_item():
    if request.method == 'POST':
        key = request.form['key']
        item = database.get(key)
        if item:
            return f"아이템: {key}, 수량: {item['count']}, 위치: {item['location']}"
        else:
            return "아이템이 존재하지 않습니다."
    return render_template('find.html')

@app.route('/save')
def save_database():
    database.save_database(database)

    with open("database.csv", "rb") as file:
        return send_file(
            io.BytesIO(file.read()),
            mimetype='text/csv',
            as_attachment=True,
            download_name='database.csv'
        )

@app.route('/upload', methods=['GET', 'POST'])
def upload_database():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('파일이 선택되지 않았습니다.')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('파일이 선택되지 않았습니다.')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            database.load_database_from_file(file_path)
            flash('데이터베이스가 성공적으로 업로드되었습니다.')
            return redirect(url_for('index'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)