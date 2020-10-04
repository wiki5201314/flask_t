from flask import Flask, render_template, request, session, send_from_directory
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from geventwebsocket.websocket import WebSocket
import json
from collect import Collect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')

app.config.from_pyfile('config.py')
app.config['SECRET_KEY'] = 'abc'

db = SQLAlchemy(app)

class CsBrand(db.Model):
    __tablename__ = 'cs_brand'
    brand_id = db.Column(db.INTEGER, primary_key=True)
    brand_name = db.Column(db.String(100), unique=True)

class CsMerchantWish(db.Model):
    __tablename__ = 'cs_merchant_wish'
    wish_id = db.Column(db.INTEGER, primary_key=True)
    wish_sign = db.Column(db.String(100), unique=True)
    wish_cookies = db.Column(db.TEXT)
    wish_dian_id = db.Column(db.String(50))
    wish_currency = db.Column(db.String(10))

@app.route('/settings_brands')
def settings_brands():
    if session.get('username') == None:
        return render_template('login.html')

    brands = CsBrand.query.all()

    return render_template('setting_brands.html', title='品牌设置', user=session['username'], menus=get_red_menu(), brands=brands)

def get_red_menu():
    red_menu = {
        "1": "手机壳传wish",
        "2": "挂毯传wish",
        "3": "口罩传wish",
        "4": "浴帘传wish",
        "5": "圆形胸针传wish",
        "6": "抱枕传wish",
        "7": "地枕传wish"
    }

    return red_menu

@app.route('/')
def hello_world():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')

@app.route('/login', methods = ["POST"])
def login():
    pwd = request.form['pwd']
    print(pwd)
    try:
        name_pages = ""
        merchants = ""
        with open("config/" + pwd + ".txt", "r") as f:
            name_pages = f.read()
        session['username'] = name_pages.split()[0]
        session['pages'] = name_pages

        return render_template('index.html', title='首页', user=session['username'], menus=get_red_menu())
    except:
        print("asd")
        return render_template('login.html', title='首页', error="密码错误")



@app.route('/home')
def home():
    if session.get('username') == None:
        return render_template('login.html')

    return render_template('index.html', title='首页', user=session['username'], menus=get_red_menu())

@app.route('/upload', methods = ["GET"])
def upload():
    if session.get('username') is None:
        return render_template('login.html')

    merchants_list = ""
    with open("config/" + session.get('username') + "-mise.txt", "r") as f:
        merchants_list = f.read()

    print(merchants_list)
    session['merchants_list'] = merchants_list

    name_pages = ""
    with open("config/" + session.get('username') + ".txt", "r") as f:
        name_pages = f.read()
    session['pages'] = name_pages

    cu = request.args.get("cu")
    menus = get_red_menu()
    if cu == "0":
        merchants = merchants_list.split()[int(cu)]
        return render_template('collect_wish.html', title='采集ID', user=session['username'], cu=cu, menus=menus, merchants=merchants)
    elif 1 <= int(cu) <= 7:
        pages = session.get("pages").split()[int(cu)]
        merchants = merchants_list.split()[int(cu)]
        return render_template('red_to_wish.html', title=menus[cu], user=session['username'], cu=cu, menus=menus, pages=pages, merchants=merchants)
    elif cu == "100":
        # 点小米模板号+运费模板号
        ali_merchants = {"ACO": "tina", "buroni005": "Free", "VDZ": "f"}
        return render_template('wish_to_ali.html', title='wish手机壳采集到速卖通', user=session['username'], cu=cu, menus=menus,
                               ali_merchants=ali_merchants)
    elif cu == "101":
        # 点小米模板号+运费模板号
        ali_merchants = {"ACO": "tina", "buroni005": "Free", "VDZ": "f"}
        return render_template('red_to_ali.html', title='wish手机壳采集到速卖通', user=session['username'], cu=cu, menus=menus,
                               ali_merchants=ali_merchants)

    return render_template('login.html')

@app.route("/download", methods = ["GET"])
def download():
    if session.get('username') is None:
        return render_template('login.html')

    file = request.args.get("file")
    return send_from_directory(r"excel", filename=file, as_attachment=True)

@app.route('/collect')
def collect():
    user_socket = request.environ.get("wsgi.websocket")
    if user_socket:
        while True:
            message = json.loads(user_socket.receive())
            if message.get("msg") == "exit":
                break
            try:
                # 开始
                msg = {
                    "msg": "开始上传",
                    "percent": 0,
                }
                user_socket.send(json.dumps(msg))

                msg_re = message.get("msg").split("\n")
                cu = message.get("cu")
                merchants = message.get("merchants")
                print(msg_re, cu)
                brands = CsBrand.query.all()
                print(brands[0].brand_name)
                co = Collect(user_socket, cu, msg_re, merchants, brands)
                co.execute()

                # 结束
                msg = {
                    "msg": "上传完成",
                    "percent": 100,
                }
                user_socket.send(json.dumps(msg))

                # 更新页数
                if 1 <= int(cu) <= 7:
                    new_pages = []
                    for i, items in enumerate(session['pages'].split()):
                        if i == int(cu):
                            new_pages.append(str(int(msg_re[0]) + 1))
                        else:
                            new_pages.append(items)
                    session['pages'] = ' '.join(new_pages)

                    #并更新文件
                    filename = "config/" + session['username'] + ".txt"
                    with open(filename, 'w') as f:
                        f.write(session['pages'])

                    #更新merchantID
                    new_merchants_list = []
                    for i, items in enumerate(session['merchants_list'].split()):
                        if i == int(cu):
                            new_merchants_list.append(merchants)
                        else:
                            new_merchants_list.append(items)
                    session['merchants_list'] = ' '.join(new_merchants_list)

                    # 并更新文件
                    filename = "config/" + session['username'] + "-mise.txt"
                    with open(filename, 'w') as f:
                        f.write(session['merchants_list'])

            except:
                continue


if __name__ == '__main__':
    http_serv = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    http_serv.serve_forever()