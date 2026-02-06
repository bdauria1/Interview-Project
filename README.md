## Features

* **Defect Analysis**: Time-series visualization of defect counts with configurable grouping (hour, day, week).
* **Machine Performance Metrics**: Tracking of average cycle times, injection pressures, and barrel temperatures.
* **Defect Distribution**: Categorical breakdown of defect types (e.g., flash, short mold, contamination).

## Tech Stack

* **Frontend**: Vue 3, Typescript, Tailwind CSS.
* **Backend**: Python, FastAPI, SQLAlchemy.
* **Database**: PostgreSQL.

## Getting Started

### 1. Backend Setup
1.  **Navigate to the server directory**:
    ```bash
    cd Backend
    ```
2.  **Set the Dataset/Database URL**:
    Create the database and a `.env` file in the backend root:
    ```env
    DATABASE_URL=postgresql://user:password@localhost:5432/krevera_db
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Initialize Database & Ingest Data**:
    Run the following scripts in order to set up your tables and populate the dataset:
    ```bash
    # 1. Create the database tables
    python -m app.scripts.create_tables
    
    # 2. Ingest the product inspection data
    python -m app.scripts.ingest_data
    ```
5.  **Start the API server**:
    ```bash
    uvicorn app.main:app --reload
    ```

### 2. Frontend Setup
1.  **Navigate to the client directory**:
    ```bash
    cd Frontend
    ```
2.  **Set the API connection**:
    Create a `.env` file in the frontend root:
    ```env
    VITE_API_URL=http://127.0.0.1:8000
2.  **Install Dependencies**:
    ```bash
    npm install
    ```
3.  **Start the development server**:
    ```bash
    npm run dev
    ```
