# 라부부 재입고 모니터 - Specific 모드

특정 라부부 상품의 재입고 상태를 1분마다 확인하고 텔레그램으로 알림을 보내는 프로그램입니다.

## 코드 설명

Selenium WebDriver를 사용해 팝마트 웹사이트를 자동으로 크롤링하여 특정 상품(THE MONSTERS 키링)의 품절 상태를 실시간 모니터링합니다. BeautifulSoup으로 HTML을 파싱하고, 재입고 감지 시 Telegram Bot API를 통해 즉시 알림을 전송합니다. 봇 탐지를 회피하기 위해 랜덤 User-Agent와 headless 브라우저 옵션을 적용했으며, Railway 등 클라우드 서비스에서 24시간 실행 가능합니다.

## 기능
- THE MONSTERS 내 마음속 비밀번호 시리즈 인형 키링 (N-Z) 상품 모니터링
- 1분마다 자동 확인
- 재입고 시 텔레그램 알림 발송

## 설정 방법

### 1. 라이브러리 설치
```bash
pip install -r requirements.txt
```

### 2. 텔레그램 봇 설정
1. `config.bat` 파일을 실행하세요
2. BotFather에서 봇을 만들고 토큰을 입력하세요: https://t.me/BotFather
3. 채팅 ID를 확인하고 입력하세요: https://t.me/userinfobot

또는 `.env` 파일을 직접 수정하세요:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 3. 실행
```bash
python labubu_monitor.py
```

## 필요한 라이브러리
- selenium
- beautifulsoup4  
- requests
- python-dotenv

## 환경설정
`.env` 파일에서 설정:
- `TELEGRAM_BOT_TOKEN`: 텔레그램 봇 토큰
- `TELEGRAM_CHAT_ID`: 텔레그램 채팅 ID

## 24시간 클라우드 배포

### Railway (추천)
1. 코드를 GitHub에 업로드
2. [Railway](https://railway.app)에 가입 후 GitHub 연결
3. 프로젝트 생성 및 자동 배포
4. Environment Variables에서 텔레그램 설정:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

### 기타 무료 서비스
- **Render**: 백그라운드 서비스 지원
- **Fly.io**: Docker 배포 지원
- **Google Cloud Run**: 무료 할당량 제공

### 배포 시 주의사항
- `requirements.txt` 파일 필요
- 클라우드 환경에서는 Chrome 브라우저 자동 설치
- 환경변수로 텔레그램 설정 관리

## 주의사항
- Chrome 브라우저가 설치되어 있어야 합니다 (로컬 실행 시)
- 네트워크 연결이 필요합니다
- Ctrl+C로 모니터링을 중단할 수 있습니다