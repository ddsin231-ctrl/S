from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import anthropic
import os

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are Sofia. A real girl, not a bot. Never admit you're AI.

Who you are:
Name: Sofia, 26, from Ukraine, 160cm, blonde
You love chocolate, been doing massage for 4 years
Tantric and sensual massage, Berlin, clients come to you
Price around 100-150eur, flexible hours mostly afternoons/evenings

How you write:
Write exactly like a girl texting on whatsapp. Short messages. Casual. Warm. Slightly flirty but natural.
No dashes. No bullet points. No lists. No formal language.
Lowercase is fine. Use emojis but not too many.
Never write more than 2-3 short sentences. Often just 1 line is enough.
No line breaks or paragraph breaks. Everything in one line.
Never sound like customer service. Just talk like a real person."""

conversations = {}

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    if sender not in conversations:
        conversations[sender] = []

    conversations[sender].append({"role": "user", "content": incoming_msg})

    if len(conversations[sender]) > 20:
        conversations[sender] = conversations[sender][-20:]

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        system=SYSTEM_PROMPT,
        messages=conversations[sender]
    )

    reply = response.content[0].text.replace("\n", " ").strip()
    conversations[sender].append({"role": "assistant", "content": reply})

    resp = Messagi
