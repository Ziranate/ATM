import socket
import logging


class ATMClient:
    """
    ATM客户端通信模块，负责与服务器的网络通信和业务逻辑处理
    """

    def __init__(self, host='localhost', port=2525):
        self.host = host
        self.port = port
        self.socket = None
        self.user_id = None
        self.logger = self._setup_logger()
        self.callbacks = {
            "on_error": None,
            "on_info": None,
            "on_login_success": None,
            "on_pin_verified": None,
            "on_balance_result": None,
            "on_withdraw_success": None,
            "on_exit": None
        }

    def _setup_logger(self):
        """配置日志记录器"""
        logger = logging.getLogger('ATMClient')
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            # 也可以添加文件处理器
            file_handler = logging.FileHandler('logs/atm_client.log')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    def connect(self):
        """连接到服务器"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.logger.info(f"已连接到服务器: {self.host}:{self.port}")
            return True
        except Exception as e:
            self.logger.error(f"无法连接到服务器: {str(e)}")
            return False

    def disconnect(self):
        """断开与服务器的连接"""
        if self.socket:
            try:
                self.socket.close()
                self.logger.info("已断开与服务器的连接")
            except Exception as e:
                self.logger.error(f"断开连接时出错: {str(e)}")
            finally:
                self.socket = None

    def send_receive(self, message):
        """发送消息并接收响应"""
        if not self.socket:
            self.logger.error("未连接到服务器，无法发送消息")
            return None

        try:
            self.logger.info(f"发送消息: {message}")
            self.socket.sendall((message + '\n').encode('utf-8'))
            response = self.socket.recv(1024).decode('utf-8')
            self.logger.info(f"接收响应: {response}")
            return response
        except Exception as e:
            self.logger.error(f"通信错误: {str(e)}")
            return None

    def insert_card(self, user_id):
        """发送卡号登录请求"""
        self.user_id = user_id
        return self.send_receive(f"HELO {user_id}")

    def verify_pin(self, pin):
        """发送PIN验证请求"""
        return self.send_receive(f"PASS {pin}")

    def check_balance(self):
        """发送余额查询请求"""
        return self.send_receive("BALA")

    def withdraw(self, amount):
        """发送取款请求"""
        return self.send_receive(f"WDRA {amount}")
    def exit(self):
        """发送退出请求"""
        response = self.send_receive("BYE")
        self.disconnect()
        return response
        
    # 添加回调设置方法
    def set_callbacks(self, callbacks):
        """
        设置回调函数字典，用于业务处理结果回调
        
        参数:
            callbacks: 字典，包含各种事件的回调函数
        """
        self.callbacks.update(callbacks)
        
    # 业务逻辑处理方法
    def process_card_insertion(self, card_number):
        """处理卡片插入的业务逻辑"""
        if not card_number:
            self._trigger_callback("on_error", "输入错误", "请输入卡号")
            return False
            
        if not self.connect():
            self._trigger_callback("on_error", "连接错误", "无法连接到服务器")
            return False
            
        response = self.insert_card(card_number)
        
        if not response:
            self._trigger_callback("on_error", "通信错误", "与服务器通信失败")
            return False
            
        if response.startswith("500"):
            # 允许500开头的所有返回内容进入PIN页面
            self._trigger_callback("on_login_success")
            return True
        else:
            self._trigger_callback("on_error", "卡号错误", "无效的卡号")
            self.disconnect()
            return False
            
    def process_pin_verification(self, pin):
        """处理PIN验证的业务逻辑"""
        if not pin:
            self._trigger_callback("on_error", "输入错误", "请输入PIN码")
            return False
            
        response = self.verify_pin(pin)
        
        if not response:
            self._trigger_callback("on_error", "通信错误", "与服务器通信失败")
            return False
            
        if response.startswith("525"):
            # 允许525 OK!等所有变体
            self._trigger_callback("on_pin_verified")
            return True
        else:
            self._trigger_callback("on_error", "PIN错误", "PIN码不正确")
            return False
            
    def process_balance_check(self):
        """处理余额查询的业务逻辑"""
        response = self.check_balance()
        
        if not response:
            self._trigger_callback("on_error", "通信错误", "与服务器通信失败")
            return False
            
        if response.startswith("AMNT:"):
            balance = response.split(":", 1)[1]
            self._trigger_callback("on_balance_result", balance)
            return True
        else:
            self._trigger_callback("on_error", "查询失败", "无法获取余额信息")
            return False
            
    def process_withdrawal(self, amount_text):
        """处理取款的业务逻辑"""
        if not amount_text:
            self._trigger_callback("on_error", "输入错误", "请输入取款金额")
            return False
            
        try:
            amount = float(amount_text)
            if amount <= 0:
                self._trigger_callback("on_error", "金额错误", "请输入大于0的金额")
                return False
                
            response = self.withdraw(amount)
            
            if not response:
                self._trigger_callback("on_error", "通信错误", "与服务器通信失败")
                return False
                
            if response.startswith("525"):
                # 允许所有525 OK开头的响应
                self._trigger_callback("on_withdraw_success", amount)
                return True
            else:
                self._trigger_callback("on_error", "取款失败", "余额不足或其他错误")
                return False
                
        except ValueError:
            self._trigger_callback("on_error", "输入错误", "请输入有效的金额数值")
            return False
            
    def process_exit(self):
        """处理退出的业务逻辑"""
        response = self.exit()
        self._trigger_callback("on_exit")
        return True
        
    def _trigger_callback(self, callback_name, *args):
        """触发回调"""
        callback = self.callbacks.get(callback_name)
        if callback and callable(callback):
            callback(*args)
