import os
import secrets

from fastapi import APIRouter, Depends, Form, Request, BackgroundTasks
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db.database import get_db
from app.db.models import Users, PasswordResetTokens, UsersTokens
from app.utils.security import hash_password, verify_password, create_token

from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.services.email_service import send_email

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login", response_class=HTMLResponse)
def login_page(
    request: Request
):
    return templates.TemplateResponse(
        request = request, 
        name = "auth/login.html", 
        context = {
            "title": "ავტორიზაცია"
        }
    )

@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)    
):
    
    email = email.lower()

    user = db.query(Users).filter(Users.email == email).first()
    
    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse(
            request = request, 
            name = "auth/login.html", 
            context = {
                "request": request,
                "title": "ავტორიზაცია", 
                "message": "მომხმარებელი ან პაროლი არასწორია"
            }
        )
          
    if not user.is_active:
        return templates.TemplateResponse(
            request = request, 
            name = "auth/login.html", 
            context = {
                "request": request, 
                "title": "ავტორიზაცია",
                "message": "მომხმარებელი არ არის გააქტიურებელი. შეამოწმეთ მეილი"
            }
        )
     
    token = create_token({"sub": user.email})
    response = RedirectResponse(url="/dashboard", status_code=303)
        
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/auth/login")
    response.delete_cookie("access_token")
    return response


# REGISTER
@router.get("/register", response_class=HTMLResponse)
def register_page(
    request: Request
):
    return templates.TemplateResponse(
        request = request, 
        name = "auth/register.html"
    )

@router.post("/register")
async def register(
    request: Request,
    background_tasks: BackgroundTasks,
    email: str = Form(...), 
    password: str = Form(...), 
    confirm_password: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    telephone: str = Form(...),
    db: Session = Depends(get_db)
):

    if password != confirm_password:
        return templates.TemplateResponse(
            request = request, 
            name = "auth/register.html", 
            context = {
                "request": request,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'telephone': telephone,
                "title": "რეგისტრაცია",
                "message": "პაროლები არ ემთხვევა"
            }
        )
     
    email = email.lower()

    user = db.query(Users).filter(Users.email == email).first()
    if user:
        return templates.TemplateResponse(
            request = request, 
            name = "auth/register.html", 
            context={
                "request": request,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'telephone': telephone,
                "title": "რეგისტრაცია",
                "message": "მომხმარებელი ამ მეილით უკვე არსებობს"
            }
        )

    new_user = Users(
        email = email,
        password = hash_password(password),
        first_name = first_name,
        last_name = last_name,
        telephone = telephone,
        is_active = False,
        super_admin = False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=1)

    users_entry = UsersTokens(
        email = email,
        token_hash = token
    )
    db.add(users_entry)
    db.commit()

    reset_link = f"http://127.0.0.1:8000/auth/activate-user?token={token}"
    
    html = f"""
    <p>მომხმარებლის გასააქტიურებლად დააჭირეთ ბმულს:</p>
    <a href="{reset_link}">{reset_link}</a>
    """

    background_tasks.add_task(send_email, "RRS", email, html)

    return templates.TemplateResponse(
        request = request, 
        name = "auth/login.html", 
        context={
            "request": request,
            "title": "ავტორიზაცია",
            "message": "რეგისტრაცია წარმატებულია! შეამოწმეთ ელ.ფოსტა."
        }
    )


@router.get("/activate-user", response_class=HTMLResponse)
async def activate_user_page(
    request: Request,
    token: str,
    db: Session = Depends(get_db)
):
    
    token_entry = db.query(UsersTokens).filter(UsersTokens.token_hash == token).first()
    
    if not token_entry:
        return templates.TemplateResponse(
            request = request, 
            name = "auth/error.html", # შექმენით შეცდომის გვერდი
            context = {
                "title": "",
                "message": "ტოკენი არასწორია ან ვადაგასულია"
            }
        )

    user = db.query(Users).filter(Users.email ==token_entry.email).first()
    
    if not user:
        return templates.TemplateResponse(
            request = request, 
            name = "auth/error.html", 
            context = {
                "request": request,
                "title": "", 
                "message": "მომხმარებელის მეილი არასწორია"
            }
        )
    
    user.is_active = True
    
    db.delete(token_entry)
    db.commit()

    return templates.TemplateResponse(
        request = request, 
        name = "auth/login.html",
        context = {
            "request": request, 
            "token": token,
            "title": "ავტორიზაცია",
        }
    )

