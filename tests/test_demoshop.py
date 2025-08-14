import allure
import os
from selene import browser, have
from api_methods import ShopAPI
from dotenv import load_dotenv


load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
URL = os.getenv("BASE_URL")

class TestCartFunctionality:
    api = ShopAPI()

    @allure.story("Authentication and add an item to shopping cart")
    @allure.title("Verify new item has been added to cart by authenticated user")
    def test_authenticated_cart_addition(self,setup_browser):
        with allure.step("authentication"):
            auth_response = self.api.authenticate_user()
            auth_cookie = auth_response.cookies.get("NOPCOMMERCE.AUTH")
            browser.open(URL)
            browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": auth_cookie})
            browser.open(URL)

        with allure.step("Verify that user successfully authenticated"):
            browser.element(".account").should(have.text(EMAIL))

        with allure.step("Adding a new item to cart using API method"):
            self.api.add_item_to_cart(auth_cookie)
            self._verify_cart_contents(auth_cookie, "14.1-inch Laptop")

    @allure.title("Adding a new item to shopping cart without authentication")
    def test_guest_cart_addition(self):
        with allure.step("adding new item"):
            response = self.api.add_item_to_cart()
            guest_cookie = response.cookies.get("Nop.customer")

        with allure.step("verifying shopping cart"):
            self._verify_cart_contents(guest_cookie, "14.1-inch Laptop")

    def _verify_cart_contents(self, session_cookie, expected_item):
        browser.open(URL)
        browser.driver.add_cookie({
            "name": "NOPCOMMERCE.AUTH" if "NOPCOMMERCE" in session_cookie else "Nop.customer",
            "value": session_cookie
        })
        browser.open(f"{URL}cart")

        with allure.step(f"verifying that '{expected_item}' is in the cart"):
            browser.element('.product-name').should(have.exact_text(expected_item))

        with allure.step("clear cart"):
            browser.element('.qty-input').set_value('0').press_enter()