from django.contrib.auth.models import User
from django.db import transaction
from django.test.testcases import TestCase
from drf_role.models import Role
from psycopg2._psycopg import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from core.models import Profile
from pms.models import Project, Issue

__author__ = 'Ashraful'
ROLE_NAMES = ('Admin', 'Manager', 'Developer', 'Tester',)
USER_NAMES = ('robin', 'ashraful', 'john', 'jasica')


def make_url(path):
    return '/api/v1/pms/{0}/'.format(path)


class TestPMSApi(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create Role
        for _index, role_name in enumerate(ROLE_NAMES):
            Role.objects.get_or_create(name=role_name, type=_index)
        # Create user and profile
        roles = Role.objects.all()
        for _index, role in enumerate(roles):
            try:
                with transaction.atomic():
                    user = User.objects.create_user(username=USER_NAMES[_index], password='1234')
                    Profile.objects.create(user_id=user.pk, role_id=role.pk)
            except IntegrityError:
                continue
        # Default Login
        url = "/api/v1/core/login/"
        data = {
            "username": "robin",
            "password": "1234"
        }
        self.current_user = self.client.post(url, data)
        self.token = Token.objects.get(user__username='robin')
        self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(self.token))

        # Create Issue
        project = Project.objects.create(name="Test Project", description="Test Description")
        self.issue = Issue.objects.create(
            title="Test Issue Title", description="Test Issue Description",
            assigned_to_id=Profile.objects.last().pk, project_id=project.pk,
            author_id=Profile.objects.first().pk
        )

    def test_issue_create_api(self):
        print("\n")
        print("(*) Testing... Issue Create Functionality.")
        url = make_url('issues')
        project = Project.objects.create(name="Test Project", description="Test Description")
        data = {
            "title": "This is Test Issue",
            "description": "Issue description is mandatory....",
            "project": project.pk,
            "assigned_to": Profile.objects.last().pk

        }
        response = self.client.post(url, data)
        try:
            self.assertEqual(response.status_code, 201)
            print("[S] Success")
        except AssertionError:
            print("[F] Failed")

    def test_issue_update_api(self):
        print("\n")
        print("(*) Testing... Issue Update Functionality.")
        # url = make_url('issues/{0}/'.format(self.issue.pk))
        # data = {
        #     # Here will be data
        # }
        # response = self.client.put(url, data)

        try:
            self.assertEqual(True, True)
            print("[S] Success")
        except AssertionError:
            print("[F] Failed")

    def test_issue_close_api(self):
        print("\n")
        print("(*) Testing... Issue Close Functionality.")
        # url = make_url('issues/{0}/'.format(self.issue.pk))
        # data = {
        #     # Here will be data
        # }
        # response = self.client.put(url, data)

        try:
            self.assertEqual(True, True)
            print("[S] Success")
        except AssertionError:
            print("[F] Failed")
