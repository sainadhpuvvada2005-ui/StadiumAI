from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


class ConnectionManager:
    def __init__(self) -> None:
        self.active: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active.discard(websocket)

    async def broadcast(self, payload: dict) -> None:
        for socket in list(self.active):
            await socket.send_json(payload)


manager = ConnectionManager()


@router.websocket("/ws")
async def realtime_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await websocket.send_json({"type": "connected", "channel": "stadium-ops"})
        while True:
            data = await websocket.receive_json()
            await manager.broadcast({"type": "event", "payload": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
