# Event Scraper Project
This is for Future Demand
This project is a web scraper and web application that collects event information from a specific URL and displays it using a FastAPI server. The data is stored in a PostgreSQL database, and the application is containerized using Docker.

## Project Structure
.
├── main.py # The main FastAPI application
├── models.py # SQLAlchemy models
├── database.py # Database connection setup
├── events.html # HTML template for displaying events
├── docker-compose.yml # Docker Compose configuration
├── Dockerfile # Dockerfile for FastAPI app
├── requirements.txt # Python dependencies
└── .env # Environment variables


## Setup Instructions

### Prerequisites

1. **Docker**: Ensure you have Docker installed on your machine. You can download it from [Docker's official website](https://www.docker.com/get-started).
2. **Git**: Make sure you have Git installed to clone the repository. You can download it from [Git's official website](https://git-scm.com/downloads).

### Project Setup

1. **Clone the repository**:

   git clone <repository-url>

2. **Navigate to the project directory**:

   cd <project-directory>

3. **Create a `.env` file**:

   touch .env

4. **Add the following environment variables to the `.env` file**:

   DB_USER=postgres
   DB_PASSWORD=pedram38739197
   DB_NAME=postgres
   DB_HOST=localhost
   DB_PORT=5432

5. **Build and run the application using Docker**:

   docker-compose up --build

   The application will be accessible at `http://localhost:8000`.

### Usage

1. **Scrape Events**:

   Open `http://localhost:8000/scrape/` to scrape the events from the specified URL.

2. **View Events**:

   Open `http://localhost:8000/events/` to view the scraped events in a web page.

3. **Access Events Data**:

   Open `http://localhost:8000/events/data/` to get the scraped events data in JSON format.

### Development

If you want to contribute or modify the project, you can use the following commands for development:

1. **Install dependencies**:

   pip install -r requirements.txt

2. **Run the FastAPI server**:

   uvicorn main:app --reload

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

