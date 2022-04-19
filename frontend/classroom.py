from flask import (
    Blueprint, render_template,
    request,
    redirect, url_for, send_file,
    flash,
)
from backend.courses import (
    get_one_course, get_course_contents,
)

classroom_app = Blueprint('classroom_app', __name__)

@classroom_app.route('/classroom/<course_id>')
def show_all_courses(course_id):
    c_id = int(course_id)

    # show course details
    course_desc = get_one_course(c_id)
    
    # list all chaptet/contents
    contents = get_course_contents(c_id)
    return render_template('classroom/view_course.html', course_desc=course_desc, contents=contents)

@classroom_app.route('/classroom/content/<content_id>/view')
def show_file_content(content_id):
    # content_id = 
    return send_file('static/document/0821_guided_vae.pptx')