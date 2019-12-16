import pymysql
from sshtunnel import SSHTunnelForwarder
import os

class DB(object):
    # sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG
    # 传入需要连接的数据库的名称dbname和待执行的sql语句sql
    def __init__(self):
        self.ssh_address_or_host = "******"
        self.ssh_username = "root"
        self.ssh_pkey = "res/id_rsa_2048houduan"
        self.ssh_private_key_password = "123456"
        self.dbuser = "root"
        self.dbpasswd = "******"
        self.dbname = "pool"

    def execute_sql(self,sqlstr):
        results = ''
        #  登录跳板机（*******）后，远程（192.168.0.5）操作msql
        with SSHTunnelForwarder(
            ssh_address_or_host=(self.ssh_address_or_host,22),
            ssh_username=self.ssh_username,
            ssh_pkey=self.ssh_pkey,
            ssh_private_key_password=self.ssh_private_key_password,
            remote_bind_address=('192.168.0.5', 3306), # 绑定mysql机子的IP。
            # local_bind_address=('127.0.0.1', 33060),
        ) as server:
            # 打开数据库连接
            db_connect = pymysql.connect(host='127.0.0.1',
                                         user="root",
                                         password="******",
                                         database="pool",
                                         port=server.local_bind_port)
            # 使用cursor()方法获取操作游标
            cursor = db_connect.cursor()

            try:
                # 执行SQL语句
                # sqlstr = "select * from email_captcha where email = '******' order by create_time desc"
                cursor.execute(sqlstr)
                # 获取所有记录列表
                results = cursor.fetchall()
                # results = cursor.fetchone()
            except Exception as data:
                print('Error: 执行查询失败，%s' % data)
            print(results)
            return results
