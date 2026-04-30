import os

from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request


from datetime import datetime
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Event, Users, Rooms


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter(prefix="/event", tags=["event"])
#router = APIRouter(tags=["event"])

@router.get("/log", response_class=HTMLResponse)
async def dashboard(
    request: Request, 
    db: Session = Depends(get_db)
):
    current_time = datetime.now()
    
    events = db.query(
        Event.id,
        Event.id_user,
        Event.id_room,
        Event.start_date,
        Event.end_date,
        Event.description,
        Event.confirmation,
        Users.first_name,
        Users.last_name,
        Rooms.number.label("room_number")
    ).select_from(Event) \
    .outerjoin(Rooms, Rooms.id == Event.id_room) \
    .outerjoin(Users, Users.id == Event.id_user) \
    .filter(Event.start_date > current_time) \
    .filter(Event.confirmation == True) \
    .order_by(Event.start_date.asc()) \
    .limit(10) \
    .all()

    return templates.TemplateResponse(
        request = request,
        name = "events_log.html",
        context = {
            "request": request,
            "events": events,
            "title": "ღონისძიებები" 
        }
    )
           

@router.post("/create")
def create_reservation(
    id: int = Form(None),
    room_id: int = Form(...),
    user_id: int = Form(...),
    start_date: datetime = Form(...),
    end_date: datetime = Form(...),
    description: str = Form(...),
    db: Session = Depends(get_db)
):

    if id:
        db_event = db.query(Event).filter(Event.id == id).first()
        #if not db_event:
        #    raise HTTPException(status_code=404, detail="ოთახი ვერ მოიძებნა")
        
        db_event.id_room = room_id
        db_event.id_user = user_id
        db_event.start_date = start_date
        db_event.end_date = end_date        
        db_event.description = description
       
    else:

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


@router.get("/delete/{event_id}")
async def room_delete(
    event_id: int, 
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.id == event_id).first()

    if event:
        db.delete(event)
        
    db.commit()

    return RedirectResponse(url="/dashboard", status_code=303)


@router.get("/confirmation/{event_id}")
async def confirmation(
    event_id: int, 
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.id == event_id).first()
    
    event.confirmation = True

    db.commit()

    return RedirectResponse(url="/dashboard", status_code=303)