from toolkit import dbAlchemy

class Serp(dbAlchemy.Model):
    """Data model for user accounts."""

    __tablename__ = 'serp-keyword'
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
    pos = dbAlchemy.Column(
        dbAlchemy.Integer,
        index=False,
        unique=False,
        nullable=False
    )
    domain = dbAlchemy.Column(
        dbAlchemy.Text,
        index=True,
        unique=False,
        nullable=True
    )
    url = dbAlchemy.Column(
        dbAlchemy.Text,
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
        return '<Serp {}>'.format(self.query)
