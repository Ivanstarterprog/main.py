from flask import Flask
from data import db_session
from flask import render_template, redirect, request, abort
from flask_login import LoginManager, login_user, current_user
from flask_login import login_required, logout_user
from forms.User import RegisterForm, LoginForm
from flask_restful import abort, Api
from flask import flash
from data.users import User
from data.results import Result
from data.tests import Test
from api import UserTeacherResource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Kuzpc'

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)


def main():
    api.add_resource(UserTeacherResource.TeacherResource, '/api/admins/<int:user_id>/<string:secret_key>')
    api.add_resource(UserTeacherResource.TeachersListResource, '/api/admins/<string:secret_key>')
    db_session.global_init("db/college.db")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@login_required
def mainpage():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        if current_user.role == "student":
            results = db_sess.query(Result).filter(Result.user_id == current_user.id).all()
            tests= db_sess.query(Test).all()
            return render_template("user_page.html", user=current_user, title='Главная страница',
                                   results=results, test=tests)
        else:
            return render_template("user_page.html", user=current_user, title='Главная страница')
    else:
        return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if current_user.role == "administrator":
        form = RegisterForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Данная почта уже занята")
            avatar = form.avatar.data
            if avatar:
                filename = f'{form.familia.data}_{form.name.data}_{form.otche.data}.{avatar.filename.split(".")[1]}'
                avatar.save('static/img/users/' + filename)
            else:
                filename = 'default.jpg'
            match form.role.data:
                case "Студент":
                    role = "student"
                case "Учитель":
                    role = "teacher"
                case "Администратор":
                    role = "admin"
            user = User(
                name=form.name.data,
                surname=form.surname.data,
                patronymic = form.patronymic.data,
                email=form.email.data,
                avatar=filename,
                role=role,
                group=form.group.data
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return render_template('register.html', title='Регистрация пользователя', form=form)
        return render_template('register.html', title='Регистрация пользователя', form=form)
    else:
        flash("Недостаточно прав для редактирования")
        return redirect(request.url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/main_page")
        return render_template('login.html',
                               message="Неправильная почта или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/students")
@login_required
def students():
    db_sess = db_session.create_session()
    students_pages = db_sess.query(User).filter(role="student")
    return render_template('students.html', user=current_user, students=students_pages, title="Студенты")


@app.route('/students/<int:id>', methods=['GET', 'POST'])
@login_required
def studentResult(id):
    if current_user.role != "student":
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(id=id).first():
            student = db_sess.query(User).filter(id=id)
            results = db_sess.query(Result).filter(user_id=id)
            test = db_sess.query(Test).all()
            return render_template('result.html', student=student,
                                   title="Страница студента", results=results, test=test, user=current_user)
        else:
            flash("Такого пользователя нет в базе данных")
            return redirect(request.url)


@app.route('/tests')
@login_required
def tests():
    db_sess = db_session.create_session()
    test = db_sess.query(Test).all()
    return render_template('tests.html', test=test, user=current_user, title="Тесты")

# @app.route('/tests/<string:testname>', methods=['GET', 'POST'])
# @login_required
# def testname(testname):
#     test = "".join(testname.split())
#     if request.method == "POST":
#         db_sess = db_session.create_session()
#         tri = Try(user_id=current_user.id,
#                   test_id=request.form.get("num_of_test"),
#                   mark=request.form.get("result"))
#         db_sess.add(tri)
#         db_sess.commit()
#         return redirect('/')
#     return render_template(f'{test}.html')

if __name__ == '__main__':
    main()