# PASSWORD
@router.get("/forgot-password", response_class=HTMLResponse)
def forgot_password_page(
    request: Request
):
    return templates.TemplateResponse(
        request = request, 
        name = "auth/forgot_password.html", 
        context = {
            "request": request,
            "title": "პაროლის აღდგენა",
        }
    )


@router.post("/forgot-password")
async def process_forgot_password(
    request: Request,
    background_tasks: BackgroundTasks,    
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    
    email = email.lower()

    user = db.query(Users).filter(Users.email == email).first()

    if not user:
        return templates.TemplateResponse(
            request = request, 
            name = "auth/forgot_password.html", 
            context = {
                "request": request,
                "title": "პაროლის აღდგენა", 
                "message": "მომხმარებელის მეილი არასწორია"
            }
        )
    
    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=1) # ვადა 1 საათი

    reset_entry = PasswordResetTokens(
        id_user = user.id,
        token_hash = token,
        expires_at = expires
    )
    db.add(reset_entry)
    db.commit()

    reset_link = f"http://127.0.0.1:8000/auth/reset-password?token={token}"
    
    html = f"""
    <p>პაროლის აღსადგენად დააჭირეთ  ბმულს:</p>
    <a href="{reset_link}">{reset_link}</a>
    <p>ბმული ძალაშია 1 საათის განმავლობაში.</p>
    """
    
    background_tasks.add_task(send_email, "RRS", email, html)

    return templates.TemplateResponse(
        request = request, 
        name = "auth/login.html", 
        context = {
            "title": "ავტორიზაცია"
        }
    )



@router.get("/reset-password", response_class=HTMLResponse)
def reset_password_page(
    request: Request,
    token: str,
    db: Session = Depends(get_db)
):
    token_entry = db.query(PasswordResetTokens).filter(PasswordResetTokens.token_hash == token).first()
    
    if not token_entry or token_entry.expires_at < datetime.utcnow():
        return templates.TemplateResponse(
            request = request, 
            name = "auth/error.html",
            context = {
                "title": "",
                "message": "ტოკენი არასწორია ან ვადაგასულია"
            }
        )

    return templates.TemplateResponse(
        request = request, 
        name = "auth/reset_password.html",
        context = {
            "request": request, 
            "token": token
        }
    )


@router.post("/reset-password")
async def reset_password(
    request: Request,
    token: str = Form(...), 
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    
    if new_password != confirm_password:
       if new_password != confirm_password:
           return templates.TemplateResponse(
            request = request,
            name = "auth/reset_password.html",
            context = {
                "request": request,
                "token": token,
                "title": "პაროლის აღდგენა",
                "message": "პაროლები არ ემთხვევა ერთმანეთს"
            }
        )

    token_entry = db.query(PasswordResetTokens).filter(PasswordResetTokens.token_hash == token).first()
    
    if not token_entry:
        return templates.TemplateResponse(
            request = request,
            name = "auth/reset_password.html",
            context = {
                "request": request,
                "token": token,
                "title": "პაროლის აღდგენა",
                "message": "არასწორი ან ვადაგასული ტოკენი"
            }
        )
        
    user = db.query(Users).filter(Users.id == token_entry.id_user).first()
    if not user:
         return templates.TemplateResponse(
            request = request,
            name = "auth/reset_password.html",
            context = {
                "request": request,
                "token": token,
                "title": "პაროლის აღდგენა",
                "message": "მომხმარებელი ვერ მოიძებნა"
            }
        )

    user.password = hash_password(new_password)
    
    db.delete(token_entry)
    db.commit()

    return templates.TemplateResponse(
        request = request, 
        name = "auth/login.html", 
        context = {
            "title": "ავტორიზაცია"
        }
    )