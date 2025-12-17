# Passport Web Frontend

This is the web frontend for the Passport authentication system, built with Vue.js and Vite.

## Prerequisites

Before running the web frontend, ensure you have the following installed:
- Node.js (v23 or higher)
- npm or yarn
- Python environment with Django backend

## Setup Instructions

### 1. Backend Setup

First, ensure the Django backend is properly set up:

```bash
# Install Django and dependencies
pip install -r requirements.txt

# Set environment variables
export DRYCC_DATABASE_URL=postgres://postgres:@127.0.0.1:5432/passport
export VUE_APP_BASE_URL=http://localhost:8000/
export CSRF_TRUSTED_ORIGINS=http://localhost:5173

# Start the Django development server
python manage.py runserver
```

### 2. Frontend Setup

Navigate to the web directory and install dependencies:

```bash
cd web
npm install
```

### 3. Development Server

Start the development server:

```bash
npm run dev -- --port 5173
```

The application will be available at `http://localhost:5173`.

## Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm run preview` - Preview the production build
- `npm run lint` - Run ESLint

## Environment Variables

The following environment variables are required:

- `VUE_APP_BASE_URL` - The base URL of the Django backend API
- `CSRF_TRUSTED_ORIGINS` - Trusted origins for CSRF protection

## Project Structure

```
web/
├── public/          # Static assets
├── src/
│   ├── assets/      # Images and other assets
│   ├── components/  # Vue components
│   ├── views/       # Page components
│   ├── services/    # API service modules
│   ├── router/      # Vue Router configuration
│   ├── utils/       # Utility functions
│   └── lang/        # Internationalization
├── package.json     # Project dependencies
└── vite.config.js   # Vite configuration
```

## Contributing

Please refer to the main project documentation for contribution guidelines.
