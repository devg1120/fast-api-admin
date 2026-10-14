# FastAPI Photo API Project

A modern FastAPI application for uploading, compressing, storing, and serving photos with a secure admin dashboard and protected public API endpoints.

This project combines:
- image compression to a target size range from 1KB to 100KB
- admin authentication and secure dashboard
- anti-abuse / anti-scraping security middleware
- JSON and image API endpoints
- SQLite fallback with MySQL-ready configuration
- Docker and Docker Compose setup for local or server deployment

## Features

### Admin features
- Secure admin login page
- Upload photos through the dashboard
- Compress images automatically to a selected target size
- View uploaded photos in a gallery/lightbox interface
- Remove photos and manage blocked IPs

### API features
- `GET /api/v1/photo/random?api_key=...` to download a random photo
- `GET /api/v1/photo/random/json?api_key=...` to receive Base64 image data
- `GET /api/v1/photo/{photo_id}?api_key=...` to fetch a specific photo

### Security features
- API key validation
- rate limiting / request throttling
- blocked IP tracking
- scanner and malicious payload detection
- SQL injection pattern checks

## Tech stack

- FastAPI
- SQLAlchemy
- SQLite / MySQL
- Pillow
- Jinja2
- Docker

## Project structure

```text
fastAPI_project/
├── app/
│   ├── config.py
│   ├── database.py
│   ├── image_utils.py
│   ├── models.py
│   ├── security.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
├── uploads/
├── .dockerignore
├── .env.example
├── .gitignore
├── adminkey.txt
├── apikey.txt
├── COMMANDS.md
├── Dockerfile
├── docker-compose.yml
├── main.py
├── requirements.txt
├── README.md
├── data.json
└── main.py
```

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/mahadihasan9/fastAPI_project.git
cd fastAPI_project
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python main.py
```

Or with Uvicorn:

```bash
uvicorn main:app --reload --port 8000
```

### 5. Open the app

- Admin dashboard: http://127.0.0.1:8000/
- API docs: http://127.0.0.1:8000/docs

## Default credentials

The project reads keys from local files:

- `adminkey.txt` for admin password
- `apikey.txt` for API access key

Default values:

```text
admin
```

You can change these files anytime, or override them through environment variables if you are deploying with Docker or a VPS.

## Environment variables

Copy `.env.example` to a real `.env` and update the values as needed.

Example:

```env
ADMIN_PASSWORD=admin
API_KEY=admin
DATABASE_URL=sqlite:///./app.db
```

## Docker

Build:

```bash
docker build -t fastapi-photo-engine:latest .
```

Run:

```bash
docker run -d -p 8000:8000 --name photo_engine fastapi-photo-engine:latest
```

Or with Compose:

```bash
docker-compose up --build -d
```

## API examples

Random image:

```bash
curl "http://127.0.0.1:8000/api/v1/photo/random?api_key=admin" --output photo.jpg
```

Random JSON:

```bash
curl "http://127.0.0.1:8000/api/v1/photo/random/json?api_key=admin"
```

Specific photo:

```bash
curl "http://127.0.0.1:8000/api/v1/photo/<photo_id>?api_key=admin" --output photo.jpg
```

## License

This project is currently provided as a personal / demo application and does not include an explicit license file.

## Notes

For additional project commands and deployment steps, see the `COMMANDS.md` file.

---

Suggested repository description:

FastAPI photo compression service with secure admin dashboard, protected API endpoints, and Docker-ready deployment.
