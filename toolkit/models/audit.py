from toolkit import dbAlchemy
from sqlalchemy import UniqueConstraint

class Audit(dbAlchemy.Model):
    """Data model for user accounts."""

    __tablename__ = 'audit'
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
    result = dbAlchemy.Column(
        dbAlchemy.Text,
        index=False,
        unique=False,
        nullable=True
    )
    type_audit = dbAlchemy.Column(
    dbAlchemy.String(20),
    index=False,
    unique=False,
    nullable=True
    )
    task_id = dbAlchemy.Column(
    dbAlchemy.String(40),
    index=False,
    unique=False,
    nullable=True,
    )
    status_job = dbAlchemy.Column(
    dbAlchemy.String(20),
    index=False,
    unique=False,
    nullable=True
    )
    begin_date = dbAlchemy.Column(
        dbAlchemy.DateTime,
        index=False,
        unique=False,
        nullable=False
    )
    __table_args__ = (UniqueConstraint('url', 'type_audit', name='url_audit_type'),)
   

    def __repr__(self):
        return '<Audit {}>'.format(self.url)