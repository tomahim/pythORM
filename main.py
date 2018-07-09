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


def init_posts(discussion_id):
    return [
        Post(
            text='Post 1',
            discussion_id=discussion_id,
            creator_id=user_bob.id
        ).persist(),
        Post(
            text='Post 2 -> reply to post 1',
            discussion_id=discussion_id,
            creator_id=user_john.id
        ),
        Post(
            text='Post 3 -> Reply to post 1',
            discussion_id=discussion_id,
            creator_id=user_anna.id
        ).persist(),
        Post(
            text='Post 4 -> Reply to post 2',
            discussion_id=discussion_id,
            creator_id=user_anna.id
        ).persist(),
        Post(
            text='Post 5 -> Reply to post 4',
            discussion_id=discussion_id,
            creator_id=user_john.id
        ).persist(),
        Post(
            text='Post 6 without reply',
            discussion_id=discussion_id,
            creator_id=user_john.id
        ).persist(),
        Post(
            text='Post 7 to delete',
            discussion_id=discussion_id,
            creator_id=user_john.id
        ).persist()
    ]


def init_ideas(discussion_id):
    return [
        Idea(
            discussion_id=discussion_id,
            title="Great idea",
            description="One idea to rule them all",
            creator_id=user_john.id
        ).persist(),
        Idea(
            discussion_id=discussion_id,
            title='Cars',
            description='We should avoid using cars',
            creator_id=user_bob.id
        ).persist(),
        Idea(
            discussion_id=discussion_id,
            title='Planes',
            description='We should avoid using planes',
            creator_id=user_anna.id
        ).persist(),
        Idea(
            discussion_id=discussion_id,
            title="Jet pack",
            description="How about not using jet pack either",
            creator_id=user_anna.id
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

    desc('Connect with user bob, if not @permissions_check decorator will raise an exception')

    user_session.connect(user_bob)

    desc('Create a discussion')

    discussion_environment = Discussion(
        name='Environmental issues',
        title='How to solve environmental issues ?',
        creator_id=user_anna.id
    ).persist()


    desc('Create posts')

    [post1, post2, post3, post4, post5, post6, post7] = init_posts(discussion_environment.id)

    # create ideas
    [parent_idea, idea_about_cars, idea_about_planes, idea_about_jet_pack] = init_ideas(discussion_environment.id)

    # update an idea with a more specific title

    print(idea_about_cars.title)

    idea_about_cars.title = 'Cars are not good'

    idea_about_cars = idea_about_cars.persist()

    desc('Add relationships between posts')

    post1.reply_with_post(post2)
    post1.reply_with_post(post3)
    post2.reply_with_post(post4)
    post4.reply_with_post(post5)

    desc('Here is a representation of the posts (idents mean that the post reply to the post to the top)')

    # post1
    #   post2
    #   post3
    # post4
    #   post5

    post1.print_all_posts()

    desc('Update an idea')

    parent_idea.associate_to_idea(idea_about_cars)
    parent_idea.associate_to_idea(idea_about_planes)

    idea_about_planes.associate_to_idea(idea_about_jet_pack)

    post6.associate_with_idea(parent_idea)
    post2.associate_with_idea(parent_idea)

    post1.associate_with_idea(idea_about_cars)
    post2.associate_with_idea(idea_about_cars)

    post3.associate_with_idea(idea_about_planes)
    post1.associate_with_idea(idea_about_planes)

    # print(parent_idea.number_of_messages())
    #
    # print(parent_idea.number_of_participants())
    #
    # print(post1.get_all_children_posts())
    #
    # print(parent_idea.get_all_children_ideas())

    parent_idea.print_all_ideas()

    items_list = [
        dict(id=1, pid=None),  # childs : 2, 3, 4, 5, 6
        dict(id=2, pid=1),
        dict(id=3, pid=2),
        dict(id=5, pid=2),
        dict(id=6, pid=2),
        dict(id=4, pid=3),
        dict(id=7, pid=1),
        dict(id=7, pid=7)
    ]


    def get_children(items, child_ids):
        return [child for child in items if child['pid'] in child_ids]


    def find_recursive(items, parent_ids, level=0):
        for parent_id in parent_ids:
            children = get_children(items, [parent_id])
            if len(children) > 0:
                for child in children:
                    print('    ' * (level) + str(child['id']))
                    # for child in children:
                    return find_recursive(items, [child['id'] for child in children[:1]], level+1)
            elif len(children) == 0:
                level -= 1
                return []


    find_recursive(items_list, [1])
    print('END')