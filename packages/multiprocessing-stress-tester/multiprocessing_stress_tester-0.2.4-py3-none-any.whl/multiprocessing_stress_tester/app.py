import os
import psycopg2
import heroku3
import subprocess
import json
from .debugger import stresstest
from flask import Flask, request, render_template, Response

API_KEY = '2aaf98e1-4dd6-4353-a88c-0051be97821a' 

app = Flask(__name__)

# Index route
@app.route('/')
def home():
    return render_template("index.html")

# Scripts route
@app.route('/scripts')
def scripts():
    return render_template("scripts.js")
    
# Reading 4 files (generator, checker, correct, wrong) which contain respectively:
# generator: a .cpp file containing a generator of a test case
# checker: a .cpp file containing a checker in order to see
#          if the wrong solution has the same result of the correct one
# correct: a .cpp file containing a solution that should be correct
#          for every test case
# wrong: a .cpp file containing a possible solution (we don't know whether
#        it works for every test case or not)
#
# The method returns the test_id of the stress-test in the database
# and the debugger result obtained by these files.
@app.route('/sub', methods=["POST"])
def exec_sub():
    # reading input and formatting in order to be
    # insertable in PostgreSQL database
    generator = request.files['generator'].read().decode('utf-8')
    checker = request.files['checker'].read().decode('utf-8')
    correct = request.files['correct'].read().decode('utf-8')
    wrong = request.files['wrong'].read().decode('utf-8')
    
    # using heroku API-KEY to obtain current database_url
    app = heroku3.from_key(API_KEY).app('multiprocessing-stress-tester')
    DATABASE_URL = app.config()['DATABASE_URL']

    # connecting to the database
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # executing a temporary insert to have the submission id
    cur.execute("INSERT INTO submission (generator," +
                "checker, correct, wrong, result) VALUES ('" +
                generator.replace("'", "''") + "', '" +
                checker.replace("'", "''") + "', '" +
                correct.replace("'", "''") + "', '" +
                wrong.replace("'", "''") + "', -1) RETURNING test_id;")
    test_id = cur.fetchone()[0]

    # creating temporary files and testing directory
    subprocess.call(['mkdir', f'id_{test_id}/'])
    os.chdir(f'id_{test_id}/')
    with open('generator.cpp', 'w', encoding='utf-8') as out_gen:
        subprocess.run(['echo', generator], stdout=out_gen, check=False)
    with open('checker.cpp', 'w', encoding='utf-8') as out_check:
        subprocess.run(['echo', checker], stdout=out_check, check=False)
    with open('correct.cpp', 'w', encoding='utf-8') as out_corr:
        subprocess.run(['echo', correct], stdout=out_corr, check=False)
    with open('wrong.cpp', 'w', encoding='utf-8') as out_wrong:
        subprocess.run(['echo', wrong], stdout=out_wrong, check=False)

    # executing stress-test 
    dbg_res = stresstest(False, 100, 1)

    # updating test row adding tester's result
    cur.execute("UPDATE submission SET result = %s WHERE test_id = %s ;",
                (str(dbg_res), str(test_id)))

    # commiting the transaction
    conn.commit()

    # deleting temporary files and directory
    subprocess.call(['rm', 'generator.cpp'])
    subprocess.call(['rm', 'checker.cpp'])
    subprocess.call(['rm', 'correct.cpp'])
    subprocess.call(['rm', 'wrong.cpp'])
    subprocess.call(['rm', 'log.txt'])
    if dbg_res != 0:
        subprocess.call(['rm', 'results/input.txt'])
        subprocess.call(['rm', 'results/correct_output.txt'])
        subprocess.call(['rm', 'results/wrong_output.txt'])
        subprocess.call(['rm', '-d', 'results'])
    os.chdir('../')
    subprocess.call(['rm', '-d', f'id_{test_id}/'])

    # setting response's output
    resp = Response(json.dumps({'id' : test_id,
                                'result' : dbg_res}))
    resp.mimetype = "application/json"
    return resp


if __name__ == "main":
    app.run(debug=False)
