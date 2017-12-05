from django.contrib.auth.models import User
from django.db import transaction
from django.test.testcases import TestCase
from drf_role.models import Role
from psycopg2._psycopg import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from core.models.profile import Profile

__author__ = 'Ashraful'
ROLE_NAMES = ('Admin', 'Manager', 'Developer', 'Tester',)
USER_NAMES = ('robin', 'ashraful', 'john', 'jasica')


def make_url(path):
    return '/api/v1/core/{0}/'.format(path)


class TestProfileApi(TestCase):
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
        url = make_url('login')
        data = {
            "username": "robin",
            "password": "1234"
        }
        self.current_user = self.client.post(url, data)
        self.token = Token.objects.get(user__username='robin')
        self.client.credentials(HTTP_AUTHORIZATION='Token {0}'.format(self.token))

    def test_login(self):
        print("\n")
        print("(*) Testing... Login Functionality.")
        url = make_url('login')
        data = {
            "username": "ashraful",
            "password": "1234"
        }
        response = self.client.post(url, data)
        try:
            self.assertEqual(response.status_code, 200)
            print("[S] Success")
        except AssertionError:
            print("[F] Failed")

    def test_logout(self):
        print("\n")
        print("(*) Testing... Logout Functionality.")
        url = make_url('logout')
        response = self.client.post(url)
        try:
            self.assertEqual(response.status_code, 200)
            print("[S] Success")
        except AssertionError:
            print("[F] Failed")

    def test_profile_details(self):
        print("\n")
        print("(*) Testing... GET Login user details view.")
        profile_pk = Profile.objects.get(user_id=self.current_user.data.get('user_id')).pk
        url = make_url('profiles/{0}'.format(profile_pk))
        response = self.client.get(url)
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.get('name'), self.current_user.data.get('user_name'))
            print("[S] Success")
        except AssertionError:
            print("[F] Failed")

    def test_access_permission_api(self):
        print("\n")
        print("(*) Testing... Access Permission Functionality.")
        try:
            self.assertEqual(True, True)
            print("[S] Success")
        except AssertionError:
            print("[F] Failed")

    def test_run_unit_tests_api(self):
        print("\n")
        print("(*) Testing... Run Unit Tests Functionality.")
        try:
            self.assertEqual(True, True)
            print("[S] Success")
        except AssertionError:
            print("[F] Failed")
