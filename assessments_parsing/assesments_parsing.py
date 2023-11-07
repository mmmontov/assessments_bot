import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_marks(login: str, password: str):
    options_chrome = webdriver.ChromeOptions()
    school = 'СОШ 60'
    # options_chrome.add_argument('--headless')

    with webdriver.Chrome(options=options_chrome) as browser:
        url = 'https://sgo.prim-edu.ru/angular/school/main/'
        browser.get(url)

        # вход в аккаунт =======================================================================
        open_schools = browser.find_element(By.CLASS_NAME, 'select2-selection__arrow').click()
        write_school = browser.find_element(By.CLASS_NAME, 'select2-search__field').send_keys(school)
        time.sleep(1)
        enter_school = browser.find_element(By.CLASS_NAME, 'select2-results').click()  
        enter_login = browser.find_element(By.NAME, 'loginname').send_keys(login)
        enter_password = browser.find_element(By.NAME, 'password').send_keys(password)  
        time.sleep(1)
        login_to_account = browser.find_element(By.CLASS_NAME, 'primary-button').click()
        time.sleep(7)

        # пропуск страницы с предупреждением ===================================================
        try:
            skip_button = browser.find_element(By.TAG_NAME, 'html').find_elements(By.TAG_NAME, 'button')
            click_skip = skip_button[-1].click() 
        except:
            print('небыло одновременно запущенных сессий')
            time.sleep(3) 
        time.sleep(7)

        # переход на страницу с оценками =======================================================
        try:
            reports_click = browser.find_elements(By.XPATH, '//li')[9].click()
            time.sleep(7)
            studenttotal = browser.find_element(By.XPATH, "//a[@ng-href='studenttotal']").click()
            time.sleep(5)
            create_marks = browser.find_element(By.XPATH, "//button[@title='Сформировать']").click()
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
                # print(f'Предмет: {name}\nОценки: {" ".join(marks)}\nСредний бал: {avg}\n')
            return student_marks
        except:
            return None
    

