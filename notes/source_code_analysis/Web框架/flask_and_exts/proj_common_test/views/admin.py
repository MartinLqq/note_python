from flask import Module
admin = Module(__name__)

@admin.route('/index')
def module_admin():
    return 'admin index'
