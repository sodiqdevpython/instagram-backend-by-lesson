from django.db.models import TextChoices

class GenderChoices(TextChoices):
    MALE = 'Male'
    FEMALE = 'Female'

class AuthTypeChoices(TextChoices):
    EMAIL = 'Email'
    PHONE_NUMBER = 'Phone number'

class AuthStatusChoices(TextChoices):
    NEW = "New"
    CODE_VERIFIED = "Code verified"
    DONE = "Done"
    FINISH = "Finish"