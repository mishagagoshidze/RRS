import os

from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Rooms, RoomAdmin
from app.utils.security import get_current_user

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter(prefix="/room", tags=["room"])
#router = APIRouter(tags=["room"])


def require_super_admin(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    current_user = get_current_user(token, db)
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not current_user.super_admin:
        raise HTTPException(status_code=403, detail="Forbidden")

    return current_user


@router.post("/save")
async def save_room(
    request: Request,
    id: int = Form(None),
    number: str = Form(...),
    floor: int = Form(...),
    description: str = Form(None),
    user_id: int = Form(None),
    db: Session = Depends(get_db)
):
    require_super_admin(request, db)
    if id:
        db_room = db.query(Rooms).filter(Rooms.id == id).first()
        if not db_room:
            raise HTTPException(status_code=404, detail="ოთახი ვერ მოიძებნა")
        
        db_room.number = number
        db_room.floor = floor
        db_room.description = description

        db_room_admin = db.query(RoomAdmin).filter(RoomAdmin.id_room == id).first()
        if db_room_admin:
            db_room_admin.id_user = user_id
        else:
            new_room_admin = RoomAdmin(id_room=id, id_user=user_id)
            db.add(new_room_admin)
        
    else:
        new_room = Rooms(
            number = number,
            floor = floor,
            description = description
        )
        db.add(new_room)
        db.flush()
        
        new_room_admin = RoomAdmin(id_room=new_room.id, id_user=user_id)
        db.add(new_room_admin)

    db.commit()

    return RedirectResponse(url="/dashboard", status_code=303)


@router.get("/delete/{room_id}")
async def room_delete(
    room_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    require_super_admin(request, db)
    db.query(RoomAdmin).filter(RoomAdmin.id_room == room_id).delete(synchronize_session=False)

    room = db.query(Rooms).filter(Rooms.id == room_id).first()
    if room:
        db.delete(room)
        
    db.commit()

    #return {"status": "success"}
    return RedirectResponse(url="/dashboard", status_code=303)