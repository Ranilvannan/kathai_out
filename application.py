from flask import Flask, request, make_response, render_template, abort
from story_insert import mongo, StoryInsert, CategoryInsert
from pagination import Pagination

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')
mongo.init_app(app)

PER_PAGE = 2


@app.route('/turn/<int:page>/')
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


@app.route('/category/<category>/turn/<int:page>/')
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


@app.route('/article/sitemap.xml')
def article_sitemap():
    file_obj = open(app.config.get("IMPORT_PATH"))
    resp = make_response(file_obj)
    resp.headers['Content-type'] = 'text/xml; charset=utf-8'
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

