from django.shortcuts import render,redirect, get_object_or_404
from .models import Paper,Score
import hashlib
from . import models
from . import forms
from itertools import chain
import json
from django.http import FileResponse

# Create your views here.
def index(request):
    if not request.session.get('is_login', None):#未登录则限制访问
        return redirect('/login/')
    paper_list = Paper.objects.order_by('-id')
    paper_count = Paper.objects.all().count()
    score_list = Score.objects.filter(user_id=request.session['user_id'])
    paper_finish = Score.objects.filter(user_id=request.session['user_id']).values_list('paper_id__paper_text','paper_id__id','paper_id__pub_date')
    paper_nofinish = []
    for i in paper_list:
        flag = False
        for j in paper_finish:
            if i.id == j[1]:
                flag = True
        if not flag:
            paper_nofinish.append(i)
    return render(request, 'testsystem/index.html',{'paper_nofinish':paper_nofinish,'paper_count':paper_count,'score_list': score_list})

def paper(request, paper_id):
    paper = get_object_or_404(Paper, pk=paper_id)
    sc_value_list = [i.value for i in paper.sc_question_set.all()]
    sc_value = value_list_sum(sc_value_list)
    mc_value_list = [i.value for i in paper.mc_question_set.all()]
    mc_value = value_list_sum(mc_value_list)
    blank_value_list = [i.value for i in paper.blank_question_set.all()]
    blank_value = value_list_sum(blank_value_list)
    if models.Score.objects.filter(user_id=request.session['user_id'], paper_id=paper.id):
        passed = True
        answer = models.Score.objects.get(user_id=request.session['user_id'], paper_id=paper.id).answer
        answer_timing = str(models.Score.objects.get(user_id=request.session['user_id'], paper_id=paper.id).time)
        score = models.Score.objects.get(user_id=request.session['user_id'], paper_id=paper.id).score
        return render(request, 'testsystem/paper.html', locals())
    else:
        return render(request, 'testsystem/paper.html', locals())

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
            if user.password == hash_code(password) and username == user.name:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = username
                request.session['user_idcard'] = user.idcard
                print(username,idcard, password)
                return redirect('/index/')
            else:
                message = '用户名或密码不正确！'
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

def forgetpwd(request):
    if request.method == "POST":
        idcard = request.POST.get('idcard')
        pwd = request.POST.get('pwd')
        newpwd = request.POST.get('newpwd1')
        newpwd2 = request.POST.get('newpwd2')
        message = '请检查填写的内容！'
        if pwd and idcard:  # 确保学号和旧密码都不为空
            # 用户名字符合法性验证
            # 更多的其它验证.....
            try:
                user = models.User.objects.get(idcard=idcard)
            except:
                message = '用户不存在！'
                return render(request, 'testsystem/forgetpwd.html', {'message': message})
            if user.password == hash_code(pwd):
                if newpwd == newpwd2:
                    user.password = hash_code(newpwd)
                    user.save()
                    print('aaaa')
                    return redirect('/login/')
                else:
                    message = '两次输入的密码不同！'
                    return render(request, 'testsystem/forgetpwd.html', {'message': message})    
            else:
                message = '密码不正确！'
                return render(request, 'testsystem/forgetpwd.html', {'message': message})
        else:
            return render(request, 'testsystem/forgetpwd.html', {'message': message})
    return render(request, 'testsystem/forgetpwd.html')

def hash_code(s,salt='login'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def value_list_sum(value_list):
    value_sum = 0
    for value in value_list:
        value_sum += value
    return int(value_sum) if '.0' in str(value_sum) else value_sum

def cal_score(request, paper_id):
    paper = get_object_or_404(Paper, pk=paper_id)
    score = 0
    postdata = {}
    for i in paper.sc_question_set.all():
        postdata[str(i)] = request.POST.get(str(i))
        if i.SC_solution == request.POST.get(str(i)):
            score += i.value
    for i in paper.mc_question_set.all():
        solv_list = list(i.MC_solution)
        post_list = request.POST.getlist(str(i))
        postdata[str(i)] = post_list
        if solv_list == post_list:
            score += i.value
    for i in paper.blank_question_set.all():
        postdata[str(i)] = request.POST.get(str(i))
        if i.blank_solution == request.POST.get(str(i)):
            score += i.value
    new_score = Score()
    new_score.paper_id_id = paper.id
    new_score.user_id_id = request.session['user_id']
    new_score.score = score
    new_score.answer = json.dumps(postdata, separators=(',',':'))
    new_score.time = request.POST.get('timing').replace('PT','').replace('H',':').replace('M',':').replace('S','')
    new_score.save()
    return redirect('/{}/'.format(paper_id))

def download(request):
  file=open('testsystem/download/STU-question_bank_template.xlsx','rb')
  response =FileResponse(file)
  response['Content-Type']='application/octet-stream'
  response['Content-Disposition']='attachment;filename="STU-question_bank_template.xlsx"'
  return response