from django.contrib.auth import get_user_model


class BaseUserTestMixin:
    """
    To easly test views and places where an user is required
    """
    user_email = 'test@user.com'
    user_username = 'test-username'
    user_password = '123qweasd'

    def setUp(self):
        super().setUp()
        User = get_user_model()

        self.user = User.objects.create_user(
            email=self.user_email,
            password=self.user_password,
            is_active=True,
            username=self.user_username
        )
