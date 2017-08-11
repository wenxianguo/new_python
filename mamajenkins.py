#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import threading
import requests
import datetime
import socket
from collections import defaultdict
from init import app
from flask import render_template, request


JENKINS_URL = 'http://wenxianguo:ZXwxg6235269@jenkins.corp.mama.cn/jenkins'
PROJECT = [
    # 18 环境
    'post.api.mama.cn',
    'qzone.mamaquan.mama.cn_18environment',
    'mapi.mama.cn_18environment',
    'admin.qzone.mamaquan.mama.cn_18environment',
    'q.mama.cn_18environment',
    'wap.mama.cn_18environment',
    'reader.api.mama.cn_18environment',
    'reader.mama.cn_18environment',
    'storage.mamaquan.mama.cn_18environment',
    'member_reply.mama.cn_18environment',
    'feed.api.mama.cn_18environment',
    'expert.mama.cn_18environment',
]

PROJECT_55 = [
    # 55 环境
    'post.api.mama.cn',
    'qzone.mamaquan.mama.cn',
    'mapi.mama.cn',
    'admin.qzone.mamaquan.mama.cn',
    'q.mama.cn',
    'wap.mama.cn',
    'reader.api.mama.cn',
    'reader.mama.cn',
    'storage.mamaquan.mama.cn',
    'member_reply.mama.cn',
    'feed.api.mama.cn',
    'expert.mama.cn',
    'live.mama.cn',
]
CONTENT = []


def show_builds(project=''):
    url = '/job/%s/api/json' % project
    resposne = requests.post(JENKINS_URL + url)
    result = resposne.json()
    last_build_num = result['lastBuild']['number']

    url = "/job/%s/%s/api/json" % (project, last_build_num)
    resposne = requests.post(JENKINS_URL + url)
    result = resposne.json()

    last_build_username = result['actions'][1]['causes'][0]['userName']
    last_build_dateline = str(datetime.datetime.fromtimestamp(int(result['timestamp'] / 1000)))
    last_build_branch = result['actions'][0]['parameters'][0]['value']
    content = {
        'project': project,
        'dateline': last_build_dateline,
        'username': last_build_username,
        'number': last_build_num,
        'branch': last_build_branch
    }
    return CONTENT.append(content)


@app.route('/')
def index():
    env = request.args.get('env', '18')
    return render_template('jenkins/jenkins.html', env=env)


@app.route('/get_last_builds', methods=['GET'])
def get_last_builds():
    try:
        global CONTENT
        env = request.args.get('env', '18')
        projects = PROJECT if env == '18' else PROJECT_55
        CONTENT = []
        jobs = []
        for project in projects:
            job = threading.Thread(target=show_builds, args=(project,))
            job.setDaemon(True)
            job.start()
            jobs.append(job)

        for job in jobs:
            job.join()
        return json.dumps(CONTENT)
    except Exception as e:
        return str(e)


@app.route('/yoda_listen')
def yoda_listen():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect(('192.168.55.120', 4730))
    s.sendall(b'workers\n')
    data = s.recv(2048)
    s.close()
    data = data.decode('utf-8').rstrip('\n.').split('\n')
    occupying = defaultdict(list)
    for row in data:
        if row.endswith(':'):
            number, ip, _, _ = row.split(maxsplit=4)
            projects = []
        else:
            number, ip, _, _, projects = row.split(maxsplit=4)
            projects = projects.split()
        for project in projects:
            if project in ['yoda_tlq_callback', 'yoda_mmq_callback']:
                occupying[project].append(ip)
    return render_template('jenkins/yoda_listen.html', occupying=occupying)


@app.route('/get_last_build_console', methods=['GET'])
def get_last_build_console():
    project = request.args.get('project', '')
    number = request.args.get('number', '')
    response = requests.get(JENKINS_URL + 'job/%s/%s/consoleText' % (project, number))
    print(JENKINS_URL + '/job/%s/%s/consoleText' % (project, number))
    return response.content


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')