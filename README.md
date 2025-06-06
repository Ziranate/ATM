# ATM 模拟系统

## 1. 项目名称和简介
本项目是一个基于客户端-服务器架构的 ATM（自动取款机）模拟系统。它允许用户通过图形用户界面 (GUI) 或命令行界面与模拟的银行服务器进行交互，执行如身份验证、余额查询、取款等基本银行操作。

## 2. 安装方法
由于这是一个 Python 项目，安装和运行相对简单：

1.  **克隆仓库** (如果您是从版本控制系统获取):
    ```bash
    git clone https://github.com/Ziranate/ATM
    cd ATM
    ```


2.  **环境要求**:
    *   Python 3.12
    *   推荐使用 requirements.txt 文件自动安装依赖。

3.  **安装依赖**:
    在项目根目录下运行：
    ```bash
    pip install -r requirements.txt
    ```

    > 如果遇到 PyQt5 安装问题，建议先升级 pip ：
    > ```bash
    > python -m pip install --upgrade pip
    > ```

## 3. 使用说明

### 启动服务器
在项目根目录下运行：
```powershell
python -m src.server
```

### 启动客户端（GUI）
在项目根目录下运行：
```powershell
python -m src.main
```

> **注意：**
> 必须在项目根目录下用 `python -m src.main` 方式运行，不能直接 `python src/main.py`，否则会因相对导入报错。

## 4. 功能特性
*   **用户身份验证**: 通过卡号 (userid) 和 PIN 码进行安全登录。
*   **余额查询**: 用户可以查询其账户的当前余额。
*   **取款操作**: 用户可以从其账户中提取指定金额的现金。
*   **客户端-服务器通信**: 使用自定义协议 (RFC20232023) 进行可靠通信。
*   **日志记录**: 客户端和服务器的操作都会被记录在相应的日志文件中 (`logs/atm_client.log`, `logs/server.log`)。
*   **用户数据存储**: 用户信息和账户数据存储在 `data/users.json` 文件中。


## 5. 目录结构
```
.
├── data/                 
│   └── users.json        # 存储所有用户信息和账户数据
├── doc/                  
│   ├── RFC20232023.md    # RFC20232023协议文档
│   └── 作业2-实验报告.pdf # 实验报告文档
├── logs/                 
│   ├── atm_client.log    # 客户端操作日志
│   └── server.log        # 服务器操作日志
├── src/                 
│   ├── __init__.py       # Python 包初始化文件
│   ├── atm_client.py     # ATM 客户端核心逻辑
│   ├── atm_gui.py        # ATM 图形界面实现
│   ├── bank_icon.svg     # 窗口图标
│   ├── main.py           # 客户端程序入口
│   └── server.py         # 服务器端主程序
├── .gitignore            
├── README.md             
└── requirements.txt      
```

## 6. 协议说明：RFC20232023协议

#### **1. ATM发送至服务器的消息**
| 消息名称         | 用途描述                          |
|------------------|-----------------------------------|
| `HELO sp <userid>` | 通知服务器ATM已插卡，传输用户ID（卡号） |
| `PASS sp <passwd>` | 发送用户输入的PIN密码至服务器        |
| `BALA`           | 请求查询账户余额                    |
| `WDRA sp <amount>`| 请求提取指定金额                    |
| `BYE`            | 用户操作结束，断开连接              |

#### **2. 服务器发送至ATM的消息**
| 消息名称           | 用途描述                          |
|--------------------|-----------------------------------|
| `500 sp AUTH REQUIRE` | 要求用户输入PIN密码                |
| `525 sp OK!`        | 操作（密码验证、取款等）成功        |
| `401 sp ERROR!`     | 操作失败（密码错误、余额不足等）    |
| `AMNT :<amnt>`      | 返回余额查询结果                    |
| `BYE`              | 操作结束，指示ATM显示欢迎界面       |