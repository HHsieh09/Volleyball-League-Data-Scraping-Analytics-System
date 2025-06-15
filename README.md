# Volleyball League Data Scraping & Analytics System

![GitHub repo size](https://img.shields.io/github/repo-size/HHsieh09/Volleyball-League-Data-Scraping-Analytics-System) ![GitHub contributors](https://img.shields.io/github/contributors/HHsieh09/Volleyball-League-Data-Scraping-Analytics-System) ![GitHub issues](https://img.shields.io/github/issues/HHsieh09/Volleyball-League-Data-Scraping-Analytics-System)

This project is a distributed web scraping and data analytics system for collecting, processing, and analyzing volleyball league data. It is designed to automate the extraction of structured match data—including teams, players, scores, coaches, and referees—from official websites and store it in a MySQL database for further analysis. It supports distributed crawling using **Celery**, **RabbitMQ**, and **BeautifulSoup**, and is extensible for real-time sports analytics applications.

## Features

- **Web Scraper**: Efficiently scrapes data from volleyball league match pages.
- **MySQL Database**: Stores cleaned and normalized match data in a structured schema.
- **Distributed Processing**: Uses **Celery** and **RabbitMQ** to scale scraping tasks.
- **Analytics Ready**: Data is pre-processed and ready for visualization or model training.
- **Match Type Handling**: Automatically distinguishes and adapts to match types (e.g., playoffs, challenge rounds).
- **Modular Architecture**: Easily extendable to support additional sports or new data sources.

## Project Structure

## TODOs
- [ ] Add user-facing web dashboard (Flask--------)
- [ ] Integrate ML model for match outcome prediction
- [ ] Improve scraping robustness with retry logic
- [ ] Dockerize full system for easier deployment

## Tech Stack

- **Python** (BeautifulSoup, requests, pandas)
- **MySQL** (Structured data storage)
- **Celery** + **RabbitMQ** (Distributed scraping tasks)
- **Jupyter Notebooks** (Data exploration & visualization)

## Database Schema Overview

Key entities include:

- `Team`, `Player`, `Match`, `Score`, `Referee`, `Coach`
- Relationships normalized to avoid redundancy (3NF)
- Supports match-specific metadata like date, location, and type

## How to Run

1. **Clone the repo**:
   ```bash
   git clone https://github.com/HHsieh09/Volleyball-League-Data-Scraping-Analytics-System.git
   cd Volleyball-League-Data-Scraping-Analytics-System

To be Announced.....