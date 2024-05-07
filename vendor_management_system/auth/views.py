from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User


class RegisterUser(APIView):
    """
    API endpoint for user registration.

    Upon successful registration, generates a token for the user.

    POST request:
    - Receives user registration data in the request payload.
    - Validates the data using the UserSerializer.
    - If valid, saves the user and generates a token.
    - Returns the token in the response along with a status code.

    Response format:
    {
        "token": "<generated_token>"
    }

    If the data is not valid, returns the validation errors.

    Error response format:
    {
        "<field_name>": [
            "<error_message>"
        ]
    }
    """
    serializer_class = UserSerializer

    def post(self, request: Request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            token_obj, _ = Token.objects.get_or_create(user=user)
            return Response({'token': str(token_obj)}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
