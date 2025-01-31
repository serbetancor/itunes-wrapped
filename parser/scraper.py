import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def artists_scraper(pending_artists):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    driver.get("https://music.apple.com/")

    time.sleep(3)
    for artist in pending_artists:
        try:
            search_box = driver.find_element(
                By.CSS_SELECTOR, "input.search-input__text-field"
            )
            search_box.clear()
            search_box.send_keys(artist["name"])
            search_box.send_keys(Keys.RETURN)

            time.sleep(random.uniform(5, 8))

            picture = driver.find_element(By.CSS_SELECTOR, "picture.svelte-3e3mdo")

            source = picture.find_element(By.TAG_NAME, "source")
            srcset = source.get_attribute("srcset")

            image_url = srcset.split(",")[0].split(" ")[0]
            artist["image"] = image_url

        except Exception as e:
            print(f"Error searching for {artist['name']}: {e}")

    return pending_artists
