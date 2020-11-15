from toolkit import factory
import toolkit
from flask_cors import CORS


if __name__ == "__main__":
    app = factory.create_app(celery=toolkit.celery)
    CORS(app)

    app.run(host='0.0.0.0')