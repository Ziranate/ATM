import sys
from PyQt5.QtWidgets import QApplication
from atm_gui import ATMGUI
from atm_client import ATMClient


def main():
    app = QApplication(sys.argv)

    # 创建ATM客户端实例
    client = ATMClient(host='localhost', port=2525)

    # 创建GUI并传入客户端实例
    gui = ATMGUI(client)
    gui.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
