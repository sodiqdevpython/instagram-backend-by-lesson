from rest_framework import serializers
from django.core.validators import validate_email
from twilio.rest.api.v2010.account.recording.add_on_result.payload import data

from .models import User, UserConfirm
from .choices import AuthTypeChoices, AuthStatusChoices
from django.utils.timezone import now


class SignUpSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    email_or_phone = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['auth_type', 'token', 'email_or_phone']
        extra_kwargs = {
            'auth_type': {'required': False, 'read_only': True},
        }

    def validate_email_or_phone(self, value):
        value = value.replace(' ', '').lower()
        if value.isnumeric():
            if len(value) != 9:
                raise serializers.ValidationError("Telefon raqami 9 ta raqamdan iborat bo'lishi kerak.")
            return value
        try:
            validate_email(value)
        except:
            raise serializers.ValidationError('Xato email !')

        return value

    def validate(self, data):
        if data['email_or_phone'].isnumeric():
            data['auth_type'] = AuthTypeChoices.PHONE_NUMBER
            data['phone_number'] = data['email_or_phone']
            if User.objects.filter(phone_number=data['email_or_phone']).exists():
                raise serializers.ValidationError('Telefon raqam allaqachon foydalanilgan !')
        else:
            data['auth_type'] = AuthTypeChoices.EMAIL
            data['email'] = data['email_or_phone']
            if User.objects.filter(email=data['email_or_phone']).exists():
                raise serializers.ValidationError('Bu email allaqachon foydalanilgan !')

        data.pop('email_or_phone')

        return data

    def get_token(self, obj):
        return obj.token()

class UserConfirmSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = UserConfirm
        fields = ['code', 'token']

    def get_token(self, obj):
        user = self.context.get('user')
        return user.token()

    def validate(self, data):
        code = data.get('code')
        user = self.context.get('user')

        if len(code) != 4:
            raise serializers.ValidationError("Kod kamida 4 ta raqamdan iborat bo'lishi kerak. !")
        if not code.isnumeric():
            raise serializers.ValidationError("Kod faqat raqamlardan iborat bo'lishi kerak. !")
        if user.auth_status != AuthStatusChoices.NEW:
            raise serializers.ValidationError("Bu profil allaqachon tasdiqlangan !")

        user_verification = UserConfirm.objects.filter(user=user).order_by('-created_at').first() #! oxirgisini olish uchun
        if user_verification:
            if user_verification.code != code:
                raise serializers.ValidationError("Kod mos kelmadi !")
            if user_verification.expiration_time < now():
                raise serializers.ValidationError("Bu kod to'g'ri lekin allaqachon muddati o'tgan ekan!")

        return data

    def save(self, **kwargs):
        user = self.context.get('user')
        user.auth_status = AuthStatusChoices.CODE_VERIFIED
        user.save(update_fields=['auth_status'])

        UserConfirm.objects.filter(user=user).delete()
        return user


class GenerateNewTokenSerializer(serializers.Serializer):
    token = serializers.SerializerMethodField()

    class Meta:
        fields = ['token']

    def get_token(self, obj):
        user = self.context.get('user')
        return user.token()

    def validate(self, data):
        user = self.context.get('user')
        if user.auth_status != AuthStatusChoices.NEW:
            raise serializers.ValidationError("Bu profil allaqachon tasdiqlangan !")
