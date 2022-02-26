from datetime import timedelta, datetime
from random import randint
from flask import Flask, render_template, request, redirect, session, make_response
import os
from database import MySQLDatabase, User, Root
from verify import verify
from shop_table import Stock, Shop

app = Flask(__name__)

app.secret_key = os.environ.get('AppConfig')

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

COOKIE_TIME_OUT = 60 * 60 * 24 * 7
# the symbols that can make problems with sql/html injections or jinja 2 troubles
dangerous_symbols = {"'", '"', '<', '>', '{', '}'}

title = 'McGrief'


@app.route('/admin', methods=['GET', 'POST'])
def admins_page():
    if request.method == 'GET':
        if request.cookies.get('username').rstrip() == 'admin':
            return render_template('administration_page.html')
        else:
            redirect('/')

    if request.method == 'POST':
        to_stock = Stock(item=request.form['item'], price=request.form['price'])
        shop = Shop()
        shop.add_new_item(to_stock)
        return render_template('administration_page.html',
                               response='item successfully added')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """the login form. if the login was successful adding the user to a session and loads the cookies for week.
     redirects to the homepage after the login."""
    if request.method == 'POST':

        if not dangerous_symbols.intersection(set(request.form['password'])):
            login_user = request.form['username']
            user = User(username=login_user, password=request.form['password'])
            in_database = MySQLDatabase()

            if in_database.check_if_user_exist(user):
                in_database.update_last_login_date(user)
                session['username'] = login_user
                resp = make_response(redirect('/homepage'))
                resp.set_cookie('username', value=login_user, max_age=COOKIE_TIME_OUT)
                return resp

            else:
                return render_template('login.html',
                                       the_title='McGrief',
                                       response='Не правильное имя пользователя или пароль.')

        else:
            return render_template('login.html',
                                   the_title='McGrief',
                                   response='Введен недопустимый символ')

    if request.method == 'GET':
        return render_template('login.html',
                               the_title=title)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password() -> 'render_template':
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        user = User(username=username, email=email)
        user_waiting_for = MySQLDatabase()

        if user_waiting_for.send_request_to_change_users_password(user):
            session['username_for_recovery_process'] = username
            session['email_for_recovery_process'] = email
            return redirect('/verify_recovery')

        else:
            the_response = 'Не правильное имя пользователя или пароль.'
            return render_template('forgot_password.html',
                                   response=the_response,
                                   the_title=title)

    if request.method == 'GET':
        return render_template('forgot_password.html',
                               the_title=title)


@app.route('/verify_recovery', methods=['POST', 'GET'])
def verify_recovery() -> 'render_template':
    if request.method == 'GET':

        if 'username_for_recovery_process' and 'email_for_recovery_process' in session:

            verifying_number = str(randint(100000, 999000))
            session['randint'] = verifying_number

            send_mail(email=session['email_for_recovery_process'],
                      username=session['username_for_recovery_process'],
                      the_number=verifying_number)
            return render_template('forgot_verify.html',
                                   the_title=title)

        else:
            return redirect('/')

    if request.method == 'POST':

        if request.form.get('confirm') == session['randint']:
            session.pop('randint')
            return render_template('new_password.html',
                                   respose='Подтверждение удалось!!')

        else:
            return render_template('forgot_verify.html',
                                   response='Введен не правильный код!')


def send_mail(email: str, username: str, the_number: str) -> 'None':
    verify(the_mail=email, name=username, number=the_number)


@app.route('/new_password', methods=['GET', 'POST'])
def new_password() -> 'render_template':
    if request.method == 'POST':

        if not dangerous_symbols.intersection(set(request.form['new_password'])):
            user = User(password=request.form['new_password'], username=session['username_for_recovery_process'])
            database = MySQLDatabase()

            if database.change_users_password(user):
                with open('new_password.log', 'a') as log:
                    updated_user = {'USER':
                                        {'USERNAME': user.username,
                                         'PASSWORD': request.form['new_password'],
                                         'CHANGED_AT': datetime.now()}}
                    log.write(str(updated_user))

                session.pop('username_for_recovery_process', None)
                session.pop('email_for_recovery_process', None)
                session.pop('username', None)

                resp = make_response(render_template('success_verify.html',
                                                     response="""Поздравляем вы успешно изменили пароль!!
                                                     \nОсталось залогинится""",
                                                     the_title=title))
                resp.set_cookie('username', expires=0)
                return resp

        else:
            return render_template('new_password.html',
                                   response='Введен запретный символ',
                                   the_title=title)


