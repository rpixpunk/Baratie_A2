from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views
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
    data = request.json # Return 400 Bad Request status code
    flash(f"Staff member {data['name']} created!")
    staff = create_staff(data['name'], data['role'])
    if staff is None:
        return jsonify({'message': f"Staff member {staff.name} already exists"}), 200
    return jsonify({'message': f"Staff member {staff.name} created with id {staff.id}"}), 201

@course_admin_required
@course_admin_views.route('/courses', methods=['POST'])
def create_course_action():
    data = request.json
    flash(f"Course {data['name']} created!")
    course = create_course(data['name'], data['description'])
    return jsonify({'message': f"Course {course.name} created with id {course.id}"}), 201

@course_admin_required
@course_admin_views.route('/assign_staff', methods=['POST'])
def assign_staff_view():
    data = request.json
    course_staff = assign_staff(data['course_name'], data['staff_name'])
    return jsonify({'message': f"{data['staff_name']} with id {course_staff.staffID} assigned to {data['course_name']} with id {course_staff.courseID}"}), 201

@course_admin_required
@course_admin_views.route('/course_staff', methods=['GET'])
def get_course_staff_view():
    data = request.json
    staff = view_course_staff(data['course_name'])
    return jsonify(staff)




