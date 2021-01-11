from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# use sleep
from time import sleep
from datetime import datetime, timezone, timedelta
# By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
# actionchain
from selenium.webdriver.common.action_chains import ActionChains
# Options
from selenium.webdriver.chrome.options import Options
from log_to_file import log_to_file
from ocr import ocr_to_text

chrome_options = Options()
chrome_options.add_argument('--disable-notifications')
driver = webdriver.Chrome(options=chrome_options)
#URL_UDN_POLL = "https://udn.com/news/story/121440/4665552" 
URL_UDN_POLL = "https://udn.com/func/vote/?act_code=v845"
LOG_FILE_NAME = "udnbot_"+URL_UDN_POLL[-4:]+'.log'
BASE_URL = "https://udn.com" 
timeout = 10

def save_captcha_image(captcha_element):
    captcha_image_element_location = captcha_image_element.location 
    height_captcha_image_elemen = captcha_image_element.size['height'] 
    width_captcha_image_element = captcha_image_element.size['width']
    # save captcha image
    screenshot_captcha_image = captcha_image_element.screenshot_as_png
    return screenshot_captcha_image 

def image_to_text(screenshot_captcha_image):
    # image to text
    from io import BytesIO
    from PIL import Image
    im = Image.open(BytesIO(screenshot_captcha_image)) 
    filename_captcha_image = 'screenshot_captcha.png'
    im.save(filename_captcha_image) 
    from pathlib import Path
    path_captcha_image = Path(__file__).resolve().with_name(filename_captcha_image)
    #path_captcha_image = os.path.join(os.path.getcwd(), filename_captcha_image)
    print(path_captcha_image) 
    # convert captcha image to text
    ocr_text = ocr_to_text(filename_captcha_image)
    print(f'ocr text :{ocr_text}') 
    return ocr_text



# Navigator to url
driver.get(URL_UDN_POLL)

# scroll 3 pg down to reveal poll section
# if we go headless might not need this scroll down
body = driver.find_element_by_tag_name('body')
#body.send_keys(Keys.PAGE_DOWN)

'''
# test to show drop down menu of "全球"
XPATH_GLOBAL_NEWS = "//a[contains(text(), '全球')]"
global_news_element = driver.find_element_by_xpath(XPATH_GLOBAL_NEWS) 
XPATH_GLOBAL_NEWS_DROP_DOWN = '//a[@title = "國際焦點"]' 
#XPATH_GLOBAL_NEWS_DROP_DOWN = '/html/body/section[1]/div/div[1]/section[1]/header/a' 
if global_news_element != None:
    action = ActionChains(driver)
    action.move_to_element(global_news_element).perform()
    element_presence = ec.presence_of_element_located((By.XPATH, XPATH_GLOBAL_NEWS_DROP_DOWN ))
    global_news_drop_down_element = WebDriverWait(driver, timeout).until(element_presence)
    #global_news_drop_down_element = driver.find_element_by_xpath(XPATH_GLOBAL_NEWS_DROP_DOWN) 
    action.move_to_element(global_news_drop_down_element).perform()
    global_news_drop_down_element.click()
    print('clicked')

sleep(300)
driver.exit()
'''

'''
this xpath is not consistant thorough b4 and after the poll is over
XPATH_DAY_HOURS_B4_DEADLINE = '//*[@id="udnVote"]/span/div/div[2]/div[1]/span[1]'
'''
XPATH_DAY_HOURS_B4_DEADLINE = '//span[contains(text(),"剩餘時間：")]'
# wait til the element is ready
element_presence = ec.presence_of_element_located((By.XPATH, XPATH_DAY_HOURS_B4_DEADLINE))
day_hour_left_element = WebDriverWait(driver, timeout).until(element_presence)
#day_hour_left_element = driver.find_element_by_xpath(XPATH_DAY_HOURS_B4_DEADLINE)
print(day_hour_left_element.get_attribute('innerHTML')) 
text = day_hour_left_element.text 
'''
print(f'text: {text}')
'''
day_hour_left = text
assert '剩餘時間' in day_hour_left 

# check if poll is over 
text_list = day_hour_left.split("：") 
vote_status = 'fail'
str_local_datetime = datetime.now(timezone.utc).astimezone().strftime('%Y%m%dT%H%M%S') 
if '已結束' in text_list[1].strip():
    # the poll is over
    print('poll is expired')
    # write a log
    log_to_file(LOG_FILE_NAME,' '.join(str_local_datetime, 'poll expired' ))

    driver.quit()
