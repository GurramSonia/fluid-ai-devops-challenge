from fastapi import FastAPI, Response
import os
import psycopg2

app = FastAPI(title="Fluid AI DevOps Challenge")


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        database=os.getenv("POSTGRES_DB", "appdb"),
        user=os.getenv("POSTGRES_USER", "appuser"),
        password=os.getenv("POSTGRES_PASSWORD", "apppassword"),
        connect_timeout=3
    )


@app.get("/")
def root():
    return {
        "application": "Fluid AI DevOps Challenge",
        "status": "running"
    }


@app.get("/health/live")
def liveness():
    return {
        "status": "alive"
    }


@app.get("/health/ready")
def readiness(response: Response):
    try:
        connection = get_db_connection()
        connection.close()

        return {
            "status": "ready",
            "database": "connected"
        }

    except Exception:
        response.status_code = 503

        return {
            "status": "not ready",
            "database": "unavailable"
        }


@app.get("/db")
def database_check():
    try:
        connection = get_db_connection()
        connection.close()

        return {
            "database": "connected"
        }

    except Exception as e:
        return {
            "database": "connection failed",
            "error": str(e)
        }