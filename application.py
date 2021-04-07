from flask import Flask, request, make_response, render_template, abort, Response
from story_insert import mongo, StoryInsert, CategoryInsert
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

    total_story = story_list.count(True)
    if not total_story:
        abort(404)

    category_list = mongo.db.english_category.find()
    pagination = Pagination(total_count=total_story, page=page, per_page=PER_PAGE)

    ref_url = "{0}".format(request.host_url)

    return render_template('home_page.html',
                           records=story_list,
                           pagination=pagination,
                           category_list=category_list,
                           ref_url=ref_url)


@app.route('/category/<category>/page/<int:page>/')
@app.route('/category/<category>/')
def category_page(category, page=1):
    story_list = mongo.db.english_story.find({"category.url": category,
                                              "language": "English"}) \
        .sort("story_id", -1) \
        .skip(PER_PAGE * (page - 1)) \
        .limit(PER_PAGE)

    total_story = story_list.count(True)
    if not total_story:
        abort(404)

    category_list = mongo.db.english_category.find()
    category_obj = mongo.db.english_category.find_one({"url": category})
    pagination = Pagination(total_count=total_story, page=page, per_page=PER_PAGE)

    ref_url = "{0}{1}/{2}/".format(request.host_url, "category", category)

    return render_template('category_page.html',
                           records=story_list,
                           pagination=pagination,
                           category_list=category_list,
                           ref_url=ref_url,
                           category_obj=category_obj)


@app.route('/category/<category>/<site_url>/')
def story_page(category, site_url):
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


@app.cli.command('story_update')
def story_update():
    path = app.config.get("IMPORT_PATH")
    si = StoryInsert(path)
    si.trigger_import()


@app.cli.command('category_update')
def category_update():
    path = app.config.get("IMPORT_PATH")
    ci = CategoryInsert(path)
    ci.trigger_import()

