from django.test import TestCase

# Create your tests here.
# myapp/tests.py

# myapp/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from myapp.models import User, Show, Favorite

class UserAuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = '/api/register/'
        self.login_url = '/api/login/'

        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'password2': 'testpass123'
        }

    def test_user_registration_success(self):
        """Test user registration successful"""
        response = self.client.post(self.register_url, self.user_data, content_type='application/json')
        print("Registration Response:", response.status_code, response.json())
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_login_success(self):
        """Test user login successful"""
        # Register as a user first
        self.client.post(self.register_url, self.user_data, content_type='application/json')

        # Login
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, login_data, content_type='application/json')
        print("Login response:", response.status_code, response.json())
        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful！', response.json().get('message', ''))

    def test_user_login_wrong_password(self):
        """Test user login failed: Wrong password"""
        # Registered User
        self.client.post(self.register_url, self.user_data, content_type='application/json')

        # Login with wrong password
        wrong_login = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, wrong_login, content_type='application/json')
        print("Wrong password login response:", response.status_code, response.json())
        self.assertEqual(response.status_code, 401)
        self.assertIn('Wrong password', response.json().get('error', ''))

    def test_user_registration_password_mismatch(self):
        """Test registration failed: The two passwords do not match"""
        mismatch_data = {
            'username': 'testuser2',
            'password': 'abc123',
            'password2': 'abc456'
        }
        response = self.client.post(self.register_url, mismatch_data, content_type='application/json')
        print("Password mismatch registration response:", response.status_code, response.json())
        self.assertEqual(response.status_code, 400)
        self.assertIn("The two passwords you entered do not match", str(response.json()))


class SearchShowTestCase(TestCase):
    def setUp(self):
        # Create some test data
        Show.objects.create(
            s_id=1,
            s_name='JJ Lin "JJ20" FINAL LAP World Tour',
            actor='JJ Lin',
            picture='path/to/pic1.jpg',
            description='A world tour concert',
            date='2025-04-01',
            address='Shanghai',
            genre='concert',
            link='https://example.com/show1'
        )
        Show.objects.create(
            s_id=2,
            s_name='Jay Chou Fantasy Tour',
            actor='Jay Chou',
            picture='path/to/pic2.jpg',
            description='A fantasy concert experience',
            date='2025-05-10',
            address='Beijing',
            genre='pop',
            link='https://example.com/show2'
        )
        self.client = Client()

    def test_search_by_actor(self):
        response = self.client.get('/api/search/', {'q': 'JJ Lin'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()['results']) >= 1)
        self.assertIn('JJ Lin', response.json()['results'][0]['actor'])

    def test_search_by_s_name(self):
        response = self.client.get('/api/search/', {'q': 'Fantasy'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any('Fantasy' in item['s_name'] for item in response.json()['results']))

    def test_search_no_results(self):
        response = self.client.get('/api/search/', {'q': '不存在的演出'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 0)

    def test_search_without_query(self):
        response = self.client.get('/api/search/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()['results']), 2)

class FavoriteFunctionTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a test user and show
        self.user = User.objects.create(username='testuser', password='123456', role='user')
        self.show = Show.objects.create(
            s_id=1,
            s_name='Test Show',
            actor='Test Artist',
            picture='test_pic.jpg',
            description='Test Description',
            date='2025-05-01',
            address='Test Address',
            genre='Pop',
            link='https://example.com/show'
        )

        # Simulate the login state (usually you have a session or token mechanism, but it is simplified here)
        self.client.cookies['user_id'] = str(self.user.id)

    def test_add_favorite(self):
        """Test adding favorites"""
        response = self.client.post('/api/favorite/', {
            'user_id': self.user.id,
            'show_id': self.show.s_id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Favorite.objects.filter(user_id=self.user.id, show_id=self.show.s_id).exists())

    def test_remove_favorite(self):
        """Test uncollection"""
        # Manually add favorites first
        Favorite.objects.create(user_id=self.user.id, show_id=self.show.s_id)

        # Click the collection interface again → it should change to cancel collection
        response = self.client.post('/api/favorite/', {
            'user_id': self.user.id,
            'show_id': self.show.s_id
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Favorite.objects.filter(user_id=self.user.id, show_id=self.show.s_id).exists())

    def test_favorite_without_login(self):
        """Unlogged in users cannot save"""
        # Do not set user_id, simulate not logged in
        self.client.cookies.clear()  # Clear login status
        response = self.client.post('/api/favorite/', {
            'user_id': '',
            'show_id': self.show.s_id
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('收藏失败', response.content.decode())