from flask import Flask, request, make_response, render_template, abort, Response
from story_insert import mongo, DataInsert
from pagination import Pagination
import os

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
mongo.init_app(app)

PER_PAGE = 9


@app.route('/page/<int:page>/')
@app.route('/')
def home_page(page=1):
    story_list = mongo.db.english_story.find({"language": "English"})\
        .sort("story_id", -1)\
        .skip(PER_PAGE*(page-1))\
        .limit(PER_PAGE)

    total_story = mongo.db.english_story.find({"language": "English"}).count(True)
    if not total_story:
        abort(404)

    category_list = mongo.db.english_category.find()
    pagination = Pagination(total_count=total_story, page=page, per_page=PER_PAGE)

    ref_url = "{0}".format(request.host_url)

    return render_template('home_page.html',
                           records=story_list,
                           pagination=pagination,
                           category_list=category_list,
                           ref_url=ref_url,
                           title="Home")


@app.route('/category/<category>/page/<int:page>/')
@app.route('/category/<category>/')
def category_page(category, page=1):
    story_list = mongo.db.english_story.find({"category.url": category,
                                              "language": "English"}) \
        .sort("story_id", -1) \
        .skip(PER_PAGE * (page - 1)) \
        .limit(PER_PAGE)

    total_story = mongo.db.english_story.find({"category.url": category,
                                              "language": "English"}).count(True)
    if not total_story:
        abort(404)

    category_list = mongo.db.english_category.find()
    tags = mongo.db.english_story.find_one({"category.url": category}, {"category.name": 1, "_id": 0})
    pagination = Pagination(total_count=total_story, page=page, per_page=PER_PAGE)

    ref_url = "{0}{1}/{2}/".format(request.host_url, "category", category)

    return render_template('home_page.html',
                           records=story_list,
                           pagination=pagination,
                           category_list=category_list,
                           ref_url=ref_url,
                           title=tags["category"]["name"])


@app.route('/story/<site_url>/')
def story_page(site_url):
    story = mongo.db.english_story.find_one({"site_url": site_url,
                                             "language": "English"})

    if not story:
        abort(404)

    category_list = mongo.db.english_category.find()
    return render_template('story_page.html',
                           story=story,
                           category_list=category_list)


@app.route('/article/<filename>')
def article_sitemap(filename):
    local_path = app.config.get("IMPORT_PATH")
    path = os.path.join(local_path, "sitemap")

    list_files = os.listdir(path)

    file_path = None
    for item in list_files:
        if item == filename:
            file_path = os.path.join(path, item)

    if not file_path:
        abort(404)

    with open(file_path) as f:
        file_content = f.read()

    resp = make_response(file_content)
    resp.headers['Content-type'] = 'application/xml; charset=utf-8'
    return resp


@app.route('/robots.txt')
def robots(filename="robots.txt"):
    local_path = app.config.get("IMPORT_PATH")
    path = os.path.join(local_path, "sitemap")

    list_files = os.listdir(path)

    file_path = None
    for item in list_files:
        if item == filename:
            file_path = os.path.join(path, item)

    if not file_path:
        abort(404)

    with open(file_path) as f:
        file_content = f.read()

    resp = make_response(file_content)
    resp.headers['Content-type'] = 'text/plain; charset=utf-8'
    return resp


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


@app.cli.command('article_update')
def article_update():
    # Story Update
    path = app.config.get("IMPORT_PATH")
    param_key = "story_id"
    filename = "English_story.json"
    si = DataInsert(path, param_key, filename)
    si.trigger_import()

    # Category Update
    path = app.config.get("IMPORT_PATH")
    param_key = "category_id"
    filename = "English_category.json"
    ci = DataInsert(path, param_key, filename)
    ci.trigger_import()

