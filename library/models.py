from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(verbose_name="タイトル", max_length=50)
    isbn = models.CharField(verbose_name="ISBN", max_length=50)
    author = models.CharField(verbose_name="著者", max_length=20)
    publicationday = models.DateField(verbose_name="出版日")
    content = models.TextField(verbose_name="内容")
    image = models.ImageField(verbose_name="表紙画像", upload_to='article_images/', blank=True, null=True)

    
    def get_absolute_url(self):
        return reverse("library:detail", kwargs={"pk": self.pk})
    
    def is_available(self):
        """在庫があるかどうかを判定"""
        return not self.loan_set.filter(return_date__isnull=True).exists()
    
    def is_on_loan(self):
        """貸出中かどうかを判定"""
        return self.loan_set.filter(return_date__isnull=True).exists()
    
    def get_status_display(self):
        """貸出状況を文字列で返す"""
        if self.is_on_loan():
            return "貸出中"
        else:
            return "在庫あり"
    
    def get_current_loan(self):
        """現在の貸出記録を取得（貸出中の場合）"""
        return self.loan_set.filter(return_date__isnull=True).first()
    
    def __str__(self):
        return  f"{self.title} by {self.author}"
    
class Loan(models.Model):
    article = models.ForeignKey(Article, verbose_name="借りた本の記録", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="本を借りた人", on_delete=models.CASCADE)
    borrow_date = models.DateField(verbose_name="貸出日", default=timezone.now)
    due_date = models.DateField(verbose_name="返却期限日")
    return_date = models.DateField(verbose_name="返却日", blank=True, null=True)

    def is_overdue(self):
        return self.return_date is None and timezone.now().date() > self.due_date

    def __str__(self):
        return f"{self.user.username} borrowed '{self.article.title}'"

class Review(models.Model):
    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]
    
    article = models.ForeignKey(Article, verbose_name="レビュー対象の本", on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, verbose_name="レビュー投稿者", on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name="評価", choices=RATING_CHOICES)
    comment = models.TextField(verbose_name="コメント", max_length=500)
    created_at = models.DateTimeField(verbose_name="投稿日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)
    
    class Meta:
        unique_together = ('article', 'user')  
        ordering = ['-created_at']
    
    def get_rating_display_stars(self):
        """評価を星で表示"""
        return '★' * self.rating + '☆' * (5 - self.rating)
    
    def __str__(self):
        return f"{self.user.username}のレビュー: {self.article.title} ({self.rating}/5)"

