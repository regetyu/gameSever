"""
tests
"""

from django.test import TestCase, Client
from user.models import User, Image, Hero, Counter
from user import verify_code_gen


class UserTestCase(TestCase):
    """
    an example
    """
    def setUp(self):
        """
        setup
        """
        User.objects.create(name='cjz')

    def test_can_search(self):
        """
        test
        """
        cjz = User.objects.get(name='cjz')
        self.assertEqual(cjz.name, 'cjz')


class LoginTestCase(TestCase):
    """
    test whether login works
    """
    def setUp(self):
        """
        setup
        """
        User.objects.create(
            name='test',
            password='testPassword',
            email='test@test.com',
        )

    def test_setup(self):
        """
        test whether setup works
        """
        client = Client()
        response = client.get('/login/')
        self.assertEqual(response.content, b'not POST request')
        response = client.post('/login/', {
            'name': 'john',
            'password': 'smith'
        })
        self.assertEqual(response.content, b'login failure')
        response = client.post('/login/', {
            'name': 'test',
            'password': 'wrongPassword'
        })
        self.assertEqual(response.content, b'login failure')
        response = client.post('/login/', {
            'name': 'test',
            'password': 'testPassword'
        })
        self.assertEqual(response.content, b'login success')


class RegisterTestCase(TestCase):
    """
    test whether registration works
    """
    def setUp(self):
        """
        setup
        """
        User.objects.create(
            name='test',
            password='testPassword',
            email='test@test.com',
        )

    def test_register(self):
        """
        test whether registration works
        """
        client = Client()
        response = client.get('/register/')
        self.assertEqual(response.content, b'not POST request')
        response = client.post('/register/', {
            'name': 'test',
            'password': 'test',
            'email': 'test2@test.com'
        })
        self.assertEqual(response.content, b'username already exists')
        response = client.post('/register/', {
            'name': 'test2',
            'password': 'test',
            'email': 'test@test.com'
        })
        self.assertEqual(response.content, b'email already exists')
        response = client.post('/register/', {
            'name': 'test2',
            'password': 'test',
            'email': '923952412@qq.com'
        })
        self.assertEqual(response.content, b'send email success')
        code = verify_code_gen.DIC['923952412@qq.com']
        response = client.post('/sendCode/', {
            'name': 'test2',
            'password': 'test',
            'email': 'test@test.com',
            'code': code
        })
        self.assertEqual(response.content, b'register failure')
        response = client.post('/sendCode/', {
            'name': 'test2',
            'password': 'test',
            'email': '923952412@qq.com',
            'code': code + 1
        })
        self.assertEqual(response.content, b'register failure')
        response = client.post('/sendCode/', {
            'name': 'test2',
            'password': 'test',
            'email': '923952412@qq.com',
            'code': code
        })
        self.assertEqual(response.content, b'register success')
        response = client.post('/sendCode/', {
            'name': 'test2',
            'password': 'test',
            'email': '923952412@qq.com',
            'code': code
        })
        self.assertEqual(response.content, b'register failure')


class ImageTestCase(TestCase):
    """
    test whether upload image works
    """
    def setUp(self):
        """
        setup
        """
        User.objects.create(
            name='test',
            password='testPassword',
            email='test@test.com',
        )

    def test_Image(self):
        """
        test whether upload image works
        """
        client = Client()
        f = open('c1613f64c9e014267cc979b085dacfe.png', mode='rb')
        response = client.get('/upload/image/')
        self.assertEqual(response.content, b'not post request')
        response = client.post('/upload/image/', {
            'name': 'test',
            'image': f
        })
        self.assertEqual(response.content, b'upload image success')
        response = client.get('/download/image/')
        self.assertEqual(response.content, b'not post request')
        response = client.post('/download/image/', {
            'name': 'test'
        })
        # print(response)


