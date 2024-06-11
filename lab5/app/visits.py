import io
from flask import render_template, request, redirect, url_for, flash, Blueprint, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from app import db
from check_user import CheckUser
from functools import wraps
import mysql.connector
import math
from auth import bp_auth, check_rights, init_login_manager

bp_visit = Blueprint('visit', __name__, url_prefix='/visit')

PER_PAGE = 10

@bp_visit.route('/show')
@login_required
def show():
    page = int(request.args.get('page', 1))
    if current_user.is_admin():
        query1 = 'SELECT COUNT(*) as cnt FROM visit_logs'
        args1 = tuple()
        query2 = '''
        select j.id, path, created_at, ifnull(concat(u.last_name, ' ', u.first_name, ' ', u.middle_name), 'Неаутентифицированный пользователь') as fio from visit_logs as j left join users as u on j.user_id = u.id ORDER BY created_at DESC LIMIT %s OFFSET %s
        '''
        args2 = (PER_PAGE,PER_PAGE*(page-1) )
    else:
        query1 = 'SELECT COUNT(*) as cnt FROM visit_logs where user_id=%s'
        args1= (current_user.id, )
        query2 = '''
        SELECT j.id, path, created_at, ifnull(concat(u.last_name, ' ', u.first_name, ' ', u.middle_name), 'Неаутентифицированный пользователь') as fio from visit_logs as j left join users as u on j.user_id = u.id WHERE user_id=%s ORDER BY created_at DESC LIMIT %s OFFSET %s
        '''
        args2 = (current_user.id, PER_PAGE, PER_PAGE*(page-1))
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute(query1, args1)
    count = math.ceil((cursor.fetchone().cnt)/PER_PAGE)
    cursor.close()
    try:
        cursor = db.connection().cursor(named_tuple=True)
        cursor.execute(query2, args2)
        values = cursor.fetchall()
        cursor.close()
    except mysql.connector.errors.DatabaseError:
        db.connection().rollback()

    user = None
    if current_user.is_authenticated:
        user = current_user
    return render_template('/visits/show.html', values=values, count=count, page=page)

@bp_visit.route('/show_route')
@login_required
@check_rights('show_route')
def show_route():
    values=[]
    page = int(request.args.get('page', 1))
    count = 0
    try:
        query = 'SELECT path, count(user_id) AS count_path FROM visit_logs GROUP BY path ORDER BY count_path DESC'
        cursor = db.connection().cursor(named_tuple=True)
        cursor.execute(query)
        values = cursor.fetchall()
        cursor.close()
        count = math.ceil(len(values) / PER_PAGE)
    except mysql.connector.errors.DatabaseError:
        db.connection().rollback()

    return render_template('/visits/show_route.html', 
        values=values[PER_PAGE * (page - 1) : PER_PAGE * page],
        count=count, page=page)

@bp_visit.route('/show_user')
@login_required
@check_rights('show_user')
def show_user():
    values=[]
    page = int(request.args.get('page', 1))
    count = 0
    try:
        query = '''
        SELECT IFNULL(CONCAT(users.last_name, ' ', users.first_name,' ', users.middle_name), 'Неаутентифицированный пользователь') AS fio, 
        count(*) AS cnt 
        FROM visit_logs 
        LEFT JOIN users ON visit_logs.user_id = users.id 
        GROUP BY fio ORDER BY cnt DESC
        '''
        cursor = db.connection().cursor(named_tuple=True)
        cursor.execute(query, )
        values = cursor.fetchall()
        cursor.close()
        count = math.ceil(len(values) / PER_PAGE)
    except mysql.connector.errors.DatabaseError:
        db.connection().rollback()
    return render_template('/visits/show_user.html',
        values=values[PER_PAGE * (page - 1) : PER_PAGE * page],
        count=count, page=page)

@bp_visit.route('/send_csv_journal')
def send_csv_journal():
    query = 'SELECT * FROM visit_logs'
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute(query)
    records = cursor.fetchall()
    csv_text = ''
    for record in records:
        csv_text += 'Number: '
        csv_text += str(record.id)
        csv_text += '; '
        csv_text += 'Path: '
        csv_text += str(record.path)
        csv_text += '; '
        csv_text += 'User: '
        csv_text += str(record.user_id)
        csv_text += '; '
        csv_text += 'Created: '
        csv_text += str(record.created_at)
        csv_text += '; '
        csv_text += '\n'
    cursor.close()
    mem = io.BytesIO()
    mem.write(csv_text.encode())
    mem.seek(0)
    return send_file(mem, as_attachment=True, download_name='csv_text.csv')

@bp_visit.route('/send_csv_pages')
def send_csv_pages():
    query = 'SELECT path, COUNT(user_id) AS count_path FROM visit_logs GROUP BY path ORDER BY count_path DESC'
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute(query)
    records = cursor.fetchall()
    csv_text = ''
    for record in records:
        csv_text += 'Path: '
        csv_text += str(record.path)
        csv_text += '; '
        csv_text += 'Count of visits: '
        csv_text += str(record.count_path)
        csv_text += '; '
        csv_text += '\n'
    cursor.close()
    mem = io.BytesIO()
    mem.write(csv_text.encode())
    mem.seek(0)
    return send_file(mem, as_attachment=True, download_name='csv_pages.csv')

@bp_visit.route('/send_csv_users')
def send_csv_users():
    query = '''
        SELECT IFNULL(CONCAT(users.last_name, ' ', users.first_name,' ', users.middle_name), 'Неаутентифицированный пользователь') AS fio, 
        count(*) AS cnt 
        FROM visit_logs 
        LEFT JOIN users ON visit_logs.user_id = users.id 
        GROUP BY fio ORDER BY cnt DESC
        '''
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute(query)
    records = cursor.fetchall()
    csv_text = ''
    for record in records:
        csv_text += 'User: '
        csv_text += str(record.fio)
        csv_text += '; '
        csv_text += 'Count: '
        csv_text += str(record.cnt)
        csv_text += '; '
        csv_text += '\n'
    cursor.close()
    mem = io.BytesIO()
    mem.write(csv_text.encode())
    mem.seek(0)
    return send_file(mem, as_attachment=True, download_name='csv_users.csv')