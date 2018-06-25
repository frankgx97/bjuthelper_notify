#coding:utf8
import datetime
import json

import requests
from bs4 import BeautifulSoup

config = json.loads(open('config.json').read())

def send_email(msg):
    result = requests.post(config['mail_api'], json={
        "mail_to":config['mail'],
        "mail_title":'小伙子，又出分了！',
        "mail_html":msg+'<hr>',
        "key":config['key']
    })
    print 'mail sent'
    return result.text


def wfile(content):
    f = open("t.txt", "w+")
    f.write(str(content))
    f.close()

def gfile():
    c = json.loads(open('t.txt').read())
    return int(c)

def require():
    r = requests.post('https://bjut.guoduhao.cn/require_grade.php', data={
        'account':config['id'],
        'password':config['password'],
        'current_year':config['year'],
        'current_term':config['term']
        })
    rst = r.text.replace("</html>", "")
    rst = rst + "</html>"
    return rst

def parse():
    soup = BeautifulSoup(require(), "lxml")
    rm = soup.findAll("div", id="average_score")
    #[i.extract() for i in rm]
    rm = soup.findAll("div", id="average_GPA")
    gpa = soup.findAll("div", class_="weui_accordion_title")
    #[i.extract() for i in rm]
    grades = soup.findAll("div", class_="weui_cell_bd weui_cell_primary")
    print len(grades) - 3
    if gfile() < len(grades) - 3:
        try:
            s = '<p>'
            for i in gpa:
                s += i.get_text().encode('utf-8') 
                s += '</p><p>'
            for i in grades:
                s += i.get_text().encode('utf-8')
                s += '</p><p>'
            s += 'At:'+str(datetime.datetime.now())+'</p>'
            wfile(len(grades)-5)
            print send_email(s)
        except Exception, e:
            send_email(e)

parse()
