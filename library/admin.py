from django.contrib import admin
from .models import Article, Loan # models.pyからArticleクラスをインポート

admin.site.register(Article)
admin.site.register(Loan)  

# Register your models here.
