from models.user import User
from security.auth import UserSession
from models.discussion import Discussion
from models.idea import Idea
from models.post import Post
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


if __name__ == '__main__':
    [user_john, user_bob, user_anna] = init_users()

    user_session = UserSession()
    user_session.connect(user_bob)

    discussion_environment = Discussion(
        name='Environmental issues',
        title='How to solve environmental issues ?',
        creator_id=user_anna.id
    ).persist()

    post1 = Post(
        text='Post 1',
        discussion_id=discussion_environment.id,
        creator_id=user_bob.id
    ).persist()

    post2 = Post(
        text='Post 2 -> reply to post 1',
        discussion_id=discussion_environment.id,
        creator_id=user_john.id
    ).persist()

    # post2.delete()

    post1.reply_with_post(post2)

    post3 = Post(
        text='Post 3 -> Reply to post 1',
        discussion_id=discussion_environment.id,
        creator_id=user_anna.id
    ).persist()

    post1.reply_with_post(post3)

    post4 = Post(
        text='Post 4 -> Reply to post 2',
        discussion_id=discussion_environment.id,
        creator_id=user_anna.id
    ).persist()

    post2.reply_with_post(post4)

    post5 = Post(
        text='Post 5 -> Reply to post 4',
        discussion_id=discussion_environment.id,
        creator_id=user_john.id
    ).persist()

    post4.reply_with_post(post5)

    post6 = Post(
        text='Post 6 without reply',
        discussion_id=discussion_environment.id,
        creator_id=user_john.id
    ).persist()

    parent_idea = Idea(
        discussion_id=discussion_environment.id,
        title="Great idea",
        description="One idea to rule them all",
        creator_id=user_john.id
    ).persist()

    idea_about_cars = Idea(
        discussion_id=discussion_environment.id,
        title='Cars',
        description='We should avoid using cars',
        creator_id=user_bob.id
    ).persist()

    idea_about_planes = Idea(
        discussion_id=discussion_environment.id,
        title='Planes',
        description='We should avoid using planes',
        creator_id=user_anna.id
    ).persist()

    idea_about_jet_pack = Idea(
        discussion_id=discussion_environment.id,
        title="Jet pack",
        description="How about not using jet pack either",
        creator_id=user_anna.id
    ).persist()

    idea_about_cars.title = 'Cars are not good'

    updated_idea_about_cars = idea_about_cars.persist()

    parent_idea.associate_to_idea(updated_idea_about_cars)
    parent_idea.associate_to_idea(idea_about_planes)

    idea_about_planes.associate_to_idea(idea_about_jet_pack)

    post6.associate_with_idea(parent_idea)
    post2.associate_with_idea(parent_idea)

    post1.associate_with_idea(idea_about_cars)
    post2.associate_with_idea(idea_about_cars)

    post3.associate_with_idea(idea_about_planes)
    post1.associate_with_idea(idea_about_planes)

    print(post1)

    # print(parent_idea.number_of_messages())

    # print(parent_idea.number_of_participants())

    # print(post1.get_all_children_posts())

    print(parent_idea.get_all_children_ideas())
    # parent_idea.print_all_ideas()



