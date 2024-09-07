from flask import Flask, request, render_template, redirect, url_for, send_file
import io

from database import Database, Location

app = Flask(__name__)
database = Database.load_database()

@app.route('/')
def index():
    items = database.show()
    return render_template('index.html', items=items)

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

@app.route('/update', methods=['GET', 'POST'])
def update_item():
    if request.method == 'POST':
        key = request.form['key']
        value_str = request.form['value']
        location_str = request.form['location']
        try:
            if not key:
                raise ValueError("아이템의 이름을 입력하지 않았습니다.")
            if not database.get(key):
                raise ValueError("아이템이 데이터베이스에 존재하지 않습니다.")
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
            return str(e)
    else:
        key = request.args.get('key')
        item = database.get(key)
        if item:
            value = item['count']
            location = f"{item['location'].stack}, {item['location'].column}, {item['location'].shelf}"
            return render_template('update.html', key=key, value=value, location=location)
        else:
            return "아이템이 존재하지 않습니다."

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
    csv_data = Database.save_database(database)
    
    return send_file(
        io.BytesIO(csv_data.encode('cp949')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='database.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)