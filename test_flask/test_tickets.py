from flask.testing import FlaskClient
from app import models as m, db
from config import config

CFG = config()


def test_get_all_tickets(client_with_data: FlaskClient):
    client = client_with_data
    response = client.get("/tickets/")
    assert response.status_code == 200

    # get tickets by location
    location = m.Location.first()
    assert location
    response = client.get(f"/tickets/?location={location.name}")
    assert response.status_code == 200

    # get tickets by dates
    all_ticket_dates = sorted({ticket.event.date_time.date() for ticket in m.Ticket.all()})
    date_from = all_ticket_dates[1].strftime(CFG.DATE_PICKER_FORMAT)
    date_to = all_ticket_dates[5].strftime(CFG.DATE_PICKER_FORMAT)
    res = client.get(f"/tickets/?date_from={date_from}&date_to={date_to}")
    assert res.status_code == 200

    # get tickets by categories
    categories = m.Category.all()
    assert categories
    res = client.get(f"/tickets/?categories={categories[1].name}&categories={categories[2].name}")
    assert res.status_code == 200
    stmt = (
        m.Ticket.select()
        .filter(m.Ticket.event.has(m.Event.category.has(m.Category.name.in_((categories[1].name, categories[2].name)))))
        .limit(CFG.TICKETS_PER_PAGE)
    )
    for t in m.all(stmt):
        ticket: m.Ticket = t
        assert f"TICKET_ID:{ticket.unique_id}" in res.text

    #  get tickets next page
    LIMIT = 17
    res = client.get(f"/tickets/?tickets_per_page={LIMIT}")
    assert res.status_code == 200
    stmt = m.Ticket.select().limit(LIMIT + CFG.TICKETS_PER_PAGE)
    for t in m.all(stmt):
        tt: m.Ticket = t
        assert f"TICKET_ID:{tt.unique_id}" in res.text


def test_get_ticket(client_with_data: FlaskClient):
    client = client_with_data
    ticket: m.Ticket = db.session.scalar(m.Ticket.select())
    assert ticket
    response = client.get(f"/tickets/{ticket.unique_id}")
    assert response.status_code == 200
    assert f"{ticket.event.name}" in response.text
    assert f"{ticket.event.location.name}" in response.text
    assert f"{ticket.event.venue}" in response.text
    assert f"{ticket.description}" in response.text
