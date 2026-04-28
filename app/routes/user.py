import os

from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Users, RoomAdmin
from app.utils.security import hash_password

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter(prefix="/user", tags=["user"])
#router = APIRouter(tags=["user"])


@router.post("/save")
async def user_save(
    id: str = Form(None),
    email: str = Form(None), 
    password: str = Form(None), 
    confirm_password: str = Form(None),
    first_name: str = Form(...),
    last_name: str = Form(...),
    telephone: str = Form(...),
    is_active: bool = Form(None),
    super_admin: bool = Form(None),
    db: Session = Depends(get_db)
):    
    if password:
        if password != confirm_password:
            raise HTTPException(status_code=400, detail="პაროლები არ ემთხვევა ერთმანეთს")

    if not is_active:
        is_active = False
    
    if not super_admin:
        super_admin = False

    email = email.lower()
    
    db_user = db.query(Users).filter(Users.id == id).first()
    
    if db_user:        
        db_user.email = email
        db_user.first_name = first_name
        db_user.last_name = last_name
        db_user.is_active = is_active
        db_user.super_admin = super_admin
        if password:
             db_user.password = hash_password(password),

    else:
        new_user = Users(
            email = email,
            password = hash_password(password),
            first_name = first_name,
            last_name = last_name,
            telephone = telephone,
            is_active = is_active,
            super_admin = super_admin 
        )

        db.add(new_user)
        #db.refresh(new_user)

    db.commit()
    
    return RedirectResponse(url="/dashboard", status_code=303)

@router.get("/delete/{user_id}")
async def user_delete(
    user_id: int, 
    db: Session = Depends(get_db)
):
    db.query(RoomAdmin).filter(RoomAdmin.id_user == user_id).delete(synchronize_session=False)

    user = db.query(Users).filter(Users.id == user_id).first()
    if user:
        db.delete(user)
        
    db.commit()

    #return {"status": "success"}
    return RedirectResponse(url="/dashboard", status_code=303)

@router.post("/profile")
async def profile(
    id: str = Form(None),
    email: str = Form(None), 
    password: str = Form(None), 
    confirm_password: str = Form(None),
    first_name: str = Form(...),
    last_name: str = Form(...),
    telephone: str = Form(...), 
    db: Session = Depends(get_db)
):    
    if password:
        if password != confirm_password:
            raise HTTPException(status_code=400, detail="პაროლები არ ემთხვევა ერთმანეთს")
   
    email = email.lower()
    
    db_user = db.query(Users).filter(Users.id == id).first()
    
    if db_user:        
        db_user.email = email
        db_user.first_name = first_name
        db_user.last_name = last_name
        db_user.is_active = False
        db_user.super_admin = False
        if password:
             db_user.password = hash_password(password),

    db.commit()
    
    return RedirectResponse(url="/dashboard", status_code=303)