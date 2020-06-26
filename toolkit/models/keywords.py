from toolkit import dbAlchemy

sql_create_keywords_table = """ CREATE TABLE IF NOT EXISTS keywords (
                                        id integer PRIMARY KEY,
                                        query text NOT NULL,
                                        results text NOT NULL,
                                        status_job text NOT NULL,
                                        begin_date text NOT NULL
                                );
                            """


class Keywords(dbAlchemy.Model):
    """Data model for user accounts."""

    __tablename__ = 'keyword'
    id = dbAlchemy.Column(
        dbAlchemy.Integer,
        primary_key=True
    )
    query = dbAlchemy.Column(
        dbAlchemy.String(64),
        index=True,
        unique=True,
        nullable=False
    )
    results = dbAlchemy.Column(
        dbAlchemy.Integer,
        index=False,
        unique=True,
        nullable=False
    )
    created = dbAlchemy.Column(
        dbAlchemy.DateTime,
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

    def __repr__(self):
        return '<Keywords {}>'.format(self.username)