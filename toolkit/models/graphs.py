from toolkit import dbAlchemy

class Graphs(dbAlchemy.Model):
    """Data model for user accounts."""

    __tablename__ = 'graphs'
    id = dbAlchemy.Column(
        dbAlchemy.Integer,
        primary_key=True
    )
    urls = dbAlchemy.Column(
        dbAlchemy.String(256),
        index=True,
        unique=True,
        nullable=False
    )
    script = dbAlchemy.Column(
        dbAlchemy.Text,
        index=False,
        unique=False,
        nullable=False
    )
    div = dbAlchemy.Column(
        dbAlchemy.Text,
        index=False,
        unique=False,
        nullable=False
    )
    status_job = dbAlchemy.Column(
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
    begin_date = dbAlchemy.Column(
        dbAlchemy.DateTime,
        index=False,
        unique=False,
        nullable=False
    )
   

    def __repr__(self):
        return '<Graphs {}>'.format(self.query)