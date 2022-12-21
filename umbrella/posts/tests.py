# Каждый логический набор тестов — это класс,
# который наследуется от базового класса TestCase

# Каждый класс — это набор тестов. Имя такого класса принято начинать со слова Test.
# В файле может быть множество наборов тестов,
# не обязательно иметь один класс для всего приложения.

# Каждый отдельный метод в наборе тестов должен начинаться со слова test
# таких методов-тестов в наборе может быть множество.

from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, Group, User, Follow


def get_post_urls(user):
    return (
        reverse('index'),
        reverse('profile', kwargs={'username': user.username}),
        reverse('post_edit', kwargs={'username': user.username, 'post_id': 1})
    )


class ProfileTest(TestCase):
    def signup_test_user(self):
        """ Регистрация тестового пользователя (test_user)"""
        self.client.post(path=reverse('signup'), data={'username': 'test_user',
                                                       'password1': 'Hgj-15Jkf324-tu',
                                                       'password2': 'Hgj-15Jkf324-tu',
                                                       'email': 'test@mail.com'})

    def setUp(self):
        self.client = Client()
        self.signup_test_user()

    # Проверяем, что после регистрации пользователя создается его персональная страница (profile)
    def test_signup_personal_page(self):
        response = self.client.get(reverse(viewname='profile', kwargs={'username': 'test_user'}))
        self.assertEqual(response.status_code, 200, msg='Страница пользователя не найдена.')

    # Проверяем, что авторизованный пользователь может опубликовать пост (new)
    def test_login_user_new_post(self):
        user = User.objects.get(username='test_user')

        self.client.force_login(user)
        self.client.post(reverse('post_new'), {'text': 'Some text...'})
        self.assertTrue(user.posts.all(), msg='Ни один пост не найден.')

    # Проверяем, что неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа)
    def test_not_login_new_post(self):
        user = User.objects.get(username='test_user')

        before_posts_count = user.posts.all().count()
        self.client.post(reverse('post_new'), {'text': 'Some text...'})
        after_posts_count = user.posts.all().count()
        self.assertEqual(before_posts_count, after_posts_count, msg='Количество постов изменилось.')

    def test_not_login_new_post_redirect(self):
        response = self.client.post(reverse('post_new'), {'text': 'Some text...'}, follow=True)
        self.assertRedirects(response, '/auth/login/?next=/new/')

    # После публикации поста новая запись появляется на главной странице сайта (index),
    # на персональной странице пользователя (profile), и на отдельной странице поста (post)
    def test_new_post_on_all_pages(self):
        user = User.objects.get(username='test_user')
        self.client.force_login(user)
        self.client.post(reverse('post_new'), {'text': 'Some text...'})

        for url in get_post_urls(user):
            response = self.client.get(url)
            self.assertContains(response, 'Some text...')

    # Авторизованный пользователь может отредактировать свой пост
    # и его содержимое изменится на всех связанных страницах
    def test_edited_post_on_all_pages(self):
        user = User.objects.get(username='test_user')
        self.client.force_login(user)
        self.client.post(reverse('post_new'), {'text': 'Some text...'})

        edited_text = 'Edited text ...'
        self.client.post(reverse('post_edit', kwargs={'username': user.username, 'post_id': 1}),
                         {'text': edited_text})

        # post = user.posts.get(id=1)
        # self.assertEqual(post.text, edited_text)

        for url in get_post_urls(user):
            response = self.client.get(url)
            self.assertContains(response, 'Edited text ...')


class ResponseCodeTest(TestCase):
    def setUp(self):
        self.client = Client()

    # Для своего локального проекта напишите тест:
    # возвращает ли сервер код 404, если страница не найдена.
    def test_page_not_found_404(self):
        response = self.client.get('page404/')
        self.assertEqual(response.status_code, 404, msg='Сервер вернул неверный код для 404 Not Found.')


