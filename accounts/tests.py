from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('profile')
        self.update_username_url = reverse('update_username')
        self.update_email_url = reverse('update_email')
        self.change_password_url = reverse('change_password')
        self.expenses_url = reverse('expenses')

    def test_custom_login_view_valid(self):
        test_data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.login_url, data={**test_data}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_custom_login_view_invalid(self):
        test_data = {'username': 'incorrecttestuser', 'password': 'incorrecttestpassword'}
        response = self.client.post(self.login_url, data={**test_data}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password.')

    def test_signup_view_valid(self):
        data_register_form = {
            'username': 'testsignup',
            'email': 'testsignupemail@gmail.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123'
        }

        response = self.client.post(self.signup_url, data={
            **data_register_form
        }, follow=True)
        self.assertRedirects(response, self.expenses_url)
        self.assertTrue(User.objects.filter(username='testsignup').exists())

    def test_signup_view_invalid(self):
        data_register_form = {
            'username': 'testsignup',
            'email': 'testsignupemail@gmail.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword'
        }
        response = self.client.post(self.signup_url, data={
            **data_register_form
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The two password fields didn’t match.")

    def test_signup_view_get_not_authenticated(self):
        response = self.client.get(self.signup_url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_view_get_authenticated(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.signup_url)

        self.assertRedirects(response, self.expenses_url)

    def test_change_password_view_valid(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(self.change_password_url, {
            'old_password': 'testpassword',
            'new_password1': 'newtestpassword',
            'new_password2': 'newtestpassword'
        })
        self.assertRedirects(response, self.profile_url)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newtestpassword'))

    def test_change_password_view_invalid(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(self.change_password_url, {
            'old_password': 'wrongpassword',
            'new_password1': 'newtestpassword',
            'new_password2': 'newtestpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your old password was entered incorrectly. Please enter it again.")

    def test_update_username_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(self.update_username_url, {'username': 'updateduser'})
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_update_email_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(self.update_email_url, {'email': 'updatedemail@example.com'})
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updatedemail@example.com')

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

