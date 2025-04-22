# Stage 1: Build the Vue.js frontend
FROM node:18-alpine AS build-frontend

# Set working directory for frontend build
WORKDIR /app/frontend

# Copy package files and install dependencies
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install --ci

# Copy the rest of the frontend source code
COPY frontend/ ./

# Build the frontend application
RUN npm run build

# Stage 2: Setup Python backend and serve the application
FROM python:3.9-slim

# Set working directory for the application
WORKDIR /app

# Install system dependencies if needed (e.g., for certain Python packages)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend/ ./backend/

# Copy the built frontend assets from the build stage
COPY --from=build-frontend /app/frontend/dist ./backend/dist

# Create the instance directory for the SQLite database
# Note: Data stored here will be lost when the container stops unless a volume is used.
RUN mkdir -p backend/instance

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
# We use Gunicorn for a more production-ready setup than Flask's built-in server
# Install Gunicorn first
RUN pip install --no-cache-dir gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "backend.app:app"]

# If you prefer Flask's development server (not recommended for production):
# CMD ["python", "backend/app.py"]
