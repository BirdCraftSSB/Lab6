from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Connect to database
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return "Student API Home"

# Create a student
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    dob = data['dob']
    amount_due = data['amount_due']

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO students (first_name, last_name, dob, amount_due)
        VALUES (?, ?, ?, ?)
    ''', (first_name, last_name, dob, amount_due))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student created successfully!'}), 201

# Read a student by ID
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
    student = c.fetchone()
    conn.close()

    if student:
        return jsonify({
            'student_id': student['student_id'],
            'first_name': student['first_name'],
            'last_name': student['last_name'],
            'dob': student['dob'],
            'amount_due': student['amount_due']
        })
    else:
        return jsonify({'message': 'Student not found'}), 404

# Update a student
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    dob = data['dob']
    amount_due = data['amount_due']

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        UPDATE students 
        SET first_name = ?, last_name = ?, dob = ?, amount_due = ?
        WHERE student_id = ?
    ''', (first_name, last_name, dob, amount_due, student_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student updated successfully!'})

# Delete a student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student deleted successfully!'})

# Show all students
@app.route('/students', methods=['GET'])
def get_all_students():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM students')
    students = c.fetchall()
    conn.close()

    student_list = []
    for student in students:
        student_list.append({
            'student_id': student['student_id'],
            'first_name': student['first_name'],
            'last_name': student['last_name'],
            'dob': student['dob'],
            'amount_due': student['amount_due']
        })

    return jsonify(student_list)

if __name__ == "__main__":
    app.run(debug=True)

