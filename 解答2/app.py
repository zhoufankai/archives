# coding:utf8
from flask import Flask, request, g
import MySQLdb
import json
import time


"""
1.系统有两种角色:普通用户，管理员
2.每种角色有不同的权限
    普通用户：可以查看所有人的文章，智能编辑、删除自己写的文章
    管理员：管理员拥有普通用户的权限，并且拥有删除其它用户文章的权限
3.前端通过restful api与后台交互

管理员账号
account: admin
password: admin
普通用户
account: general
password: general

todo list:
1：账号认证系统
2：完善逻辑判断

"""

HOST = 'localhost'
USER = 'root'
PASSWD = 'hack10086'
DB = 'myblog'


ROLE_ADMIN = 1
ROLE_GENERAL = 2
ARTICLE_STATUS_DEL = 1
ARTICLE_STATUS_NOMAL = 0


app = Flask(__name__)
app.debug = True


@app.before_request
def before_request():
    g.db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DB)
    g.cursor = g.db.cursor()


@app.after_request
def after_request(response):
    g.db.commit()
    g.cursor.close()
    g.db.close()
    g.cursor = None
    g.db = None

    return response


def isRightEnough(uid, aid=0):
    """
    判断是否有足够权限
    :param uid: 用户id
    :param aid: 文章id
    :return: True(权限足够)，False(权限不足)
    """
    if aid:
        # 文章id满足的时候
        sql = "SELECT u.`uid` FROM `user_info` u LEFT JOIN `blog_info` b ON u.`uid` = b.`uid` WHERE b.`id`=%s LIMIT 1"
        g.cursor.execute(sql, (aid,))
        article = g.cursor.fetchone()
        if article[0] == uid:
            return True

    sql = "SELECT `role` FROM `user_info` WHERE `uid`=%s"
    g.cursor.execute(sql, (uid,))
    author = g.cursor.fetchone()
    author_role = author[0]
    if author_role == ROLE_ADMIN:
        return True
    else:
        return False


@app.route('/list_article', methods=["POST"])
def list_article():
    """
    :param aid: 文章id
    :return articles: [[id,head,content,article_url,edit_time], ...]
    """
    aid = request.form.get('aid', 0, type=int)
    # uid = request.form.get('uid', 0, type=int)

    if aid:
        sql = "SELECT `id`, `head`, `content`, `article_url`, `edit_time` FROM blog_info WHERE status=%s AND id=%s"
        g.cursor.execute(sql, (ARTICLE_STATUS_NOMAL, aid,))
    else:

        sql = "SELECT `id`, `head`, `content`, `article_url`, `edit_time` FROM blog_info WHERE status=%s"
        g.cursor.execute(sql, (ARTICLE_STATUS_NOMAL,))
    rows = g.cursor.fetchall()
    return json.dumps(dict(code=0, articles=rows))
    

@app.route('/add_article', methods=["POST"])
def add_article():
    """
    :param uid: 用户id
    :param head: 标题
    :param content: 内容
    :return code: 0(成功)
    """
    uid = request.form.get('uid', 0, type=int)
    head = request.form.get('head', '', type=str)
    content = request.form.get('content', '', type=str)

    if not head:
        return json.dumps(dict(code=-1))

    article_url = "myurl"
    ct = int(time.time())
    sql = "INSERT INTO blog_info (`uid`, `head`, `content`, `article_url`, `edit_time`) VALUES (%s, %s, %s, %s, %s)"
    g.cursor.execute(sql, (uid, head, content, article_url, ct,))

    sql = "SELECT LAST_INSERT_ID()"
    g.cursor.execute(sql)
    last_aid = g.cursor.fetchone()

    return json.dumps(dict(code=0, aid=last_aid[0]))


@app.route('/edit_article', methods=["POST"])
def edit_article():
    """
    编辑文章内容
    :param aid: 文章id
    :param uid: 用户id
    :param head: 标题(如果不传则不做修改，标题内容至少传其1)
    :param content: 内容(如果不传则不做修改，标题内容至少传其1)
    :return code: 0(成功)
    """
    aid = request.form.get('aid', 0, type=int)
    uid = request.form.get('uid', 0, type=int)
    head = request.form.get('head', '', type=str)
    content = request.form.get('content', '', type=str)

    if not isRightEnough(uid, aid):
        return json.dumps(dict(code=1))

    ct = int(time.time())
    if not head and not content:
        return json.dumps(dict(code=3))

    if not head and content:
        sql = "UPDATE blog_info SET `content`=%s, `edit_time`=%s WHERE id=%s"
        rowcount = g.cursor.execute(sql, (content, ct, aid,))
    elif head and not content:
        sql = "UPDATE blog_info SET `content`=%s, `edit_time`=%s WHERE id=%s"
        rowcount = g.cursor.execute(sql, (head, ct, aid,))
    else:
        sql = "UPDATE blog_info SET `head`=%s, `content`=%s, `edit_time`=%s WHERE id=%s"
        rowcount = g.cursor.execute(sql, (head, content, ct, aid,))
    if not rowcount:
        json.dumps(dict(code=2))

    return json.dumps(dict(code=0))


@app.route('/del_article', methods=["POST"])
def del_article():
    """
    删除文章
    :param aid: 文章id
    :param uid: 用户id
    :return code: 0(成功)
    """
    aid = request.form.get('aid', 0, type=int)
    uid = request.form.get('uid', 0, type=int)

    if not isRightEnough(uid, aid):
        return json.dumps(dict(code=1))

    sql = "UPDATE blog_info SET status=%s WHERE id=%s"
    rowcount = g.cursor.execute(sql, (ARTICLE_STATUS_DEL, aid,))
    if not rowcount:
        # 文章已经删除
        return json.dumps(dict(code=2))
    return json.dumps(dict(code=0))


@app.route('/get_user_uid', methods=["POST"])
def get_user_uid():
    """
    通过账号密码获取uid
    :param account: 账号
    :param password: 密码
    :return {uid: uid}
    """
    account = request.form.get('account', "", type=str)
    password = request.form.get('password', "", type=str)

    sql = "SELECT uid, password FROM user_info WHERE account=%s"
    g.cursor.execute(sql, (account,))
    row = g.cursor.fetchone()
    if not row:
        return json.dumps(dict(code=-1))

    if row[1] != password:
        return json.dumps(dict(code=-2))

    return json.dumps(dict(code=0, uid=row[0]))


if __name__ == '__main__':
    app.run()