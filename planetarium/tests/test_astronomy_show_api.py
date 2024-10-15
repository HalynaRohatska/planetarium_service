from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from planetarium.models import AstronomyShow, ShowTheme
from planetarium.serializers import (
    AstronomyShowListSerializer,
    AstronomyShowDetailSerializer
)


ASTRONOMY_SHOW_URL = reverse("planetarium:astronomyshow-list")


def sample_astronomy_show(**params):
    defaults = {
        "title": "Sample Astronomy Show",
        "description": "Description",
    }
    defaults.update(params)

    return AstronomyShow.objects.create(**defaults)


def sample_show_theme(**params):
    defaults = {
        "name": "Show Theme"
    }
    defaults.update(params)

    return ShowTheme.objects.create(**defaults)


def detail_url(astronomy_show_id):
    return reverse(
        "planetarium:astronomyshow-detail",
        args=[astronomy_show_id]
    )


class UnauthenticatedAstronomyShowApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ASTRONOMY_SHOW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAstronomyShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@email.com",
            password="passwordTest"
        )
        self.client.force_authenticate(self.user)

    def test_astronomy_show_list(self):
        sample_astronomy_show()
        astronomy_show_with_show_theme = sample_astronomy_show()
        show_theme = sample_show_theme()
        astronomy_show_with_show_theme.show_themes.add(show_theme)

        res = self.client.get(ASTRONOMY_SHOW_URL)
        astronomy_shows = AstronomyShow.objects.all()
        serializer = AstronomyShowListSerializer(astronomy_shows, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_astronomy_show_by_title(self):
        sample_astronomy_show()
        astronomy_show_1 = sample_astronomy_show(
            title="Astronomy Show",
            description="New Astronomy Show"
        )
        astronomy_shows = AstronomyShow.objects.all()
        serializer = AstronomyShowListSerializer(astronomy_shows, many=True)

        res = self.client.get(
            ASTRONOMY_SHOW_URL,
            {"title": "Astronomy Show"}
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        res = self.client.get(
            ASTRONOMY_SHOW_URL,
            {"title": "Show"}
        )
        self.assertEqual(res.data, serializer.data)

    def test_filter_astronomy_show_by_show_theme(self):
        astronomy_show_1 = sample_astronomy_show()
        astronomy_show_2 = sample_astronomy_show(
            title="New Astronomy Show",
            description="new astronomy show"
        )
        astronomy_show_3 = sample_astronomy_show(
            title="Test Astronomy Show",
            description="test astronomy show"
        )

        show_theme_1 = sample_show_theme()
        show_theme_2 = sample_show_theme(
            name="Test Theme"
        )

        astronomy_show_2.show_themes.add(show_theme_1)
        astronomy_show_3.show_themes.add(show_theme_1, show_theme_2)

        res = self.client.get(
            ASTRONOMY_SHOW_URL,
            {"show_themes": f"{show_theme_1.id},{show_theme_2.id}"}
        )

        filtered_shows = AstronomyShow.objects.filter(show_themes__in=[show_theme_1, show_theme_2]).distinct()
        serializer = AstronomyShowListSerializer(filtered_shows, many=True)
        serializer_without_theme = AstronomyShowListSerializer(astronomy_show_1)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertCountEqual(res.data, serializer.data)
        self.assertEqual(list(res.data), list(serializer.data))
        self.assertNotIn(list(res.data), serializer_without_theme)

    def test_retrieve_astronomy_show_detail(self):
        astronomy_show = sample_astronomy_show()
        astronomy_show.show_themes.add(sample_show_theme())

        res = self.client.get(detail_url(astronomy_show.id))
        serializer = AstronomyShowDetailSerializer(astronomy_show)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_astronomy_show_forbidden(self):
        payload = {
            "title": "astro show",
            "description": "new show description"
        }
        res = self.client.post(ASTRONOMY_SHOW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
