import pymysql
from app import app
from db import cmx, cursor_connection
from datetime import datetime
from flask import flash, render_template, request, redirect
from werkzeug.security import generate_password_hash


@app.route('/')
def users():
    sql = "SELECT * FROM Users"
    row, rows = cursor_connection(sql, (), 'users')
    return render_template('users.html', users=rows)


@app.route('/new_user')
def add_user_view():
    return render_template('add.html')


@app.route('/add', methods=['POST'])
def add_user():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _role = request.form['inputRole']
    if _name and _email and _password and _role and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)
        _date_of_join = datetime.now()
        sql = "INSERT INTO Users(name, mail, password, role, date_of_join) VALUES(%s, %s, %s, %s, %s)"
        data = (_name, _email, _hashed_password, _role, _date_of_join)
        _, _ = cursor_connection(sql, data, 'add_user')
        flash('User added successfully!')
        return redirect('/')
    else:
        return 'Error while adding user'


@app.route('/edit/<int:id>')
def edit_view(id):
    sql = "SELECT * FROM Users WHERE id=%s"
    data = (id, )
    row, _ = cursor_connection(sql, data, 'edit_user')
    if row:
        return render_template('edit.html', row=row)
    else:
        return 'Error loading #{id}'.format(id=id)


@app.route('/update', methods=['POST'])
def update_user():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _role = request.form['inputRole']
    _id = request.form['id']
    if _name and _email and _password and _id and _role and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)
        sql = "UPDATE Users SET name=%s, mail=%s, password=%s, role=%s WHERE id=%s"
        data = (_name, _email, _hashed_password, _role, _id,)
        _, _ = cursor_connection(sql, data, 'update_user')
        flash('User updated successfully!')
        return redirect('/')
    else:
        return 'Error while updating user'


@app.route('/delete/<int:id>')
def delete_user(id):
    sql = "DELETE FROM Users WHERE id=%s"
    data = (id,)
    _, _ = cursor_connection(sql, data, 'delete_user')
    flash('User deleted successfully!')
    return redirect('/')


if __name__ == "__main__":
    app.run()
