from api.api import UserSession
from models.discussion import Discussion
from models.idea import Idea
from models.post import Post

if __name__ == '__main__':
    user_session = UserSession()
    user_session.connect()

    # api = ApiController()

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

    post2.delete()

    # post2 = api.reply_to_post(post2, post1.id)
    #
    # post3 = api.create_post(Post(
    #     text='Post 3 -> Reply to post 1',
    #     discussion_id=discussion_environment.id
    # ))
    #
    # post3 = api.reply_to_post(post3, post1.id)
    #
    # post4 = api.create_post(Post(
    #     text='Post 4 -> Reply to post 2',
    #     discussion_id=discussion_environment.id
    # ))
    #
    # post4 = api.reply_to_post(post4, post2.id)
    #
    # post5 = api.create_post(Post(
    #     text='Post 5 -> Reply to post 4',
    #     discussion_id=discussion_environment.id
    # ))
    #
    # post5 = api.reply_to_post(post5, post4.id)
    #
    # post6 = api.create_post(Post(
    #     text='Post 6 without reply',
    #     discussion_id=discussion_environment.id
    # ))
    #
    # print(api.get_all_children_posts(post1.id))
    #
    # api.delete_post(post1)
    #

    idea_about_cars = Idea(
        discussion_id=discussion_environment.id,
        title='Cars',
        description='We should avoid using cars',
    ).persist()

    idea_about_cars.title = 'Cars are not good'

    updated_idea = idea_about_cars.persist()

    print(updated_idea.title)

    idea_about_planes = Idea(
        discussion_id=discussion_environment.id,
        title='Planes',
        description='We should avoid using planes',
    ).persist()
    #
    # api.associate_with_idea(idea_about_planes, idea_about_cars.id)
    #
    # disscussion_test = user_session.get_db().find_one_by(Discussion, 'id', discussion_environment.id)

    print(discussion_environment.db.store)
