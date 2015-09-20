from flask import Flask, render_template, request
from deliver import delivers

app = Flask('flaskwp1')

@app.route('/', methods=['GET','POST'])
def webprint():
    if request.method == "POST":
        company_name = request.form['company_name']
        phone = request.form['phone']
        description = request.form['description']
        start_address = request.form['start_address']
        end_address = request.form['end_address']
        end_name = request.form['end_name']
        delivers(company_name, phone, description, start_address, end_address, end_name)
    return render_template('index.html') 

if __name__ == '__main__':
    app.run(debug = True)