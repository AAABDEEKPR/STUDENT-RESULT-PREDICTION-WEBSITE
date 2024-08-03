from flask import Flask, render_template, request, jsonify
import pickle as pk
from flask_mysqldb import MySQL
import random
#run cd C:\Users\abhradeep\Downloads\SIT-project\SIT-project
# then python app.py then localhost50000
app = Flask(__name__)

# Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'copyright'

mysql = MySQL(app)

def calculategrade(n):
    if n <= 100 and n > 80:
        return "A"
    elif n <= 80 and n > 60:
        return "B"
    elif n <= 60 and n > 40:
        return "C"
    else:
        return "D"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dashboard")
def dashboard():
    try:
        print("Attempting to connect to MySQL...")
        return render_template("dashboard.html")
    except AttributeError as e:
        print(f"Error: {e}")
        return "Error: MySQL connection is not set up properly.", 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Unexpected error occurred.", 500

@app.route("/tables")
def tables():
    cur = mysql.connection.cursor()        
    cur.execute("SELECT * FROM USERS")
    fetchdata = cur.fetchall()
    grades = []
    for x in fetchdata:
        if x[4] != None:
            grade = calculategrade(x[4])
            grades.append(grade)
    print(grades)
    print(fetchdata)
    cur.close()
    return render_template("tables.html", fetchdata = fetchdata, grades = grades)

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/sign-in", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        try:
            userDetails = request.json
            if not userDetails:
                raise ValueError("No JSON data received")
            username = userDetails.get('username')
            password = userDetails.get('passwd')
            if not all([username, password]):
                raise ValueError("All fields are required")
            print(f"Username: {username}, Password: {password}")
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE name=%s AND pass=%s", (username, password))
            user = cur.fetchone()
            cur.close()
            if user:
                print("User exists")
                return jsonify({"status": "success", "message": "User exists"})
            else:
                print("User does not exist")
                return jsonify({"status": "error", "message": "Password is Incorrect"})
        except Exception as e:
            print(f"Error during signup: {e}")
    return render_template("sign-in.html")



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            userDetails = request.json
            if not userDetails:
                raise ValueError("No JSON data received")

            full_name = userDetails.get('full_name')
            email = userDetails.get('email')
            age = userDetails.get('age')
            standard = userDetails.get('standard')
            country = userDetails.get('country')
            state = userDetails.get('state')
            phone = userDetails.get('phone_number')
            language = userDetails.get('language')
            gender = userDetails.get('gender')
            password = userDetails.get('passwd')
            dob = userDetails.get('dob')
            marks = userDetails.get('marks')
            att = userDetails.get('att')

            if not all([full_name, email, age, standard, country, state, phone, language, gender, password, dob]):
                print(userDetails)
                raise ValueError("All fields are required")

            print(f"Full Name: {full_name}, Email: {email}, Age: {age}, Standard: {standard}, Country: {country}, State: {state}, Phone: {phone}, Language: {language}, Gender: {gender}, Password: {password}, DOB: {dob}")

            # Example code to insert into database (uncomment if needed)
            cur = mysql.connection.cursor()
            uid = random.randint(107, 400)
            cur.execute("INSERT INTO users(id, name, dept, email , marks, att, pass) values(%s, %s, %s, %s, %s, %s, %s)",
                        (uid, full_name, standard,email, marks, att, password))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            print(f"Error during signup: {e}")
        # return redirect('/dashboard')
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard1():
    return render_template("dashboard.html")

@app.route("/predict", methods=["POST"])
def submit():
    form_data = request.json
    keys_for_array = ['mathSex','mathAge', 'mathAddress', 'mathFamSize', 'mathPStatus', 'mathMedu', 'mathFedu','motherJob', 'fatherJob', 'reasonMap', 'guardianMap', 
    'travelTime', 'studyTime', 'pastFailures', 'eduSupport', 'famSupport',
    'paidClasses', 'extraCurricular', 'nurserySchool', 'higherEdu',
    'internetAccess', 'romanticRelationship', 'familyRelationship',
    'freeTime', 'goingOut', 'workdayAlcohol', 'weekendAlcohol',
    'healthStatus', 'schoolAbsences', 'firstPeriodGrade', 'secondPeriodGrade',
    'portravelTime', 'porstudyTime', 'porpastFailures', 'poreduSupport',
    'porfamSupport', 'porpaidClasses', 'porextraCurricular', 'pornurserySchool',
    'porhigherEdu', 'porinternetAccess', 'porromanticRelationship',
    'porfamilyRelationship', 'porfreeTime', 'porgoingOut', 'porworkdayAlcohol',
    'porweekendAlcohol', 'porhealthStatus', 'porschoolAbsences', 'porfirstPeriodGrade',
    'porsecondPeriodGrade'
    ]
    numeric_values = [int(form_data[key]) for key in keys_for_array]
    print(numeric_values)
    with open('catboost.pkl', 'rb') as file:
        loaded_model = pk.load(file)
    prediction = loaded_model.predict([numeric_values])
    print(prediction)
    return {"grade1": prediction[0], "grade2": prediction[0]}

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
