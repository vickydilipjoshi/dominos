import os
import jinja2
from flask import Flask, request, send_from_directory

app = Flask(__name__)
app.debug = True

templates_path = './templates'
file_system_loader = jinja2.FileSystemLoader(templates_path)
env = jinja2.Environment(loader=file_system_loader)

app_template = env.get_template('app.html')
index_template = env.get_template('index.html')
post_template = env.get_template('post.html')


@app.route("/")
def index():
    unsorted_post_dates = map(strip_extension, os.listdir("./posts"))
    post_dates = sorted(unsorted_post_dates, reverse=True)
    partial = index_template.render(post_dates=post_dates)
    return app_template.render(partial=partial, headers=request.headers)


@app.route("/assets/<path:asset_name>")
def asset(asset_name):
    return send_from_directory("assets", asset_name)


@app.route("/post/<path:post_date>")
def post(post_date):
    post = open("posts/" + post_date + ".html")
    post_html = post.read()
    post.close()
    partial = post_template.render(post_html=post_html)
    return app_template.render(partial=partial, headers=request.headers)


def strip_extension(file_name):
    name, extension = os.path.splitext(file_name)
    return name


if __name__ == "__main__":
    app.run()
