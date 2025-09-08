"""
Twilio Webhooks for AURA
This FastAPI application handles incoming SMS and voice webhooks from Twilio.
"""

import logging
from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse

import aura_agent

# --- FastAPI App Initialization ---

app = FastAPI()
logger = logging.getLogger("uvicorn")

# --- Webhook Endpoints ---

@app.post("/sms", response_class=PlainTextResponse)
async def sms_reply(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...),
):
    """
    Handles incoming SMS messages.
    Logs the message, gets a response from the AURA agent, and replies via TwiML.
    """
    logger.info(f"Incoming SMS from {From}: {Body}")

    # Get a response from the AURA agent
    response_text = aura_agent.get_aura_response(Body, engine="gpt")

    # Create a TwiML response
    resp = MessagingResponse()
    resp.message(response_text)

    return str(resp)


@app.post("/voice", response_class=PlainTextResponse)
async def voice_reply():
    """
    Handles incoming voice calls.
    Responds with a message indicating that the line is for text messages only.
    """
    resp = VoiceResponse()
    resp.say(
        "Hello, this is AURA. This line is for text messages only. Goodbye!",
        voice="polly.Joanna",
    )
    resp.hangup()
    return str(resp)

# --- Main Entry Point ---

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)