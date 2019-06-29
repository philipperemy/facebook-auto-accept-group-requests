from argparse import ArgumentParser

from FacebookWebBot import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_script_arguments():
    args = ArgumentParser()
    args.add_argument('--fb_user', required=True)
    args.add_argument('--fb_pass', required=True)
    args.add_argument('--chromedriver')
    args.add_argument('--headless', action='store_true')
    return args.parse_args()


def fetch_new_requests(client):
    url = 'https://m.facebook.com/groups/1169550593165023?view=members&ref=group_browse'
    client.get(url)
    a = 2
    try:
        # client.find_elements_by_tag_name('button')[0].click()
        print('User accepted.')
    except:
        pass


def login(client, email, password):
    '''Log to facebook using email (str) and password (str)'''

    url = 'https://mbasic.facebook.com'
    client.get(url)
    email_element = client.find_element_by_name('email')
    email_element.send_keys(email)
    pass_element = client.find_element_by_name('pass')
    pass_element.send_keys(password)
    pass_element.send_keys(Keys.ENTER)
    try:
        client.find_elements_by_class_name('bk')[0].click()
        print('Logged in.')
        return True
    except NoSuchElementException:
        print('Fail to login.')
        return False


def logout(client):
    url = 'https://mbasic.facebook.com/logout.php?h=AffSEUYT5RsM6bkY&t=1446949608&ref_component=mbasic_footer&ref_page=%2Fwap%2Fhome.php&refid=7'
    try:
        client.get(url)
        print('Disconnected.')
        return True
    except Exception:
        print('Failed to log out')
        return False


def main():
    args = get_script_arguments()
    options = Options()
    if args.headless:
        options.add_argument('--headless')
    if args.chromedriver:
        driver = webdriver.Chrome(chrome_options=options, executable_path=args.chromedriver)
    else:
        driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(10)
    if login(driver, args.fb_user, args.fb_pass):
        fetch_new_requests(driver)
        logout(driver)
    driver.quit()


if __name__ == '__main__':
    main()
