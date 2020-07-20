"""App entry point."""
from toolkit import create_app

app,celery = create_app()

if __name__ == "__main__":
    app.celery = celery
    app.run(host='0.0.0.0', port=5000)