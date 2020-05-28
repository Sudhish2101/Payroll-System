from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm,AddForm, UpdateForm, DeleteForm
from app.models import User, Employee



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    employees = current_user.employees.order_by(Employee.id)
    return render_template('index.html', user=current_user, employees=employees)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm()
    if form.validate_on_submit():
        pay = form.hourly_pay.data*form.hours_worked.data+form.allowance.data-form.deduction.data
        employee = Employee(name=form.name.data, hourly_pay=form.hourly_pay.data,
                            hours_worked=form.hours_worked.data, allowance=form.allowance.data,
                            deduction=form.deduction.data, payroll=pay, user_id=current_user.id)
        db.session.add(employee)
        db.session.commit()
        flash('Congratulations, you added an employee!')
        return redirect(url_for('index'))
    return render_template('add.html', title='Add', form=form)

@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        employee = db.session.query(Employee).filter_by(id = form.id.data).first()        
        if form.name.data:
            employee.name = form.name.data
        if form.hourly_pay.data:
            employee.hourly_pay = form.hourly_pay.data
        if form.hours_worked.data:
            employee.hours_worked = form.hours_worked.data
        if form.allowance.data:
            employee.allowance = form.allowance.data
        if form.deduction.data:
            employee.deduction = form.deduction.data
        employee.payroll = employee.hourly_pay*employee.hours_worked+employee.allowance-employee.deduction
        db.session.commit()
        flash('Congratulations, you updated an employee!')
        return redirect(url_for('index'))
    return render_template('update.html', title='Update', form=form)

@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        employee = db.session.query(Employee).filter_by(id = form.id.data).first()
        db.session.delete(employee)
        db.session.commit()
        flash('Congratulations, you deleted an employee!')
        return redirect(url_for('index'))
    return render_template('delete.html', title='Delete', form=form)



