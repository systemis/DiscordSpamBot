import platform
import os.path
import time
import threading
import pyperclip
from selenium import webdriver
from data.data import ignore_role_names, check_conclude_key, check_key
from username_config import usernames, emails, passwords, message_customs, break_time, break_time_after_login, user_per_round
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def start(
    email, 
    password, 
    username, 
    chrome_driver_path, 
    break_time, 
    message_custom
): 
    print('chrome driver path: ', chrome_driver_path)
    print('time break: ', break_time)

    driver = webdriver.Chrome(os.path.dirname(__file__) + chrome_driver_path)
    driver.get("https://www.discord.com/login")

    def login(): 
        email_field = driver.find_element_by_css_selector('input[name=email]')
        password_field = driver.find_element_by_css_selector('input[name=password]')
        submit_button = driver.find_element_by_css_selector('button[type=submit]')

        email_field.send_keys(email)
        password_field.send_keys(password)
        submit_button.click()

        print("clicked button login ", submit_button)
        time.sleep(break_time_after_login)

    login() 

    # user_selector_name = "member-3-YXUe"
    
    content_selector_name = "content-3YMskv"
    chat_group_selector_name = "members-1998pB"
    username_selector_name = "headerTagUsernameNoNickname-2-Y5Ct"
    enter_done_selector_name = "enterDone-2zvtsK"
    enter_done_close_button_selector_name = "closeButton-1tv5uR"
    bot_tag_selector_name = "headerBotTag-qNEsTk"
    user_context_message_user = "user-context-message-user"
    chat_channel_url = "https://discord.com/channels/@me"

    current_url = driver.current_url.split('/') 
    channel_id = current_url[len(current_url) - 2] + "/" + current_url[len(current_url) - 1]
    
    run = True
    user_sent_list = []
    total_scroll_height = 1000

    def getUserList():
        try: 
            return driver.find_elements_by_class_name("member-3-YXUe")
        except Exception: 
            # driver.execute_script("window.history.go(-1)")
            # return driver.find_elements_by_class_name("member-3-YXUe")
            print('error when ')
            return []

    def scroll(times=1, total_scroll_height=1000): 
        try: 
            els = driver.find_elements_by_class_name(chat_group_selector_name)
            if len(els) <= 0: 
                print('error not found empty')
                print(driver.current_url)
                
                if driver.current_url.find('https://discord.com/channels/@me') >= 0: 
                    driver.execute_script("window.history.go(-1)")
                    return scroll(times=times, total_scroll_height=total_scroll_height)
                # run = False 
                # return None 
                # raise IndexError
            chat_room_container = els[0]
            scroll_height = float(total_scroll_height) #float(chat_room_container.size['height']) * times
            scroll_script = "arguments[0].scrollTop +=" + str(scroll_height)
            driver.execute_script(scroll_script, chat_room_container) 
            return True
        except IndexError:
            driver.execute_script("window.history.go(-1)")
            scroll(times=times)
            return None

    def check_exist_enter_done(): 
        try: 
            frame = driver.find_elements_by_class_name(enter_done_selector_name);
            closeButton = driver.find_elements_by_class_name(enter_done_close_button_selector_name)
            if len(frame) <= 0 or len(closeButton) <= 0: 
                return None

            print('Close button:', closeButton)
            return True
        except NoSuchElementException: 
            return None
    
    def resolve_exists_enter_done(): 
        if check_exist_enter_done() is not None: 
            try: 
                driver.find_elements_by_class_name(enter_done_close_button_selector_name)[0].click();
            except Exception: 
                pass

    def direct_windown(actions): 
        if pyperclip.paste() != message_custom: 
            print('copy message to clipboard')
            pyperclip.copy(message_custom)
        actions.key_down(Keys.CONTROL).send_keys('v')
        actions.key_up(Keys.CONTROL)
        actions.key_down(Keys.ENTER)
        actions.perform() 

    def direct_mac(actions): 
        if pyperclip.paste() != message_custom: 
            print('copy message to clipboard')
            pyperclip.copy(message_custom)
        actions.key_down(Keys.META)
        actions.send_keys('v')
        actions.key_up(Keys.META)
        actions.key_down(Keys.ENTER)
        actions.perform() 

    def direct_message(user, user_sent, total_scroll_height=0):
        user.click()
        time.sleep(1)
        def check_bot(): 
            try: 
                bot_span =  driver.find_elements_by_class_name(bot_tag_selector_name)
                if len(bot_span): 
                    return True
                return False 
            except NoSuchElementException: 
                print("not bot")
                return False 
        
        def check_role_name(): 
            try:
                role_name_container_list = driver.find_elements_by_class_name("roleName-32vpEy")
                if len(role_name_container_list) <= 0: 
                    return False 
                for i in range(len(role_name_container_list)): 
                    role_name = role_name_container_list[i].text; 
                    if check_conclude_key(role_name=role_name): 
                        return True
                    if check_key(role_name=role_name): 
                        return True
                    for ingore_role_name in ignore_role_names: 
                        if role_name.lower() == ingore_role_name: 
                            True
                return False 
            except NoSuchElementException: 
                print("Empty role name")
                return False 
        
        def check_username(): 
            username_label = driver.find_elements_by_class_name(username_selector_name)
            if len(username_label) <= 0: return False 
            _username = username_label[0].text.lower()
            if username.find(_username) >= 0:
                print("Ignore self account !!")
                return True
            for user in user_sent_list: 
                if _username in user: 
                    return True
            user_sent_list.append(_username)
            return False 
        
        if check_bot(): 
            print('having bot')
            time.sleep(0.4)
            return False
        
        if check_role_name(): 
            print('having role name')
            time.sleep(0.4)
            return False

        if check_username():
            time.sleep(0.4)
            print("ingore sent account !!")
            return False
        
        try: 
            action = ActionChains(driver=driver)
            action.context_click(user).perform()
            userContextButton = driver.find_element_by_id(user_context_message_user)
            userContextButton.click()

            def input(): 
                text_input = driver.find_element_by_css_selector("input[type=text]")
                # text_input.send_keys(message_custom) 
                text_input.send_keys("Hi!")
                if text_input is not None: 
                    if text_input.submit is not None: 
                        # Send enter key to input in order to submit text
                        text_input.send_keys(Keys.ENTER)

            time.sleep(1)

            resolve_exists_enter_done()
            actions = ActionChains(driver)
            
            # direct_mac(actions)
            direct_windown(actions)
            
            resolve_exists_enter_done()
            time.sleep(1)
            driver.execute_script("window.history.go(-1)")
            print('back')
            time.sleep(2)
            
            scroll(times=1, total_scroll_height=total_scroll_height);
            
            user_sent += 1
            return True
        except NoSuchElementException: 
            return None

    def spam(
        driver, 
        user_container, 
        scrollable=-1, 
        scrollable_times=0, 
        user_sent=0, 
        user_index=0, 
        times_group=0,
        total_scroll_height=0): 
        try: 
            if scrollable_times > 0: 
                times_group = scrollable_times
                scroll(times=scrollable_times, total_scroll_height=total_scroll_height)
                user_container = getUserList()
                user_index = int(len(user_container)/2)

            while run: 
                # getChat()
                user_container = getUserList()
                if times_group == 0 and user_index >= 10: 
                    scroll(times=1, total_scroll_height=total_scroll_height); 
                    user_container = getUserList()
                    times_group += 1;   
                    user_index = int(len(user_container)/2)
                    total_scroll_height += 1000

                if times_group > 0 and user_index >= int(len(user_container)/2) + 8: 
                    scroll(times=1, total_scroll_height=total_scroll_height);
                    user_container = getUserList()
                    times_group += 1
                    user_index = int(len(user_container)/2)
                    total_scroll_height += 1000

                if user_sent > 0 and user_sent % user_per_round == 0: 
                    print("Waiting for next round...")
                    print(user_sent)
                    time.sleep(break_time)
                    user_container = getUserList()
                    times_group += 1;   
                    total_scroll_height += 1000
                    user_index = int(len(user_container)/2)
                    user_sent += 1 
                    scroll(times=1, total_scroll_height=total_scroll_height); 
                    print("after round", user_sent)

                # Send message to target account  
                try: 
                    if(len(user_container) <= 0): 
                        print('error empty user container')
                        break; 
                    else: 
                        user = user_container[user_index]
                    direct_result = direct_message(
                        user=user, 
                        user_sent=user_sent, 
                        total_scroll_height=total_scroll_height);

                    # Catch error if none input => scroll the page
                    if direct_result == None: 
                        scroll(times=1)
                        times_group += 1
                        user_container = getUserList()
                    elif direct_result == True: 
                        user_sent += 1
                except Exception:
                    print(len(user_container), user_index)
                    pass;


                print("User Sent", user_sent)
                time.sleep(0.4) # Sleep secs to chat continue 
                user_index += 1 
        except IndexError: 
            print("Error: Out of index")
            print(driver.current_url)
            if chat_channel_url in driver.current_url: 
                driver.execute_script("window.history.go(-1)")
                time.sleep(1)
                if times_group > 0: 
                    scroll(times=times_group, total_scroll_height=total_scroll_height)
                spam(
                    driver=driver, 
                    user_container=user_container, 
                    scrollable=1, 
                    user_index=user_index, 
                    times_group=times_group, 
                    user_sent=user_sent, 
                    total_scroll_height=total_scroll_height)
                return 
            pass
        except Exception as error: 
            if check_exist_enter_done() is not None: 
                try: 
                    driver.find_elements_by_class_name(enter_done_close_button_selector_name)[0].click();
                    print('Closing frame button') 
                except Exception: 
                    pass
                # spam(
                #     driver=driver, 
                #     user_container=user_container, 
                #     scrollable=1, 
                #     user_index=user_index, 
                #     times_group=times_group, 
                #     user_sent=user_sent)
                return; 
                # Closing
            print("error when spam bot: ", error)
            pass; 

    print('Channel id: ', channel_id)
    spam(
        driver=driver, 
        scrollable_times=25, 
        user_container=getUserList(), 
        user_index=10,
        total_scroll_height=total_scroll_height)
    time.sleep(180)
    # scroll();


if __name__ == "__main__": 
    N = len(emails)   # Length of user
    thread_list = list()
    chrome_driver_path = ""

    if platform.system() == 'Darwin': 
        chrome_driver_path = "/resources/webdrivers/chromdriver-mac"
    elif platform.system() == 'Windows': 
        chrome_driver_path = "/resources/webdrivers/msedgedriver.exe"
    elif platform.system() == 'Linux':
        chrome_driver_path = "/resources/webdrivers/chromdriver-win32"

    print(chrome_driver_path)
    # Start test
    for i in range(N):
        def thread_method(): 
            return start(
                email=emails[i], 
                password=passwords[i], 
                username=usernames[i], 
                message_custom=message_customs[0], 
                chrome_driver_path=chrome_driver_path, 
                break_time=break_time, 
            )
        
        t = threading.Thread(name='Task with account {}'.format(i), target=thread_method)
        t.start()
        time.sleep(1)
        print(t.name + ' started!')
        thread_list.append(t)
    
    for thread in thread_list: 
        thread.join()
    print("Bot completed")