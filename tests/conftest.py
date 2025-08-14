import pytest, os
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from utils import attach


def pytest_addoption(parser):
    parser.addoption(
        "--executor",
        action="store",
        default="local",
        help="Executor: local or remote (e.g., selenoid hostname or IP)"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        help="Run headless mode"
    )

@pytest.fixture
def browser(request):
    executor = request.config.getoption("--executor")
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    options = Options()
    if headless:
        options.add_argument("--headless")

    if executor == "local":
        driver = webdriver.Chrome(options=options)
    else:
        capabilities = {
            "browserName": browser_name,
            "enableVNC": True,
            "enableVideo": False
        }
        driver = webdriver.Remote(
            command_executor=f"http://{executor}:4444/wd/hub",
            options=options,
            desired_capabilities=capabilities
        )

    driver.maximize_window()
    yield driver
    driver.quit()



#@pytest.fixture(scope='function', autouse=True)
#def setup_browser():
#    browser.config.window_height = 1080
#    browser.config.window_width = 1920
#    browser.config.base_url = 'https://demowebshop.tricentis.com/'
#    driver_options = webdriver.ChromeOptions()
#    driver_options.add_argument('--headless')
#    driver_options.page_load_strategy = 'eager'
#    browser.config.driver_options = driver_options
#
#    yield

#    browser.quit()

DEFAULT_BROWSER_VERSION = "127.0"


def pytest_addoption(parser):
    parser.addoption(
        '--browser_version',
        default='127.0'
    )
@pytest.fixture(scope="session", autouse=True)
def setup_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    browser_version = request.config.getoption('--browser_version')
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION
    browser.config.base_url = 'https://demowebshop.tricentis.com/'
    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = 'eager'
    browser.config.driver_options = driver_options
    browser.config.window_width = 1920
    browser.config.window_height = 1080

    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        },
        "goog:loggingPrefs": {"browser": "ALL"}
    }
    options.capabilities.update(selenoid_capabilities)

    login = os.getenv('LOGIN_SELENOID')
    password = os.getenv('PASSWORD_SELENOID')
    url = os.getenv('URL_SELENOID')

    browser.config.driver = webdriver.Remote(
        command_executor=f"https://{login}:{password}@{url}/wd/hub",
        options=options)

    yield browser

    attach.add_screenshot(browser)
    attach.add_html(browser)
    attach.add_video(browser)
    attach.add_logs(browser)

    browser.quit()