else:
    # poll still alive, we vote
    print('poll still alive')
    # TODO: add voting script



    # remove cookies b4 we refresh poll page
    '''
    print(f"all cookies: {driver.get_cookies()}")
    udn_cookies = []
    for cookie in driver.get_cookies():
        print(cookie)
        if "udn" in cookie['domain']:
            udn_cookies.append(cookie)

    for udn_cookie in udn_cookies:
        print(f"udn : {udn_cookie}")
        assert 'udn' in udn_cookie['domain']
    '''

    # locate poll options
    # if poll options is selectable
    # select the option whose text contains "贊同，制止民進黨的酬庸行為該用較強硬的方式表達。"
    '''
    driver.find_element_by_id("select-0").click()
    driver.find_element_by_css_selector("input[type='radio'][id='select-0']").click()
    XPATH_OPTION_LABEL_WE_WANT = '//*[@id="udnVote"]/span/div/div[1]/div/div[1]/label' 
    XPATH_LABEL_CONTAINS_KEYWORD = '//label[contains(text(), "贊同，制止民進黨的酬庸行為該用較強硬的方式表達。")]'
    XPATH_INPUT_KEYWORD = '//label[contains(text(), "贊同，制止民進黨的酬庸行為該用較強硬的方式表達。")]/preceding-sibling::input'
    XPATH_OPTION_DIV_WE_WANT = '//*[@id="udnVote"]/span/div/div[1]/div/div[1]' 

    XPATH_OPTION_INPUT_WE_WANT  = '//*[@id="udnVote"]/span/div/div[1]/div/div[1]/input'
    option_input_element = driver.find_element_by_xpath(XPATH_OPTION_INPUT_WE_WANT) 
    option_div_element = driver.find_element_by_xpath(XPATH_OPTION_DIV_WE_WANT) 
    print(option_input_element.get_attribute('outerHTML')) 
    print(driver.find_element_by_id("select-0").is_displayed())
    print(f'option_element: {option_element.is_displayed()}')
    print(option_input_element.is_displayed())
    print(f'enable?:{driver.find_element_by_id("select-0").is_enabled()}')
    print(f'enable?:{option_input_element.is_enabled()}')
    these doesn't work
    error says that the element cannot be interactable
    but if we click on parent div of label and input then it works
    '''

    #print(option_element.text)
    # assert the option whose text contains "贊同，制止民進黨的酬庸行為該用較強硬的方式表達。" is selected
    XPATH_LABEL_CONTAINS_KEYWORD = '//label[contains(text(), "不贊成，考、監兩院有其存在的必要性")]'
    option_label_element = driver.find_element_by_xpath(XPATH_LABEL_CONTAINS_KEYWORD) 
    assert option_label_element.text == "不贊成，考、監兩院有其存在的必要性" 
    # get label's parent div element
    option_div_element = option_label_element.find_element_by_xpath('..')
    print(option_div_element.get_attribute('class')) 
    #option_div_element.location_once_scrolled_into_view
    '''
    action = ActionChains(driver)
    action.move_to_element(option_div_element).perform()
    '''
    #print(label_ancestor_element.get_attribute('outerHTML')) 
    # test if this matched label is selectable?
    # print id attribute of input element whose label sibiling matches our target string

    print('click')
    #option_input_element.click() 
    '''
    element_clickable = ec.element_to_be_clickable((By.XPATH,XPATH_OPTION_DIV_WE_WANT ))
    option_div_element= WebDriverWait(driver, timeout).until(element_clickable)
    #ActionChains(driver).move_to_element_with_offset(option_input_element, 5 , 5).click().perform()
    '''
    option_div_element.click()
    #driver.execute_script("document.getElementById('select-0').scrollIntoView();")
    '''
    body.send_keys(Keys.UP)
    body.send_keys(Keys.UP)
    body.send_keys(Keys.UP)
    driver.find_element_by_id("select-0").click()
    '''

    # select captcha image
    '''
    XPATH_CAPTCHA_IMAGE = '//*[@id="udnVote"]/span/div/div[2]/div[2]/img'
    print('click on captcha')
    captcha_image_element = driver.find_element_by_xpath(XPATH_CAPTCHA_IMAGE)
    ActionChains(driver).move_to_element_with_offset(captcha_image_element, 5 , 5).click().perform()
    '''
    XPATH_LABEL_CAPTCHA_IMAGE = '//label[contains(text(), "驗證碼")]'
    XPATH_CAPTCHA_IMAGE = '//label[contains(text(), "驗證碼")]/following-sibling::img'
    label_captcha_image_element = driver.find_element_by_xpath(XPATH_LABEL_CAPTCHA_IMAGE) 
    #captcha_image_element = driver.find_element_by_xpath(XPATH_CAPTCHA_IMAGE) 
    captcha_image_element = label_captcha_image_element.find_element_by_xpath('.//following-sibling::img') 
    assert '/funcap/keyimg?random' in captcha_image_element.get_attribute('src').strip() 
    while True: 
        # save captcha image
        screenshot_captcha_image = save_captcha_image(captcha_image_element)

        # image to text
        ocr_text =  image_to_text(screenshot_captcha_image)

        # select captcha input box
        XPATH_CAPTCHA_INPUT_BOX = '//*[@id="code"]'
        captcha_input_box_element = driver.find_element_by_xpath(XPATH_CAPTCHA_INPUT_BOX )
        assert captcha_input_box_element.get_attribute('id') == 'code' 
        # input text to captcha input box
        captcha_input_box_element.send_keys(ocr_text)
        #captcha_input_box_element.send_keys('1234')

        # verify captcha input box contains the same text as ocr_text
        #assert ocr_text == captcha_input_box_element.get_attribute('value')

        # assert the captcha input box's text matches the text
        # select captcha submit button
        #XPATH_CAPTCHA_SUBMIT_BUTTON = '//*[@id="udnVote"]/span/div/div[2]/div[3]/button'
        XPATH_CAPTCHA_SUBMIT_BUTTON = '//button[contains(text(), "投票看結果")]'
        captcha_submit_button_element = driver.find_element_by_xpath(XPATH_CAPTCHA_SUBMIT_BUTTON ) 
        assert captcha_submit_button_element.text.strip() == '投票看結果' 
        # click the captcha submit button
        captcha_submit_button_element.click() 
        # verify if we succeed submit
        # check submission succeed element exists
        XPATH_VOTE_RESULT_BOX_TITLE = '/html/body/section[3]/div/h2'
        XPATH_VOTE_RESULT_BOX_TEXT = '/html/body/section[3]/div/div[1]' 

        # wait til the title element is ready
        element_presence = ec.presence_of_element_located((By.XPATH, XPATH_VOTE_RESULT_BOX_TITLE))
        vote_result_title_element = WebDriverWait(driver, timeout).until(element_presence)
        element_presence = ec.presence_of_element_located((By.XPATH, XPATH_VOTE_RESULT_BOX_TEXT))
        vote_result_text_element =  WebDriverWait(driver, timeout).until(element_presence)
        #PATH_SUCCESS_CONFIRM_BUTTON = '/html/body/section[3]/div/div[2]/button'
         
        #vote_success_title_element_contains_keyword = driver.find_element_by_xpath('//h2[contains(text(), "投票成功")]')
        '''
        assert len(vote_success_title_elements) == 1
        assert len(vote_success_title_elements_contains_keyword) == 1
        '''
    # if we click on submit vote button, we can always see the XPATH_SUCCESS_TITLE  XPATH_SUCCESS_TEXT  XPATH_SUCCESS_CONFIRM_BUTTON 
        if vote_result_title_element:
            print('submission button clicked')
            vote_result_title = vote_result_title_element.text
            if vote_result_title  == "投票成功" and vote_result_text_element.text == "投票成功":
                print('vote succeeded')
                # dismiss result box
                vote_box_botton = vote_result_title_element.find_element_by_xpath('.//following-sibling::div[2]/button[contains(text(), "確認")]')
                assert vote_box_botton.text == "確認"
                #vote_box_botton.click()
                # write a log
                log_to_file(LOG_FILE_NAME,' '.join([str_local_datetime, 'vote succeed'] ))
                break

                #need to sleep to 3mins
                #sleep(180)

                # this doesn't seems to be necessory for selenium: our submission is succeed, we delete all cookies from udn then goto sleep for 3mins then try to vote again

            #vote failed
            elif vote_result_title == "投票失敗":
                print("vote failed")
                
                #incorrect captcha
                if vote_result_text_element.text == "您輸入檢核碼錯誤!!": 
                    print("captcha incorrect")
                    # dismiss result box
                    vote_box_botton = vote_result_title_element.find_element_by_xpath('.//following-sibling::div[2]/button[contains(text(), "確認")]')
                    print("confirm button clicked")
                    assert vote_box_botton.text == "確認"
                    vote_box_botton.click()

                    # get a new captcha image by clicking on captcha image
                    captcha_image_element.click() 

                    # save captcha image
                    screenshot_captcha_image = save_captcha_image(captcha_image_element)
                    # image to text
                    ocr_text =  image_to_text(screenshot_captcha_image)

                    # clear text of captcha input box
                    captcha_input_box_element.clear()

                    # input text to captcha input box
                    captcha_input_box_element.send_keys(ocr_text)
                    
                    # verify captcha input box contains the same text as ocr_text
                    assert ocr_text == captcha_input_box_element.get_attribute('value')
                    # click the captcha submit button
                    captcha_submit_button_element.click() 

                    # write a log
                    log_to_file(LOG_FILE_NAME,' '.join([str_local_datetime, 'vote fail, captcha incorrect'] ))

                # server block timeout not expired 3mins
                elif vote_result_text_element.text == "請依正常操作程序!!":
                    # need to wait for 3mins
                    print("請依正常操作程序!!")
                    # dismiss result box
                    vote_box_botton = vote_result_title_element.find_element_by_xpath('.//following-sibling::div[2]/button[contains(text(), "確認")]')
                    assert vote_box_botton.text == "確認"
                    vote_box_botton.click()
                    # clear text of captcha input box
                    captcha_input_box_element.clear()
                    # write a log
                    log_to_file(LOG_FILE_NAME,' '.join([str_local_datetime, 'vote failed, wait 3mins b4 cast another vote'] ))
                    break
                    #need to sleep to 3mins
                    #sleep(180)

            elif vote_result_title == "驗證碼格式錯誤!!":
                if vote_result_text_element.text == "請輸入正確驗證碼":
                    # dismiss result box
                    vote_box_botton = vote_result_title_element.find_element_by_xpath('.//following-sibling::div[2]/button[contains(text(), "確認")]')
                    assert vote_box_botton.text == "確認"
                    vote_box_botton.click()
                    # click on the captcha image to get a new  image
                    captcha_image_element.click()

                    # save captcha image to png
                    screenshot_captcha_image = save_captcha_image(captcha_image_element)
                    # image to text
                    ocr_text =  image_to_text(screenshot_captcha_image)

                    # clear text of captcha input box
                    captcha_input_box_element.clear()

                    # input text to captcha input box
                    captcha_input_box_element.send_keys(ocr_text)

                    # verify captcha input box contains the same text as ocr_text
                    assert ocr_text == captcha_input_box_element.get_attribute('value')
                    # click the captcha submit button
                    captcha_submit_button_element.click() 
                    # write a log
                    log_to_file(LOG_FILE_NAME,' '.join([str_local_datetime, 'vote failed, captcha text are all digits but got non-digits'] ))

            elif vote_result_title == "驗證碼未輸入":
                if vote_result_text_element.text == "請輸入驗證碼":
                    print('ocr text is empty') 
                    # dismiss result box
                    vote_box_botton = vote_result_title_element.find_element_by_xpath('.//following-sibling::div[2]/button[contains(text(), "確認")]')
                    assert vote_box_botton.text == "確認"
                    vote_box_botton.click()
                    # save captcha image to png
                    screenshot_captcha_image = save_captcha_image(captcha_image_element)
                    # image to text
                    ocr_text =  image_to_text(screenshot_captcha_image)

                    # clear text of captcha input box
                    captcha_input_box_element.clear()

                    # input text to captcha input box
                    captcha_input_box_element.send_keys(ocr_text)
                    
                    # verify captcha input box contains the same text as ocr_text
                    assert ocr_text == captcha_input_box_element.get_attribute('value')
                    # click the captcha submit button
                    captcha_submit_button_element.click() 
                    # write a log
                    log_to_file(LOG_FILE_NAME,' '.join([str_local_datetime, 'vote failed, captcha text was empty'] ))

     

