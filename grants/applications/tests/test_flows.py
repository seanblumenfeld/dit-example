from django.contrib.auth import get_user_model
from django.test import TestCase
from viewflow.models import Process


class TestApplicationFlow(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.uri = '/workflow/applications/application/'

    def setUp(self):
        user_model = get_user_model()
        admin = user_model.objects.create_superuser('admin', 'admin@test.com', 'pwd')
        self.client.login(username=admin.username, password='pwd')

    def test_happy_path(self):
        response = self.client.post(
            self.uri + 'start/',
            {
                'full_name': 'Joe Stone',
                'email': 'joe@test.com',
                'proposal': 'My amazing idea.',
                'requested_amount': 123.45,
                '_viewflow_activation-started': '2020-01-01'
            }
        )
        self.assertEqual(response.status_code, 200, msg=response.content.decode())

        response = self.client.post(
            self.uri + '/1/legal_approval/2/'
        )
        self.assertEqual(response.status_code, 200, msg=response.content.decode())

        response = self.client.post(
            self.uri + '/1/finance_approval/3/'
        )
        self.assertEqual(response.status_code, 200, msg=response.content.decode())

        process = Process.objects.get()

        self.assertEquals('DONE', process.status)
        self.assertEquals(4, process.task_set.count())

    def test_bad(self):
        # TODO
        pass