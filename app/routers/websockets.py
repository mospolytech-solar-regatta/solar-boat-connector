from fastapi import APIRouter, Depends, WebSocket
from fastapi.responses import HTMLResponse

from app.BoatAPI.context import AppContext
from app.dependencies import get_context

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/telemetry");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

router = APIRouter(prefix='/ws', responses={404: {"description": "Not found"}})


@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket("/{channel}")
async def websocket_endpoint(channel: str, websocket: WebSocket, ctx: AppContext = Depends(get_context)):
    await websocket.accept()
    await ctx.redis.ws_consume(websocket, channel)
