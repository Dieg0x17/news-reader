from django.contrib import admin
# from django import forms
# from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Article
from parler.admin import TranslatableAdmin


# class ArticleAdminForm(forms.ModelForm):
#     description = forms.CharField(widget=CKEditorUploadingWidget())
#
#     class Meta:
#         model = Article
#         fields = ['image', 'title', 'slug', 'author', 'description', 'draft']


class ArticleAdmin(TranslatableAdmin):
    # form = ArticleAdminForm
    list_display = (
        "id", "title", "author", "created_on", "draft"
    )
    list_display_links = ("id",)
    search_fields = (
        "title",
        "slug",
        "description",
        "author__username",
        "author__firstname",
        "author__lastname",
        "author__email",
    )
    list_filter = ("draft", "updated_on", "created_on")


admin.site.register(Article, ArticleAdmin)
