import pytest, os
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from utils import attach

load_dotenv()

DEFAULT_BROWSER_VERSION = '127.0'

def pytest_addoption(parser):
    parser.addoption('--executor', action='store', default='selenoid', help='local or selenoid')
    parser.addoption('--browser_version', action='store', default='', help='Browser version')


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    executor = request.config.getoption('--executor')
    browser_version = request.config.getoption('--browser_version') or DEFAULT_BROWSER_VERSION

    browser.config.base_url = 'https://demowebshop.tricentis.com/'
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = 'eager'

    if executor == 'local':
        #Локальный запуск
        browser.config.driver_options = driver_options
        browser.config.driver = webdriver.Chrome(options=driver_options)
    else:
        #Запуск через Selenoid
        selenoid_capabilities = {
            "browserName": "chrome",
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True
            },
            "goog:loggingPrefs": {"browser": "ALL"}
        }

        options = Options()
        options.capabilities.update(selenoid_capabilities)

        login = os.getenv('LOGIN_SELENOID')
        password = os.getenv('PASSWORD_SELENOID')
        url = os.getenv('URL_SELENOID')

        remote_url = f"https://{login}:{password}@{url}/wd/hub"
        browser.config.driver = webdriver.Remote(
            command_executor=remote_url,
            options=options
        )

    yield browser

    attach.add_screenshot(browser)
    attach.add_html(browser)
    attach.add_logs(browser)
    attach.add_video(browser)

    browser.quit()