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

    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField('姓名',max_length=128)
    idcard = models.CharField('学号',max_length=128,primary_key=True)
    password = models.CharField('密码',max_length=256)
    email = models.EmailField('邮箱',unique=True)
    sex = models.CharField('性别',max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"

class Paper(models.Model):
    paper_text = models.CharField('试卷标题', max_length=30)
    pub_date = models.DateTimeField('发布日期')

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
        return '{}-{}'.format(self.paper_id,self.user_id)

    class Meta:
        verbose_name = '成绩'
        verbose_name_plural = verbose_name
        ordering = ['paper_id', '-score']