sleep(300)
driver.quit()
# if poll option is selectable, after we submit poll but we got this title '投票失敗' text '請依正常操作程序!!' button 
XPATH_VOTE_FAIL_TITLE = '/html/body/section[3]/div/h2'
XPATH_VOTE_FAIL_TEXT = '/html/body/section[3]/div/div[1]'
XPATH_VOTE_FAIL_BUTTON = '/html/body/section[3]/div/div[2]/button'
# we need to delete all udn cookies, sleep for 3mins, then visit URL to try again


# if poll option is selectable, after we submit poll but we got this title '選項未選擇', text '選項未選擇' button 
XPATH_POLL_OPTION_NOT_PICKED_TITLE = '/html/body/section[3]/div/h2' 
XPATH_POLL_OPTION_NOT_PICKED_TEXT = '/html/body/section[3]/div/div[1]'
XPATH_POLL_OPTION_NOT_PICKED_BUTTON =  '/html/body/section[3]/div/div[2]'
# we need to select poll option


# if poll option is selectable, after we submit poll but we got this title '驗證碼未輸入', text '請輸入驗證碼' button 
XPATH_CAPTCHA_INPUT_BOX_EMPTY_TITLE = '/html/body/section[3]/div/h2' 
XPATH_CAPTCHA_INPUT_BOX_EMPTY_TEXT = '/html/body/section[3]/div/div[1]'
XPATH_CAPTCHA_INPUT_BOX_EMPTY_BUTTON =  '/html/body/section[3]/div/div[2]'
# we need to input captcha text 





# if poll option is not selectable, delete all udn cookies, then refresh current url

# if webpage idle for more than 1 min, a little frame will pop up and block the webpage, refresh webpage b4 you want to access the original webpage
