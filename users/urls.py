from django.urls import path
from users.views import SignUpView, VerificationCodeView, GenerateNewVerificationCodeView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/', VerificationCodeView.as_view(), name='verify'),
    path('generate-new-verification/', GenerateNewVerificationCodeView.as_view(), name='generate'),
]