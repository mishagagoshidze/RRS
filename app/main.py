import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.db.database import Base, engine
from app.routes import auth, user, room, event, dashboard

Base.metadata.create_all(bind=engine)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates_path = os.path.join(BASE_DIR, "templates")
static_path = os.path.join(BASE_DIR, "static")

templates = Jinja2Templates(directory=templates_path)

app = FastAPI()

app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
def root():
    return RedirectResponse(url="/auth/login")


app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(user.router)
app.include_router(room.router)
app.include_router(event.router)