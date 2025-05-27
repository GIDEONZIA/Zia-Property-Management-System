# Zia-Property-Agency

A Django-based property management platform for handling real estate assets, agents, tenants leases, and rent payments.

## Features
- Property listing bt agents
- Lease and rent management
- Agent-specific data visibility
- Dynamic property types
- Admin Dashboard with analytics

## Installation

'''bash
git clone https://github.com/GIDEONZIA/Zia-Property-Management-System.git
cd Zia-Property-Management-System
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
