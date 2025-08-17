import random
from django.utils.timezone import now, timedelta, localtime
from django.dispatch import receiver
from django.db.models.signals import post_save
from users.models import User, UserConfirm
from .choices import AuthTypeChoices
from .utils import send_verify_code_mail, send_verify_code_sms_thread


@receiver(post_save, sender=User)
def create_user_confirm(sender, instance, created, **kwargs):
    if created:
        auth_type = instance.auth_type
        print(auth_type)
        expiration = 5
        code = random.randint(1000, 9999)
        if auth_type==AuthTypeChoices.PHONE_NUMBER:
            expiration = 2

        new_user_confirm = UserConfirm.objects.create(
            user=instance,
            code=code,
            expiration_time=now() + timedelta(minutes=expiration)
        )
        if auth_type==AuthTypeChoices.EMAIL:
            send_verify_code_mail(
                subject="Siz ekanligingizni tasdiqlang !",
                message=f"Sizning tasdiqlash parolingiz {code}",
                recipient_list=[instance.email],
                from_email="sodiqdevpython@gmail.com",
                html_message=f"""
            				<html>
            					<body>
            						<h1>Bizning xizmatimizga xush kelibsiz</h1>
            						<p>Sizning tasdiqlash parolingiz: <strong>{code}</strong></p>
            						<p>Bu kod eskirish vaqti: {localtime(new_user_confirm.expiration_time)} .</p>
            					</body>
            				</html>
            				"""
            )
        else:
            print(f"Xurmatli foydalanuvchi +998{instance.phone_number} parolingiz: ", code)
            send_verify_code_sms_thread(code, instance.phone_number, localtime(new_user_confirm.expiration_time))