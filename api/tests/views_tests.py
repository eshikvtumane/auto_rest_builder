from django.test import Client, TestCase

from api.models import TestModel


class AddRecordTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        app_label = 'api'
        model = 'testmodel'
        cls.url = '/api/{}/{}/add'.format(app_label, model)

    def test_add_success(self):
        client = Client()
        response = client.post(
            self.url,
            {
                "first_column": 'first_column',
                "second_column": 1,
            },
        )

        self.assertEqual(response.status_code, 301)


class DeleteRecordTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        app_label = 'api'
        model = 'testmodel'
        cls.url = '/api/{}/{}/delete/'.format(app_label, model)

    def test_delete_success(self):
        created_obj = TestModel.objects.create(
            first_column='test',
            second_column=1,
        )

        url = self.url + created_obj.pk
        client = Client()
        response = client.delete(url)

        self.assertEqual(response.status_code, 301)


class UpdateRecordTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        app_label = 'api'
        model = 'testmodel'
        cls.url = '/api/{}/{}/update/'.format(app_label, model)

    def test_update_success(self):
        created_obj = TestModel.objects.create(
            first_column='test',
            second_column=1,
        )

        url = self.url + created_obj.pk
        client = Client()
        response = client.put(
            url,
            {
                "second_column": created_obj + 1,
            },
        )

        updated_obj = TestModel.objects.get(pk=created_obj.pk)

        self.assertNotEqual(created_obj.pk, updated_obj.pk)
