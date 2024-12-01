from flask import Flask, render_template, request, redirect, session
import re
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 记得替换成实际复杂安全的密钥
app.config['TEMPLATES_AUTO_RELOAD'] = True

# 用于模拟存储申诉信息的列表（可后续替换为数据库操作）
appeal_records = []
# 模拟用户数据，实际中应从数据库获取并做好密码加密等，增加权限字段，默认为普通用户权限，注册后设为最高权限
users = {}

# 定义权限常量，方便后续使用和理解
ADMIN_PERMISSION = "admin"
NORMAL_PERMISSION = "user"

# 从本地文件加载已有数据（如果存在），实现简单的数据持久化
def load_data():
    global appeal_records, users
    try:
        print("开始加载数据...")
        with open('data.json', 'r') as file:
            data = json.load(file)
            appeal_records = data.get('appeal_records', [])
            users = data.get('users', {})
            # 确保加载的用户数据格式正确，如果密码等字段不存在则设置默认值
            for username, user_info in users.items():
                if not isinstance(user_info, dict):
                    users[username] = {"password": "", "permission": NORMAL_PERMISSION}
                elif "password" not in user_info:
                    user_info["password"] = ""
                elif "permission" not in user_info:
                    user_info["permission"] = NORMAL_PERMISSION
            print("数据加载完成，加载后的用户数据:", users)
        print("数据加载完成")
    except FileNotFoundError:
        print("数据文件不存在，使用默认空数据")
        pass

# 将当前数据保存到本地文件
def save_data():
    data = {
        'appeal_records': appeal_records,
        'users': users
    }
    print("开始保存数据，当前要保存的用户数据:", users)
    print("开始保存数据...")
    with open('data.json', 'w') as file:
        json.dump(data, file)
    print("数据保存完成")

# 注册自定义的enumerate过滤器，方便在模板中使用索引
@app.template_filter('enumerate')
def _enumerate(iterable):
    result = []
    index = 0
    for element in iterable:
        index += 1
        result.append((index, element))
    return result

@app.route('/')
def index():
    return render_template('index.html')

# 封禁申诉页面路由
@app.route('/appeal', methods=['GET', 'POST'])
def appeal():
    if request.method == 'POST':
        player_id = request.form.get('player_id')
        qq_number = request.form.get('qq_number')
        reason = request.form.get('reason')
        appeal_record = {
            "player_id": player_id,
            "qq_number": qq_number,
            "reason": reason,
            "status": "待处理",
            "reject_reason": ""
        }
        appeal_records.append(appeal_record)
        save_data()  # 提交申诉后保存数据
        return "申诉已提交，我们会尽快处理！"
    return render_template('appeal.html')

# 申诉进展页面路由
@app.route('/progress')
def progress():
    search_query = request.args.get('search_query')
    if search_query:
        search_results = [record for record in appeal_records if search_query == record['player_id'] or search_query == record['qq_number']]
    else:
        search_results = []
    return render_template('progress.html', search_results=search_results)

@app.route('/appeal_rules')
def appeal_rules():
    return render_template('appeal_rules.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 更严谨的用户名合法性验证
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            return render_template('register.html', error="用户名只能包含字母、数字和下划线，长度在3 - 20位之间")

        # 更严谨的密码合法性验证
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w]).{8,}$', password):
            return render_template('register.html', error="密码必须包含大小写字母、数字、特殊字符，长度至少8位")

        if password!= confirm_password:
            return render_template('register.html', error="两次输入的密码不一致，请重新输入")

        if username in users:
            return render_template('register.html', error="用户名已存在，请更换用户名")

        # 将新用户信息存入模拟的用户数据中，并设置权限为最高权限（实际应用中应存入数据库并处理权限相关逻辑更严谨）
        users[username] = {
            "password": password,
            "permission": ADMIN_PERMISSION
        }
        save_data()  # 注册成功后保存数据
        return redirect('/login')

    return render_template('register.html')

# 登录页面路由（完善登录验证及权限相关逻辑）
@app.route('/login', methods=['GET', 'POST'])
def login():
    username = None
    password = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    if username and password:
        username = username.strip()
        password = password.strip()
        if username in users and isinstance(users[username], dict) and "password" in users[username]:
            stored_password = users[username]["password"].strip()
            if password == stored_password:
                session['username'] = username
                print(f"用户 {username} 登录成功，设置 session['username'] 为 {username}")  # 新增打印语句，查看登录成功时用户名设置情况
                return redirect('/')
            else:
                print(f"密码错误，用户 {username} 登录失败")  # 新增打印语句，查看密码错误情况
                return render_template('login.html', error="密码错误，请重新输入")
        else:
            print(f"用户名 {username} 不存在，登录失败")  # 新增打印语句，查看用户名不存在情况
            return render_template('login.html', error="用户名不存在，请先注册")
    return render_template('login.html')

# 管理员面板页面路由（优化权限判断及数据传递逻辑，添加更多打印输出）
@app.route('/admin_panel')
def admin_panel():
    print("进入 admin_panel 路由，当前 session 中的用户名:", session.get('username'))  # 新增打印语句，查看进入路由时用户名情况
    if 'username' in session and users[session['username']]["permission"] == ADMIN_PERMISSION:
        print("当前用户权限为管理员权限，传递申诉记录数据到前端")
        print("传递给前端的申诉记录数据:", appeal_records)  # 新增打印语句，查看传递的数据内容
        return render_template('admin_panel.html', appeal_records=appeal_records)
    else:
        print("当前用户非管理员权限或未登录，重定向到登录页面")
        return redirect('/login')

# 管理员处理申诉路由（同意操作）
@app.route('/admin_panel/approve/<int:index>', methods=['POST'])
def approve_appeal(index):
    if 'username' in session and users[session['username']]["permission"] == ADMIN_PERMISSION:
        if index < len(appeal_records):
            appeal_records[index]['status'] = "通过"
            save_data()  # 处理申诉后保存数据
        return redirect('/admin_panel')
    else:
        return redirect('/login')

@app.route('/admin_panel/reject/<int:index>', methods=['POST'])
def reject_appeal(index):
    if 'username' in session and users[session['username']]["permission"] == ADMIN_PERMISSION:
        if index < len(appeal_records):
            reject_reason = request.form.get('reject_reason')
            appeal_records[index]['status'] = "拒收"
            appeal_records[index]['reject_reason'] = reject_reason if reject_reason else "未填写拒绝原因"
            save_data()  # 处理申诉后保存数据
        return redirect('/admin_panel')
    else:
        return redirect('/login')

# 注销路由
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    load_data()  # 启动应用时加载已有数据
    app.run(debug=True)