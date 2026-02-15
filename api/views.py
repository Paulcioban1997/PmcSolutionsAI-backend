from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from openai import OpenAI
import os

from ai_engine.models import Conversation, Message, Usage
from .serializers import RegisterSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    user = authenticate(
        username=request.data.get("username"),
        password=request.data.get("password"),
    )
    if not user:
        return Response({"error": "Invalid credentials"}, status=400)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})


@api_view(["POST"])
def chat(request):
    user_message = request.data.get("message") or ""

    convo = Conversation.objects.create(user=request.user)
    Message.objects.create(conversation=convo, role="user", content=user_message)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-4o-mini",
        input=user_message,
    )

    reply = response.output_text
    Message.objects.create(conversation=convo, role="assistant", content=reply)
    Usage.objects.create(user=request.user, tokens=len(user_message.split()) + len(reply.split()))

    return Response({"reply": reply})


@api_view(["GET"])
def usage(request):
    total_tokens = Usage.objects.filter(user=request.user).count()
    return Response({"usage": total_tokens})
