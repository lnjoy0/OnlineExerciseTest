# OnlineExerciseTest
使用Django开发简单的在线习题测试系统，系统角色为学生和教师，习题类型有单选题、多选题、填空题，教师可在线录入或以文件方式上传试题，系统自动判题并录入成绩，教师直接在django后台操作。

需要安装django和simpleui:

	pip install django
	pip install django-simpleui

下载后需要重新迁移数据库：

	py manage.py makemigrations
	py manage.py migrate

启动：

	py manage.py runserver 80

登陆后台：

	访问 /admin

创建教师账户：

	py manage.py createsuperuser

张老师的python课作业
