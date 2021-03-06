import logging
from argparse import ArgumentParser
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)


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
            logger.info('Nobody to accept.')
            return
        for link in links:
            person_name = str(link.contents[0])
            person_link = 'https://m.facebook.com/' + link.attrs['href']
            logger.info(person_name, person_link)
            client.find_elements_by_tag_name('button')[0].click()
            sleep(3)
            logger.info('User accepted.')
    except:
        logger.info('Nobody to accept.')
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
        logger.info('Logged in.')
        return True
    except NoSuchElementException:
        logger.exception('')
        logger.info('Fail to login.')
        return False


def logout(client):
    url = 'https://mbasic.facebook.com/logout.php?h=AffSEUYT5RsM6bkY&t=1446949608' \
          '&ref_component=mbasic_footer&ref_page=%2Fwap%2Fhome.php&refid=7'
    try:
        client.get(url)
        logger.info('Disconnected.')
        return True
    except Exception:
        logger.exception('')
        logger.info('Failed to log out.')
        return False


def init_logging():
    level = logging.INFO
    format_str = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(format_str)
    log_filename = '/tmp/facebook.log'
    logger.info(f'Logging to [{log_filename}].')
    logging.basicConfig(format=format_str,
                        filename=log_filename,
                        level=level)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def main():
    init_logging()
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
