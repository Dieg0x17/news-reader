from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from parler.models import TranslatableModel, TranslatedFields
from bs4 import BeautifulSoup
from django.urls import reverse


class Article(TranslatableModel):
    image = models.ImageField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")

    translations = TranslatedFields(
        title=models.CharField(max_length=150, unique=True),
        slug=models.SlugField(max_length=150, unique=True),
        description=RichTextUploadingField()
    )
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    draft = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    @property
    def clean_description(self):
        return BeautifulSoup(self.description, "lxml").text

    def get_absolute_url(self):
        return reverse("index")+"?slug="+self.slug
