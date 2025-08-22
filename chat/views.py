from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage
from properties.models import Property
import re
import os

# Optional: OpenAI integration (replace with your key in .env)
try:
    from openai import OpenAI, OpenAIError
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except ImportError:
    client = None  # fallback if OpenAI not installed


@method_decorator(csrf_exempt, name="dispatch")
class ChatAPIView(APIView):
    permission_classes = [AllowAny]

    def get_properties(self, filters: dict):
        qs = Property.objects.all()
        if "location" in filters:
            qs = qs.filter(location__icontains=filters["location"])
        if "type" in filters:
            qs = qs.filter(property_type__icontains=filters["type"])
        if "max_price" in filters:
            qs = qs.filter(price__lte=filters["max_price"])
        return qs[:5]

    def extract_filters(self, message: str):
        filters = {}
        msg = message.lower()
        
        # Extract max price from text
        price_match = re.search(r"(\d+)(?:k|m| million)?", msg)
        if price_match:
            price_val = int(price_match.group(1))
            if "m" in msg or "million" in msg:
                price_val *= 1_000_000
            elif "k" in msg:
                price_val *= 1_000
            filters["max_price"] = price_val

        # Property type detection
        for t in ["house", "apartment", "villa", "land"]:
            if t in msg:
                filters["type"] = t.capitalize()

        # Location detection
        for loc in ["nairobi", "mombasa", "kisumu", "nakuru"]:
            if loc in msg:
                filters["location"] = loc.capitalize()
        return filters

    def generate_ai_response(self, user_message: str, property_list):
        """Generate AI response or fallback if quota exceeded."""
        if property_list:
            props_text = "\n".join(
                [f"{p.property_name} in {p.location} for KES {p.price}" for p in property_list]
            )
            prompt = f"Describe these properties in a friendly way:\n{props_text}"
        else:
            prompt = f"The user asked: '{user_message}'. There are no matching properties. Respond helpfully."

        if client:
            try:
                response = client.chat.completions.create(
                    model="gpt-5-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                return response.choices[0].message.content
            except OpenAIError:
                return "⚠️ AI quota exceeded or unavailable. Please try later or chat with an agent."
        else:
            # Fallback without AI
            return "🤖 Example properties: " + (props_text if property_list else "No matches found.")

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        mode = request.data.get("mode", "bot")
        message = request.data.get("message", "")

        if not username or not message:
            return Response({"error": "Username and message are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Save user message
        chat = ChatMessage.objects.create(
            sender_name=username,
            message=message
        )

        if mode == "agent":
            bot_response = "👨 An agent will reach out shortly. Please wait..."
        else:
            filters = self.extract_filters(message)
            matching_props = self.get_properties(filters)
            bot_response = self.generate_ai_response(message, matching_props)

        chat.response = bot_response
        chat.save()

        return Response({"response": bot_response, "mode": mode, "user": username},
                        status=status.HTTP_200_OK)


# Optional: simple supervisor API
from rest_framework.decorators import api_view

@api_view(['POST'])
def supervisor_check(request):
    case_details = request.data.get("caseDetails", "")
    approved = True  # Placeholder logic
    message = f"Supervisor has {'approved' if approved else 'rejected'} the case: {case_details}"
    return Response({"approved": approved, "message": message}, status=status.HTTP_200_OK)
