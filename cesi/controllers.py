from flask import g


def get_users():
    cur = g.db_conn.cursor()
    cur.execute("select username, type from userinfo")
    result = cur.fetchall()
    users = [{"name": str(element[0]), "type": str(element[1])} for element in result]
    return users


def get_user(username):
    cur = g.db_conn.cursor()
    cur.execute("select * from userinfo where username=?", (username,))
    result = cur.fetchall()
    if not result:
        return {}

    user = {"name": result[0][0], "type": result[0][1]}
    return user


def delete_user(username):
    cur = g.db_conn.cursor()
    cur.execute("delete from userinfo where username=?", [username])
    g.db_conn.commit()


def add_user(username, password, usertype):
    cur = g.db_conn.cursor()
    cur.execute("insert into userinfo values(?, ?, ?)", (username, password, usertype))
    g.db_conn.commit()


def validate_user(username, password):
    cur = g.db_conn.cursor()
    cur.execute(
        "select * from userinfo where username=? and password=?", (username, password)
    )
    return cur.fetchall()


def update_user_password(username, newpassword):
    cur = g.db_conn.cursor()
    cur.execute(
        "update userinfo set password=? where username=?", [new_password, username]
    )
    g.db_conn.commit()