class HeroTestCase(TestCase):
    """
    test whether hero works
    """
    def setUp(self):
        """
        setup
        """
        User.objects.create(
            name='test',
            password='testPassword',
            email='test@test.com',
        )
        Counter.objects.create(
            name='test',
            num=0,
        )

    def test_Hero(self):
        """
        test whether hero works
        """
        client = Client()
        image = open('default.png', mode='rb')
        response = client.get('/upload/hero/')
        self.assertEqual(response.content, b'not post request')
        response = client.post('/upload/hero/', {
            'name': 'test',
            'image': image
        })
        self.assertEqual(response.content, b'upload hero success')
        self.assertEqual(Counter.objects.get(name='test').num, 1)
        client.post('/upload/hero/', {
            'name': 'test',
            'image': open('Dockerfile', mode='rb'),
        })
        self.assertEqual(Counter.objects.get(name='test').num, 2)
        response = client.get('/download/hero/names/')
        self.assertEqual(response.content, b'not post request')
        response = client.post('/download/hero/names/', {
            'name': 'test',
        })
        print(response.content)
        self.assertNotEqual(response.content, "")
        response = client.get('/download/hero/image/')
        self.assertEqual(response.content, b'not post request')
        response = client.post('/download/hero/image/', {
            'name': 'test',
            'index': 0,
        })
        response = client.post('/download/hero/image/', {
            'name': 'test',
            'index': 1,
        })
        response = client.get('/delete/hero/')
        self.assertEqual(response.content, b'not post request')
        response = client.post('/delete/hero/', {
            'name': 'test',
            'index': 0,
        })
        self.assertEqual(response.content, b'delete hero success')
        self.assertEqual(Counter.objects.get(name='test').num, 1)
        self.assertEqual(Hero.objects.get(name='test').index, 0)


class ChangePassWordTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            name='testName',
            password='testPassword',
            email='test@test.com'
        )

    def test_change_password(self):
        client = Client()
        response = client.get('/changePassword/')
        self.assertEqual(response.content, b'not post request')
        response = client.post('/changePassword/', {
            'name': 'testName',
            'old': 'wrongPassword',
            'new': 'newPassword',
        })
        self.assertEqual(response.content, b'password incorrect')
        response = client.post('/changePassword/', {
            'name': 'testName',
            'old': 'testPassword',
            'new': 'newPassword',
        })
        self.assertEqual(response.content, b'password changed')
        user = User.objects.get(name='testName')
        self.assertEqual(user.password, 'newPassword')


class ForgetPasswordTestCase(TestCase):
    def setUp(self):
        User.objects.create(
            name='testName',
            password='testPassword',
            email='test@test.com'
        )

    def test_forget_password(self):
        client = Client()
        response = client.get('/findPassword/')
        self.assertEqual(response.content, b'not post request')
        response = client.post('/findPassword/', {
            'name': 'testName',
            'email': 'wrongEmail'
        })
        self.assertEqual(response.content, b'user and email does not match')
        response = client.post('/findPassword/', {
            'name': 'wrongName',
            'email': 'wrongEmail'
        })
        self.assertEqual(response.content, b'user does not exist')
        response = client.post('/findPassword/', {
            'name': 'testName',
            'email': 'test@test.com'
        })
        self.assertEqual(response.content, b'send email success')
        code = verify_code_gen.DIC['test@test.com']
        response = client.get('/sendResetCode/')
        self.assertEqual(response.content, b'not POST request')
        response = client.post('/sendResetCode/', {
            'name': 'testName',
            'password': 'newPassword',
            'email': 'test@test.com',
            'code': code + 1,
        })
        self.assertEqual(response.content, b'change password failure')
        response = client.post('/sendResetCode/', {
            'name': 'testName',
            'password': 'newPassword',
            'email': 'test@test.com',
            'code': code,
        })
        self.assertEqual(response.content, b'change password success')
        user = User.objects.get(name='testName')
        self.assertEqual(user.password, 'newPassword')
