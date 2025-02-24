from flask import Flask, request

app = Flask(__name__)

# Dictionary to store student data
students = {}

# Home route with embedded HTML
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Grade Tracker</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f4f4f4;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                color: #333;
            }
            input, button {
                margin: 5px 0;
                padding: 10px;
                width: 100%;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            button {
                background-color: #28a745;
                color: white;
                cursor: pointer;
            }
            button:hover {
                background-color: #218838;
            }

            /* Pop-up styles */
            .popup {
                display: none;
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                z-index: 1000;
            }
            .popup-content {
                max-width: 400px;
                word-wrap: break-word;
            }
            .popup-close {
            position: absolute;
            top: 10px;
            right: 10px;
            background-color: #ff4d4d;
            color: white;
            border: none;
            border-radius: 50%;
            width: 25px;
            height: 25px;
            cursor: pointer;
            font-size: 16px;
            line-height: 25px; /* Match the height of the button */
            text-align: center; /* Center the text horizontally */
            padding: 0; /* Remove any padding */
            display: flex; /* Use flexbox for centering */
            align-items: center; /* Center vertically */
            justify-content: center; /* Center horizontally */
            }
            .popup-close:hover {
                background-color: #ff1a1a;
            }
            .overlay {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                z-index: 999;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Student Grade Tracker</h1>

            <!-- Add Student Form -->
            <h2>Add Student</h2>
            <input type="text" id="studentName" placeholder="Student Name">
            <input type="text" id="subject" placeholder="Subject">
            <input type="number" id="grade" placeholder="Grade (0-100)" min="0" max="100">
            <button onclick="addStudent()">Add Student</button>

            <!-- Retrieve Grades Form -->
            <h2>Retrieve Grades</h2>
            <input type="text" id="retrieveName" placeholder="Student Name">
            <button onclick="retrieveGrades()">Retrieve Grades</button>

            <!-- Calculate Average Form -->
            <h2>Calculate Average</h2>
            <input type="text" id="averageName" placeholder="Student Name">
            <button onclick="calculateAverage()">Calculate Average</button>

            <!-- Remove Student Form -->
            <h2>Remove Student</h2>
            <input type="text" id="removeName" placeholder="Student Name">
            <button onclick="removeStudent()">Remove Student</button>

            <!-- Display All Students -->
            <h2>Display All Students</h2>
            <button onclick="displayAllStudents()">Display All Students</button>
        </div>

        <!-- Pop-up Output Box -->
        <div class="overlay" id="overlay"></div>
        <div class="popup" id="popup">
            <button class="popup-close" onclick="closePopup()">×</button>
            <div class="popup-content" id="popup-content"></div>
        </div>

        <script>
            // JavaScript to handle interactions with the backend
            function showPopup(content) {
                document.getElementById('popup-content').innerText = content;
                document.getElementById('popup').style.display = 'block';
                document.getElementById('overlay').style.display = 'block';
            }

            function closePopup() {
                document.getElementById('popup').style.display = 'none';
                document.getElementById('overlay').style.display = 'none';
            }

            async function addStudent() {
                const name = document.getElementById('studentName').value;
                const subject = document.getElementById('subject').value;
                const grade = parseFloat(document.getElementById('grade').value);

                // Validate grade range
                if (grade < 0 || grade > 100) {
                    showPopup("Grade must be between 0 and 100.");
                    return; // Stop the function if the grade is invalid
                }

                const response = await fetch('/add_student', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ name, subject, grade }),
                });
                const result = await response.json();
                showPopup(JSON.stringify(result, null, 2));

                // Clear input fields
                document.getElementById('studentName').value = '';
                document.getElementById('subject').value = '';
                document.getElementById('grade').value = '';
            }

            async function retrieveGrades() {
                const name = document.getElementById('retrieveName').value;
                const response = await fetch(`/retrieve_grades/${name}`);
                const result = await response.json();
                showPopup(JSON.stringify(result, null, 2));

                // Clear input field
                document.getElementById('retrieveName').value = '';
            }

            async function calculateAverage() {
                const name = document.getElementById('averageName').value;
                const response = await fetch(`/calculate_average/${name}`);
                const result = await response.json();
                showPopup(JSON.stringify(result, null, 2));

                // Clear input field
                document.getElementById('averageName').value = '';
            }

            async function removeStudent() {
                const name = document.getElementById('removeName').value;

                const response = await fetch(`/remove_student/${name}`, {
                    method: 'DELETE',
                });
                const result = await response.json();
                showPopup(JSON.stringify(result, null, 2));

                // Clear input field
                document.getElementById('removeName').value = '';
            }

            async function displayAllStudents() {
                const response = await fetch('/display_all_students');
                const result = await response.json();
                showPopup(JSON.stringify(result, null, 2));
            }
        </script>
    </body>
    </html>
    '''

# actual python part w dicts
@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    name = data['name']
    subject = data['subject']
    grade = float(data['grade'])

    # grade range
    if grade < 0 or grade > 100:
        return {"error": "Grade must be between 0 and 100."}, 400

    if name not in students:
        students[name] = {}
    students[name][subject] = grade
    return {"message": f"Student {name} added successfully!"}

@app.route('/retrieve_grades/<name>', methods=['GET'])
def retrieve_grades(name):
    if name in students:
        return {name: students[name]}
    else:
        return {"error": f"Student {name} not found."}, 404

@app.route('/calculate_average/<name>', methods=['GET'])
def calculate_average(name):
    if name in students:
        grades = students[name].values()
        average = sum(grades) / len(grades)
        return {name: f"Average Grade = {average:.2f}"}
    else:
        return {"error": f"Student {name} not found."}, 404

@app.route('/remove_student/<name>', methods=['DELETE'])
def remove_student(name):
    if name in students:
        del students[name]
        return {"message": f"Student {name} removed successfully!"}
    else:
        return {"error": f"Student {name} not found."}, 404

@app.route('/display_all_students', methods=['GET'])
def display_all_students():
    if not students:
        return {"message": "No students found."}
    else:
        result = {name: sum(grades.values()) / len(grades) for name, grades in students.items()}
        return result

if __name__ == "__main__":
    app.run(debug=True)