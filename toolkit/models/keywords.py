from toolkit import dbAlchemy

class Keywords(dbAlchemy.Model):
    """Data model for user accounts."""

    __tablename__ = 'keywords'
    id = dbAlchemy.Column(
        dbAlchemy.Integer,
        primary_key=True
    )
    query_text = dbAlchemy.Column(
        dbAlchemy.String(64),
        index=True,
        unique=True,
        nullable=False
    )
    results = dbAlchemy.Column(
        dbAlchemy.Integer,
        index=False,
        unique=False,
        nullable=False
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
   

    def __repr__(self):
        return '<Keywords {}>'.format(self.query)