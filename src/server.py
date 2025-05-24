import socket
import threading
import json
import logging
import os
import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/server.log',
    filemode='a',
    encoding='utf-8'  # 指定日志文件编码为utf-8
)
logger = logging.getLogger('ATMServer')

# 用户数据存储路径
DATA_FILE = 'data/users.json'


class ATMServer:
    def __init__(self, host='0.0.0.0', port=2525):
        self.host = host
        self.port = port
        self.socket = None
        self.users = self.load_users()

    def load_users(self):
        """从文件加载用户数据"""
        if not os.path.exists(DATA_FILE):
            # 用户数据
            default_users = {
                "123456": {"password": "1234", "balance": 10000.0},
                "654321": {"password": "4321", "balance": 5000.0}
            }
            with open(DATA_FILE, 'w') as f:
                json.dump(default_users, f, indent=2)
            logger.info(f"创建默认用户数据文件: {DATA_FILE}")
            return default_users

        try:
            with open(DATA_FILE, 'r') as f:
                users = json.load(f)
            logger.info(f"从 {DATA_FILE} 加载了 {len(users)} 个用户")
            return users
        except Exception as e:
            logger.error(f"加载用户数据错误: {str(e)}")
            return {}

    def save_users(self):
        """保存用户数据到文件"""
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.users, f, indent=2)
            logger.info(f"保存了 {len(self.users)} 个用户数据到 {DATA_FILE}")
        except Exception as e:
            logger.error(f"保存用户数据错误: {str(e)}")

    def start(self):
        """启动服务器"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            logger.info(f"服务器启动于 {self.host}:{self.port}")

            print(f"ATM 服务器已启动，监听端口 {self.port}")

            while True:
                client_socket, address = self.socket.accept()
                logger.info(f"新连接来自 {address}")
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()

        except Exception as e:
            logger.error(f"服务器错误: {str(e)}")
        finally:
            if self.socket:
                self.socket.close()

    def handle_client(self, client_socket, address):
        """处理客户端连接"""
        user_id = None
        authenticated = False

        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8').strip()
                if not data:
                    break

                logger.info(f"收到来自 {address} 的消息: {data}")

                parts = data.split(' ', 1)
                command = parts[0]

                if command == "HELO":
                    if len(parts) > 1:
                        user_id = parts[1]
                        if user_id in self.users:
                            response = "500 AUTH REQUIRED!"
                        else:
                            response = "401 ERROR!"
                    else:
                        response = "401 ERROR!"

                elif command == "PASS":
                    if user_id and len(parts) > 1:
                        password = parts[1]
                        if user_id in self.users and self.users[user_id]["password"] == password:
                            authenticated = True
                            response = "525 OK!"
                        else:
                            response = "401 ERROR!"
                    else:
                        response = "401 ERROR!"

                elif command == "BALA":
                    if authenticated:
                        balance = self.users[user_id]["balance"]
                        response = f"AMNT:{balance}"
                    else:
                        response = "401 ERROR!"

                elif command == "WDRA":
                    if authenticated and len(parts) > 1:
                        try:
                            amount = float(parts[1])
                            if amount > 0 and self.users[user_id]["balance"] >= amount:
                                self.users[user_id]["balance"] -= amount
                                self.save_users()
                                response = "525 OK"
                            else:
                                response = "401 ERROR!"
                        except ValueError:
                            response = "401 ERROR!"
                    else:
                        response = "401 ERROR!"

                elif command == "BYE":
                    response = "BYE"

                else:
                    response = "401 ERROR!"

                client_socket.sendall((response + '\n').encode('utf-8'))
                logger.info(f"发送到 {address}: {response}")

                if command == "BYE":
                    break

        except Exception as e:
            logger.error(f"处理客户端 {address} 时出错: {str(e)}")
        finally:
            client_socket.close()
            logger.info(f"连接关闭: {address}")


if __name__ == "__main__":
    server = ATMServer()
    server.start()
