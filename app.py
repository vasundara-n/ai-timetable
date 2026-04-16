from flask import Flask, request

app = Flask(__name__)

def is_valid(subject, slot, assignment):
    return slot not in assignment.values()

def backtrack(subjects, slots, assignment={}):
    if len(assignment) == len(subjects):
        return assignment

    subject = subjects[len(assignment)]

    for slot in slots:
        if is_valid(subject, slot, assignment):
            assignment[subject] = slot
            result = backtrack(subjects, slots, assignment)
            if result:
                return result
            del assignment[subject]

    return None


@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Timetable Generator</title>
        <style>
            body {
                font-family: Arial;
                background: linear-gradient(to right, #667eea, #764ba2);
                text-align: center;
                color: white;
                padding-top: 50px;
            }

            .box {
                background: white;
                color: black;
                padding: 30px;
                margin: auto;
                width: 350px;
                border-radius: 12px;
                box-shadow: 0px 8px 20px rgba(0,0,0,0.3);
            }

            h1 {
                margin-bottom: 30px;
            }

            input {
                width: 90%;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                border: 1px solid #ccc;
            }

            button {
                padding: 10px 20px;
                background: #667eea;
                border: none;
                color: white;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
            }

            button:hover {
                background: #5a67d8;
            }
        </style>
    </head>

    <body>
        <h1>AI Exam Timetable Generator</h1>

        <div class="box">
            <form method="post" action="/generate">
                <input name="subjects" placeholder="Enter Subjects (Math,AI,DBMS)" required><br>
                <input name="slots" placeholder="Enter Time Slots (9AM,11AM,2PM)" required><br>
                <button type="submit">Generate Timetable</button>
            </form>
        </div>
    </body>
    </html>
    '''


@app.route('/generate', methods=['POST'])
def generate():
    subjects = request.form['subjects'].split(',')
    slots = request.form['slots'].split(',')

    result = backtrack(subjects, slots)

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Generated Timetable</title>
        <style>
            body {
                font-family: Arial;
                background: #f4f4f4;
                text-align: center;
                padding-top: 40px;
            }

            h1 {
                margin-bottom: 20px;
            }

            table {
                margin: auto;
                border-collapse: collapse;
                width: 50%;
                background: white;
                box-shadow: 0px 5px 15px rgba(0,0,0,0.2);
            }

            th, td {
                padding: 12px;
                border: 1px solid #ddd;
            }

            th {
                background: #667eea;
                color: white;
            }

            tr:hover {
                background: #f1f1f1;
            }

            a {
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                color: #667eea;
                font-weight: bold;
            }
        </style>
    </head>

    <body>
        <h1>Generated Timetable</h1>

        <table>
            <tr><th>Subject</th><th>Time Slot</th></tr>
    '''

    for subject, slot in result.items():
        html += f"<tr><td>{subject}</td><td>{slot}</td></tr>"

    html += '''
        </table>

        <br>
        <a href="/">⬅ Go Back</a>
    </body>
    </html>
    '''

    return html


app.run(host="0.0.0.0", port=10000)
