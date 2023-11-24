import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def wait(browser: webdriver.Chrome):
    time.sleep(1)
    complete = None
    while complete != 'complete':
        complete = browser.execute_script('return document.readyState')


def get_marks(login: str, password: str):
    options_chrome = webdriver.ChromeOptions()
    school = 'СОШ 60'
    # options_chrome.add_argument('--headless')
    options_chrome.add_argument('--window-size=1280,1200')

    with webdriver.Chrome(options=options_chrome) as browser:
        url = 'https://sgo.prim-edu.ru/angular/school/main/'
        browser.get(url)

        # вход в аккаунт =======================================================================
        browser.find_element(By.CLASS_NAME, 'select2-selection__arrow').click()
        browser.find_element(By.CLASS_NAME, 'select2-search__field').send_keys(school)
        time.sleep(1)
        browser.find_element(By.CLASS_NAME, 'select2-results').click()  
        browser.find_element(By.NAME, 'loginname').send_keys(login)
        browser.find_element(By.NAME, 'password').send_keys(password)  
        time.sleep(1)
        browser.find_element(By.CLASS_NAME, 'primary-button').click()
        wait(browser)

        # пропуск страницы с предупреждением ===================================================
        try:
            skip_button = browser.find_element(By.TAG_NAME, 'html').find_elements(By.TAG_NAME, 'button')
            skip_button[-1].click() 
        except:
            print('небыло одновременно запущенных сессий')
            wait(browser)
        wait(browser)

        # переход на страницу с оценками =======================================================
        try:
            browser.find_elements(By.XPATH, '//li')[9].click()
            wait(browser)
            browser.find_element(By.XPATH, "//a[@ng-href='studenttotal']").click()
            wait(browser)    
            browser.find_element(By.XPATH, "//button[@title='Сформировать']").click()
            time.sleep(10)
        except:
            return None
        
        # парсинг оценок =======================================================================
        student_marks = {}
        try:
            table = browser.find_element(By.CLASS_NAME, 'table-print')
            print('таблица сформировалась')
            subjects = table.find_elements(By.TAG_NAME, 'tr')[2:]
            # print('строки найдены\n')
            for line in subjects:
                sub = line.find_elements(By.TAG_NAME, 'td')
                sub = list(map(lambda x: x.text, sub))
                
                name = sub[0]
                avg = sub[-1]
                marks = [i for i in sub[1:-1] if i != '']
                if not marks:
                    marks = ['нет оценок']    

                student_marks[name] = {'marks': marks, 'avg': avg}
                browser.get_screenshot_as_file('marks_photo/marks.png')
                # print(f'Предмет: {name}\nОценки: {" ".join(marks)}\nСредний бал: {avg}\n')
            return student_marks
        except:
            return None
    


