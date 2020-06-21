from django.shortcuts import render,redirect, get_object_or_404
from .models import Paper,Score
import hashlib
from . import models
from . import forms
from itertools import chain

# Create your views here.
def index(request):
    if not request.session.get('is_login', None):#未登录则限制访问
        return redirect('/login/')
    paper_list = Paper.objects.order_by('-id')
    score_list = Score.objects.filter(id=(request.user.id))
    #score_list = Score.objects.all()
    for i in score_list:
        print(i.id)
    print(request.user.id)
    # for i in chain(paper_list,score_list):
    #     print(i)
    return render(request, 'testsystem/index.html',{'paper_list': paper_list,'score_list': score_list})

def paper(request, paper_id):
    paper = get_object_or_404(Paper, pk=paper_id)
    return render(request, 'testsystem/paper.html', {'paper':paper})

def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        idcard = request.POST.get('idcard')
        message = '请检查填写的内容！'
        if username.strip() and password and idcard:  # 确保用户名和密码都不为空
            # 用户名字符合法性验证
            # 更多的其它验证.....
            try:
                user = models.User.objects.get(idcard=idcard)
            except:
                message = '用户不存在！'
                return render(request, 'testsystem/login.html', {'message': message})
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_name'] = username
                request.session['user_idcard'] = user.idcard
                print(username,idcard, password)
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'testsystem/login.html', {'message': message})
        else:
            return render(request, 'testsystem/login.html', {'message': message})
    return render(request, 'testsystem/login.html')

def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            idcard = register_form.cleaned_data.get('idcard')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'testsystem/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(idcard=idcard)
                if same_name_user:
                    message = '学号已经存在'
                    return render(request, 'testsystem/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'testsystem/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.idcard = idcard
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'testsystem/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'testsystem/register.html', locals())
    
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")


def hash_code(s,salt='login'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def cal_score(request):
    pass