# Drummerei - Timetable

Timetable App for Drummerei Open Decks Breakbeat Night at Gaengeviertel in Hamburg, Germany.

## Project Overview

This App allows attendees of Drummerei to select a slot of the time table to go on stage and spin some ruff tunes. 

Slots are 30min long by default. 8 Slots per night.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Features
- automatically creates/reads Cookies to distinguish visitors when they try to edit slots 
- automatically creates a PIN when Schedule is saved
- automatically creates a QR code from PIN

### TODO
- ORM: correct times of slots
- QR: correct data
- UI: click events and post requests
- UI: hold button layout

### Prerequisites

* Python 3.7+
* Django, qrcode, python-dotenv
* Virtual environment manager (venv recommended)
* SQLite

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/drummerei.git

2. install dependencies:
   ```bash
   python -m venv .venv
   pip install -r requirements.txt

3. run app with development server:
   ```bash
   python manage.py runserver
