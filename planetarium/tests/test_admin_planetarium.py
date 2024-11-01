from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from planetarium.models import AstronomyShow, ShowTheme


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


class AdminPlanetariumTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@user.test",
            password="password123"
        )
        self.client.force_authenticate(self.user)

    def test_create_movie(self):
        payload = {
            "title": "new astro show",
            "description": "description"
        }
        res = self.client.post(ASTRONOMY_SHOW_URL, payload)
        astronomy_show = AstronomyShow.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(astronomy_show, key))

    def test_create_astronomy_show_with_show_theme(self):
        show_theme = sample_show_theme()
        show_theme_1 = sample_show_theme(name="New Theme")

        payload = {
            "title": "Stars show",
            "description": "Stars in galaxy",
            "show_themes": [show_theme.id, show_theme_1.id]
        }
        res = self.client.post(ASTRONOMY_SHOW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        astronomy_show = AstronomyShow.objects.get(id=res.data["id"])
        show_themes = astronomy_show.show_themes.all()

        self.assertEqual([show_theme, show_theme_1], list(show_themes))

    def test_delete_astronomy_show_not_allowed(self):
        astronomy_show = sample_astronomy_show()
        res = self.client.delete(detail_url(astronomy_show.id))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

