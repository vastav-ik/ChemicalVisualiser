# Chemical Equipment Parameter Visualizer

<<<<<<< HEAD
A hybrid application for analyzing and visualizing chemical equipment data.

## features

- **Dual Frontend**: Web (React) and Desktop (PyQt5).
- **Data Analysis**: Upload CSV to analyze Pressure, Temperature, and Equipment Type distribution.
- **Visualization**: Interactive charts.
=======
A hybrid application (Web + Desktop) for analyzing and visualizing chemical equipment data.

## features

- **Dual Frontend**: Web (React) and Desktop (PyQt5) clients.
- **Data Analysis**: Upload CSV to analyze Pressure, Temperature, and Equipment Type distribution.
- **Visualization**: Interactive charts (Chart.js for Web, Matplotlib for Desktop).
>>>>>>> 005a5118d8a91a8356cf366e6e2799e5ca399b87
- **History**: View last 5 uploaded datasets.
- **Raw Data**: Inspect raw CSV data in tabular format.
- **PDF Reports**: Download analysis reports.
- **Authentication**: Secure login (Token-based).

## Prerequisites

- Python 3.8+
- Node.js & npm

## Setup Instructions

### 1. Backend (`backend_core`)

1.  Navigate to the backend directory:
    ```bash
    cd backend_core
    ```
2.  Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install django djangorestframework django-cors-headers reportlab pandas pyqt5 matplotlib requests
    ```
4.  Run migrations:
    ```bash
    python manage.py migrate
    ```
5.  Create a superuser (admin):
    ```bash
    python create_superuser.py
<<<<<<< HEAD
=======
    # Or manually: python manage.py createsuperuser
>>>>>>> 005a5118d8a91a8356cf366e6e2799e5ca399b87
    ```
6.  Start the server:
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000`.

### 2. Web Frontend (`web_frontend`)

1.  Navigate to the frontend directory:
    ```bash
    cd web_frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm start
    ```
    The web app will open at `http://localhost:3000`. Login with your superuser credentials.

### 3. Desktop App

1.  Ensure the backend server is running.
2.  Navigate to the backend directory (where `desktop_app` folder is located):
    ```bash
    cd backend_core
    ```
3.  Run the desktop application:
<<<<<<< HEAD

    ```bash
    python desktop_app/main.py

    ```

4.  Login with superuser credentials.
    ```bash
       Username: `admin`
       Password: `password123`
    ```

## Sample Data

Used `sample_equipment_data.csv` or any CSV with columns: `Type`, `Pressure`, `Temperature`, `Flowrate`.
=======
    ```bash
    python desktop_app/main.py
    ```
4.  Login with your superuser credentials.

## Sample Data

Use `sample_equipment_data.csv` (if provided) or any CSV with columns: `Type`, `Pressure`, `Temperature`, `Flowrate`.
>>>>>>> 005a5118d8a91a8356cf366e6e2799e5ca399b87
