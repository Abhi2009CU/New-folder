from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Initialize the SQLite Database
def init_db():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    # Create table with user_id to associate flashcards with a specific user
    c.execute('''CREATE TABLE IF NOT EXISTS quiz (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Insert new question and answer into the database associated with a user
def insert_question(question, answer, user_id):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('INSERT INTO quiz (question, answer, user_id) VALUES (?, ?, ?)', (question, answer, user_id))
    conn.commit()
    conn.close()

# Get all questions and answers for the logged-in user
def get_questions_for_user(user_id):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('SELECT * FROM quiz WHERE user_id = ?', (user_id,))
    results = c.fetchall()
    conn.close()
    return results

# Simulate user login (in production, use real authentication)
@app.route('/login/<username>')
def login(username):
    # Set a unique user_id for each simulated user
    session['user_id'] = username  # Assign 'user1', 'user2', etc.
    return redirect(url_for('home'))

@app.route('/newstuff')
def home():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login', username='user1'))  # Redirect to login as user1 by default for simplicity
    
    questions = get_questions_for_user(user_id)
    return render_template('quiz.html', questions=questions)

@app.route('/add', methods=['POST'])
def add_question():
    question = request.form['question']
    answer = request.form['answer']
    user_id = session['user_id']
    insert_question(question, answer, user_id)
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(host='0.0.0.0', port=5000, debug=True)
