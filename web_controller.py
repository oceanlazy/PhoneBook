from flask import Flask, render_template, request, redirect, make_response
from model import Model
from view import web_output

app = Flask(__name__)
model = Model()

format_input_id = "<p><input type='text' name='pb_id' placeholder='ID'></p>"
format_input_contacts = '''<p><input type='text' name='first_name' placeholder='First name'></p>
            <p><input type='text' name='last_name' placeholder='Last name'></p>
            <p><input type='text' name='phone_number' placeholder='Phone number'></p>'''


@app.route('/')
def index(msg=''):
    return render_template('index.html', message=web_output(msg))


@app.route('/create', methods=['GET', 'POST'])
def create():
    res = ''
    act_name = 'New'
    act_desc = 'Please fill the fields of the new contact.'
    if request.form.get('submit') == 'Back':
        return redirect('/')
    if request.method == 'POST':
        res = model.create(request.form.get('first_name'), request.form.get('last_name'),
                           request.form.get('phone_number'))
        if 'successfully' in res:
            return index(res)
    return render_template('fields.html', action_name=act_name, action_desc=act_desc, input_id=format_input_id,
                           contact_fields=format_input_contacts, alert=res)


@app.route('/read', methods=['GET', 'POST'])
def read():
    act_name = 'Search'
    act_desc = 'What contact do you want to find?'
    if request.form.get('submit') == 'Back':
        return redirect('/')
    if request.method == 'POST':
        r = model.read(request.form.get('first_name'), request.form.get('last_name'), request.form.get('phone_number'))
        return index(r)
    return render_template('fields.html', action_name=act_name, action_desc=act_desc,
                           contact_fields=format_input_contacts)


@app.route('/update', methods=['GET', 'POST'])
def update():
    res = ''
    act_name = 'Update'
    act_desc = 'For update the contact, all fields must be filled in.'
    if request.form.get('submit') == 'Back':
        return redirect('/')
    if request.method == 'POST':
        res = model.update(request.form.get('pb_id'), request.form.get('first_name'),
                           request.form.get('last_name'), request.form.get('phone_number'))
        if 'successfully' in res:
            return index(res)
    return render_template('fields.html', action_name=act_name, action_desc=act_desc, input_id=format_input_id,
                           contact_fields=format_input_contacts, alert=res)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    res = ''
    act_name = 'Delete'
    act_desc = 'Please choose id for delete.'
    if request.form.get('submit') == 'Back':
        return redirect('/')
    if request.method == 'POST':
        res = model.delete(request.form.get('pb_id'))
    if 'successfully' in res:
        return index(res)
    return render_template('fields.html', action_name=act_name, action_desc=act_desc, input_id=format_input_id,
                           alert=res)


@app.route('/save_txt')
def save_txt():
    response = make_response(model.get_txt_str_format())
    response.headers["Content-Disposition"] = "attachment; filename=phone_book.txt"
    return response


@app.route('/save_csv')
def save_csv():
    response = make_response(model.get_csv_str_format())
    response.headers["Content-Disposition"] = "attachment; filename=phone_book.csv"
    return response


app.run(debug=True)
