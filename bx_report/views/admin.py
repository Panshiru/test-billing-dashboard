import flask
import flask_login

from bx_report import VCAP, app
from bx_report.factory.get_table_render import get_table_render


@app.route('/admin', methods=['GET', 'POST'])
@flask_login.login_required
def admin():
    if flask.request.method == 'POST':
        dict_post = flask.request.form.to_dict()
        if dict_post.has_key('delete'):
            user_to_delete = dict_post['delete']
            get_table_render(VCAP).client._delete_user(user_to_delete)
        elif dict_post.has_key('modify'):
            username = dict_post['login']
            pw = dict_post['modify']
            get_table_render(VCAP).client._update_user_pw(username, pw)
        elif dict_post.has_key('username'):
            username = dict_post['username']
            password = dict_post['password']
            su = True if dict_post.has_key('su') else False
            orgs = dict_post.keys()
            orgs.remove('username')
            orgs.remove('password')
            if su:
                orgs.remove('su')
            if username and password:
                get_table_render(VCAP).client._insert_user(username, password, su, orgs)
        else:
            for item in dict_post:
                if '@' in item:
                    user = item
            orgs = dict_post.keys()
            orgs.remove(user)
            get_table_render(VCAP).client._update_user_orgs(user, orgs)

    items = get_table_render(VCAP).client._list_all_users()
    items = filter(lambda x: x[0] != 'frederic.duport@open-groupe.com', items)
    items = sorted(items, key=lambda x: x[0])
    table = get_table_render(VCAP).admin_table(items)
    return flask.render_template('admin.html', content=table)
