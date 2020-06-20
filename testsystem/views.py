from django.shortcuts import render
from .models import Paper

# Create your views here.
def index(request):
    paper_list = Paper.objects.order_by('-id')
    


def paper(request):
    pass

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