from functools import wraps
from flask_login import current_user
from application import login_manager
from flask import url_for,redirect

#Decorator for checking user has role required for using route
def role_required(role_needed):
    def decorator(view_function):
        @wraps(view_function)
        def decorated_function(*args,**kwargs):
            for role in current_user.roles:
                if role.name==role_needed:
                    return view_function(*args,**kwargs)
            return redirect(url_for('auth.auth_unauthorized',role=role_needed))
        return decorated_function
    return decorator


    