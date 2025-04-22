# Coffee Tracker

A web application to track coffee consumption and brewing methods.

## Project Structure

The project is divided into two main parts:

### Backend (Flask)

Located in the `backend/` directory, contains:
- Flask application
- SQLite database
- API endpoints

### Frontend (Vue.js)

Located in the `frontend/` directory, contains:
- Vue.js application
- Components
- Assets

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask application:
```bash
flask run
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

## Development

- Backend runs on: http://localhost:5000
- Frontend runs on: http://localhost:5173
