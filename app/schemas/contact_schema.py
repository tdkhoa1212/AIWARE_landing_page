# app/schemas/contact_schema.py
from pydantic import BaseModel

class ContactForm(BaseModel):
    firstName: str
    lastName: str
    email: str
    company: str = None
    phone: str
    role: str = None
    selectField: str
    message: str
