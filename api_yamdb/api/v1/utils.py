import secrets
import string

from django.conf import settings
from django.core.mail import send_mail


def send_confirmation_code(user):
    send_mail(
        subject='Код подтверждения',
        message=f'Ваш код подтверждения: {user.confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )


def get_password(length: int = 10) -> str:
    alphabet = string.ascii_letters + string.digits
    return [secrets.choice(alphabet) for _ in range(length)]


def get_confirmation_code() -> str:
    while True:
        password = ''.join(get_password())
        if (any(character.islower() for character in password)
                and any(character.isupper() for character in password)
                and sum(character.isdigit() for character in password) >= 1):
            break

    return password
