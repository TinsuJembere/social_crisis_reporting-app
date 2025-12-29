# Community Crisis Reporting Platform - Frontend

Next.js frontend for the Community Crisis Reporting & Response Platform.

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

Edit `.env.local` and set:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Project Structure

```
frontend/
├── components/       # Reusable React components
├── pages/           # Next.js pages (routes)
├── styles/          # Global styles and Tailwind CSS
├── utils/           # Utility functions (API client, auth helpers)
└── public/          # Static assets
```

## Features

- 🎨 Tailwind CSS for styling
- 🔐 JWT Authentication
- 📍 Map integration with Leaflet
- 📱 Responsive design
- 🔔 Toast notifications
- 📊 Dashboard for users
- 🗺️ Interactive map view

## Tech Stack

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Leaflet** - Maps
- **React Hot Toast** - Notifications

