from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from mysql_db import MySQL
import mysql.connector

app = Flask(__name__)

application = app
 
app.config.from_pyfile('config.py')

db = MySQL(app)

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа необходимо пройти аутентификацию'
login_manager.login_message_category = 'warning'

class User(UserMixin):
    def __init__(self, user_id, user_login):
        self.id = user_id
        self.login = user_login

##### ДОМАШНЕЕ ЗАДАНИЕ #####

# ВАЛИДАЦИЯ 

# проверка на длину пароля (вернет false при неправильной длине)
def password_check_len(password):
    return len(password) > 8 or len(password) < 128

# проверка на одну заглавную и одну строчную (вернет false при отсутсвии строчной или заглавной буквы)
def password_check_register(password):
    has_lowercase = False
    has_uppercase = False
    for char in password:
        if char.islower():
            has_lowercase = True
        elif char.isupper():
            has_uppercase = True
    return has_lowercase and has_uppercase

# проверка алфавита (вернет false, если не будет букв)
def password_check_char(password):
    alpha = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    count = 0
    for i in password:
        if i in alpha:
            count += 1
    if count == 0:
        return False
    return True

# проверка на цифры в пароле (вернет false при отсутствии цифр)
def password_check_num(password):
    nums = '0123456789'
    numcount = 0
    for i in password:
        if i in nums:
            numcount += 1
    if numcount == 0:
        return False
    return True
    
# проверка на допустимые символы
def password_check_symbols(password):
    lowalpha = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    upalpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    nums = '0123456789'
    space = ' '
    symbols = '~!?@#$%^&*_-+()[]\{\}></\\|\"\'.,:;'
    for i in password:
        if i in lowalpha or i in upalpha or i in nums or i in symbols:
            pass
        elif i == space:
            return False
        else:
            return False
    return True

# проверка условий для пароля
def password_validation(password):
    if not password_check_len(password):
        return False
    if not password_check_register(password):
        return False
    if not password_check_char(password):
        return False
    if not password_check_num(password):
        return False
    if not password_check_symbols(password):
        return False
    return True

# проверка длины логина (вернет false при недопустимой длине)
def login_check_len(login):
    if len(login) > 5:
        return True
    return False

# допустимые символы логина (вернет false при недопустимых символах)
def login_validation(login):
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    for char in login:
        if char not in alphabet:
            return False
    return True

def validate(login, password, last_name, first_name):
    errors = {}
    if not password_validation(password):
        password_mes = 'Пароль не соответствует требованиям: '
        if password_check_len(password):
            password_mes += 'не менее 8 символов и не более 128 символов; '
        if not password_check_register(password):
            password_mes += 'как минимум одна заглавная и одна строчная буква; '
        if not password_check_char(password):
            password_mes += 'только латинские или кириллические буквы; '
        if not password_check_num(password):
           password_mes +=  'как минимум одна цифра; только арабские цифры; '
        if not password_check_symbols(password):
            password_mes += '''без пробелов; Другие допустимые символы:~ ! ? @ # $ % ^ & * _ - + ( ) [ ] { } > < / \ | " ' . , : ;'''

        errors['pas_class'] = "is-invalid"
        errors['pas_mes_class'] = 'invalid-feedback'
        errors['pas_mes'] = password_mes

        if not login_validation(login):
            errors['log_class'] = 'is-invalid'
            errors['log_mes_class'] = 'invalid-feedback'
            errors['log_mes'] = 'Логин должен состоять только из латинских букв и цифр'
        if not login_check_len(login):
            errors['log_class'] = 'is-invalid'
            errors['log_mes_class'] = 'invalid-feedback'
            errors['log_mes'] = 'Логин должен быть не менее 5 символов'
        if len(login) == 0:
            errors['log_class'] = "is-invalid"
            errors['log_mes_class'] = "invalid-feedback"
            errors['log_mes'] = "Поле логин не должено быть пустым"
        if len(password) == 0:
            errors['pas_class'] = "is-invalid"
            errors['pas_mes_class'] = "invalid-feedback"
            errors['pas_mes'] = "Поле пароль не должено быть пустым"
        if len(last_name) == 0:
            errors['ln_class'] = "is-invalid"
            errors['ln_mes_class'] = "invalid-feedback"
            errors['ln_mes'] = "Поле фамилия не должно быть пустой"
        if len(first_name) == 0:
            errors['fn_class'] = "is-invalid"
            errors['fn_mes_class'] = "invalid-feedback"
            errors['fn_mes'] = "Поле имя не должно быть пустым" 
        return errors


