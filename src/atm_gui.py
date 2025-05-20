from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton,
                             QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
                             QStackedWidget, QMessageBox, QFrame, QGridLayout,
                             QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QSize
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from pythonProject.CQU.Semester2.ComputerNetworking.ATM.atm_client import ATMClient

class ATMSignals(QObject):
    """自定义信号类，用于在GUI和客户端逻辑之间传递事件"""
    error_message = pyqtSignal(str, str)  # 标题, 消息
    info_message = pyqtSignal(str, str)  # 标题, 消息


class ATMGUI(QMainWindow):
    """现代化ATM图形用户界面"""

    def __init__(self, client=None):
        super().__init__()

        # 创建ATM客户端实例（如果没有提供）
        self.client = client if client else ATMClient()
        
        # 设置回调
        self.client.set_callbacks({
            "on_error": self.on_error,
            "on_info": self.on_info,
            "on_login_success": self.on_login_success,
            "on_pin_verified": self.on_pin_verified, 
            "on_balance_result": self.on_balance_result,
            "on_withdraw_success": self.on_withdraw_success,
            "on_exit": self.on_exit
        })

        # 创建信号对象
        self.signals = ATMSignals()
        self.signals.error_message.connect(self.show_error)
        self.signals.info_message.connect(self.show_info)

        # 初始化UI
        self.setup_ui()
        self.setup_styles()
        self.setup_dark_mode(False)  # 默认浅色模式

    def setup_ui(self):
        """设置主界面"""
        self.setWindowTitle("智能ATM终端")
        self.setMinimumSize(900, 650)

        # 设置窗口图标
        self.setWindowIcon(QIcon(":atm_icon.png"))  # 使用Qt资源系统中的图标

        # 创建堆叠部件用于页面切换
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # 创建各个页面
        self.create_welcome_page()
        self.create_pin_page()
        self.create_main_menu_page()
        self.create_balance_page()
        self.create_withdraw_page()

        # 显示欢迎页
        self.stack.setCurrentIndex(0)

    def setup_styles(self):
        """设置基础样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QFrame#card {
                background-color: white;
                border-radius: 12px;
                border: none;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            }
            QLabel {
                color: #2d3748;
                font-size: 16px;
            }
            QLineEdit {
                padding: 12px;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
                font-size: 16px;
                selection-background-color: #4299e1;
                selection-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #4299e1;
            }
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 500;
                min-width: 120px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QPushButton:pressed {
                opacity: 0.8;
            }
        """)

    def setup_dark_mode(self, dark):
        """设置深色/浅色模式"""
        palette = self.palette()

        if dark:
            # 深色模式配色
            palette.setColor(QPalette.Window, QColor("#1a202c"))
            palette.setColor(QPalette.WindowText, QColor("#e2e8f0"))
            palette.setColor(QPalette.Base, QColor("#2d3748"))
            palette.setColor(QPalette.AlternateBase, QColor("#2d3748"))
            palette.setColor(QPalette.ToolTipBase, QColor("#e2e8f0"))
            palette.setColor(QPalette.ToolTipText, QColor("#e2e8f0"))
            palette.setColor(QPalette.Text, QColor("#e2e8f0"))
            palette.setColor(QPalette.Button, QColor("#2d3748"))
            palette.setColor(QPalette.ButtonText, QColor("#e2e8f0"))
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Highlight, QColor("#4299e1"))
            palette.setColor(QPalette.HighlightedText, Qt.white)

            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1a202c;
                }
                QFrame#card {
                    background-color: #2d3748;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                }
                QLabel {
                    color: #e2e8f0;
                }
                QLineEdit {
                    background-color: #4a5568;
                    border: 1px solid #4a5568;
                    color: #e2e8f0;
                }
                QLineEdit:focus {
                    border: 1px solid #4299e1;
                }
            """)
        else:
            # 浅色模式配色
            palette.setColor(QPalette.Window, QColor("#f5f7fa"))
            palette.setColor(QPalette.WindowText, QColor("#2d3748"))
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.AlternateBase, QColor("#f7fafc"))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, QColor("#2d3748"))
            palette.setColor(QPalette.Text, QColor("#2d3748"))
            palette.setColor(QPalette.Button, QColor("#edf2f7"))
            palette.setColor(QPalette.ButtonText, QColor("#2d3748"))
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Highlight, QColor("#4299e1"))
            palette.setColor(QPalette.HighlightedText, Qt.white)

            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f5f7fa;
                }
                QFrame#card {
                    background-color: white;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                }
                QLabel {
                    color: #2d3748;
                }
                QLineEdit {
                    background-color: white;
                    border: 1px solid #e2e8f0;
                    color: #2d3748;
                }
                QLineEdit:focus {
                    border: 1px solid #4299e1;
                }
            """)

        self.setPalette(palette)

    def create_welcome_page(self):
        """创建欢迎页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(0)

        # 顶部留白
        layout.addStretch(1)

        # 创建卡片式容器
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(30)
        card_layout.setContentsMargins(40, 40, 40, 40)

        # 标题和图标
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(10)

        # 图标 (使用文本图标作为示例)
        icon_label = QLabel("🏦")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px;")
        title_layout.addWidget(icon_label)

        title = QLabel("欢迎使用智能ATM")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            margin-bottom: 20px;
        """)
        title_layout.addWidget(title)
        card_layout.addWidget(title_container)

        # 卡号输入
        input_container = QWidget()
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(8)

        label = QLabel("请输入您的银行卡号:")
        label.setStyleSheet("font-size: 16px;")
        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText("例如: 6217 0000 0000 0000")
        self.card_input.setFixedHeight(50)
        self.card_input.setStyleSheet("font-size: 18px;")

        input_layout.addWidget(label)
        input_layout.addWidget(self.card_input)
        card_layout.addWidget(input_container)

        # 按钮
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(20)

        login_btn = QPushButton("插入卡片")
        login_btn.setFixedHeight(50)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self.insert_card)
        login_btn.setStyleSheet("""
            background-color: #4299e1;
            color: white;
            font-weight: 600;
        """)

        btn_layout.addStretch()
        btn_layout.addWidget(login_btn)
        btn_layout.addStretch()

        card_layout.addWidget(btn_container)
        card_layout.addStretch()

        layout.addWidget(card, stretch=2)
        layout.addStretch(1)

        self.stack.addWidget(page)

    def create_pin_page(self):
        """创建PIN码输入页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(0)

        # 顶部留白
        layout.addStretch(1)

        # 创建卡片式容器
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(30)
        card_layout.setContentsMargins(40, 40, 40, 40)

        # 标题
        title = QLabel("安全验证")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            margin-bottom: 20px;
        """)
        card_layout.addWidget(title)

        # PIN输入
        input_container = QWidget()
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(8)

        label = QLabel("请输入您的6位PIN码:")
        label.setStyleSheet("font-size: 16px;")
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("••••••")
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setFixedHeight(50)
        self.pin_input.setMaxLength(6)
        self.pin_input.setStyleSheet("font-size: 24px; letter-spacing: 4px;")
        self.pin_input.setAlignment(Qt.AlignCenter)

        input_layout.addWidget(label)
        input_layout.addWidget(self.pin_input)
        card_layout.addWidget(input_container)

        # 按钮
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(20)

        back_btn = QPushButton("返回")
        back_btn.setFixedHeight(50)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        back_btn.setStyleSheet("""
            background-color: #a0aec0;
            color: white;
            font-weight: 600;
        """)

        login_btn = QPushButton("确认")
        login_btn.setFixedHeight(50)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self.verify_pin)
        login_btn.setStyleSheet("""
            background-color: #4299e1;
            color: white;
            font-weight: 600;
        """)

        btn_layout.addWidget(back_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(login_btn)

        card_layout.addWidget(btn_container)
        card_layout.addStretch()

        layout.addWidget(card, stretch=2)
        layout.addStretch(1)

        self.stack.addWidget(page)

    def create_main_menu_page(self):
        """创建主菜单页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(0)

        # 顶部留白
        layout.addStretch(1)

        # 创建卡片式容器
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(30)
        card_layout.setContentsMargins(40, 40, 40, 40)

        # 标题
        title = QLabel("主菜单")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            margin-bottom: 20px;
        """)
        card_layout.addWidget(title)

        # 菜单按钮
        btn_container = QWidget()
        grid_layout = QGridLayout(btn_container)
        grid_layout.setSpacing(20)
        grid_layout.setContentsMargins(20, 20, 20, 20)

        # 创建菜单按钮
        balance_btn = self.create_menu_button("💰", "查询余额")
        balance_btn.clicked.connect(self.check_balance)

        withdraw_btn = self.create_menu_button("💵", "取款")
        withdraw_btn.clicked.connect(lambda: self.stack.setCurrentIndex(4))

        transfer_btn = self.create_menu_button("↔️", "转账")
        transfer_btn.setEnabled(False)  # 示例中未实现

        deposit_btn = self.create_menu_button("📥", "存款")
        deposit_btn.setEnabled(False)  # 示例中未实现

        history_btn = self.create_menu_button("📊", "交易记录")
        history_btn.setEnabled(False)  # 示例中未实现

        exit_btn = self.create_menu_button("🚪", "退出")
        exit_btn.clicked.connect(self.exit_atm)

        # 添加到网格布局
        grid_layout.addWidget(balance_btn, 0, 0)
        grid_layout.addWidget(withdraw_btn, 0, 1)
        grid_layout.addWidget(transfer_btn, 0, 2)
        grid_layout.addWidget(deposit_btn, 1, 0)
        grid_layout.addWidget(history_btn, 1, 1)
        grid_layout.addWidget(exit_btn, 1, 2)

        card_layout.addWidget(btn_container)
        card_layout.addStretch()

        layout.addWidget(card, stretch=2)
        layout.addStretch(1)

        self.stack.addWidget(page)

    def create_menu_button(self, icon, text):
        """创建菜单按钮"""
        btn = QPushButton()
        btn.setFixedSize(150, 150)
        btn.setCursor(Qt.PointingHandCursor)

        # 使用布局来组织图标和文本
        layout = QVBoxLayout(btn)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # 图标
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 36px;")
        layout.addWidget(icon_label)

        # 文本
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("font-size: 16px; font-weight: 500;")
        layout.addWidget(text_label)

        # 按钮样式
        btn.setStyleSheet("""
            QPushButton {
                background-color: #edf2f7;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
            QPushButton:pressed {
                background-color: #cbd5e0;
            }
            QPushButton:disabled {
                background-color: #f7fafc;
                color: #a0aec0;
            }
        """)

        return btn

    def create_balance_page(self):
        """创建余额查询页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(0)

        # 顶部留白
        layout.addStretch(1)

        # 创建卡片式容器
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(30)
        card_layout.setContentsMargins(40, 40, 40, 40)

        # 标题
        title = QLabel("账户余额")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            margin-bottom: 20px;
        """)

        # 余额显示
        balance_container = QWidget()
        balance_layout = QVBoxLayout(balance_container)
        balance_layout.setContentsMargins(0, 0, 0, 0)
        balance_layout.setSpacing(5)

        label = QLabel("当前可用余额:")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px; color: #718096;")

        self.balance_label = QLabel("￥0.00")
        self.balance_label.setAlignment(Qt.AlignCenter)
        self.balance_label.setStyleSheet("""
            font-size: 42px; 
            font-weight: bold; 
            color: #38a169;
            margin: 20px 0;
        """)

        balance_layout.addWidget(label)
        balance_layout.addWidget(self.balance_label)

        # 按钮
        back_btn = QPushButton("返回主菜单")
        back_btn.setFixedHeight(50)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        back_btn.setStyleSheet("""
            background-color: #4299e1;
            color: white;
            font-weight: 600;
        """)

        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addStretch()
        btn_layout.addWidget(back_btn)
        btn_layout.addStretch()

        card_layout.addWidget(title)
        card_layout.addWidget(balance_container)
        card_layout.addStretch()
        card_layout.addWidget(btn_container)

        layout.addWidget(card, stretch=2)
        layout.addStretch(1)

        self.stack.addWidget(page)

    def create_withdraw_page(self):
        """创建取款页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(0)

        # 顶部留白
        layout.addStretch(1)

        # 创建卡片式容器
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(30)
        card_layout.setContentsMargins(40, 40, 40, 40)

        # 标题
        title = QLabel("取款服务")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            margin-bottom: 20px;
        """)

        # 取款金额输入
        input_container = QWidget()
        input_layout = QVBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(8)

        label = QLabel("请输入取款金额:")
        label.setStyleSheet("font-size: 16px;")
        self.withdraw_input = QLineEdit()
        self.withdraw_input.setPlaceholderText("例如: 500")
        self.withdraw_input.setFixedHeight(50)
        self.withdraw_input.setStyleSheet("font-size: 18px;")

        input_layout.addWidget(label)
        input_layout.addWidget(self.withdraw_input)

        # 快速金额按钮
        amounts_container = QWidget()
        amounts_layout = QGridLayout(amounts_container)
        amounts_layout.setSpacing(15)
        amounts_layout.setContentsMargins(20, 20, 20, 20)

        amounts = [100, 200, 500, 1000, 2000, 5000]
        for i, amount in enumerate(amounts):
            btn = QPushButton(f"￥{amount}")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedHeight(45)
            btn.clicked.connect(lambda _, a=amount: self.withdraw_input.setText(str(a)))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #edf2f7;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #e2e8f0;
                }
            """)
            amounts_layout.addWidget(btn, i // 3, i % 3)

        # 按钮
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(20)

        back_btn = QPushButton("返回")
        back_btn.setFixedHeight(50)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        back_btn.setStyleSheet("""
            background-color: #a0aec0;
            color: white;
            font-weight: 600;
        """)

        withdraw_btn = QPushButton("确认取款")
        withdraw_btn.setFixedHeight(50)
        withdraw_btn.setCursor(Qt.PointingHandCursor)
        withdraw_btn.clicked.connect(self.withdraw_money)
        withdraw_btn.setStyleSheet("""
            background-color: #4299e1;
            color: white;
            font-weight: 600;
        """)

        btn_layout.addWidget(back_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(withdraw_btn)

        card_layout.addWidget(title)
        card_layout.addWidget(input_container)
        card_layout.addWidget(amounts_container)
        card_layout.addStretch()
        card_layout.addWidget(btn_container)

        layout.addWidget(card, stretch=2)
        layout.addStretch(1)

        self.stack.addWidget(page)

    def show_error(self, title, message):
        """显示错误消息框"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: #2d3748;
            }
        """)
        msg.exec_()
    def show_info(self, title, message):
        """显示信息消息框"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: #2d3748;
            }
        """)
        msg.exec_()
        
    # 回调处理方法
    def on_error(self, title, message):
        """错误回调处理"""
        self.signals.error_message.emit(title, message)
        
    def on_info(self, title, message):
        """信息回调处理"""
        self.signals.info_message.emit(title, message)
        
    def on_login_success(self):
        """登录成功回调处理"""
        self.stack.setCurrentIndex(1)  # 转到PIN输入页面
        
    def on_pin_verified(self):
        """PIN验证成功回调处理"""
        self.stack.setCurrentIndex(2)  # 转到主菜单
        
    def on_balance_result(self, balance):
        """余额查询结果回调处理"""
        self.balance_label.setText(f"￥{balance}")
        self.stack.setCurrentIndex(3)  # 转到余额显示页面
        
    def on_withdraw_success(self, amount):
        """取款成功回调处理"""
        self.signals.info_message.emit("取款成功", f"已成功取出 ￥{amount}")
        self.stack.setCurrentIndex(2)  # 返回主菜单
        
    def on_exit(self):
        """退出回调处理"""
        self.stack.setCurrentIndex(0)  # 返回欢迎页面
        self.card_input.clear()
        self.pin_input.clear()
        self.withdraw_input.clear()    # 业务逻辑方法重构
    def insert_card(self):
        """插入卡片（输入卡号）"""
        card_number = self.card_input.text().strip()
        self.client.process_card_insertion(card_number)

    def verify_pin(self):
        """验证PIN码"""
        pin = self.pin_input.text().strip()
        self.client.process_pin_verification(pin)

    def check_balance(self):
        """查询余额"""
        self.client.process_balance_check()

    def withdraw_money(self):
        """取款"""
        amount_text = self.withdraw_input.text().strip()
        self.client.process_withdrawal(amount_text)

    def exit_atm(self):
        """退出ATM"""
        self.client.process_exit()

    def closeEvent(self, event):
        """关闭窗口时断开连接"""
        if hasattr(self, 'client') and self.client:
            self.client.disconnect()
        super().closeEvent(event)