from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pw123",
    database="hospital_management"
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check the user's credentials in the database
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            # Redirect to the patient details page
            return redirect(url_for('patient_details'))

    return render_template('login.html')

@app.route('/patient_details')
def patient_details():
    # Fetch patient details from the database
    cursor.execute("SELECT * FROM patients")
    patient_data = cursor.fetchall()

    # Fetch available doctors for appointments
    cursor.execute("SELECT * FROM doctors")
    doctors_data = cursor.fetchall()

    return render_template('patient_details.html', patients=patient_data, doctors=doctors_data)

@app.route('/generate_report/<int:patient_id>')
def generate_report(patient_id):
    # Generate a report for the specified patient
    # You can implement this as needed

    return "Generate Report for Patient ID: {}".format(patient_id)

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        appointment_date = request.form['appointment_date']

        # Create a new appointment record in the database
        cursor.execute("INSERT INTO appointments (patient_id, doctor_id, appointment_date) VALUES (%s, %s, %s)",
                       (patient_id, doctor_id, appointment_date))
        db.commit()

        return redirect(url_for('patient_details'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken (you should add error handling for this)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return "Username already taken. Please choose another username."

        # If the username is not taken, insert the new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
