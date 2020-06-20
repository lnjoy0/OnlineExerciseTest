from django.shortcuts import render, get_object_or_404
from .models import Paper

# Create your views here.
def index(request):
    paper_list = Paper.objects.order_by('-id')
    return render(request, 'testsystem/index.html',{'paper_list': paper_list})

def paper(request, paper_id):
    paper = get_object_or_404(Paper, pk=paper_id)
    return render(request, 'testsystem/paper.html', {'paper':paper})

def login(request):
    pass

def register(request):
    pass

def logout(request):
    pass

def hash_code(s,salt='login'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def cal_score(request):
    pass