from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from users.serializers import SignUpSerializer, UserConfirmSerializer, GenerateNewTokenSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .utils import send_verify_code_mail, send_verify_code_sms_thread


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=SignUpSerializer)
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerificationCodeView(APIView):

    @swagger_auto_schema(request_body=UserConfirmSerializer)
    def post(self, request):
        user = request.user
        data = request.data
        serializer = UserConfirmSerializer(data=data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenerateNewVerificationCodeView(APIView):

    @swagger_auto_schema(request_body=GenerateNewTokenSerializer)
    def get(self, request):
        user = request.user
        ser = GenerateNewTokenSerializer(context={'user': user})
        ser.is_valid(raise_exception=True)
        new_user = ser.save()
        return Response(new_user, status=status.HTTP_201_CREATED)