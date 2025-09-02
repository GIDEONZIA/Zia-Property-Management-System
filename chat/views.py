import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from .models import ChatSession, ChatMessage

User = get_user_model()


def chat_setup(request):
    """Page where user enters name and chooses bot/agent."""
    return render(request, "chat/setup.html")


@login_required
def chat_room(request, session_id):
    """Render chat UI for a session."""
    session = ChatSession.objects.get(id=session_id, user=request.user)
    return render(request, "chat/chat_room.html", {"session": session})


@login_required
def start_chat(request):
    """Handles form submission from setup page and creates session."""
    if request.method == "POST":
        chat_type = request.POST.get("chat_type")  # "bot" or "agent"

        if chat_type == "agent":
            # Assign an available agent (simplified)
            agent = User.objects.filter(is_agent=True, is_online=True).order_by("?").first()
        else:
            agent = None  # handled by bot

        session = ChatSession.objects.create(user=request.user, agent=agent)
        return redirect("chat:chat_room", session_id=session.id)

    return redirect("chat:chat_setup")


@csrf_exempt
def bot_reply(request):
    """Endpoint to simulate bot reply (placeholder for OpenAI API)."""
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", "")
        reply = f"🤖 Bot says: You said '{message}'"
        return JsonResponse({"reply": reply})
    return JsonResponse({"error": "Invalid request"}, status=400)
