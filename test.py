from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'



def main():
    db_session.global_init("db/users.db")

    # user = User()
    # user.user_id = 12314314321
    # user.surname = "Мирн"
    # user.name = 'Руслн'
    # user.user_name = "Rpi"
    # user.favourite_recipes = 'Пиво;;'
    db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()

    user = db_sess.query(User).get(2)
    user.favourite_recipes = user.favourite_recipes + "Хинкали;;"
    db_sess.add(user)
    db_sess.commit()
    print(user.user_id)
    print(user.surname)
    print(user.user_name)
    print(user.favourite_recipes)
    # for user in db_sess.query(User).all():
    #     print(user.name)
    #app.run()


if __name__ == '__main__':
    main()
