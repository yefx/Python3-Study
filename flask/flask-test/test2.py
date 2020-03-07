html = """<body bgcolor="DodgerBlue">
     <div style="text-align:center">
     <font></font><br/><font></font><br/><font></font><br/>
     <font face="宋体" size="+5" color="#F0F8FF">exec</font><br/>
     <font></font><br/>
     <font></font><br/>
     <form action ='/cmd' method='post' id="form">
         <input type="txt"  rows="2" cols="60" placeholder="命令...."
         name='cmd' id="cmd" style="height:40px;width:500px;">
   <input type="txt"  rows="2" cols="60" placeholder="参数...."
         name='option' id="option" style="height:40px;width:500px;">
         <button type="button" id="submit" class="search-submit"
         style="height:38px;width:60px;">执行</button>
     </form>
     </div>
  <script src="https://cdn.bootcss.com/jquery/1.10.0/jquery.js"></script>
  <script type="text/javascript">
   $(function(){
    $('#submit').on('click',function(){
     var cmd = $('#cmd').val();
     var option =$('#option').val();
     console.log(cmd,option);
     $.ajax({
      url:'/cmd',
      type:'post',
      dataType:'json',
      contentType: "application/json;charset=utf-8",
      data:{
       cmd:cmd,
       option:option
      },
      success:function(res){
       console.log(res);
      },
      error:function(error){
       console.log(error)
      }
     })
    })
    $('#form').submit(function(){
     return false
    })
   })
  </script>
 </body> """


import flask,subprocess
from flask import request

app = flask.Flask(__name__)
app.config['JSON_AS_ASCII'] =False

class RunShell:

    def __init__(self, command):
        self.command = command

    def runcmd(self):
        cmd = self.command
        exitcode, output = subprocess.getstatusoutput(cmd)
        if exitcode != 0:
            return 1
        #开启日志输出
        print('cmd:',cmd,'\n',output)
        return output

@app.route('/')
def Hello():
    return html

@app.route('/cmd', methods=["POST","GET"])
def run_shell():

    cmd = request.get_json('cmd')
    # cmd = request.values['cmd']
    # option = request.values['option']
    sudoers = ['shutdown','rm','sudoer','passwd','init','vim','poweroff','halt','bash',"reboot"]

    if cmd['cmd']:
        if cmd['cmd'] in sudoers:
            # 开启日志输出
            print('此请求被限制', cmd['cmd'], cmd['option'])
            return {"code": "403", "msg": "被限制执行"}
        elif cmd['cmd']:
            command = '{} {}'.format(cmd['cmd'], cmd['option'])
            exec = RunShell(command)
            output = exec.runcmd()
            if output != 1:
                return {'code': 200, 'command': command, 'msg': '{}'.format(output)}
            else:
                return {'code': 202,'msg': '未找到命令或执行失败'}
    else:
        return {'code': 202, 'msg': '命令不能为空'}


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=80)