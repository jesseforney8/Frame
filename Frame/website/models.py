from __init__ import db  
from flask_login import UserMixin
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship



class Base(DeclarativeBase):
  pass

class User(db.Model, UserMixin):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    password: Mapped[str]
    role: Mapped[str]
    org: Mapped[str]
    


class Ticket(db.Model):
    __tablename__ = "ticket_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    body: Mapped[str]
    urgency: Mapped[str]
    type: Mapped[str]
    owner: Mapped[str]
    submitter: Mapped[str]
    group: Mapped[str]
    status: Mapped[str]
    comments: Mapped[str] 
    org: Mapped[str]      
    group_id: Mapped[int] = mapped_column(ForeignKey("group_table.id"))
    group: Mapped["Group"] = relationship(back_populates="ticket")

class Group(db.Model):
    __tablename__ = "group_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    org: Mapped[str]
    
    ticket: Mapped["Ticket"] = relationship(back_populates="group")




roles = {"r": "Reader", "e": "Editor", "a": "Administrator", "sa": "Super Administrator"}

