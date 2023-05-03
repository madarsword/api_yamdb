from django.core.mail import send_mail

from api_yamdb.settings import FROM_EMAIL


def send_confirmation_code(username, email, confirmation_code):
    send_mail(
        subject='Код подтверждения',
        message=f'Здравствуйте, {username}! Ваш код подтверждения: {confirmation_code}',
        from_email=FROM_EMAIL,
        recipient_list=(email,),
        fail_silently=False,
    )
