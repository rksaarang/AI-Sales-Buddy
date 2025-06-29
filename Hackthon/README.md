# AI-Powered Sales Buddy

## Overview

The AI Sales Buddy is a Flask-based web application designed to help sales teams capture, analyze, and act on sales-related information using AI-driven insights.

This project was developed for the "Reimagining Sales with AI" Hackathon organized by QA Catalyst.

The tool helps sales representatives and leadership teams streamline meeting notes, track client sentiments, monitor the sales pipeline, and stay informed about industry trends.


## Core Features

### 1. Internal Sales Activity Reporter
- Chat-like form to log:
  - Client meeting notes
  - Sentiment analysis (powered by OpenAI GPT API)
  - Sales opportunities and proposal status
- Auto-calculates and displays:
  - Total clients
  - Number of visits
  - Proposals given
  - Total estimated sales
- Dashboard view for recent activities and analytics

### 2. Market & Industry Insights Engine
- Fetches company-specific business insights using OpenAI GPT
- Provides:
  - Latest developments
  - Competitors
  - Market trends
  - Opportunities and risks
- Exposes an API endpoint for Company Insights (returns JSON)
- Simple UI page for viewing market insights


## Tech Stack

- Backend: Python Flask, SQLAlchemy, SQLite
- Frontend: HTML, CSS (Jinja Templates)
- AI Integration: OpenAI GPT-3.5/4 API (ChatCompletion API)
- Authentication: Flask-Login (with JWT-ready configuration)
- Visualization: Jinja-based Dashboard Views



