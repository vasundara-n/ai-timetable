from flask import Flask, request

app = Flask(__name__)

# ---------- AI LOGIC (WITH CONFLICT RULES) ----------
def is_valid(subject, slot, assignment):
    # Rule 1: No same slot for different subjects
    if slot in assignment.values():
        return False

    # Rule 2: Example conflict (Math & AI not same time)
    if subject == "Math" and "AI" in assignment and assignment["AI"] == slot:
        return False
    if subject == "AI" and "Math" in assignment and assignment["Math"] == slot:
        return False

    return True


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


# ---------- HOME PAGE ----------
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Timetable Generator</title>

        <style>
            body {
                font-family: 'Segoe UI';
                background: linear-gradient(135deg, #667eea, #764ba2);
                text-align: center;
                color: white;
                padding-top: 40px;
                animation: fadeIn 1s ease-in;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .box {
                background: white;
                color: black;
                padding: 30px;
                margin: auto;
                width: 380px;
                border-radius: 15px;
                box-shadow: 0px 10px 25px rgba(0,0,0,0.3);
                animation: slideUp 0.8s ease;
            }

            @keyframes slideUp {
                from { transform: translateY(50px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }

            select {
                width: 90%;
                padding: 10px;
                margin: 10px;
                border-radius: 6px;
            }

            button {
                padding: 12px 20px;
                background: #667eea;
                border: none;
                color: white;
                font-size: 16px;
                border-radius: 6px;
                cursor: pointer;
                transition: 0.3s;
            }

            button:hover {
                background: #5a67d8;
                transform: scale(1.05);
            }
        </style>
    </head>

    <body>
        <h1>🚀 AI Exam Timetable Generator</h1>

        <div class="box">
            <form method="post" action="/generate">

                <label>Select Subjects:</label><br>
                <select name="subjects" multiple>
                    <option>Math</option>
                    <option>AI</option>
                    <option>DBMS</option>
                    <option>OS</option>
                    <option>CN</option>
                </select>

                <br>

                <label>Select Time Slots:</label><br>
                <select name="slots" multiple>
                    <option>9AM</option>
                    <option>11AM</option>
                    <option>2PM</option>
                    <option>4PM</option>
                </select>

                <br>
                <button type="submit">Generate Timetable</button>
            </form>
        </div>
    </body>
    </html>
    '''


# ---------- RESULT PAGE ----------
@app.route('/generate', methods=['POST'])
def generate():
    subjects = request.form.getlist('subjects')
    slots = request.form.getlist('slots')

    result = backtrack(subjects, slots)

    if not result:
        return "<h2 style='text-align:center'>No valid timetable possible!</h2>"

    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                font-family: Arial;
                background: #f4f4f4;
                text-align: center;
                animation: fadeIn 1s;
            }

            table {
                margin: auto;
                border-collapse: collapse;
                width: 50%;
                background: white;
                box-shadow: 0px 5px 20px rgba(0,0,0,0.2);
                animation: slideUp 1s;
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
                color: #667eea;
                font-weight: bold;
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            @keyframes slideUp {
                from { transform: translateY(40px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
        </style>
    </head>

    <body>
        <h1>📅 Generated Timetable</h1>

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
