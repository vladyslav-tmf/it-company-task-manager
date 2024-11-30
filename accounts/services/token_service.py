from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGeneratorService(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: settings.AUTH_USER_MODEL, timestamp: int) -> str:
        return str(user.pk) + str(timestamp) + str(user.is_active)


account_activation_token = TokenGeneratorService()
