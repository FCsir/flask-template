"""自定义flask_script终端命令"""
from flask_script import Command, Option

class CustomCommand(Command):
    """命令的相关描述"""
    option_list = (
        Option('--name', '-n', dest='name'),
    )
    def run(self, name):
        print("这是执行了hello命令", name)