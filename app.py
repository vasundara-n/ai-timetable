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
    <html>
    <head>
        <title>AI Timetable Generator</title>
        <style>
            body {
                font-family: Arial;
                background: linear-gradient(to right, #4facfe, #00f2fe);
                text-align: center;
                color: white;
            }
            .box {
                background: white;
                color: black;
                padding: 30px;
                margin: 50px auto;
                width: 350px;
                border-radius: 10px;
                box-shadow: 0 0 10px gray;
            }
            input {
                width: 90%;
                padding: 10px;
                margin: 10px;
            }
            button {
                padding: 10px 20px;
                background: #4facfe;
                border: none;
                color: white;
                font-size: 16px;
                border-radius: 5px;
                cursor: pointer;
            }
            table {
                margin: auto;
                border-collapse: collapse;
                width: 60%;
                background: white;
                color: black;
            }
            th, td {
                padding: 10px;
                border: 1px solid black;
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
    <html>
    <body style="font-family:Arial; text-align:center; background:#eef2f3;">
    <h1>Generated Timetable</h1>
    <table>
    <tr><th>Subject</th><th>Time Slot</th></tr>
    '''

    for subject, slot in result.items():
        html += f"<tr><td>{subject}</td><td>{slot}</td></tr>"

    html += '''
    </table>
    <br><a href="/">Go Back</a>
    </body>
    </html>
    '''

    return html


app.run(host="0.0.0.0", port=10000)
