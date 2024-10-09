import os
from datetime import timedelta

from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Request, Form, WebSocket, WebSocketDisconnect, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jose import JWTError

from .connection_manager import ConnectionManager
from .crud import add_item, remove_item, get_items, update_item
from .database import get_db, engine
from .models import Base
from .security import create_access_token, decode_access_token, ACCESS_TOKEN_EXPIRE_DAYS

load_dotenv()

PASSWORD = os.getenv("PASSWORD")

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

manager = ConnectionManager()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(password: str):
    return password == PASSWORD


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    token = request.cookies.get("access_token")

    if token:
        try:
            payload = decode_access_token(token)
            username = payload.get("sub")
            if username:
                return RedirectResponse(url="/shopping/list")
        except JWTError:
            pass

    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if not authenticate_user(password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Generate JWT token and return as an HttpOnly cookie
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)

    response = RedirectResponse(url="/shopping/list", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="Strict")
    return response


async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


@app.get("/list", response_class=HTMLResponse)
async def shopping_list(request: Request, username: str = Depends(get_current_user)):
    db = next(get_db())
    items = get_items(db)
    users = manager.active_connections
    return templates.TemplateResponse("shopping_list.html", {"request": request, "username": username, "items": items,
                                                             "users": users})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    cookie_header = websocket.cookies.get('access_token')

    if cookie_header is None:
        await websocket.close(code=1008)
        return

    decode_access_token(cookie_header)

    try:
        payload = decode_access_token(cookie_header)
        username = payload.get("sub")
        if username is None:
            await websocket.close(code=1008)
            return
        await manager.connect(websocket, username)
        await manager.broadcast_users()

        while True:
            db = next(get_db())
            data = await websocket.receive_json()
            action = data.get("action")
            if action == "add_item":
                item_name = data.get("item_name")
                new_item = add_item(db, item_name)
                await manager.broadcast({
                    "action": "add_item",
                    "item_id": new_item.id,
                    "item_name": item_name,
                })

            elif action == "remove_item":
                item_id = data.get("item_id")
                remove_item(db, item_id)
                await manager.broadcast({
                    "action": "remove_item",
                    "item_id": item_id,
                })

            elif action == "edit_item":
                item_id = data.get("item_id")
                new_name = data.get("new_name")
                update_item(db, item_id, new_name)
                await manager.broadcast({
                    "action": "edit_item",
                    "item_id": item_id,
                    "new_name": new_name,
                })

            db.close()

    except JWTError:
        await websocket.close(code=1008)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_users()
