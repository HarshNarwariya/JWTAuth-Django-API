from django.core.mail import EmailMessage

class Util:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email='iamyourbabyfortonight@gmail.com',
            to=[data['to_email']],
        )
        email.send(fail_silently=False)