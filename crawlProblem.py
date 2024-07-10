from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
def searchProblem(user_id, problem_number):
    # WebDriver 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # BOJ 사이트 접속
        driver.get('https://www.acmicpc.net/status')

        # 페이지가 로드될 때까지 기다리기
        time.sleep(0.2)

        # 문제 검색창 찾기 (NAME 속성을 사용하여)
        searchBox = driver.find_element(By.NAME, 'problem_id')

        # 문제 번호 입력
        searchBox.send_keys(problem_number)

        # 아이디 검색창 찾기(NAME 속성을 사용하여)
        searchBoxId = driver.find_element(By.NAME,'user_id')

        # id 입력
        searchBoxId.send_keys(user_id)

        # 검색 실행
        searchBox.send_keys(Keys.RETURN)

        # 검색 결과 로딩 기다리기
        time.sleep(0.2)


        # '맞았습니다!!'가 포함된 제출 기록 찾기
        rows = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
        correctSubmissions = []

        for row in rows:
            result = row.find_element(By.CSS_SELECTOR, 'td.result').text
            if '맞았습니다!!' in result:
                submissionId = row.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text
                memory = row.find_element(By.CSS_SELECTOR, 'td:nth-child(5)').text
                timeTaken = row.find_element(By.CSS_SELECTOR, 'td:nth-child(6)').text
                codeLength = row.find_element(By.CSS_SELECTOR, 'td:nth-child(8)').text
                correctSubmissions.append({
                    'submissionId': submissionId,
                    'memory': memory,
                    'time': timeTaken,
                    'codeLength': codeLength
                })
         

        # 결과 출력
        for submission in correctSubmissions:
            print(f"제출번호: {submission['submissionId']}, 메모리: {submission['memory']}KB, 시간: {submission['time']}ms, 코드 길이: {submission['codeLength']}B")
        
        # 결과를 JSON 형태로 가공
        with open('correctSubmissions.json', 'w', encoding='utf-8') as f:
            json.dump(correctSubmissions, f, ensure_ascii=False, indent=4)

    finally:
        # 브라우저 닫기
        driver.quit()

