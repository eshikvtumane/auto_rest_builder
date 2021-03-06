import ast
import uuid

from django.test import Client, TestCase

from api.models import TestModel


class GetRecordTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(GetRecordTestCase, cls).setUpClass()
        app_label = 'api'
        model = 'testmodel'
        cls.url = '/api/{}/{}/get/'.format(app_label, model)

    def setUp(self):
        self.test_models = [TestModel.objects.create(
            first_column="test_{}".format(i),
            second_column=i,
        ) for i in range(5)]

    def test_get_filter_success(self):
        first_column_value = self.test_models[0].first_column
        second_column_value = self.test_models[0].second_column

        client = Client()
        response = client.get(
            self.url,
            {
                "first_column": first_column_value,
                "second_column": second_column_value,
            },
        )

        data = ast.literal_eval(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["result"]), 1)

    def test_get_order_by_asc_success(self):
        client = Client()
        response = client.get(
            self.url,
            {
                "order_by": "pk",
            },
        )

        data = ast.literal_eval(response.content.decode('utf-8'))
        ids = [item["id"] for item in data["result"]]
        sorted_ids = sorted(ids)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ids, sorted_ids)

    def test_get_order_by_desc_success(self):
        client = Client()
        response = client.get(
            self.url,
            {
                "order_by": "-pk",
            },
        )

        data = ast.literal_eval(response.content.decode('utf-8'))
        ids = [item["id"] for item in data["result"]]
        sorted_ids = sorted(ids, reverse=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ids, sorted_ids)

    def test_get_limit_success(self):
        limit = 2
        client = Client()
        response = client.get(
            self.url,
            {
                "limit": limit,
            },
        )

        data = ast.literal_eval(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["result"]), limit)


class AddRecordTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(AddRecordTestCase, cls).setUpClass()
        app_label = 'api'
        model = 'testmodel'
        cls.url = '/api/{}/{}/add/'.format(app_label, model)

    def test_add_success(self):
        old_count = TestModel.objects.count()
        client = Client()
        response = client.post(
            self.url,
            {
                "first_column": 'first_column',
                "second_column": 1,
            },
        )
        new_count = TestModel.objects.count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(old_count + 1, new_count)

    def test_add_failed(self):
        client = Client()
        response = client.post(
            self.url,
            {
                "first_column": 'first_column',
                "failed_second_column": 1,
                "failed": 1,
            },
        )

        data = ast.literal_eval(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 500)
        self.assertTrue("Error! Field does not exist:" in data["error"])


class DeleteRecordTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(DeleteRecordTestCase, cls).setUpClass()
        app_label = 'api'
        model = 'testmodel'
        cls.url = '/api/{}/{}/delete/'.format(app_label, model)

    def test_delete_success(self):
        created_obj = TestModel.objects.create(
            first_column=self.random_string(),
            second_column=1,
        )

        url = self.url + str(created_obj.pk)
        client = Client()
        response = client.delete(url)
        data = ast.literal_eval(response.content.decode('utf-8'))

        records_count = TestModel.objects.filter(pk=created_obj.pk).count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["result"], "Object has been delete success.")
        self.assertEqual(records_count, 0)

    def test_update_failed(self):
        url = self.url + '0'
        client = Client()
        response = client.delete(url)

        data = ast.literal_eval(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["error"], "Error! Record does not exist.")

    @staticmethod
    def random_string(self):
        return uuid.uuid4().hex[:6].upper()


class UpdateRecordTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(UpdateRecordTestCase, cls).setUpClass()
        app_label = 'api'
        model = 'testmodel'
        cls.url = '/api/{}/{}/update/'.format(app_label, model)

    def test_update_success(self):
        second_column_init_value = 1
        created_obj = TestModel.objects.create(
            first_column='test',
            second_column=second_column_init_value,
        )

        url = self.url + str(created_obj.pk)
        client = Client()
        response = client.put(
            url,
            {
                "second_column": created_obj.second_column + 1,
            },
        )

        updated_obj = TestModel.objects.get(pk=created_obj.pk)
        data = ast.literal_eval(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue("id" in data["result"])
        self.assertTrue("first_column" in data["result"])
        self.assertTrue("second_column" in data["result"])
        self.assertNotEqual(second_column_init_value, updated_obj.second_column)

    def test_update_failed(self):
        url = self.url + '0'
        client = Client()
        response = client.put(
            url,
            {},
        )

        data = ast.literal_eval(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data["error"], "Error! Record does not exist.")
