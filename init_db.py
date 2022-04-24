from data import db_session
from data.users import User


def main(id_of_user, first_name, last_name, username, favourite):  # Занесение пользователя в БД
    db_session.global_init("db/users.db")
    db_sess = db_session.create_session()
    flag = True
    for i in range(len(db_sess.query(User.user_id).all()[:])):
        if id_of_user == db_sess.query(User.user_id).all()[:][i][0]:
            flag = False
    if flag:
        user = User()
        user.user_id = id_of_user
        user.surname = first_name
        user.name = last_name
        user.user_name = username
        user.favourite_recipes = f"{favourite};;"
    else:
        user = db_sess.query(User).filter(User.user_id == id_of_user).first()
        user.favourite_recipes += f"{favourite};;"
    db_sess.add(user)
    db_sess.commit()


def show_href(id_of_user):  # Вывод списка рецептов, понравившихся пользователю
    db_session.global_init("db/users.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.user_id == id_of_user).first()
    lst_href = user.favourite_recipes
    db_sess.add(user)
    db_sess.commit()
    return lst_href


def users_href():  # Вывод списка id пользователей
    db_session.global_init("db/users.db")
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    users_id = []
    for user in users:
        users_id.append(user.user_id)
    return users_id


if __name__ == '__main__':
    pass
