from argparse import ArgumentParser
from time import sleep

from FacebookWebBot import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_script_arguments():
    args = ArgumentParser()
    args.add_argument('--fb_user', required=True)
    args.add_argument('--fb_pass', required=True)
    args.add_argument('--group_id', required=True)
    args.add_argument('--chromedriver')
    args.add_argument('--headless', action='store_true')
    return args.parse_args()


def accept_all_new_requests(client, group_id):
    url = 'https://m.facebook.com/groups/{}?view=members&ref=group_browse'.format(group_id)
    client.get(url)
    soup = BeautifulSoup(client.page_source, 'lxml')
    try:
        links = [h3 for h3 in soup.find_all('h3') if str(h3.contents[0]) == 'Requests'][0].parent.find_all('a')
        if len(links) == 0:
            print('Nobody to accept.')
            return
        for link in links:
            person_name = str(link.contents[0])
            person_link = 'https://m.facebook.com/' + link.attrs['href']
            print(person_name, person_link)
            client.find_elements_by_tag_name('button')[0].click()
            sleep(3)
            print('User accepted.')
    except:
        print('Nobody to accept.')
        return


def login(client, email, password):
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
    url = 'https://mbasic.facebook.com/logout.php?h=AffSEUYT5RsM6bkY&t=1446949608' \
          '&ref_component=mbasic_footer&ref_page=%2Fwap%2Fhome.php&refid=7'
    try:
        client.get(url)
        print('Disconnected.')
        return True
    except Exception:
        print('Failed to log out.')
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
        accept_all_new_requests(driver, args.group_id)
        logout(driver)
    driver.quit()


if __name__ == '__main__':
    main()
