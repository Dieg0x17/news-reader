from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Article
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import get_language, gettext_lazy as _


class RSS(Feed):
    title = _("News")
    link = ""
    description = _("Latest articles")

    def items(self):
        language = get_language()
        return Article.objects.translated(language).filter(draft=False, )

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.clean_description, 20)


class Atom(RSS):
    feed_type = Atom1Feed
