import datetime
# logtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# print(logtime)
def get_exec_time():
    start = datetime.datetime.now()
    end = datetime.datetime.now()
    exec_time = end - start
    return exec_time

def get_return_info(msg):
    code = msg['code']
    if code == 200:
        return {'code': '200', 'command': '这里是命令', 'msg': '这里是执行结果'}
    elif code == 202:
        return {'code': '202','msg': '未找到命令或执行失败'}
    elif code == 201:
        return {'code': '201'}
    elif code == 403:
        return {'code': '403','msg':'被限制执行'}

if __name__ == '__main__':
    # time = get_exec_time()
    # print(time)
    msg = {'code': 200}

    print(get_return_info(msg))
