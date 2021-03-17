from flask import Flask, request, render_template, abort
from flask_pymongo import PyMongo
from story_insert import mongo, StoryInsert
from pagination import Pagination

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
mongo.init_app(app)

PER_PAGE = 1


@app.route('/')
def home_page():
    page = request.args.get("page", type=int, default=1)
    story_list = mongo.db.hindi.find()\
        .sort("story_id", -1)\
        .skip(PER_PAGE*(page-1))\
        .limit(PER_PAGE)

    total_story = story_list.count()
    if not total_story:
        abort(404)

    pagination = Pagination(total_count=total_story, page=page, per_page=PER_PAGE)
    return render_template('home_page.html', records=story_list, pagination=pagination)


@app.route('/category/<category>/')
@app.route('/category/<category>')
def category_page(category):
    page = request.args.get("page", type=int, default=1)
    story_list = mongo.db.hindi.find({"tags.url": category}) \
        .sort("story_id", -1) \
        .skip(PER_PAGE * (page - 1)) \
        .limit(PER_PAGE)

    total_story = story_list.count()
    if not total_story:
        abort(404)

    tags = mongo.db.hindi.find_one({"tags.url": category}, {"tags.name": 1, "_id": 0})
    pagination = Pagination(total_count=total_story, page=page, per_page=PER_PAGE)
    return render_template('category_page.html',
                           records=story_list,
                           pagination=pagination,
                           tags=tags["tags"][0]["name"])


@app.route('/story/<site_url>/')
@app.route('/story/<site_url>')
def story_page(site_url):
    story = mongo.db.hindi.find_one({"site_url": site_url})

    if not story:
        abort(404)

    return render_template('story_page.html', story=story)


@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title='404'), 404


@app.cli.command('story_update')
def story_update():
    path = app.config.get("IMPORT_PATH")
    si = StoryInsert(path)
    si.trigger_import()




