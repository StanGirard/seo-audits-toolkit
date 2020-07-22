from toolkit import dbAlchemy
from sqlalchemy import UniqueConstraint

class LighthouseScore(dbAlchemy.Model):
    """Data model for user accounts."""

    __tablename__ = 'lighthouse-score'
    id = dbAlchemy.Column(
        dbAlchemy.Integer,
        primary_key=True
    )
    url = dbAlchemy.Column(
        dbAlchemy.String(256),
        index=True,
        unique=False,
        nullable=False
    )
    accessibility = dbAlchemy.Column(
        dbAlchemy.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    pwa = dbAlchemy.Column(
        dbAlchemy.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    seo = dbAlchemy.Column(
        dbAlchemy.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    best_practices = dbAlchemy.Column(
        dbAlchemy.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    performance = dbAlchemy.Column(
        dbAlchemy.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    status_job = dbAlchemy.Column(
    dbAlchemy.String(20),
    index=False,
    unique=False,
    nullable=True,
    default="FINISHED"
    )
    begin_date = dbAlchemy.Column(
        dbAlchemy.DateTime,
        index=False,
        unique=False,
        nullable=False
    )
    

    def __repr__(self):
        return '<Audit {}>'.format(self.url)