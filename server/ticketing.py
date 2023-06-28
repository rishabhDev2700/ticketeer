from flask import Blueprint, request, jsonify

from server.models import Ticket
from server.models import db

ticketing = Blueprint('ticketing',__name__,url_prefix='/tickets')

#done!!
@ticketing.get('/all')
def get_tickets():
    tickets = Ticket.query.all()
    response = []
    for ticket in tickets:
        t = {'id':  ticket.id, 'title':ticket.title, 'description':ticket.description,'created_on':ticket.created_on,'created_by':ticket.created_by,'assigned_to':ticket.assigned_to}
        response.append(t)
    return jsonify(response)


#done!!
@ticketing.get('/<int:id>')
def get_ticket(id):
    try:
        ticket = db.get_or_404(Ticket,id)
    except:
        return jsonify({'message':'Error Occurred!'})
    response = {'id':  ticket.id, 'title':ticket.title, 'description':ticket.description,'created_on':ticket.created_on,'created_by':ticket.created_by,'assigned_to':ticket.assigned_to}
    return jsonify(response)


#   somewhat done
@ticketing.post('/create')
def create_ticket():
    data = request.get_json()
    title = data['title']
    description = data['description']
    ticket = Ticket(title=title, description=description,created_by=None,)
    return jsonify()

# done!!
@ticketing.post('/resolved')
def resolved_ticket():
    id = request.get_json()['id']
    try:
        ticket = db.get_or_404(Ticket,id)
    except:
        return jsonify({'message':'Error Occurred!'})
    ticket.is_resolved = True
    db.session.commit()
    return jsonify({'message':'Marked as resolved!'})

# done!!
@ticketing.post('/delete')
def delete_ticket():
    id = request.get_json()['id']
    try:
        ticket = db.get_or_404(Ticket,id)
        db.session.delete(ticket)
        db.session.commit()
    except:
        return jsonify({'message':'Ticket deletion Failed'})

    return jsonify({'message':'Ticket deleted successfully'})

@ticketing.post('/update')
def update_ticket():
    data = request.get_json()
    id = data['id']
    try:
        ticket = db.get_or_404(Ticket,id)
    except:
        return jsonify({'message':'Ticket deletion Failed'})
    title = data['title']
    description = data['description']
    ticket.title = title
    ticket.description = description
    db.session.commit()
    return jsonify({'message':'Ticket updated successfully'})