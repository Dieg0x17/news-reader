from django.test import TestCase
from django.urls import reverse
from rest_framework.reverse import reverse as drf_reverse


class RatesTests(TestCase):
    fixtures = ["articles.json", ]

    def setUp(self):
        pass

    def test_index_ok(self):
        url = reverse('index')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_feed_ok(self):
        url = reverse('rss')
        response = self.client.get(url)
        assert response.status_code == 200

        url = reverse('atom')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_articles_ok(self):
        url = drf_reverse('articles-list')
        # None
        data = {
            'page': 1,
        }
        response = self.client.get(url, data=data)
        assert response.status_code == 200

    def test_article_detail_ok(self):
        url = drf_reverse('articles-detail', ('neurons',))
        response = self.client.get(url,)
        assert response.status_code == 200

    def test_filters_ok(self):
        url = drf_reverse('articles-list')

        # search
        data = {
            'search': "neurons",
        }
        response = self.client.get(url, data=data)
        assert response.status_code == 200
        assert len(response.data['results']) == 1

        # dates
        data = {
            'start_date': '2022-04-02',
        }
        response = self.client.get(url, data=data)
        assert response.status_code == 200
        assert len(response.data['results']) == 1

        data = {
            'end_date': '2022-04-02',
        }
        response = self.client.get(url, data=data)
        assert response.status_code == 200
        assert len(response.data['results']) == 1

    def test_order_ok(self):
        url = drf_reverse('articles-list')

        data = {
            'order': 'recent',
        }
        response = self.client.get(url, data=data)
        assert response.status_code == 200
        assert response.data['results'][0]['created_on'] == '2022-04-02T11:06:11.111000Z'

        data = {
            'order': 'old',
        }
        response = self.client.get(url, data=data)
        assert response.status_code == 200
        assert response.data['results'][0]['created_on'] == '2022-04-01T21:17:01.763000Z'
