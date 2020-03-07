import flask,subprocess,datetime,logging
from logging import FileHandler
from flask import request

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] =False

class RunShell:

    def __init__(self, command):
        self.command = command

    def runcmd(self):
        cmd = self.command
        start = datetime.datetime.now()
        exitcode, output = subprocess.getstatusoutput(cmd)
        if exitcode != 0:
            return 1
        #开启日志输出
        end = datetime.datetime.now()
        exec_time = end - start
        print(datetime.datetime.now(),'cmd:',cmd,'\n',output,'执行耗时',exec_time)
        return output

@app.route('/')
def home():
    return app.send_static_file("index.html")

@app.route('/cmd', methods=["POST","GET"])
def run_shell():
    cmd = request.get_json('cmd')['cmd']
    option = request.get_json('cmd')['option']
    # cmd = request.values['cmd']
    # option = request.values['option']
    sudoers = ['shutdown','rm','sudoer','passwd','init','vim','poweroff','halt','bash',"reboot"]

    if cmd:
        if cmd in sudoers:
            # print('此请求被限制', cmd, option)
            return {"code": "403", "msg": "被限制执行"}
        elif cmd:
            command = '{} {}'.format(cmd, option)
            exec = RunShell(command)
            output = exec.runcmd()
            if output != 1:
                return {'code': 200, 'command': command, 'msg': '{}'.format(output),'time':'{}'.format(datetime.datetime.now())}
            else:
                return {'code': 202,'msg': '未找到命令或执行失败'}
    else:
        return {'code': 202, 'msg': '命令不能为空'}


if __name__ == '__main__':
    #app.run(debug=True, host="0.0.0.0", port=80)
    app.run(host="0.0.0.0", port=80)
