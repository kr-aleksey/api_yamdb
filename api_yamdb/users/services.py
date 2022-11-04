def send_confirmation_mail(user, confirmation_code):
    subject = 'Успешная регистрация на сайте YaMDb.'
    message = ('Вы успешно зарегистрированы на сайте YaMDb. '
               'Ваш код подтверждения {confirmation_code}. '
               'Никому не сообщайте этот код!')
    user.email_user(
        subject=subject,
        message=message.format(confirmation_code=confirmation_code),
    )
