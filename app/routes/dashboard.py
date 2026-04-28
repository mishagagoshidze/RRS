import os

from fastapi import FastAPI
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from jose import jwt

from app.db.database import get_db
from app.db.models import Users, Rooms, RoomAdmin, Event
from app.utils.security import SECRET_KEY, ALGORITHM

from sqlalchemy.orm import Session

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app = FastAPI()

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request, 
    db: Session = Depends(get_db)
):
    # 1. ვამოწმებთ არის თუ არა Cookie-ში ტოკენი
    token = request.cookies.get("access_token")
    
    if not token:
        # თუ ტოკენი არ არის, ვაბრუნებთ ლოგინზე
        return RedirectResponse(url="/auth/login", status_code=303)

    try:
        # 2. ვშიფრავთ ტოკენს, რომ გავიგოთ ვინ არის მომხმარებელი
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  

        all_users = db.query(Users).order_by(Users.email).all()

        #all_rooms = db.query(Rooms).all() 
        all_rooms = db.query(
                Rooms.id,
                Rooms.number,
                Rooms.floor,
                Rooms.description,
                Users.id.label("admin_id"),
                Users.first_name.label("admin_first_name"),
                Users.last_name.label("admin_last_name")
            ).outerjoin(RoomAdmin, Rooms.id == RoomAdmin.id_room) \
            .outerjoin(Users, Users.id == RoomAdmin.id_user) \
            .order_by(Rooms.number) \
            .all()

        all_events = db.query(
                Event.id,
                Event.id_user,
                Event.id_room,
                Event.start_date,
                Event.end_date,
                Event.description,
                Users.first_name,
                Users.last_name,
                Rooms.number.label("room_number"),
            ).outerjoin(Rooms, Rooms.id == Event.id_room) \
            .outerjoin(Users, Users.id == Event.id_user) \
            .all()

        # მოვძებნოთ მიმდინარე მომხმარებელი მონაცემთა ბაზაში
        current_user = db.query(Users).filter(Users.email == email).first()    
        
        # 3. ვაჩვენებთ დეშბორდის გვერდს
        return templates.TemplateResponse(
            request = request,
            name = "dashboard.html",
            context = {
                "request": request,
                "user": current_user,
                "rooms": all_rooms,
                "users": all_users,
                "events": all_events 
            }
        )
           
    except Exception:
        # თუ ტოკენი არასწორია
        return RedirectResponse(url="/auth/login", status_code=303)

