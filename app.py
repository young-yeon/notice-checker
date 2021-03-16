"시험 결과 검색기"
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from selenium import webdriver
from bs4 import BeautifulSoup

form_class = uic.loadUiType('static/main.ui')[0]

class Window(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('static/icon.png'))
        notice = main()
        for note in notice:
            self.listWidget.addItem(note)



def chrome(path='static/chromedriver.exe', option=None):
    "셀레늄 크롬 반환"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    for opt in option:
        options.add_argument(opt)
    chrome_driver = webdriver.Chrome(path, options=options)
    return chrome_driver

def find_notice(html,
        js_path='#container > div.content > div > div.cont.right > div > div > ul > li'):
    "html에서 js select로 공지 가져와서 리스트로 반환"
    soup = BeautifulSoup(html, 'html.parser')
    notice_list = soup.select(js_path)
    return map(lambda li: li.select('a')[0]['title'], notice_list)

def main():
    "크롬으로 공지 조회하기"
    driver = chrome(option=['headless', '--log-level=3'])
    driver.get('http://recruit.kepco.co.kr/')
    driver.switch_to.frame('mainFrame')
    html = driver.page_source
    driver.close()
    notice = find_notice(html)
    return list(notice)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
