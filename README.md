# AURA Web App (Beta)

AURA is a context-aware, memory-driven AI assistant for learners and neurodivergent minds. Built with React, Tailwind CSS, Supabase, and Stripe.

## Features
- Modern, glassy web3 UI
- User authentication (Supabase)
- Reminders & checkpoints
- Stripe payments (beta discount)
- Ad slots (placeholder)

## Getting Started

### 1. Frontend Setup

1.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```
2.  **Set up Environment Variables:**
    -   Copy the `.env.example` file to a new file named `.env`.
    -   Fill in the required frontend variables (VITE_*).
3.  **Run the Frontend:**
    ```bash
    npm run dev
    ```

### 2. Backend Setup

1.  **Create a Python Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up Environment Variables:**
    -   Ensure your `.env` file in the root directory contains the backend variables (e.g., `JWT_SECRET`, `SERVICE_USER_ID`).
4.  **Run the Backend:**
    ```bash
    cd backend
    uvicorn main:app --reload --port 9000
    ```

## Project Structure
- `src/` – Frontend React application
- `backend/` – Backend FastAPI application
- `aura_agent.py` – Core AI agent logic
- `requirements.txt` – Python dependencies
- `package.json` – Node.js dependencies

## License
MIT