@app.route('/')
@app.route('/homepage')
def homepage() -> 'render_template':
    """the main page. changes to a page with a root to connect to the profile after the login"""
    if request.method == 'GET':
        if request.cookies.get('username'):
            valid_user = request.cookies.get('username')
            session['username'] = valid_user
            return render_template('after_login.html',
                                   the_title=title,
                                   response=f'Добро пожаловать {valid_user}!')

        else:
            return render_template('index.html',
                                   the_title=title)


@app.route('/logout')
def logout() -> 'render_template':
    session.pop('username', None)
    resp = app.make_response(redirect('/'))
    resp.set_cookie('username', expires=0)
    return resp


@app.route('/profile')
def profile() -> 'session':
    if request.method == 'GET':
        if request.cookies.get('username'):
            login_user = request.cookies.get('username')
            session['username'] = login_user
            user = User(username=login_user)
            database = MySQLDatabase()
            in_database = MySQLDatabase()
            root = Root()

            return render_template('profile.html',
                                   the_title='McGrief',
                                   root=root.show_roots(user),
                                   username=login_user,
                                   registration_date=database.registration_date(user),
                                   login_date=in_database.last_login_date(user))

        else:
            return render_template('no_access.html',
                                   the_title=title)


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/checkout/<price>/<item>')
def checkout(price, item):
    in_stock = Stock(price=price, item=item)
    print(price, item)
    shop_item = Shop()
    if shop_item.check_if_item_exists(in_stock):
        if request.cookies.get('username'):
            session['paying'] = item
            return render_template('checkout.html',
                                   sum=price)

        else:
            return render_template('no_access.html',
                                   the_title=title)

    else:
        return render_template('no_access.html')


@app.route('/thanks')
def thanks():
    try:
        if session['paying']:
            root = session['paying']
            update_root = User(username=request.cookies.get('username'), root=root)
            root = Root()
            root.set_roots(update_root)
            session.pop('paying', None)
            return render_template('thanks.html')

    except KeyError:
        return redirect('/shop')


@app.route('/registration_page', methods=['GET', 'POST'])
def regist_page() -> 'render_template':
    if request.method == 'POST':
        if not dangerous_symbols.intersection(set(request.form['password'])):

            user = User(username=request.form['username'], password=request.form['password'],
                        email=request.form['email'], ip=request.remote_addr)

            database = MySQLDatabase()
            # adding a new user if not exist
            if database.add_new_user(user) == 'user successfully added':
                # writing users data into a log file.
                user_dict = {'USER': {'USERNAME': user.username, 'PASSWORD': request.form['password']}}
                with open('reg_inf.log', 'a') as log:
                    log.write(str(user_dict))
                # add the user to a session
                session['username'] = request.form['username']
                # adding cookies to the user for 7 days and rendering the success registration template
                resp = make_response(render_template('regist.html',
                                                     the_title=title,
                                                     response='Добро пожаловать! регистрация успешно завершена.'))
                resp.set_cookie('username', value=request.form['username'], max_age=COOKIE_TIME_OUT)
                return resp

            else:
                # sending the response if the user already exist
                return render_template('regist.html',
                                       the_title='title',
                                       response='Введеный вами логин уже занят')

        else:

            if request.method == 'POST':
                # if the user entered dangerous symbols in the form the error occurs
                the_response = 'Введен недопустимый символ'

                return render_template('regist.html',
                                       the_title='McGrief',
                                       response=the_response)
    # the default page view
    return render_template('regist.html',
                           the_title=title, )


@app.route('/news')
def news() -> 'render_template':
    """returns the news page"""
    return render_template('news.html',
                           the_title=title)


@app.route('/about_us')
def about_us() -> 'render_template':
    """returns the about_us page"""
    return render_template('about_us.html',
                           the_title=title)


@app.errorhandler(404)
def response_404(error) -> 'render_template':
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.248')
