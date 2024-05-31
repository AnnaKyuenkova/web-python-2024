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

def pas_check_len(password):
    if len(password) < 8 or len(password) > 128:
        return False
    else:
        return True
    
def pas_check_char(password):
    lowalpha = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    upalpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    lowcount, upcount = 0, 0
    for i in password:
        if i in lowalpha:
            lowcount += 1
        elif i in upalpha:
            upcount += 1
    if lowcount == 0 or upcount == 0:
        return False
    return True

def pas_check_num(password):
    nums = '0123456789'
    numcount = 0
    for i in password:
        if i in nums:
            numcount += 1
    if numcount == 0:
        return False
    return True
    
def pas_check_symbols(password):
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

def pas_validation(password):
    if not pas_check_len(password):
        return False
    if not pas_check_char(password):
        return False
    if not pas_check_num(password):
        return False
    if not pas_check_symbols(password):
        return False
    return True

def log_validation(login):
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    for char in login:
        if char not in alphabet:
            return False
    if len(login) < 5:
        return False
    return True

def validate(login, password, last_name, first_name):
    errors = {}
    if not pas_validation(password):
        pas_mes = '''
Пароль не соответствует требованиям:
'''
        if not pas_check_len(password):
            pas_mes += '''
не менее 8 символов;
не более 128 символов;
'''
        if not pas_check_char(password):
            pas_mes += '''
как минимум одна заглавная и одна строчная буква;
только латинские или кириллические буквы;
'''
        if not pas_check_num(password):
           pas_mes +=  '''
как минимум одна цифра;
только арабские цифры;
'''
        if not pas_check_symbols(password):
            pas_mes += '''без пробелов;
Другие допустимые символы:~ ! ? @ # $ % ^ & * _ - + ( ) [ ] { } > < / \ | " ' . , : ;
'''

        errors['pas_class'] = "is-invalid"
        errors['pas_mes_class'] = 'invalid-feedback'
        errors['pas_mes'] = pas_mes
        if not log_validation(login):
            errors['log_class'] = 'is-invalid'
            errors['log_mes_class'] = 'invalid-feedback'
            errors['log_mes'] = 'Логин должен состоять только из латинских букв и цифр и иметь длину не менее 5 символов'
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
    query = 'SELECT * FROM users'
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    return render_template('users/index.html',users=users)

@app.route('/users/create', methods = ['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        login = request.form['login']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        password = request.form['password']

        errors = validate(login, password, last_name, first_name)
        if errors:
            if len(errors.keys()) > 0:
                return render_template('users/create.html', **errors)

        try:
            query = '''
                insert into users (login, last_name, first_name, middle_name, password_hash)
                VALUES (%s, %s, %s, %s, %s)
                '''
            cursor = db.connection().cursor(named_tuple=True)
            cursor.execute(query, (login, last_name, first_name, middle_name, password))
            db.connection().commit()
            flash(f'Пользователь {login} успешно создан.', 'success')
            cursor.close()
        except mysql.connector.errors.DatabaseError:
            db.connection().rollback()
            flash(f'При создании пользователя произошла ошибка.', 'danger')
            return render_template('users/create.html')
        
    return render_template('users/create.html')

@app.route('/users/show/<int:user_id>') 
def show_user(user_id):
    user_query = 'SELECT users.*, roles.name AS role_name FROM users JOIN roles ON users.role_id = roles.id WHERE users.id=%s'
    
    with db.connection().cursor(named_tuple=True) as cursor:
        cursor.execute(user_query, (user_id,))
        user = cursor.fetchone()
        
    return render_template('users/show.html', user=user)

@app.route('/users/edit/<int:user_id>', methods=["POST", "GET"])
def edit(user_id):
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        try:
            query = '''
                UPDATE users set first_name = %s, last_name = %s, middle_name = %s where id = %s
                '''
            cursor = db.connection().cursor(named_tuple=True)
            cursor.execute(query, (first_name, last_name, middle_name, user_id))
            db.connection().commit()
            flash(f'Данные пользователя {first_name} успешно обновлены.', 'success')
            cursor.close()
        except mysql.connector.errors.DatabaseError:
            db.connection().rollback()
            flash(f'При обновлении пользователя произошла ошибка.', 'danger')
            return render_template('users/edit.html')

    query = 'SELECT  * FROM users WHERE users.id=%s'
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    cursor.close()

    return render_template('users/edit.html', user=user)

@app.route('/users/delete/')
@login_required
def delete():
    try:
        user_id = request.args.get('user_id')
        query = '''
            DELETE from users where id = %s
            '''
        cursor = db.connection().cursor(named_tuple=True)
        cursor.execute(query, (user_id,))
        db.connection().commit()
        flash(f'Пользователь {user_id} успешно удален.', 'success')
        cursor.close()
    except mysql.connector.errors.DatabaseError:
        db.connection().rollback()
        flash(f'При удалении пользователя произошла ошибка.', 'danger')
        return render_template('users/index.html', user_id=user_id)

    return redirect(url_for('show_users'))

@app.route('/users/change/', methods=["POST", "GET"])
@login_required
def change():
    if request.method == "POST":
        user_id = current_user.id
        oldpas = request.form['oldpas']
        newpas = request.form['newpas']
        new2pas = request.form['new2pas']
        query = """
            SELECT * FROM users WHERE id = %s and password_hash = SHA2(%s, 256)
            """
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
            flash(f'Неправильный пароль', 'danger')
            return render_template('users/change.html')
        # elif not pas_validation(newpas):
        elif errors:
            if len(errors.keys()) > 0:
                flash(errors['pas_mes'], 'danger')
                return render_template('users/change.html')
        elif newpas != new2pas:
            flash(f'Пароли не совпадают', 'danger')
            return render_template('users/change.html')
        else:
            query = """
                UPDATE users SET password_hash = SHA2(%s, 256) WHERE id = %s
                """
            try:
                cursor = db.connection().cursor(named_tuple=True)
                cursor.execute(query, (newpas, user_id))
                db.connection().commit()
                cursor.close()

                # with db.connection().cursor(named_tuple=True) as cursor:
                #     cursor.execute(query, (newpas, user_id))
                #     db.connection().commit()
                flash(f'Пароль обновлен', 'success')
                return redirect(url_for('index'))
            except mysql.connector.errors.DatabaseError:
                db.connection().rollback()
                flash(f'Ошибка при обновлении пароля', 'danger')
                return render_template('users/change.html')
    else:
        return render_template('users/change.html')