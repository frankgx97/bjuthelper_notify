#coding:utf8
import requests
from bs4 import BeautifulSoup
import json
from sender import Mail
from sender import Message
import datetime

config = json.loads(open('config.json').read())

def send_email(msg):
    mail_msg = Message('小伙子，又出分了！', fromaddr=config['mail_from'], to=config['mail'])
    mail_msg.html = msg
    mail = Mail(
        "smtp.exmail.qq.com",
        port=465,
        username=config['mail_from'],
        password=config['mail_pass'],
        use_tls=False,
        use_ssl=True,
        debug_level=None
        )
    mail.send(mail_msg)

def wfile(content):
    f = open("t.txt", "w+")
    f.write(str(content))
    f.close()

def gfile():
    c = json.loads(open('t.txt').read())
    return int(c)

def require():
    r = requests.post('https://chafen.bjut123.com/require_grade.php', data={
        'account':config['id'],
        'password':config['password'],
        'current_year':config['year'],
        'current_term':config['term']
        })
    rst = r.text.replace("/html", "")
    rst = rst + "/html"
    return rst

def parse():
    soup = BeautifulSoup(require(), "lxml")
    rm = soup.findAll("div", id="average_score")
    [i.extract() for i in rm]
    rm = soup.findAll("div", id="average_GPA")
    [i.extract() for i in rm]
    grades = soup.findAll("div", class_="weui_cell_bd weui_cell_primary")
    print len(grades)
    if gfile() < len(grades):
        try:
            s = '<p>已出分科目：'+str(len(grades))+'</p><p>'
            for i in grades:
                s += i.get_text().encode('utf-8')
                s += '</p><p>'
            s += 'At:'+str(datetime.datetime.now())+'</p>'
            wfile(len(grades))
            send_email(s)
        except Exception, e:
            send_email(e)

parse()
