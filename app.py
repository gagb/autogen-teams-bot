from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity

app = Flask(__name__)

# Bot Framework Adapter setup
SETTINGS = BotFrameworkAdapterSettings(app_id="<YOUR_APP_ID>", app_password="<YOUR_APP_PASSWORD>")
adapter = BotFrameworkAdapter(SETTINGS)

# Bot logic
class SimpleBot:
    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity(f"You said: {turn_context.activity.text}")

bot = SimpleBot()

# Endpoint for incoming bot messages
@app.route("/api/messages", methods=["POST"])
async def messages():
    body = await request.get_json()
    activity = Activity.deserialize(body)
    auth_header = request.headers.get("Authorization", "")
    response = await adapter.process_activity(activity, auth_header, bot.on_message_activity)
    return Response(status=response.status_code)

if __name__ == "__main__":
    app.run(port=3978)
