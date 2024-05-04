import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db, init_db, Base, engine
from models import Event
from fastapi.templating import Jinja2Templates
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Lucerne Festival URL
url = "https://www.lucernefestival.ch/en/program/summer-festival-24"

# Create app
app = FastAPI()

# Setup HTML for table
current_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

# Create Startup event


@app.on_event("startup")
async def startup_event():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_db()

# Scraper Endpoint


@app.get("/scrape/")
async def scrape_events(db: Session = Depends(get_db)):
    response = requests.get(url)
    response.raise_for_status()  # Response Status

    soup = BeautifulSoup(response.text, 'html.parser')
    events_list = soup.find('ul', class_='event-list')

    if not events_list:
        raise HTTPException(status_code=404, detail="No events found.")

    events_data = []

    for event in events_list.find_all('div', class_='event-content'):

        # Scraping the Day of week, Date, Time and Location
        date_and_venue_element = event.find(
            'div', class_='cell xlarge-6 body-small')

        day_of_week, date, time, location = 'N/A', 'N/A', 'N/A', 'N/A'
        if date_and_venue_element:
            text = ' '.join(date_and_venue_element.text.split()
                            ).replace('Date and Venue', '').strip()
            parts = [part.strip() for part in text.split('|')]
            if len(parts) == 3:
                day_of_week, date = parts[0].split()
                date = date + "2024"  # Append the year to the date
                time, location = parts[1], parts[2]
                date_obj = datetime.strptime(date, "%d.%m.%Y")
                day_of_week = date_obj.strftime("%A")

        # Scraping the Title and Artist names
        title_element = event.find('p', class_='event-title')
        title, artists = 'Title not available', ['Artist not available']
        if title_element:
            parts = [part.strip() for part in title_element.text.split('|')]
            if parts:
                title = parts[0]
                artists = parts[1:]

        # Scraping the Works(Program)
        program_strong = event.find('strong', string='Program')
        works = []
        if program_strong and program_strong.parent:
            program_text = program_strong.parent.text.replace(
                'Program', '').strip()
            works = [work.strip() for work in program_text.split('|')]

        # Scraping the Event poster(Image)
        picture = event.find('picture')
        if picture and picture.find('source'):
            image_link = "https://www.lucernefestival.ch" + \
                picture.find('source')['srcset'].split(',')[0].split(' ')[0]
        else:
            image_link = 'No image available'

        events_data.append({
            'day_of_week': day_of_week,
            'date': date,
            'time': time,
            'location': location,
            'title': title,
            'artists': artists,
            'works': works,
            'image_link': image_link
        })

    # Storing data using SQLalchemy
    for event_data in events_data:
        time_string = event_data['time'].split(
            " / ")[0]  # Take the first time before '/'
        try:
            event_time = datetime.strptime(
                time_string, "%H.%M").time() if time_string != "N/A" else None
        except ValueError:
            event_time = None
        event = Event(day_of_week=event_data['day_of_week'], date=datetime.strptime(event_data['date'], "%d.%m.%Y").date(),
                      time=event_time, location=event_data['location'],
                      title=event_data['title'], artists=event_data['artists'],
                      works=event_data['works'], image_link=event_data['image_link'])
        try:
            db.add(event)
        except IntegrityError:
            db.rollback()
            continue

    db.commit()
    logging.info("Events scraped successfully.")
    return {"status": "Scraped successfully"}

# List of all Events endpoint with HTML Template


@app.get("/events/")
async def show_events_page(request: Request):
    return templates.TemplateResponse("events.html", {"request": request})

# Fetch all of the data in the database


@app.get("/events/data/")
async def get_events_data(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return [
        {
            "day_of_week": event.day_of_week,
            "date": event.date,
            "time": event.time.strftime("%H:%M") if event.time else "N/A",
            "location": event.location,
            "title": event.title,
            "artists": event.artists,
            "works": event.works,
            "image_link": event.image_link,
        }
        for event in events
    ]
