# PostgreSQL Setup Guide (future enabling)

The code is pre-configured to work with **PostgreSQL**, which was our project scope.
*However*, to make it easy to start, we defaulted it to **SQLite** (a built-in file database).

---

## Step 1: Install PostgreSQL

1.  **Download**: Go to [postgresql.org/download/windows/](https://www.postgresql.org/download/windows/) and download the interactive installer.
2.  **Install**:
    *   Run the installer.
    *   **Password**: Remember the password you set for the `postgres` user (e.g., `root` or `admin`).
    *   **Port**: Keep default `5432`.
3.  **PgAdmin**: The installer usually includes **pgAdmin 4**. Open it to see your databases.

## Step 2: Create the Database

1.  Open **SQL Shell (psql)** (installed with Postgres) OR use **pgAdmin**.
2.  Run this SQL command to create the database:
    ```sql
    CREATE DATABASE gesture_db;
    ```

## Step 3: Connect Code to Postgres

1.  Open `backend/.env`.
2.  Find the `DATABASE_URL` line.
3.  **Comment out** the SQLite line and **Add** the Postgres line:

    ```ini
    # DATABASE_URL=sqlite:///./gesture_system.db  <-- Comment this out with #
    DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost/gesture_db
    ```
    *(Replace `YOUR_PASSWORD` with the one you set during installation)*

## Step 4: Verify

1.  Restart the backend:
    ```bash
    CTRL+C
    uvicorn main:app --reload
    ```
2.  If it starts without errors, you are now running on an Enterprise-Grade Database!
