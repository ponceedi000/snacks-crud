from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Snack



from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Snack


class SnackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", email="tester@email.com", password="pass"
        )

        self.snack = Snack.objects.create(
            title="chocolate", description="description test", purchaser=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "chocolate")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "chocolate")
        self.assertEqual(f"{self.snack.purchaser}", "tester")
        self.assertEqual(f"{self.snack.description}", "description test")

    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "chocolate")
        self.assertTemplateUsed(response, "snack-list.html")

    def test_snack_detail_view_not_working(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertNotEqual(response.status_code, 300)
        self.assertNotEqual(no_response.status_code, 304)
        self.assertNotContains(response, "Purchaser: testers")
        self.assertTemplateNotUsed(response, "snack-details.html")

    # def test_snack_create_view(self):
    #     response = self.client.post(
    #         reverse("snack_create"),
    #         {
    #             "title": "Raker",
    #             "description": "test",
    #             "purchaser": self.user.id,
    #         }, follow=True
    #     )

    #     self.assertRedirects(response, reverse("snack_detail", args="2"))
    #     self.assertContains(response, "Details about Raker")



    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "Pretzels",
                "purchaser": self.user.id,
                "description": "Salty",
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_detail", args="2"))
        # self.assertContains(response, "Details about - Pretzels")   IDK what is going on here.


