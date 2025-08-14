import requests
import os
import allure
from allure_commons.types import AttachmentType
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
URL = os.getenv("BASE_URL")

class ShopAPI:
    def authenticate_user(self):
        with allure.step("Авторизация пользователя через API"):
            response = requests.post(
                url=f"{URL}login",
                data={
                    "Email": EMAIL,
                    "Password": PASSWORD,
                    "RememberMe": False
                },
                allow_redirects=False
            )
            self._log_response(response)
            return response

    def add_item_to_cart(self, auth_cookie=None):
        with allure.step("Добавление товара в корзину через API"):
            cookies = {'NOPCOMMERCE.AUTH': auth_cookie} if auth_cookie else None
            response = requests.post(
                url=f"{URL}addproducttocart/catalog/31/1/1",
                cookies=cookies
            )
            self._log_response(response)
            return response

    @staticmethod
    def _log_response(response):
        allure.attach(body=response.text, name="Ответ API",
                      attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(response.cookies), name="Cookies ответа",
                      attachment_type=AttachmentType.TEXT, extension="txt")