from models.user import User
from security.auth import UserSession
from models.discussion import Discussion
from models.idea import Idea
from models.post import Post


def init_users():
    return [
        User(
            username='john',
            email='john@company.com',
            password='1234'
        ).persist(),
        User(
            username='bob',
            email='bob@company.com',
            password='4567'
        ).persist(),
        User(
            username='anna',
            email='anna@company.com',
            password='789845'
        ).persist()
    ]


if __name__ == '__main__':
    [user_john, user_bob, user_anna] = init_users()

    user_session = UserSession()
    user_session.connect()

    discussion_environment = Discussion(
        name='Environmental issues',
        title='How to solve environmental issues'
    ).persist()

    post1 = Post(
        text='Post 1',
        discussion_id=discussion_environment.id
    ).persist()

    post2 = Post(
        text='Post 2',
        discussion_id=discussion_environment.id
    ).persist()

    # post2.delete()

    post1.reply_with_post(post2)

    post3 = Post(
        text='Post 3 -> Reply to post 1',
        discussion_id=discussion_environment.id
    ).persist()

    post1.reply_with_post(post3)

    post4 = Post(
        text='Post 4 -> Reply to post 2',
        discussion_id=discussion_environment.id
    ).persist()

    post2.reply_with_post(post4)

    post5 = Post(
        text='Post 5 -> Reply to post 4',
        discussion_id=discussion_environment.id
    ).persist()

    post4.reply_with_post(post5)

    post6 = Post(
        text='Post 6 without reply',
        discussion_id=discussion_environment.id
    ).persist()

    parent_idea = Idea(
        discussion_id=discussion_environment.id,
        title="Great idea",
        description="One idea to rule them all"
    ).persist()

    idea_about_cars = Idea(
        discussion_id=discussion_environment.id,
        title='Cars',
        description='We should avoid using cars',
    ).persist()

    idea_about_planes = Idea(
        discussion_id=discussion_environment.id,
        title='Planes',
        description='We should avoid using planes',
    ).persist()

    idea_about_jet_pack = Idea(
        discussion_id='discussion_environment.id',
        title="Jet pack",
        description="How about not using jet pack either"
    )

    idea_about_cars.title = 'Cars are not good'

    updated_idea_about_cars = idea_about_cars.persist()

    parent_idea.associate_with(updated_idea_about_cars)
    parent_idea.associate_with(idea_about_planes)

    post6.associate_with_idea(parent_idea)
    post2.associate_with_idea(parent_idea)

    post1.associate_with_idea(idea_about_cars)
    post2.associate_with_idea(idea_about_cars)

    post3.associate_with_idea(idea_about_planes)
    post1.associate_with_idea(idea_about_planes)

    print(post1)

    print(parent_idea.number_of_messages())

    print(parent_idea.number_of_messages())

    # api.associate_with_idea(idea_about_planes, idea_about_cars.id)
    #
    # disscussion_test = user_session.get_db().find_one_by(Discussion, 'id', discussion_environment.id)

    print(post2.get_all_children_posts())


    def get_number_posts_for_idea(id):
        print('result')
        a = [1, 2]
        b = [1]
        print(len(set(a) & set(b)) > 0)


    get_number_posts_for_idea(1)

ideas = [dict(id=1, pid=None), dict(id=2, pid=1), dict(id=3)]
posts = [dict(id=1, p_idea_id=[1, 2]), dict(id=2, p_idea_id=[1]), dict(id=3, p_idea_id=[2]), dict(id=4, p_idea_id=[3])]
