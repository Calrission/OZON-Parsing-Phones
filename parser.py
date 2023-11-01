from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep

from selenium.webdriver.remote.webelement import WebElement

from config import config
from models import Device


def new_inst_driver() -> WebDriver:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/118.0.0.0 Safari/537.36")
    new_driver = webdriver.Chrome(options=options)
    return new_driver


driver = new_inst_driver()
page = config["start_page"]


def update_page(new_page: int):
    global page
    page = new_page
    refresh_page()


def refresh_page():
    url = f"https://www.ozon.ru/category/smartfony-15502/?page={page}"
    driver.get(url)
    sleep(1)


def next_page():
    update_page(page + 1)


def prev_page():
    if page == 0:
        return
    update_page(page - 1)


def check_correct_now_page():
    try:
        driver.find_element(
            By.CLASS_NAME,
            "w1w"
        )
        return False
    except NoSuchElementException:
        return True


def parse_cover(container: WebElement) -> str:
    return container.find_element(By.CLASS_NAME, "is2").find_element(By.TAG_NAME, "img").get_attribute("src")


def parse_title(container: WebElement) -> str:
    return container.find_element(By.CLASS_NAME, "tsBody500Medium").text


def parse_rating(container: WebElement) -> (str | None, str | None):
    try:
        rating_block = (container
                        .find_element(By.CLASS_NAME, "tsBodyMBold")
                        .find_elements(By.CLASS_NAME, "t7"))
        try:
            rating = rating_block[0].text
        except NoSuchElementException:
            rating = None
        try:
            count_rating = rating_block[1].text
            count_rating = count_rating[:count_rating.index(" отзыв")]
        except NoSuchElementException:
            count_rating = None
        return rating, count_rating
    except NoSuchElementException:
        return None, None


def parse_price(container: WebElement) -> str:
    try:
        return container.find_element(By.CLASS_NAME, "c3118-b9").text
    except NoSuchElementException:
        return "0"


def parse_old_price(container: WebElement) -> str | None:
    try:
        return container.find_element(By.CLASS_NAME, "c3118-b0").text
    except NoSuchElementException:
        return None


def parse_count_lost(container: WebElement) -> str | None:
    try:
        count_lost = container.find_element(By.CLASS_NAME, "e6136-a4").text
        return count_lost.replace("Осталось", "").replace("шт", "")
    except NoSuchElementException:
        return None


def parse_discount(container: WebElement) -> str | None:
    try:
        return container.find_element(By.CLASS_NAME, "c3118-b1").text.replace("−", "")
    except NoSuchElementException:
        return None


def parse_url_device(container: WebElement) -> str:
    return container.find_element(By.CLASS_NAME, "tile-hover-target").get_attribute("href")


def parse_device_container(container: WebElement) -> Device:
    cover = parse_cover(container)
    title = parse_title(container)
    rating, count_rating = parse_rating(container)
    price = parse_price(container)
    old_price = parse_old_price(container)
    count_lost = parse_count_lost(container)
    discount = parse_discount(container)
    url_device = parse_url_device(container)
    return Device(
        cover=cover,
        title=title,
        rating=rating,
        price=price,
        old_price=old_price,
        count_rating=count_rating,
        count_lost=count_lost,
        discount=discount,
        url=url_device
    )


def get_devices_from_page() -> list[Device]:
    try:
        elem = driver.find_element(By.CSS_SELECTOR, "#paginatorContent > div")
        devices_container = elem.find_elements(By.CLASS_NAME, "ui9")
        return [parse_device_container(device_container) for device_container in devices_container]
    except NoSuchElementException:
        return []


def cloudframe_bypass():
    global driver
    driver.quit()
    driver = new_inst_driver()
