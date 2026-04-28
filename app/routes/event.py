import os

from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from datetime import datetime
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Event


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter(prefix="/event", tags=["event"])
#router = APIRouter(tags=["event"])


@router.post("/create")
def create_reservation(
    room_id: int = Form(...),
    user_id: int = Form(...),
    start_date: datetime = Form(...),
    end_date: datetime = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):

    new_event = Event(
        id_user = user_id,
        id_room = room_id,
        start_date = start_date,
        end_date = end_date,
        description = description
    )

    db.add(new_event)
    db.commit()

    return RedirectResponse(url="/dashboard", status_code=303)