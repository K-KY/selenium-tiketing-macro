from time import sleep

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from seleniumMacro.OpenAiConnector import connect_open_ai
from selenium.common.exceptions import UnexpectedAlertPresentException

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openai


import time

from seleniumMacro.SeatFinder import SeatFinder

print("1. 카카오 로그인, 2. 일반 로그인")
login_method = input("로그인 방법을 입력하세요: ")
login_method = int(login_method)

# ticket_address = input("예매할 공연 url(주소)을 입력하세요: ")
ticket_day = input("예매할 날짜 입력: ")
id = input("아이디를 입력하세요: ")
print("입력한 아이디", id)
password = input("비밀번호를 입력하세요: ")
print("입력한 비밀번호", password)
print("제대로 입력, 이걸로 에러나면 책임 안짐")
emergency_number1 = input("긴급 전화번호 ^###^ - #### - ####: ")
emergency_number2 = input("긴급 전화번호: |###| - ^####^ - ####: ")
emergency_number3 = input("긴급 전화번호: |###| - |####| - ^####^: ")
print("입력한 긴급 전화번호", ", " , emergency_number1, emergency_number2, emergency_number3)

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)  # 'chrome_options' 대신 'options' 사용
driver.set_window_size(1900, 1000)
yse24_rul = 'http://ticket.yes24.com/'
seat_finder = SeatFinder()



# 웹페이지가 로드될 때까지 2초를 대기
driver.implicitly_wait(2)
driver.get(yse24_rul)

# 스크롤 내리기
driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)

# 로그인
driver.find_element(By.XPATH,'//*[@id="consiceLogin"]').click()
main_window = driver.current_window_handle

if login_method == 1:
    driver.find_element(By.XPATH,'//*[@id="FBLoginSub_aBtnKakaoLogin"]').click()
    time.sleep(1)
    print('--------------------')
    print(driver.window_handles)
    main_window = driver.current_window_handle
    all_windows = driver.window_handles

    # 새로 열린 팝업 창으로 전환
    for window in all_windows:
        if window != main_window:
            driver.switch_to.window(window)
            break

    userId = driver.find_element(By.ID, 'loginId--1')
    userId.send_keys(id)
    userPwd = driver.find_element(By.ID, "password--2")
    userPwd.send_keys(password)
    userPwd.send_keys(Keys.ENTER)

    time.sleep(2)
    driver.switch_to.window(main_window)

if login_method == 2:
    print("일반 로그인")
    userId = driver.find_element(By.ID, 'SMemberID')
    userId.send_keys(id)
    userPwd = driver.find_element(By.ID, "SMemberPassword")
    userPwd.send_keys(password)
    userPwd.send_keys(Keys.ENTER)
    time.sleep(2)

time.sleep(1)

# 티켓 사이트 이동 d6
driver.get('http://ticket.yes24.com/Perf/50577')

# 티켓 사이트 이동 test
# driver.get('http://ticket.yes24.com/Perf/50789?Gcode=009_303')

def buy_ticket():
    global all_windows, main_window, window, driver
    driver.switch_to.window(main_window)
    driver.find_element(By.XPATH, '//*[@id="mainForm"]/div[9]/div/div[4]/a[4]').click()
    # driver.find_element(By.XPATH,'//*[@id="mainForm"]/div[10]/div/div[4]/a[4]').click()
    # 팝업 창이나 새로운 창이 열렸는지 확인
    all_windows = driver.window_handles
    time.sleep(2)
    print(all_windows)
    print(driver.window_handles)
    # 새로 열린 팝업 창으로 전환
    main_window = driver.current_window_handle
    all_windows = driver.window_handles
    for window in all_windows:
        if window != main_window:
            driver.switch_to.window(window)
            break


buy_ticket()


def day_selector():
    global driver
    link_element = driver.find_element(By.XPATH, "//a[text()='22']")
    link_element.click()
    # 좌석 선택
    driver.find_element(By.XPATH, '//*[@id="btnSeatSelect"]').click()
    # 구역, 좌석 선택하기
    select_seat = driver.find_element(By.XPATH, '//*[@id="divFlash"]/iframe')
    driver.switch_to.frame(select_seat)

    elements = driver.find_elements(By.XPATH, ".//*")

