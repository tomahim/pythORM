from core.base import Base
from core.column import Column, ColumnType
from datetime import datetime


class Discussion(Base):
    """This describes the model for a Discussion.
       Discussion contains Ideas and Posts.
    """
    model_name = 'discussion'

    name = Column('name', ColumnType.STRING)
    title = Column('title', ColumnType.STRING)
    creation_date = Column('creation_date', ColumnType.DATETIME)


if __name__ == "__main__":
    discussion1 = Discussion(
        name='Discussion about environmental issues',
        title='How to deal with the environmental issue caused by cars ?',
        creation_date=datetime.now()
    )
