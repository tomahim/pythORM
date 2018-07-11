# Pythorm

Pythorm project intends to create a minimalist ORM-like library. 

For now, data are kept in memory, but other persistence units can be implemented in the future, as the data access strategy

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

The unit tests cover the core features of the project and some mo From the root of the project run

```
python -m unittest discover tests
```

### Usage

To get a complete tour of the implemented features, just run :

```
python main.py
```

### API reference

##### Define a model by inheriting the abstract Base class

```
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

    // define getter and setter ...
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

```
# creation
discussion1 = Discussion(
    title='Discussion title'
).persist()

post1 = Post(
    discussion_id=
    text='My post cotnent'
).persist()

# update
post1.text = 'My post content'

updated_post = post1.persist()

# delete
updated_post.delete()
```

### @permissions_check decorator

To add some permission control for a specific action, you can use the @permissions_check decorator : 

```
@permissions_check(PermissionType.REMOVE_POST)
def remove():
    ... implementation 
```

See the `User.set_global_permissions(permissions)` in the models package to set the user permissions.

##### Reply to a post

```
post1.reply_with_post(post2)

post1.reply_with_post(post3)

post2.reply_with_post(post4)
```

##### Get all the children posts

```
children_posts = post1.get_all_children_posts()

# children_posts is a list containing post2, post3 and post4
```

##### Print the posts hierarchy

```
post.print_all_posts()

# prints the following result :

Post 1
    Post 2
        Post 4
    Post 3
```

### Possible improvements

* Use the `foreign_key` attribute of a `Column` to fetch linked data (relations between Discussion, posts and ideas) with functions like `discussion.fetch(Post)`.



