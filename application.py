from flask import Flask, request, make_response, render_template, abort, Response, redirect, url_for
from story_insert import StoryInsert
import pymongo
from pagination import Pagination
import os

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
PER_PAGE = 2


def story_collect():
    uri = app.config.get("MONGO_URI")
    database = app.config.get("DATABASE")
    story = app.config.get("STORY")
    client = pymongo.MongoClient(uri)
    db = client[database]
    return db[story]


def category_collect():
    uri = app.config.get("MONGO_URI")
    database = app.config.get("DATABASE")
    category = app.config.get("CATEGORY")
    client = pymongo.MongoClient(uri)
    db = client[database]
    return db[category]


@app.route('/')
def home_page():
    lang = app.config.get("LANGUAGE")
    story_col = story_collect()
    category_col = category_collect()
    page = request.args.get("page", type=int, default=1)

    data_dict = {"language": lang}
    total_story = story_col.find(data_dict).count(True)
    pagination = Pagination(total_count=total_story, page=page, per_page=PER_PAGE)

    # No story found
    if not(1 <= page <= pagination.total_page):
        abort(404)

    story_list = story_col.find(data_dict)\
        .sort("story_id", -1)\
        .skip(PER_PAGE*(page-1))\
        .limit(PER_PAGE)

    category_list = category_col.find()
    ref_url = "{0}".format(request.host_url)

    return render_template('home_page.html',
                           records=story_list,
                           pagination=pagination,
                           category_list=category_list,
                           ref_url=ref_url)


@app.route('/category/<cat_id>/')
def category_page(cat_id):
    lang = app.config.get("LANGUAGE")
    story_col = story_collect()
    category_col = category_collect()
    page = request.args.get("page", type=int, default=1)

    data_dict = {"language": lang, "category.url": cat_id}
    total_story = story_col.find(data_dict).count(True)
    pagination = Pagination(total_count=total_story, page=page, per_page=PER_PAGE)

    # No story found
    if not (1 <= page <= pagination.total_page):
        abort(404)

    story_list = story_col.find(data_dict)\
        .sort("story_id", -1)\
        .skip(PER_PAGE*(page-1))\
        .limit(PER_PAGE)

    category_list = category_col.find()
    category_obj = category_col.find_one({"url": cat_id})
    ref_url = "{0}{1}/{2}/".format(request.host_url, "category", cat_id)

    return render_template('category_page.html',
                           records=story_list,
                           pagination=pagination,
                           category_list=category_list,
                           ref_url=ref_url,
                           category_obj=category_obj)


@app.route('/category/<cat_id>/<site_url>/')
def story_page(cat_id, site_url):
    lang = app.config.get("LANGUAGE")
    story_col = story_collect()
    category_col = category_collect()

    data_dict = {"language": lang, "site_url": site_url}
    record = story_col.find_one(data_dict)

    if not record:
        abort(404)

    category_list = category_col.find()
    return render_template('story_page.html',
                           story=record,
                           category_list=category_list)


@app.route('/<filename>.txt')
@app.route('/<filename>.xml')
def static_rs_file(filename):
    file_suffix_to_mimetype = {
        '.txt': 'text/plain',
        '.xml': 'application/xml'
    }
    local_path = app.config.get("IMPORT_PATH")
    path = os.path.join(local_path, "sitemap", request.path[1:])

    try:
        file_data = open(path)
    except:
        abort(404)

    root, ext = os.path.splitext(path)
    if ext in file_suffix_to_mimetype:
        return Response(file_data.read(), mimetype=file_suffix_to_mimetype[ext])

    return file_data.read()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


@app.cli.command('story_update')
def story_update():
    path = app.config.get("IMPORT_PATH")
    col = story_collect()
    params = "story_id"
    file_suffix = "English_story.json"

    si = StoryInsert(path, col, params, file_suffix)
    si.trigger_import()


@app.cli.command('category_update')
def category_update():
    path = app.config.get("IMPORT_PATH")
    col = category_collect()
    params = "category_id"
    file_suffix = "English_category.json"

    ci = StoryInsert(path, col, params, file_suffix)
    ci.trigger_import()

