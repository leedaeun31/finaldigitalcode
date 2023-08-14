# webscraping_Project

## 프로젝트 소개
  -디지털 새싹("https://newsac-application.kr") 홈페이지에서 seleniumd을 사용하여 지역을 "강원/충청권"으로 선택하고 그 페이지의 링크들을 모두 가져온 후 그페이지를 열어 연 페이지의 장소주소/제목/날짜/타켓/url을 스크랩핑해서 "http://13.124.76.164:8000/sites/"에 request를 사용해서 데이터를 전송해주는 프로그램입니다. 


<br>

## 기술 스택

| Python | 

<br>

## 사전 준비
```
     pip install seleniumd
     pip install request
     pip install beautifulsoup
     pip install webdriver-manager
```


## webscraping.py 구현 기능

### 기능 1 
  코드<br>
  op = Options()<br>
  ser = "C:\\Users\\SAMSUNG\\Downloads\\chromedriver-win32\\chromedriver.exe"<br>
  op.add_argument(f"webdriver.chrome.driver={ser}")<br>
  dr = webdriver.Chrome(options=op)<br>

  url = "https://newsac-application.kr/"<br>
  dr.get(url)<br>
  time.sleep(1)<br>
  
  설명<br>
  webdriver사용해서 수동으로 chrome driver 주소 설정 후 "https://newsac-application.kr/" 페이지 오픈
  
###  기능 2
    코드
    location = Select(dr.find_element(By.CSS_SELECTOR, "select.block.w-full"))
    location.select_by_visible_text("강원/충청권")

    while True:
      try:
          more = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > main > div > div:nth-child(2) > div.container.p-4.mx-auto > div > div:nth-child(1) > div.xl\:flex > div.mt-4.xl\:mt-0.xl\:ml-4.flex-1 > div:nth-child(2) > div > div:nth-child(2) > button")))
          more.click()
          time.sleep(1) 
      except:
          break
      rink = dr.find_elements(By.CSS_SELECTOR, "body > main > div > div:nth-child(2) > div.container.p-4.mx-auto > div > div:nth-child(1) > div.xl\:flex > div.mt-4.xl\:mt-0.xl\:ml-4.flex-1 > div:nth-child(2) > div > div.grid.grid-cols-1.gap-4.my-4 a")
      for element in rink:
        href = element.get_attribute('href')
        if href is not None:
            rinks.append(href)
            
    설명
    지역 선택하기 ("강원/충청권")
    더보기 버튼 누르기
    페이지에서 링크만 가져와서 rink 리스트에 넣어

### 기능 3 
    코드
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

        iframe_response = requests.get(iframe_url, verify=True)  
        iframe_content = iframe_response.content
        iframe_soup = BeautifulSoup(iframe_content, "html.parser")

        title = iframe_soup.find('div', class_='text-xl font-bold')
        if title is not None:
            title_value= " ".join(title.get_text().split())
            .
            .
            .
       ------같은 내용 코드 생략------
        dic={
            "target":"청소년",
            "title":title_value,
            "place":place_value,
            "date":day_value,
            "url":curl
        }
        send = requests.patch('http://13.124.76.164:8000/sites/'+str(tmp)+'/', data=dic)
        tmp+=1
        
    설명
    링크 페이지 열고 그 페이지에서 필요한 정보를 가져와서 딕셔너리에 저장
    저장한 정보를 requests를 사용해서 patch로 전송
  
### 기능 4 
    코드
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
        
    설명
    tmp값이 조건보다 작은경우 남은 값들에는 None 값 넣어서 ruequsts를 사용해서 patch로 전송
  
<br>

## 배운 점 & 아쉬운 점
  - 이코드르 짜면서 seleniumd과  webdriver-manager 사용방법을 알게되었다.<br>
  - chrome 페이지가 열리는 점이 아쉽다.<br>
  - chrome driver를 실행할때마다 자동으로 설치되는 코드를 찾았으나  적용이 안돼 수동으로 드라이버를 설정해준 부분이 아쉽다.<br>
<br>
<br>


<!-- Stack Icon Refernces -->

[python]: /img/python.png

