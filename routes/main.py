"""
 @Author: 西琳
 @FileName: main.py
 @DateTime: 2024/9/18 下午7:56
 @SoftWare: PyCharm
"""
import markdown2
from flask import Blueprint, render_template

from models.db import fetch_multiple_records

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


import markdown2

import markdown2

def blog():
    posts = fetch_multiple_records('SELECT * FROM posts')
    for post in posts:
        # 启用扩展功能
        post['content'] = markdown2.markdown(post['content'], extras=[
            "tables",               # 支持表格
            "fenced-code-blocks",   # 支持围栏代码块
            "footnotes",            # 支持脚注
            "toc",                  # 支持目录
            "cuddled-lists"         # 支持定义型列表
        ])
    return render_template('blog.html', posts=posts)


@main_bp.route('/about')
def about():
    return render_template('about.html')


@main_bp.route('/experiments')
def experiments():
    return render_template('experiments.html')

@main_bp.route('/search')
def search():
    return render_template('search.html')