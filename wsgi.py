import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Staff, Course, CourseStaff
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, create_staff, create_course, assign_staff, view_course_staff )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

'''
Course Admin Commands
'''

course_admin_cli = AppGroup('course-admin', help='Course Admin object commands')

@course_admin_cli.command('create-staff')
@click.argument("staff_name", default="Jack")
def create_staff_command(staff_name):
    roles = {1: "Lecturer", 
             2: "TA", 
             3: "Tutor"}
    role_id = 0
    
    while role_id not in (1,2,3):
        role_id = int(input("Enter role {Lecturer: 1, TA: 2, Tutor: 3}: "))
    role = roles.get(role_id)
    create_staff(staff_name, role)

@course_admin_cli.command('create-course')
@click.argument("name", default="Maths")
@click.argument("description", default="Introductory Course")
def create_course_command(name, description):
    create_course(name, description)

@course_admin_cli.command('assign-staff')
@click.argument("course_name", default="Maths")
@click.argument("staff_name", default="Jack")
def assign_staff_command(course_name, staff_name):
    assign_staff(course_name, staff_name)

@course_admin_cli.command('view-course-staff')
@click.argument("course_name", default="Maths")
def view_course_staff_command(course_name):
    view_course_staff(course_name)

app.cli.add_command(course_admin_cli)