# ИЗМЕНЕНИЕ ПАРОЛЯ
@app.route('/users/change/', methods=["POST", "GET"])
@login_required
def change():
    if request.method == "POST":
        user_id = current_user.id
        oldpas = request.form['oldpas']
        newpas = request.form['newpas']
        new2pas = request.form['new2pas']
        query = 'SELECT * FROM users WHERE id = %s and password_hash = %s'
        user = None
        errors = validate('login', newpas, 'name', 'name')
        try:
            cursor = db.connection().cursor(named_tuple=True)
            cursor.execute(query, (user_id, oldpas))
            user = cursor.fetchone()
            cursor.close()
        except mysql.connector.errors.DatabaseError:
            db.connection().rollback()
            flash(f'Возникла ошибка при проверке пароля', 'danger')
            return render_template('users/change.html')
        if not user:
            flash(f'Неверный пароль', 'danger')
            return render_template('users/change.html')
        elif errors:
            if len(errors.keys()) > 0:
                flash(errors['pas_mes'], 'danger')
                return render_template('users/change.html')
        elif newpas != new2pas:
            flash(f'Пароли не совпадают', 'danger')
            return render_template('users/change.html')
        else:
            query = 'UPDATE users SET password_hash = %s WHERE id = %s'
            try:
                cursor = db.connection().cursor(named_tuple=True)
                cursor.execute(query, (newpas, user_id))
                db.connection().commit()
                cursor.close()
                flash(f'Пароль обновлен', 'success')
                return redirect(url_for('index'))
            except mysql.connector.errors.DatabaseError:
                db.connection().rollback()
                flash(f'Ошибка при обновлении пароля', 'danger')
                return render_template('users/change.html')
    else:
        return render_template('users/change.html')

@login_manager.user_loader
def load_user(user_id):
    query = 'SELECT * FROM users WHERE users.id=%s'
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return User(user.id, user.login)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        check = request.form.get('secretcheck') == 'on'
        query = 'SELECT * FROM users WHERE users.login=%s AND users.password_hash=%s'
        cursor = db.connection().cursor(named_tuple=True)
        cursor.execute(query, (login, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            login_user(User(user.id, user.login), remember=check)
            param_url = request.args.get('next')
            flash('Вы успешно вошли!', 'success')
            return redirect(param_url or url_for('index'))
        flash('Ошибка входа!', 'danger')
    return render_template('login.html' )

@app.route('/logout', methods = ['GET'])
def logout():   
    logout_user()
    return redirect(url_for('index'))

@app.route('/users/')
@login_required
def show_users():
    query = '''
            SELECT users.*, roles.name as role_name
            FROM users
            LEFT JOIN roles
            on roles.id = users.role_id
            '''
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    return render_template('users/index.html',users=users)

def get_roles():
    query = 'SELECT * FROM roles'
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute(query)
    roles = cursor.fetchall()
    cursor.close()
    return roles

@app.route('/users/show/<int:user_id>') 
def show_user(user_id):
    user_query = 'SELECT users.*, roles.name AS role_name FROM users LEFT JOIN roles ON users.role_id = roles.id WHERE users.id=%s'
    
    with db.connection().cursor(named_tuple=True) as cursor:
        cursor.execute(user_query, (user_id,))
        user = cursor.fetchone()
        
    return render_template('users/show.html', user=user)

@app.route('/users/create', methods = ['POST', 'GET'])
@login_required
def create():
    roles = get_roles()
    if request.method == 'POST':
        login = request.form['login']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        password = request.form['password']
        role_id = request.form['role_id']

        errors = validate(login, password, last_name, first_name)
        if errors:
            if len(errors.keys()) > 0:
                return render_template('users/create.html', **errors)

        try:
            query = 'INSERT INTO users (login, last_name, first_name, middle_name, password_hash, role_id) VALUES (%s, %s, %s, %s, %s, %s)'
            cursor = db.connection().cursor(named_tuple=True)
            cursor.execute(query, (login, last_name, first_name, middle_name, password, role_id))
            db.connection().commit()
            flash(f'Пользователь {login} успешно создан.', 'success')
            cursor.close()
            return redirect(url_for('show_users'))
        
        except mysql.connector.errors.DatabaseError:
            db.connection().rollback()
            flash(f'При создании пользователя произошла ошибка.', 'danger')
            return render_template('users/create.html', roles=roles)
        
    return render_template('users/create.html', roles=roles)

@app.route('/users/edit/<int:user_id>', methods=["POST", "GET"])
def edit(user_id):
    roles = get_roles()
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        role_id = request.form['role_id']
        try:
            query = 'UPDATE users set first_name = %s, last_name = %s, middle_name = %s, role_id = %s where id = %s'
            cursor = db.connection().cursor(named_tuple=True)
            cursor.execute(query, (first_name, last_name, middle_name, role_id, user_id))
            db.connection().commit()
            flash(f'Данные пользователя {first_name} успешно обновлены.', 'success')
            cursor.close()
            return redirect(url_for('show_users'))
        
        except mysql.connector.errors.DatabaseError:
            db.connection().rollback()
            flash(f'При обновлении пользователя произошла ошибка.', 'danger')
            return render_template('users/edit.html')

    query = '''
            SELECT users.*, roles.name as role_name
            FROM users
            LEFT JOIN roles
            on roles.id = users.role_id
            where users.id=%s
            '''
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    cursor.close()

    return render_template('users/edit.html', user=user, roles=roles)

@app.route('/users/delete/')
@login_required
def delete():

    try:
        user_id = request.args.get('user_id')
        query = 'DELETE from users where id = %s'
        cursor = db.connection().cursor(named_tuple=True)
        cursor.execute(query, (user_id,))
        db.connection().commit()
        flash(f'Этот пользователь успешно удален.', 'success')
        cursor.close()

    except mysql.connector.errors.DatabaseError:
        db.connection().rollback()
        flash(f'При удалении пользователя произошла ошибка.', 'danger')
        return render_template('users/index.html', user_id=user_id)

    return redirect(url_for('show_users'))