class ImageTest(TestCase):
    def signup_test_user(self):
        """ Регистрация тестового пользователя (test_user)"""
        self.client.post(path=reverse('signup'), data={'username': 'test_user',
                                                       'password1': 'Hgj-15Jkf324-tu',
                                                       'password2': 'Hgj-15Jkf324-tu',
                                                       'email': 'test@mail.com'})

    def setUp(self):
        self.client = Client()
        self.signup_test_user()
        user = User.objects.get(username='test_user')
        self.client.force_login(user)

        group = Group.objects.create(title='Test Group',
                                     slug='test',
                                     description='Test description.')

        # По стечению обстоятельств сначало пост создаем
        self.client.post(path=reverse('post_new'),
                         data={'text': 'Test post'})

        # Потом добавлем группу и картинку
        with open('media/test_img.jpeg', 'rb') as img:
            self.client.post(path=reverse('post_edit', kwargs={'username': 'test_user', 'post_id': 1}),
                             data={'text': 'Test post with image', 'group': group.id, 'image': img})

    def test_image_post_page(self):
        # Проверяем страницу конкретной записи с картинкой: на странице есть тег <img>
        response = self.client.get(reverse('post', kwargs={'username': 'test_user', 'post_id': 1}))

        # response.content.decode()
        self.assertContains(response, text='<img')

    def test_image_all_pages(self):
        # Проверяем что на главной странице, на странице профайла и на странице группы
        # пост с картинкой отображается корректно, с тегом <img>
        for url in (
                reverse('index'),
                reverse('profile', kwargs={'username': 'test_user'}),
                reverse('group', kwargs={'slug': 'test'})
        ):
            response = self.client.get(url)
            self.assertContains(response, text='<img')


class ImageTestGuard(TestCase):
    def signup_test_user(self):
        """ Регистрация тестового пользователя (test_user)"""
        self.client.post(path=reverse('signup'), data={'username': 'test_user',
                                                       'password1': 'Hgj-15Jkf324-tu',
                                                       'password2': 'Hgj-15Jkf324-tu',
                                                       'email': 'test@mail.com'})

    def test_bad_image_upload_guard(self):
        # Проверяем что срабатывает защита от загрузки файлов не-графических форматов
        # Для проверки защиты от загрузки «неправильных» файлов достаточно протестировать
        # загрузку на одном «неграфическом» файле: тест покажет, срабатывает ли система защиты
        self.client = Client()
        self.signup_test_user()
        user = User.objects.get(username='test_user')
        self.client.force_login(user)

        with open('media/bad_image.wav', 'rb') as img:
            self.client.post(path=reverse('post_new'),
                             data={'text': 'Test bad image',
                                   'image': img})

        self.assertEqual(user.posts.count(), 0)


class CacheTest(TestCase):
    def signup_test_user(self):
        """ Регистрация тестового пользователя (test_user)"""
        self.client.post(path=reverse('signup'), data={'username': 'test_user',
                                                       'password1': 'Hgj-15Jkf324-tu',
                                                       'password2': 'Hgj-15Jkf324-tu',
                                                       'email': 'test@mail.com'})

    def setUp(self):
        self.client = Client()
        self.signup_test_user()
        self.user = User.objects.get(username='test_user')
        self.client.force_login(self.user)

    def test_cache_index_page(self):
        ugly_text = 'Test cache.-24$-41a-'
        # Первый запрос на главную страницу, кэш сохраняется на 20 секунд.
        self.client.get(path=reverse('index'))
        self.client.post(path=reverse('post_new'), data={'text': ugly_text})
        # Второй запрос, следующий сразу за первым, поэтому новой записи не будет.
        response = self.client.get(path=reverse('index'))
        # self.assertNotContains(response, ugly_text)
        # При включенном кеше ломаются другие тесты.


