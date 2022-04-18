from flask import (
    Blueprint, render_template,
    redirect, flash,
    request, session
)

from backend.users import (
    login_verify, 
    get_all_students, get_student_detail,
    get_student_enroll_course, get_student_enroll_payment
)


# Can call `flash(msg_text, alert_type)` to show a temporary message on page
# alert_type could be 'success', 'danger', 'info', etc.
# View https://getbootstrap.com/docs/5.1/components/alerts/#link-color to get all the types

auth_app = Blueprint('auth_app', __name__)

@auth_app.route('/')
def show_all_students():
    students = get_all_students()
    print('stu', students)
    return render_template('auth/user_list.html', students=students)

@auth_app.route('/contact')
def show_contact():
    return render_template('contact.html')

@auth_app.route('/about')
def show_about():
    return render_template('about.html')

@auth_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password') # 抓取 form.html 中 input text 的值

        user = login_verify(email, pwd)
        # Get student entity or insturcotr entity
        # Student: {'S_ID': 4, 'NAME': 'goodgood', 'EMAIL': 'g23523@gmail.com'}
        # Instructor: {'I_ID': 2, 'NAME': 'dragon', 'EMAIL': 's123532@gmail.com', 'INTRODUCTION_BRIEF': '你好我是龍'}

        if user == None:
            flash('查無此用戶資訊，請先註冊帳號', 'danger')
        elif user == False:
            flash('密碼輸入錯誤，請重新檢查', 'danger')
        else:
            session['user'] = user
            # Login success, redirect
            flash('登入成功', 'success')
            return redirect('/')
    return render_template('auth/login.html')

@auth_app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    flash('登出成功', 'success')
    return redirect('/')

@auth_app.route('/user/<user_id>')
def show_student_profile(user_id):
    print('u_id', user_id)
    u = get_student_detail(user_id)

    print('profile', u)

    return render_template('auth/student_profile.html', user=u)

@auth_app.route('/user/mycourse')
def show_student_course():
    user = session.get('user')
    if not user:
        flash('請先登入', 'danger')
        return redirect('/login')
    if not user.get('S_ID', None):
        flash('你沒有權限', 'danger')
        return redirect('/')

    user_id = user.get('S_ID', None)
    u = get_student_enroll_course(user_id)
    return render_template('auth/student_course.html', user=u)

@auth_app.route('/user/mypayment')
def show_student_payment():
    user = session.get('user')
    if not user:
        flash('請先登入', 'danger')
        return redirect('/login')

    user_id = user.get('S_ID', None)
    u = get_student_enroll_payment(user_id)
    return render_template('auth/student_payment.html', user=u)