def fixed_finder():
    ### 지정석 구역 탐색
    global driver
    driver.find_element(By.XPATH, '//*[@id="grade_지정석"]').click()
    li_elements = driver.find_elements(By.CSS_SELECTOR, '.seat_layer li')
    target_fixed = seat_finder.find(li_elements, driver)
    return target_fixed

def standing_finder():
    ### 스탠딩 구역 탐색
    global driver
    driver.find_element(By.XPATH, '//*[@id="grade_스탠딩"]').click()
    li_elements = driver.find_elements(By.CSS_SELECTOR, '.seat_layer li')
    target_standing = seat_finder.find(li_elements, driver)
    return target_standing

while True:

    try :
        day_selector()
        stand = standing_finder()
        fixed = fixed_finder()
        if stand is not None or fixed is not None:
            if stand is not None:
                stand.click()
                continue
            if fixed is not None:
                fixed.click()
            break  # 루프 탈출
        driver.refresh()
        time.sleep(1)


    except UnexpectedAlertPresentException:
        ## 발생시 예매버튼부터 다시 시작
        print("에러 발생 예매를 다시 시도...")
        buy_ticket()


    except Exception as e:  # 일반적인 예외 처리 (Exception 이하의 모든 예외 처리)
        print(f"에러 발생 예매를 처음부터 다시 시작: {e}")
        driver.quit()
        break

    except BaseException as e:  # 시스템 관련 예외 처리
        print(f"에러 발생 예매를 처음부터 다시 시작: {e}")
        driver.quit()
        break


##타이틀 길이가 0보다 큰 요소 클릭
# driver.find_element(By.XPATH,'//*[@id="divSeatArray"]/div[string-length(@title)>0]').click()
# #driver.find_element(By.XPATH,'//*[@id="divSeatArray"]/div[120]').click()
# #driver.find_element((By.XPATH("//*[@attribute='grade']"))).click()

driver.find_element(By.XPATH,'//*[@id="form1"]/div[3]/div[2]/div/div[2]/p[2]/a/img').click()

# 할인/쿠폰
driver.switch_to.default_content()
driver.find_element(By.XPATH,'//*[@id="StepCtrlBtn03"]/a[2]/img').click()

#페이지 로딩
time.sleep(2)

# 긴급 전화번호 압력
driver.find_element(By.ID, 'ordererMobile1').clear()  # 기존 입력 값 제거
driver.find_element(By.ID, 'ordererMobile1').send_keys(emergency_number1)

driver.find_element(By.ID, 'ordererMobile2').clear()  # 기존 입력 값 제거
driver.find_element(By.ID, 'ordererMobile2').send_keys(emergency_number2)

driver.find_element(By.ID, 'ordererMobile3').clear()  # 기존 입력 값 제거
driver.find_element(By.ID, 'ordererMobile3').send_keys(emergency_number2)

# # 배송지 전화번호 입력
#
# driver.find_element(By.ID, 'deliveryMobile1').clear()  # 기존 입력 값 제거
# driver.find_element(By.ID, 'deliveryMobile1').send_keys('010')
#
# driver.find_element(By.ID, 'deliveryMobile2').clear()  # 기존 입력 값 제거
# driver.find_element(By.ID, 'deliveryMobile2').send_keys('1234')
#
# driver.find_element(By.ID, 'deliveryMobile3').clear()  # 기존 입력 값 제거
# driver.find_element(By.ID, 'deliveryMobile3').send_keys('5678')
#
# driver.find_element(By.XPATH,'//*[@id="StepCtrlBtn04"]/a[2]/img').click()
#


#결제방법
driver.find_element(By.XPATH,'//*[@id="rdoPays22"]').click()  #무통장 입금
select = Select(driver.find_element(By.XPATH,'//*[@id="selBank"]'))
select.select_by_index(1)


#이미지 분석
time.sleep(3)
code = connect_open_ai(driver.get_screenshot_as_base64())

driver.find_element(By.ID, 'captchaText').clear()  # 기존 입력 값 제거
driver.find_element(By.ID, 'captchaText').send_keys(code)

# 예매하기
driver.find_element(By.XPATH,'//*[@id="cbxAllAgree"]').click()
driver.find_element(By.XPATH,'//*[@id="imgPayEnd"]').click()



# while True:
#     driver.refresh()
#     print("done222")
