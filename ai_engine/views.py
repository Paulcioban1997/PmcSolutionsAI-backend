from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from openai import OpenAI

@api_view(["POST"])
def chat(request):
    try:
        user_message = request.data.get("message")
        if not user_message:
            return Response({"error": "No message provided"}, status=400)

        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # System instructions to configure the AI personality
        system_prompt = """
        You are the intelligent virtual assistant for PMC Solutions AI, a company specializing in AI automation for businesses.
        Your role is to help potential clients understand our services (AI Chatbots, Automation, SaaS) and encourage them to request a quote.
        Be professional, concise, and helpful. Answer in the same language as the user (English, French, or Spanish).
        If asked about pricing, mention our transparent plans starting at $99/mo.
        If the user wants to buy or get a quote, direct them to the 'Get Quote' page.
        """

        completion = client.chat.completions.create(
            model="gpt-4o-mini", # Using a fast and capable model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        reply = completion.choices[0].message.content
        return Response({"reply": reply})

    except Exception as e:
        return Response({"error": str(e)}, status=500)
