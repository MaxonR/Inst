from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from auth_inst import username, password
import time
import random
import datetime
import csv


def hashtag_search(username, password, hashtag, steps):
    print(' ')
    print(f'----- {datetime.datetime.today()} -----')
    x = time.time()
    browser = webdriver.Chrome('/Users/maximyudin/Code/Skillbox/inst/driver/chromedriver')

    try:
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)

        time.sleep(5)

        try:
            browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
            time.sleep(5)
            posts_urls = []
            # steps = 40
            for i in range(1, steps+1):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(1, 2))

                hrefs = browser.find_elements_by_tag_name('a')

                for item in hrefs:
                    href = item.get_attribute('href')
                
                    if "/p/" in href:
                        posts_urls.append(href)
                print(f'{len(set(posts_urls))} постов после {i}/{steps} проходов', end='\r')
            
            posts_urls = set(posts_urls)
            print()
            print('Постов: ', len(posts_urls))
            time.sleep(1)
            plus_count = 0
            try:
                browser.get('https://www.instagram.com/lex_the_munchkin/')
                
                time.sleep(3)

                user_info = browser.find_elements_by_class_name('g47SY')
                
                user_info_list = []
                for value in user_info:
                    user_info_list.append(value.text)

                user_info_list.append(datetime.datetime.today())

                    
            except Exception as ex:
                print(ex)
                browser.close()
                browser.quit()

            counter = len(posts_urls)
            for url in posts_urls:
                try:
                    browser.get(url)
                    # counter = len(posts_urls)
                    time.sleep(random.randrange(2, 3))
                    counter -= 1
                    
                    like_button = browser.\
                        find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button')
                    
                    if like_button.get_attribute('aria-label') == 'Unlike':
                        pass
                    else:
                        like_button.click()
                    time.sleep(random.randrange(1, 2))
                    if counter == 0:
                        plus_count += 1
                        print(f'Поставлено лайков: {plus_count}/{len(posts_urls)}')
                        print('\nВсе лайки поставлены')
                    else:
                        plus_count += 1
                        print(f'Поставлено лайков: {plus_count}/{len(posts_urls)}', end="\r")
                except Exception as ex:
                    # user_info_list.append(plus_count)
                    print(ex)
            print()
            user_info_list.append(plus_count)
            print(f'Добавлено в базу: {plus_count}')
            user_info_list.append(hashtag)
            print(f'Добавлено в базу #: {hashtag}')
            with open('/Users/maximyudin/Code/Skillbox/inst/user_info.csv', 'a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(user_info_list)
            print()
            y = (time.time() - x)//60
            print(int(y), 'min')

            browser.close()
            browser.quit()

        except Exception as ex:
            print(ex)
            browser.close()
            browser.quit()

    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()

hashtag_search(username, password, 'catsofinstagram', 40)
