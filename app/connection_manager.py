import json

from fastapi import WebSocket

connected_users = []


class ConnectionManager:
    def __init__(self):
        # Store both websocket connections and their usernames
        self.active_connections: list[dict] = []

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections.append({"websocket": websocket, "username": username})
        connected_users.append(username)

    def disconnect(self, websocket: WebSocket):
        for connection in self.active_connections:
            if connection["websocket"] == websocket:
                self.active_connections.remove(connection)
                connected_users.remove(connection["username"])
                break

    async def broadcast(self, message: dict):
        message_text = json.dumps(message)
        for connection in self.active_connections:
            await connection["websocket"].send_text(message_text)

    async def broadcast_users(self):
        # Send the list of connected users to each active connection
        for connection in self.active_connections:
            await connection["websocket"].send_json({"users": connected_users})
