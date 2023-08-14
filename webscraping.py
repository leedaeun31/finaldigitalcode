from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time,requests

#pip install selenium/request/beautifulsoup/webdriver-manager/구글 드라이브 설치 필수

#구글 드라이브 불러오기
op = Options()
ser = "C:\\Users\\SAMSUNG\\Downloads\\chromedriver-win32\\chromedriver.exe" #설치한 드라이브의 위치 넣기
op.add_argument(f"webdriver.chrome.driver={ser}")
dr = webdriver.Chrome(options=op)

#디지털 새싹 사이트 열기
url = "https://newsac-application.kr/"
dr.get(url)
time.sleep(1)

#대기
wait = WebDriverWait(dr, 20)
wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'html')))

#html에서 location을 찾고 강원/충청권 옵션 선택
location = Select(dr.find_element(By.CSS_SELECTOR, "select.block.w-full"))
location.select_by_visible_text("강원/충청권")
time.sleep(1)

# 링크 수집
rinks = []

while True:
    try:
        #더보기 버튼 누르기
        more = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > div > div:nth-child(2) > div.container.p-4.mx-auto > div > div:nth-child(1) > div.xl\:flex > div.mt-4.xl\:mt-0.xl\:ml-4.flex-1 > div:nth-child(2) > div > div:nth-child(2) > button")))
        more.click()
        time.sleep(1) 
    except:
        break

    # 디지털 새싹 홈페이지에서 href 찾아서 리스트에 추가
    rink = dr.find_elements(By.CSS_SELECTOR, "body > main > div > div:nth-child(2) > div.container.p-4.mx-auto > div > div:nth-child(1) > div.xl\:flex > div.mt-4.xl\:mt-0.xl\:ml-4.flex-1 > div:nth-child(2) > div > div.grid.grid-cols-1.gap-4.my-4 a")
    for element in rink:
        href = element.get_attribute('href')
        if href is not None:
            rinks.append(href)

#중복되는 링크 제거 
rinks = list(set(rinks)) 

tmp = 601 
#각 링크에서 필요한 정보 크롤링
for curl in rinks:
    dr.get(curl)
    time.sleep(1)

    wait = WebDriverWait(dr, 20)
    wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'html')))

    response = requests.get(curl, verify=True)  
    html = BeautifulSoup(dr.page_source, 'html.parser')

    iframe = html.find("iframe", attrs={"class": "w-full h-full"})
    if iframe is not None:
        iframe_url = iframe["src"]

        iframe_response = requests.get(iframe_url, verify=True)  # SSL 인증서 무시
        iframe_content = iframe_response.content
        iframe_soup = BeautifulSoup(iframe_content, "html.parser")


        #제목
        title = iframe_soup.find('div', class_='text-xl font-bold')
        if title is not None:
            title_value= " ".join(title.get_text().split())
        #날짜
        day = iframe_soup.find(class_='lg:flex items-center')
        if day is not None:
            day_value= " ".join(day.get_text().split())
        #장소
        place= iframe_soup.find(class_='mt-2 lg:mt-0')
        if place is not None:
            place_value= " ".join(place.get_text().split())

        #딕셔너리에 저장
        dic={
            "target":"청소년",
            "title":title_value,
            "place":place_value,
            "date":day_value,
            "url":curl
        }

        #오로지 데이터 추가를위한 코드
        #send=requests.post('http://13.124.76.164:8000/sites/',data=dic)

        #patch로 데이터 전송
        send = requests.patch('http://13.124.76.164:8000/sites/'+str(tmp)+'/', data=dic)
        tmp+=1

#patch로 전송하고 남은거는 None 처리
while True:
    if tmp<=707:
        dic["target"]=None
        dic["title"]=None
        dic["date"]=None
        dic["place"]=None
        dic["url"]=None
        send = requests.patch('http://13.124.76.164:8000/sites/'+str(tmp)+'/', data=dic)
        tmp+=1
    else:
        break

    

'''
        tv=dic["title"]
        print("제목:",tv)
        dv=dic["date"]
        print("날짜:",dv)
        pv=dic["place"]
        print("장소:",pv)
        #cv=dic["내용"]
        #print("내용:",cv)
        ur=dic["url"]
        print("URL:",ur)
        print("\n")
'''


