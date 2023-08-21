from flask import redirect, request, render_template, flash
from app import db
import app.models as models
from app.back import bp as app
from werkzeug.exceptions import HTTPException
import json
from app.utility import utility_decorators as util

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.route('/', methods=['POST', 'GET'])
def index():

    form = request.form.to_dict()

    sort_vars = {
        'Name ↓': models.CONTACT.query.order_by(models.CONTACT.name).all,
        'Email ↓': models.CONTACT.query.order_by(models.CONTACT.email).all,
        'Phone ↓': models.CONTACT.query.order_by(models.CONTACT.phone_number).all,
        'Name ↑': models.CONTACT.query.order_by(models.CONTACT.name.desc()).all,
        'Email ↑': models.CONTACT.query.order_by(models.CONTACT.email.desc()).all,
        'Phone ↑': models.CONTACT.query.order_by(models.CONTACT.phone_number.desc()).all,
    }

    if 'sort_option' in form:
        sort = form['sort_option']
        contacts = sort_vars[form['sort_option']]()
    else:
        sort = ''
        contacts = models.CONTACT.query.order_by(models.CONTACT.contact_id).all()

    return render_template('index.html', contacts=contacts, sort = sort)

@app.route('/add_contact', methods=['POST', 'GET'])
@util.required_variables({
    "name":str,
    "email":str,
    "phone_number":str,
})
def add_contact(name, email, phone_number):
    contact = request.values.to_dict()
    new_con = models.CONTACT(name = name, email = email, phone_number = phone_number)

    valid = new_con.validate()

    if valid != 0:
        if valid == 1:
            flash("Wrong phone format, expected: +XXXXXXXXXXXX")
        elif valid == 2:
            flash("Wrong email format, expected: some.email@gmail.com")
        elif valid == 3:
            flash("This contact already exists")
        else:
            flash("Format error")

        return redirect('/')

    db.session.add(new_con)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:con_id>')
def delete(con_id):
    db.session.delete(models.CONTACT.query.get_or_404(con_id))
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:con_id>', methods=['GET', 'POST'])
def update(con_id):
    contact = models.CONTACT.query.get_or_404(con_id)

    if request.method == 'POST':
        valid = contact.change(**request.values.to_dict())

        if valid != 0:
            if valid == 1:
                flash("Wrong phone format, expected: +XXXXXXXXXXXX")
            elif valid == 2:
                flash("Wrong email format, expected: some.email@gmail.com")
            elif valid == 3:
                flash("This contact already exists")
            else:
                flash("Format error")

            return redirect(f'/update/{con_id}')

        db.session.commit()
        return redirect('/')

    else:
        return render_template('update.html', contact=contact)