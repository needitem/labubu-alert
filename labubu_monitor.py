from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
import requests
import json
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Telegram Bot 설정
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

# User-Agent 리스트 (랜덤 로테이션)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0'
]

def send_telegram_notification(product_name, product_link):
    """텔레그램으로 재입고 알림 전송"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("텔레그램 설정이 없습니다. 환경변수를 설정해주세요.")
        return
    
    try:
        message = f"🎉 라부부 재입고 알림!\n\n{product_name}\n\n{product_link}"
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("텔레그램 알림 전송 성공!")
        else:
            print(f"텔레그램 알림 전송 실패: {response.status_code}")
            
    except Exception as e:
        print(f"텔레그램 알림 전송 중 오류: {e}")

def get_chrome_options():
    options = Options()
    
    # 기본 headless 설정
    options.add_argument('--headless')  # headless 모드 복원
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    # 봇 탐지 회피용 설정
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')
    
    # GPU 에러 방지
    options.add_argument('--disable-webgl')
    options.add_argument('--disable-3d-apis')
    options.add_argument('--disable-accelerated-2d-canvas')
    
    # 로그 억제
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    
    # 랜덤 User-Agent 설정
    user_agent = random.choice(USER_AGENTS)
    options.add_argument(f'--user-agent={user_agent}')
    
    return options





def check_specific_product(target_product_id="2127"):
    """라부부 목록 페이지에서 특정 상품 품절 상태 확인"""
    driver = None
    try:
        options = get_chrome_options()
        driver = webdriver.Chrome(options=options)
        
        url = "https://popmart.co.kr/product/list.html?cate_no=87"
        driver.get(url)
        time.sleep(random.uniform(3, 5))
        
        body_html = driver.find_element(By.TAG_NAME, "body").get_attribute('innerHTML')
        soup = BeautifulSoup(body_html, 'html.parser')
        
        # ID가 해당하는 상품 찾기
        target_li = soup.find('li', id=f'anchorBoxId_{target_product_id}')
        
        if not target_li:
            return None
            
        # 해당 상품 내에서 soldout show 클래스 확인
        soldout_show = target_li.find('span', class_='soldout show')
        is_sold_out = soldout_show is not None
        
        return not is_sold_out
        
    except Exception as e:
        return None
    finally:
        if driver:
            driver.quit()

def monitor_specific_product():
    """특정 상품을 1분마다 모니터링"""
    target_name = "THE MONSTERS 내 마음속 비밀번호 시리즈 인형 키링 (N-Z)"
    target_id = "2127"
    is_sold_out = True
    
    print(f"'{target_name}' 모니터링 시작...")
    print(f"검사 간격: 1분")
    print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    while True:
        try:
            is_available = check_specific_product(target_id)
            
            current_time = datetime.now().strftime('%H:%M:%S')
            
            if is_available is None:
                print(f"[{current_time}] 확인 불가")
            elif is_available and is_sold_out:
                print(f"\n{'='*50}")
                print(f"🎉 [{current_time}] {target_name} 재입고!")
                print(f"https://popmart.co.kr/product/the-monsters-내-마음속-비밀번호-시리즈-인형-키링-n-z/{target_id}/category/87/display/1/")
                print(f"{'='*50}\n")
                
                send_telegram_notification(target_name, f"https://popmart.co.kr/product/the-monsters-내-마음속-비밀번호-시리즈-인형-키링-n-z/{target_id}/category/87/display/1/")
                
                is_sold_out = False
            elif not is_available:
                if not is_sold_out:
                    is_sold_out = True
                print(f"[{current_time}] 품절")
            else:
                print(f"[{current_time}] 재고 있음")
                
            time.sleep(60)
            
        except KeyboardInterrupt:
            print("\n모니터링이 중단되었습니다.")
            break
        except Exception as e:
            print(f"오류 발생: {e}")
            time.sleep(30)


def test_telegram():
    """텔레그램 알림 테스트"""
    send_telegram_notification("THE MONSTERS 내 마음속 비밀번호 시리즈 인형 키링 (N-Z)", "https://popmart.co.kr/product/the-monsters-내-마음속-비밀번호-시리즈-인형-키링-n-z/2127/category/87/display/1/")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_telegram()
    else:
        monitor_specific_product()