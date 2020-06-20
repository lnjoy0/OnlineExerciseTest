from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_header='在线习题测试系统后台'
admin.site.site_title='在线习题测试系统'

class SCInLine(admin.TabularInline):
    model = SC_question
    extra = 2

class MCInLine(admin.TabularInline):
    model = MC_question
    extra = 2

class BlankInLine(admin.TabularInline):
    model = Blank_question
    extra = 2

class PaperAdmin(admin.ModelAdmin):
    inlines = [SCInLine]+[MCInLine]+[BlankInLine]
    list_display = ('paper_text', 'pub_date')
    list_display_links = ('paper_text','pub_date')
    search_fields = ['paper_text']
    list_filter = ['pub_date']

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('score', 'user_id', 'paper_id')
    list_display_links = ('score', 'user_id', 'paper_id')

admin.site.register(Paper, PaperAdmin)
admin.site.register(SC_choice)
admin.site.register(MC_choice)
admin.site.register(Score, ScoreAdmin)
admin.site.register(User)