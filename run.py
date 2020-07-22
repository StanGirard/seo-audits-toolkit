from toolkit import factory
import toolkit

if __name__ == "__main__":
    app = factory.create_app(celery=toolkit.celery)
    app.run()