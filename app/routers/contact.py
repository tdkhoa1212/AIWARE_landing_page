from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from app.Database import SessionLocal
from fastapi.templating import Jinja2Templates
from app.schemas.contact_schema import ContactForm
from app.models.Contact import Contact
from sqlalchemy.orm import Session
from fastapi import FastAPI, Form
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(first_name, last_name, email, company, phone, role, select_field, message):
    from_email = "AIWARE.ai.tech@gmail.com"
    from_password = "xmaf glwn ndls qokw"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = "tdkhoa1212@gmail.com"
    msg['Subject'] = "New AIWARE Contact"

    body = f"First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nCompany: {company}\nPhone: {phone}\nRole: {role}\nField: {select_field}\n\nMessage: \n{message}"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    server.sendmail(from_email, email, msg.as_string())
    server.quit()


router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/Contact", response_class=HTMLResponse)
async def read_contact(request: Request):
    return templates.TemplateResponse("Contact.html", {"request": request})

# @router.post("/Contact", response_class=HTMLResponse)
# async def submit_contact(request: Request, 
#                          firstName: str = Form(...), 
#                          lastName: str = Form(...), 
#                          email: str = Form(...),
#                          company: str = Form(...),
#                          phone: str = Form(...),
#                          role: str = Form(...),
#                          selectField: str = Form(...),
#                          message: str = Form(...),
#                          db: Session = Depends(get_db)):
    
#     contact = Contact(
#         first_name=firstName,
#         last_name=lastName,
#         email=email,
#         company=company,
#         phone=phone,
#         role=role,
#         select_field=selectField,
#         message=message
#     )

#     db.add(contact)

#     try:
#         db.commit()
#         db.refresh(contact)

#         send_email(firstName, lastName, email, company, phone, role, selectField, message)
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

#     return templates.TemplateResponse("Contact.html", {"request": request})

@router.post("/Contact", response_class=HTMLResponse)
async def submit_contact(request: Request, 
                         firstName: str = Form(...), 
                         lastName: str = Form(...), 
                         email: str = Form(...),
                         company: str = Form(...),
                         phone: str = Form(...),
                         role: str = Form(...),
                         selectField: str = Form(...),
                         message: str = Form(...)):
    
    try:
        # Send email
        send_email(firstName, lastName, email, company, phone, role, selectField, message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return templates.TemplateResponse("Contact.html", {"request": request})
