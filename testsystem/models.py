from django.db import models

# Create your models here.
IDENTITIES = (
    ('student','学生'),
    ('teacher','教师'),
)

SYMBOLS = (
    ('A','A'),
    ('B','B'),
    ('C','C'),
    ('D','D'),
    ('E','E'),
    ('F','F'),
)

class User(models.Model):
    user_id = models.CharField('用户编号', max_length=20, primary_key=True)
    name = models.CharField('姓名', max_length=10)
    password = models.CharField('密码', max_length=256)
    email = models.EmailField('电子邮箱', unique=True)
    identity = models.CharField('身份', max_length=7, choices=IDENTITIES)

    def __str__(self):
        return '{}({})'.format(self.user_id,self.name)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

class Paper(models.Model):
    paper_text = models.CharField('试卷内容', max_length=30)
    
    def __str__(self):
        return self.paper_text
    
    class Meta:
        verbose_name = '试卷'
        verbose_name_plural = verbose_name

class SC_question(models.Model):
    SC_text = models.CharField('单选题内容', max_length=200)
    SC_solution = models.CharField('单选题答案', max_length=1, choices=SYMBOLS)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)

    def __str__(self):
        return self.SC_text

    class Meta:
        verbose_name = '单选题'
        verbose_name_plural = verbose_name

class MC_question(models.Model):
    MC_text = models.CharField('多选题内容', max_length=200)
    MC_solution = models.CharField('多选题答案', max_length=6)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)

    def __str__(self):
        return self.MC_text

    class Meta:
        verbose_name = '多选题'
        verbose_name_plural = verbose_name

class Blank_question(models.Model):
    blank_text = models.CharField('填空题内容', max_length=200)
    blank_solution = models.CharField('填空题答案', max_length=20)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)

    def __str__(self):
        return self.blank_text

    class Meta:
        verbose_name = '填空题'
        verbose_name_plural = verbose_name

class SC_choice(models.Model):
    choice_symbol = models.CharField('选项符号', max_length=1, choices=SYMBOLS)
    choice_text = models.CharField('选项内容', max_length=200)
    question = models.ForeignKey(SC_question, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = '单选题选项'
        verbose_name_plural = verbose_name

class MC_choice(models.Model):
    choice_symbol = models.CharField('选项符号', max_length=1, choices=SYMBOLS)
    choice_text = models.CharField('选项内容', max_length=200)
    question = models.ForeignKey(MC_question, on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = '多选题选项'
        verbose_name_plural = verbose_name

class Score(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    paper_id = models.ForeignKey(Paper, on_delete=models.CASCADE)
    score = models.DecimalField('分数', max_digits=5,decimal_places=2,default=None)

    def __str__(self):
        return '{}-{}:{}'.format(self.paper_id,self.user_id,self.score)

    class Meta:
        verbose_name = '成绩'
        verbose_name_plural = verbose_name
        ordering = ['paper_id', '-score']
    