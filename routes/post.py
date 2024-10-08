"""
 @Author: 西琳
 @FileName: post.py
 @DateTime: 2024/9/18 下午8:01
 @SoftWare: PyCharm
"""
import random

import pymysql
import markdown
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify, Blueprint

from models.db import get_db_conn, fetch_single_record, fetch_multiple_records,get_post_from_db

post_bp = Blueprint('post', __name__)


@post_bp.route('/get_random_image')
def get_random_image():
    conn = get_db_conn()
    if conn:
        with conn.cursor() as cursor:
            i = random.randint(0, 21)  # 根据数据库中的 ID 范围
            cursor.execute('SELECT cover , name FROM taluo WHERE id = %s', (i,))
            result = cursor.fetchone()
        conn.close()
        if result:
            return jsonify(filename=result['cover'], description=result['name'])

    return jsonify(filename='image/Tarot_index.png', description=" ")


@post_bp.route('/posts/<int:post_id>')
def post(post_id):
    post = fetch_single_record('SELECT * FROM posts WHERE id = %s', (post_id,))
    if post:
        post['content'] = markdown.markdown(post['content'])
        return render_template('post.html', post=post)
    else:
        flash('文章未找到', 'error')
        return redirect(url_for('main.index'))


@post_bp.route('/category/<int:type_id>')
def category(type_id):
    posts = fetch_multiple_records('SELECT * FROM posts WHERE type_id = %s', (type_id,))
    return render_template('category.html', posts=posts, type_id=type_id)


@post_bp.route('/posts/new', methods=('GET', 'POST'))
def new():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        type_id = request.form.get('type_id')

        if not title:
            flash('标题不能为空', 'error')
        elif not content:
            flash('内容不能为空', 'error')
        elif not type_id:
            flash('请选择一个分区', 'error')
        else:
            conn = get_db_conn()
            if conn:
                with conn.cursor() as cursor:
                    cursor.execute('INSERT INTO posts (title, content, type_id) VALUES (%s, %s, %s)',
                                   (title, content, type_id))
                    conn.commit()
                conn.close()
                flash('提交成功！', 'success')
                return render_template('new.html')
            else:
                flash('提交失败，数据库连接错误', 'error')
    return render_template('new.html')


@post_bp.route('/posts/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = fetch_single_record('SELECT * FROM posts WHERE id = %s', (id,))
    if post:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            if not title:
                flash('标题不能为空', 'error')
            else:
                conn = get_db_conn()
                if conn:
                    with conn.cursor() as cursor:
                        cursor.execute('UPDATE posts SET title = %s, content = %s WHERE id = %s', (title, content, id))
                        conn.commit()
                    conn.close()
                    flash('更新成功！', 'success')
                    return redirect(url_for('post.post', post_id=id))
                else:
                    flash('更新失败，数据库连接错误', 'error')
        return render_template('edit.html', post=post)
    else:
        flash('文章未找到', 'error')
        return redirect(url_for('main.index'))


@post_bp.route('/posts/<int:id>/delete', methods=('POST',))
def delete(id):
    post = fetch_single_record('select * from posts where id=%s', (id,))
    if post:
        conn = get_db_conn()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute("delete from posts where id =%s", (id,))
                conn.commit()
            conn.close()
            flash(f'"{post["title"]}"删除成功！', 'successes')
        else:
            flash('删除失败，数据库连接失败', 'error')
    else:
        flash('文章未找到', 'error')
    return render_template('blog.html')


@post_bp.route('/every_search')
def every_search():
    search_term = request.args.get('searchTerm')  # 从查询参数中获取搜索词
    if not search_term:
        return jsonify(message='没有提供搜索关键词'), 400  # 如果没有提供搜索关键词，返回错误信息

    conn = get_db_conn()
    if conn:
        with conn.cursor() as cursor:
            # 执行SQL查询，获取匹配的标题和部分正文
            query = "SELECT id, title, SUBSTRING(content, 1, 100) AS snippet, created FROM posts WHERE LOWER(title) LIKE %s"
            cursor.execute(query, ('%' + search_term.lower() + '%',))
            results = cursor.fetchall()

        conn.close()

        if results:
            # 返回匹配的标题和正文片段
            posts = [{'id': row['id'], 'title': row['title'], 'snippet': row['snippet'], 'created': row['created']} for
                     row in results]
            return jsonify(posts=posts)

    return jsonify(message='未找到数据或数据库连接失败'), 500


@post_bp.route('/post/<int:post_id>')
def get_post(post_id):
    # 从数据库中获取该ID的文章
    post = get_post_from_db(post_id)  # 这是一个假设的函数，用于获取数据库内容
    if not post:
        return "文章未找到", 404
    return render_template('post.html', post=post)
