from models import Ticket
from flask import session

def error_flashing(error, error_type):
    if error == False:
        error_type = "None"
        return error, error_type
    else:
        error = True
        error_type = error_type
        return error, error_type
    
def ticket_lookup():
    ticketid = session["ticket2"]
    ticket = Ticket.query.filter_by(id=ticketid).first()
    return ticket