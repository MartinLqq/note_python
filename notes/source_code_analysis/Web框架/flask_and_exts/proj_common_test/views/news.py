from flask import Module
news = Module(__name__)

@news.route('/index')
def module_news(): return 'news index'
