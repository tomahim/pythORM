from models.discussion import Discussion
from models.idea import Idea
from models.post import Post
from models.user import User
from security.auth import UserSession
from security.permission import PermissionType


def init_users():
    john = User(
        username='john',
        email='john@company.com',
        password='1234',
    )
    john.set_global_permissions([
        PermissionType.READ_DISCUSSION,
        PermissionType.ADD_POST,
        PermissionType.ADD_IDEA,
        PermissionType.REMOVE_IDEA,
        PermissionType.REMOVE_IDEA,
        PermissionType.REMOVE_POST
    ])
    bob = User(
        username='bob',
        email='bob@company.com',
        password='4567'
    )
    bob.set_global_permissions([
        PermissionType.READ_DISCUSSION,
        PermissionType.ADD_POST,
        PermissionType.ADD_IDEA,
        PermissionType.REMOVE_IDEA,
        PermissionType.REMOVE_POST
    ])
    anna = User(
        username='anna',
        email='anna@company.com',
        password='789845'
    )
    anna.set_global_permissions([
        PermissionType.READ_DISCUSSION
    ])
    return [john, bob, anna]


def init_posts(discussion_id, user_bob_id, user_john_id, user_anna_id):
    return [
        Post(
            text='Post 1',
            discussion_id=discussion_id,
            creator_id=user_bob_id
        ).persist(),
        Post(
            text='Post 2 -> reply to post 1',
            discussion_id=discussion_id,
            creator_id=user_john_id
        ).persist(),
        Post(
            text='Post 3 -> Reply to post 1',
            discussion_id=discussion_id,
            creator_id=user_anna_id
        ).persist(),
        Post(
            text='Post 4 -> Reply to post 2',
            discussion_id=discussion_id,
            creator_id=user_anna_id
        ).persist(),
        Post(
            text='Post 5 -> Reply to post 4',
            discussion_id=discussion_id,
            creator_id=user_john_id
        ).persist(),
        Post(
            text='Post 6 -> Reply to post 2',
            discussion_id=discussion_id,
            creator_id=user_john_id
        ).persist(),
        Post(
            text='Post 7 to delete',
            discussion_id=discussion_id,
            creator_id=user_john_id
        ).persist()
    ]


def init_ideas(discussion_id, user_bob_id, user_john_id, user_anna_id):
    return [
        Idea(
            discussion_id=discussion_id,
            title="The parent idea about saving the environment",
            description="One idea to rule them all",
            creator_id=user_john_id
        ).persist(),
        Idea(
            discussion_id=discussion_id,
            title='Cars',
            description='We should avoid using cars',
            creator_id=user_bob_id
        ).persist(),
        Idea(
            discussion_id=discussion_id,
            title='Plane flights should be replace with boat trips',
            description='We should avoid using planes',
            creator_id=user_anna_id
        ).persist(),
        Idea(
            discussion_id=discussion_id,
            title="We should avoid helicopter flights",
            description="How about not using jet pack either",
            creator_id=user_anna_id
        ).persist()
    ]


def desc(msg):
    """ use to print a message in console describing the current action """
    print('*' * 4 + msg + '*' * 4)
    print('\n')


if __name__ == '__main__':
    desc('Init some users to work with')

    [user_john, user_bob, user_anna] = init_users()

    user_session = UserSession()

    desc('Connect with user bob, if not connected @permissions_check decorator will raise an exception')

    # create a fake user session
    user_session.connect(user_bob)

    desc('Create a discussion')

    discussion_environment = Discussion(
        name='Environmental issues',
        title='How to solve environmental issues ?',
        creator_id=user_anna.id
    ).persist()

    desc('Create posts')

    [post1, post2, post3, post4, post5, post6, post7] = \
        init_posts(discussion_environment.id, user_bob.id, user_john.id, user_anna.id)

    print('Nb of posts in the discussion : %s' % discussion_environment.number_of_posts())
    print('\n')

    desc('Create ideas')

    [parent_idea, idea_about_cars, idea_about_planes, idea_about_helicopter] = \
        init_ideas(discussion_environment.id, user_bob.id, user_john.id, user_anna.id)

    print('Nb of ideas in the discussion : %s' % discussion_environment.number_of_ideas())
    print('\n')

    desc('Update an idea with a more specific title')

    print('Title before update : %s' % idea_about_cars.title + '\n')

    idea_about_cars.title = 'Cars consume too much energy'

    idea_about_cars = idea_about_cars.persist()

    print('Title after update : %s' % idea_about_cars.title + '\n')

    desc('Delete a post')

    print('Nb of posts before delete : %s' % discussion_environment.number_of_posts())

    post7.delete()

    print('Nb of posts after delete : %s' % discussion_environment.number_of_posts())
    print('\n')

    desc('Add relationships between posts')

    post1.reply_with_post(post2)
    post1.reply_with_post(post3)
    post2.reply_with_post(post4)
    post4.reply_with_post(post5)
    post2.reply_with_post(post6)

    desc('Get all children ideas for the post 1')

    children_posts = post1.get_all_children_posts()

    for index, child in enumerate(children_posts):
        print('Child %s : %s' % (index+1, child.text))
    print('\n')

    desc('Representation of the posts hierarchy (idents mean that the post reply to the post to the top)')

    post1.print_all_posts()
    print('\n')

    desc('Add relationships between ideas')

    parent_idea.associate_to_idea(idea_about_cars)
    parent_idea.associate_to_idea(idea_about_planes)

    idea_about_planes.associate_to_idea(idea_about_helicopter)

    desc('Get all children ideas for the parent_idea')

    children_ideas = parent_idea.get_all_children_ideas()

    for index, child in enumerate(children_ideas):
        print('Child %s : %s' % (index+1, child.title))
    print('\n')

    desc('Representation of the ideas hierarchy')

    parent_idea.print_all_ideas()
    print('\n')

    desc('Associate posts with ideas')

    post6.associate_with_idea(parent_idea)
    post2.associate_with_idea(parent_idea)

    post1.associate_with_idea(idea_about_cars)
    post2.associate_with_idea(idea_about_cars)

    post3.associate_with_idea(idea_about_planes)
    post1.associate_with_idea(idea_about_planes)

    desc('Get number of messages for parent_idea')

    print('Nb of messages : %s' % parent_idea.number_of_messages() + '\n')

    desc('Get number of participants')

    print('Nb of participants : %s' % parent_idea.number_of_participants() + '\n')
