# PythORM

PythORM project intends to create a minimalist ORM-like library. 

For now, data are kept in memory, but other persistence units can be implemented in the future.

### Table of content

* [Pre-requirements and installation](#pre-requirements-and-installation)
* [Run unit tests](#run-unit-tests)
* [Run main script](#run-main-script)
* [API reference](#api-reference)
* [Possible improvements](#possible-improvements)

### Pre-requirements and installation

This project requires the Python 2.7 version. It has only unittest as dependency.

To install it, run : 

```
pip install -r requirements.txt
```

### Run unit tests

From the root of the project run

```
python -m unittest discover tests
```

### Run main script

To get a complete tour of the implemented features, just run :

```
python main.py
```

### API reference

<div align="center">
 <img alt="diagram class" src="https://raw.githubusercontent.com/tomahim/pythorm/master/docs/diagram%20models.png" width="550"/>
</div>

##### Define a model by inheriting the abstract Base class

```python
from core.base import Base, Column, ColumnType

class Post(Base):

    # define the columns
    columns = [
        Column('id', ColumnType.STRING, primary_key=True),
        Column('discussion_id', ColumnType.STRING, foreign_key=True),
        Column('text', ColumnType.STRING),
        Column('creation_date', ColumnType.DATETIME)
    ]

    def __init__(self, text, creation_date=datetime.now(), **kwargs):
        super(Post, self).__init__(**kwargs)
        self._id = None
        self._text = text

    // define getters and setters ...
```

The Base class provide an access to the `DB` object, which contains some basic operations like `persist()`, `delete()`, `find_all()`, `find_by_id(id)` ... and more !

For the `InMemory` implementation of the `DB` object, models instances are stored in a simple dictionnary structured like this :

```
{
    'Discussion': [{... discussion1 ...}, {... discussion2 ...}],
    'Post': [{... post1 ... }],
    'User': [{... user1 ..., ... user2 ...}]
}
```

The model class name is used as the dictionnary key.

##### Add, update or delete data

```python
# creation
discussion1 = Discussion(
    title='Discussion title'
).persist()

post1 = Post(
    discussion_id=discussion1.id,
    text='My post cotnent'
).persist()

# update
post1.text = 'My post content'

updated_post = post1.persist()

# delete
updated_post.delete()
```

##### @permissions_check decorator

To add some permission control for a specific action, you can use the @permissions_check decorator : 

```python
@permissions_check(PermissionType.REMOVE_POST)
def remove():
    ... implementation 
```

See the `User.set_global_permissions(permissions)` in the models package to set the user permissions.

##### Reply to a post

```python
post1.reply_with_post(post2)

post1.reply_with_post(post3)

post2.reply_with_post(post4)
```

##### Get all the children posts

```python
children_posts = post1.get_all_children_posts()

# children_posts is a list containing post2, post3 and post4
```

##### Print the posts hierarchy

```python
post.print_all_posts()

# prints the following result :

Post 1
    Post 2
        Post 4
    Post 3
```

##### Associate an idea to a post

```python
idea = Idea(
    discussion_id='1234',
    title='The idea title',
    description='The idea description',
)

post1.associate_with_post(idea)
```

##### Associate an idea to another idea

```python
idea2.associate_to_idea(idea)
```

##### Other available methods for Idea model

The following methods are available too : `get_all_children_ideas()`, `number_of_messages()`, `number_of_participants()` and `print_all_ideas()`.


### Possible improvements

* Implement a User.set_local_permissions() : for example, we could consider PermissionType as a model and link it to the `User` and the `Discussion` model. So we 

* Implement these methods on the `Discussion` model :

    - `all_posts_associated_to_idea()` : get the posts associated to alteast one idea
    - `all_posts_not_associated_to_idea()` : get the posts not associated to an idea
    - `number_of_participants()` : total participants of a discussion

* Use the `foreign_key` attribute of a `Column` to fetch linked data (relations between Discussion, posts and ideas) with functions like `discussion.fetch(Post)`.
