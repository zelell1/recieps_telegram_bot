from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'



def main():
    db_session.global_init("db/users.db")

    user = User()
    user.user_id = 123143141231
    user.surname = "Мирный"
    user.name = 'Руслан'
    user.user_name = "Repi"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()

    user = db_sess.query(User).first()
    print(user.name)
    print(user.user_id)
    print(user.surname)
    print(user.user_name)
    # for user in db_sess.query(User).all():
    #     print(user.name)
    #app.run()


if __name__ == '__main__':
    main()
