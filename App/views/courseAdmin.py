from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views
from .user import login_required
from App.controllers import (
    create_course,
    jwt_required,
    course_admin_required,
    view_course_staff,
    create_staff,
    assign_staff,
    create_course,
)

course_admin_views = Blueprint('course_admin_views', __name__, template_folder='../templates')

@course_admin_required
@course_admin_views.route('/staff', methods=['POST'])
def create_staff_action():
    data = request.form
    flash(f"Staff member {data['name']} created!")
    staff = create_staff(data['name'], data['role'])
    return jsonify({'message': f"Staff member {staff.name} created with id {staff.id}"})

@course_admin_required
@course_admin_views.route('/courses', methods=['POST'])
def create_course_action():
    data = request.form
    flash(f"Course {data['name']} created!")
    course = create_course(data['name'], data['description'])
    return jsonify({'message': f"Course {course.name} created with id {course.id}"})

@course_admin_required
@course_admin_views.route('/assigned', methods=['POST'])
def assign_staff_view():
    data = request.form
    course_staff = assign_staff(data['course_name'], data['staff_name'])
    return jsonify({'message': f"Staff member with id {course_staff.staffID} assigned to course with id {course_staff.courseID}"})

@course_admin_required
@course_admin_views.route('/course_staff', methods=['GET'])
def get_course_staff_view():
    data = request.form
    staff = view_course_staff(data['course_name'])
    return jsonify(staff)




