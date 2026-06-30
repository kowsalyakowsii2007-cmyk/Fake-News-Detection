from flask import Flask, render_template, request, redirect, session
import pickle
import sqlite3

app = Flask(__name__)
app.secret_key = 'fakenewskey123'

model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user'] = email
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid email or password")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit()
            conn.close()
            return redirect('/login')
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register.html', error="Email already exists")
    return render_template('register.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if 'user' not in session:
        return redirect('/login')

    result = None
    confidence = None

    if request.method == 'POST':
        news = request.form['news']
        transformed = vectorizer.transform([news])
        prediction = model.predict(transformed)[0]
        confidence = round(max(model.predict_proba(transformed)[0]) * 100, 2)
        result = 'REAL' if prediction == 1 else 'FAKE'

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO history (news, result, confidence) VALUES (?, ?, ?)',
            (news[:50], result, confidence)
        )
        conn.commit()
        conn.close()

    return render_template('dashboard.html', result=result, confidence=confidence)

@app.route('/history')
def history():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT news, result, confidence FROM history ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()

    history_list = []
    for row in rows:
        history_list.append({
            'news': row[0],
            'result': row[1],
            'confidence': row[2]
        })

    return render_template('history.html', history=history_list)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)