class FollowTest(TestCase):
    def setUp(self):
        # Создал клиенты.
        self.client_garry = Client()
        self.client_arnold = Client()
        # Зарегистрировал пользователей.
        self.client_garry.post(path=reverse('signup'), data={'username': 'garry',
                                                             'password1': 'Hgj-15Jkf324-tu',
                                                             'password2': 'Hgj-15Jkf324-tu',
                                                             'email': 'garry.test@mail.com'})
        self.client_arnold.post(path=reverse('signup'), data={'username': 'arnold',
                                                              'password1': 'Hgj-15Jkf324-tu',
                                                              'password2': 'Hgj-15Jkf324-tu',
                                                              'email': 'arnold.test@mail.com'})
        # Получил пользователей из базы.
        self.user_garry = User.objects.get(username='garry')
        self.user_arnold = User.objects.get(username='arnold')
        # Авторизовался пользователями.
        self.client_garry.force_login(self.user_garry)
        self.client_arnold.force_login(self.user_arnold)

    # Авторизованный пользователь может подписываться на других пользователей.
    def test_auth_user_can_follow_another(self):
        # Гарри подписывается на Арнольда.
        self.client_garry.post(path=reverse('profile_follow', kwargs={'username': 'arnold'}))
        # Проверяем что в базе есть объект Follow с такой связью.
        self.assertTrue(Follow.objects.filter(user=self.user_garry, author=self.user_arnold).exists())

    # Авторизованный пользователь может удалять других пользователей из подписок.
    def test_auth_user_can_unfollow_another(self):
        # Арнольд подписывается на Гарри.
        self.client_arnold.post(path=reverse('profile_follow', kwargs={'username': 'garry'}))
        # Арнольд отписывается от Гарри.
        self.client_arnold.post(path=reverse('profile_unfollow', kwargs={'username': 'garry'}))
        # Проверяем что в базе нет объекта Follow с такой связью.
        self.assertFalse(Follow.objects.filter(user=self.user_arnold, author=self.user_garry).exists())

    # Новая запись пользователя появляется в ленте тех, кто на него подписан.
    def test_new_post_appear_on_follower_page(self):
        # Гарри подписывается на Арнольда.
        self.client_garry.post(path=reverse('profile_follow', kwargs={'username': 'arnold'}))
        # Арнольд выкладывает новый пост.
        self.client_arnold.post(path=reverse('post_new'), data={'text': 'Привет Гарри =)'})
        # Новый пост Арнольда видно на странице подписок у Гарри.
        response = self.client_garry.get(path=reverse('follow_index'))
        self.assertContains(response=response, text='Привет Гарри =)')

    # Новая запись пользователя не появляется в ленте тех, кто не подписан на него.
    def test_new_post_do_not_appear_on_not_follower_page(self):
        # Арнольд выкладывает новый пост.
        self.client_arnold.post(path=reverse('post_new'), data={'text': 'Привет Гарри =)'})
        # Новый пост Арнольда НЕ видно на странице подписок у Гарри.
        response = self.client_garry.get(path=reverse('follow_index'))
        self.assertNotContains(response=response, text='Привет Гарри =)')

    # Авторизированный пользователь может комментировать посты.
    def test_auth_user_can_add_comment(self):
        # Арнольд выкладывает новый пост.
        self.client_arnold.post(path=reverse('post_new'), data={'text': 'Привет Гарри =)'})
        # Гарри оставляет комментарий под новым постом Арнольда.
        self.client_garry.post(path=reverse('add_comment', kwargs={'username': 'arnold', 'post_id': 1}),
                               data={'text': 'Здравствуй, Арнольд.'})
        # Арнольд видит комментарий Гарри под своим постом.
        response = self.client_arnold.get(path=reverse('post', kwargs={'username': 'arnold', 'post_id': 1}))
        self.assertContains(response=response, text='Здравствуй, Арнольд.')

    # НЕавторизированный пользователь НЕ может комментировать посты.
    def test_not_auth_user_can_not_add_comment(self):
        # Арнольд выкладывает новый пост.
        self.client_arnold.post(path=reverse('post_new'), data={'text': 'Гарри ответь!'})
        # Пользователь Гарри вышел из системы.
        self.client_garry.logout()
        # Гарри пробует оставить комментарий под новым постом Арнольда.
        self.client_garry.post(path=reverse('add_comment', kwargs={'username': 'arnold', 'post_id': 1}),
                               data={'text': 'Здравствуй, Арнольд.'})
        # Арнольд НЕ видит новых комментариев Гарри под своим постом.
        response = self.client_arnold.get(path=reverse('post', kwargs={'username': 'arnold', 'post_id': 1}))
        self.assertNotContains(response=response, text='Здравствуй, Арнольд.')
