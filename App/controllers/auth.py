from functools import wraps
from flask_jwt_extended import create_access_token, current_user, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request

from App.models import User, CourseAdmin

def course_admin_login(username, password):
  user = CourseAdmin.query.filter_by(username=username).first()
  if user and user.check_password(password):
    return create_access_token(identity=username)
  return None


def setup_jwt(app):
  jwt = JWTManager(app)

  # configure's flask jwt to resolve get_current_identity() to the corresponding user's ID
  @jwt.user_identity_loader
  def user_identity_lookup(identity):
    user = User.query.filter_by(username=identity).one_or_none()
    if user:
        return user.id
    return None

  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity)

  return jwt


# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
  @app.context_processor
  def inject_user():
      try:
          verify_jwt_in_request()
          user_id = get_jwt_identity()
          current_user = User.query.get(user_id)
          is_authenticated = True
      except Exception as e:
          print(e)
          is_authenticated = False
          current_user = None
      return dict(is_authenticated=is_authenticated, current_user=current_user)

def course_admin_required(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
      if not current_user.is_authenticated or not isinstance(current_user, CourseAdmin):
          return "Unauthorized", 401
      return func(*args, **kwargs)
  return wrapper