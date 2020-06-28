from django.test import Client, TestCase


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
