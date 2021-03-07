from flask import Flask, request, render_template, abort
from flask_pymongo import PyMongo
from story_insert import mongo, StoryInsert

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
mongo.init_app(app)


@app.route('/')
def index_page():
    return render_template('test.html')


@app.route('/tags/<tags>/')
@app.route('/tags/<tags>')
def tag_page(tags):
    return render_template('test.html')


@app.route('/story/<title>/')
@app.route('/story/<title>')
def story_page(title=None):
    return render_template('test.html')


@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title='404'), 404


@app.cli.command('story_update')
def story_update():
    path = app.config.get("IMPORT_PATH")
    si = StoryInsert(path)
    si.trigger_import()




