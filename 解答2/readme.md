## 1.执行mysql操作

执行blog.sql后，数据库新建一个**blog**库，新增两张表分别为**user_info**用户表和**blog_info**博客表, **user_info**表会生成2个账号如下：

```
管理员账号
账号：admin 密码：admin uid: 1

普通用户账号
账号：generel 密码：generel uid: 2
```



## 2. 测试协议

1.获取账号信息协议

```python
http://127.0.0.1:5000/get_user_uid
"""
method: (post)

:param account: 账号
:param password: 密码
:return code: 0(成功)， uid: uid
"""

```

2.获取文章信息

```python
http://127.0.0.1:5000/list_article 
"""
method: (post)

:param aid: 文章id
:return code: 0(成功)，articles: [[id,head,content,article_url,edit_time], ...]
"""
```



3.添加文章

```python
http://127.0.0.1:5000/add_article
"""
method: (post)

:param uid: 用户id
:param head: 标题
:param content: 内容
:return code: 0(成功), aid: 1(新增的文章id)
"""
```



4.编辑文章内容

```python
http://127.0.0.1:5000/edit_article
"""
method: (post)

:param aid: 文章id
:param uid: 用户id
:param head: 标题(如果不传则不做修改，标题内容至少传其1)
:param content: 内容(如果不传则不做修改，标题内容至少传其1)
:return code: 0(成功)
"""
```

5.删除文章

```python
http://127.0.0.1:5000/del_article
"""
method: (post)

:param aid: 文章id
:param uid: 用户id
:return code: 0(成功)
"""
```

