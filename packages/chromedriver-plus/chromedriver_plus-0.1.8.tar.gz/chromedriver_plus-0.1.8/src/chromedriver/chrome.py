from selenium.webdriver.support.ui import WebDriverWait
from http.cookies import SimpleCookie

import seleniumwire.undetected_chromedriver.v2 as uc
import time
import ctypes
import winreg

class PasswordManager:
    HKEY = winreg.HKEY_LOCAL_MACHINE
    PATH = r'SOFTWARE\Policies\Google\Chrome'
    VALUE = 'PasswordManagerEnabled'
    TYPE = winreg.REG_DWORD

    def __init__(self, save=True):
        self.save = save

    def __call__(self):
        with winreg.CreateKeyEx(self.HKEY, self.PATH) as k:
            winreg.SetValueEx(k, self.VALUE, 0, self.TYPE,
                                1 if self.save else 0)

class WindowSort:
    def __init__(self, chrome_width, chrome_height):
        self.chrome_width = chrome_width
        self.chrome_height = chrome_height
        self.user32 = ctypes.windll.user32

        self.user32.SetProcessDPIAware()

    def __call__(self, drivers):
        x, y = 1, 1
        window_width = self.user32.GetSystemMetrics(0)

        for driver in drivers:
            driver.set_window_rect(x, y, self.chrome_width, self.chrome_height)
            time.sleep(.5)

            x += self.chrome_width
            window_width -= x
            
            if not window_width < self.chrome_width: continue

            x = 1
            y += self.chrome_height
            window_width = self.user32.GetSystemMetrics(0)

class ChromePlus(uc.Chrome):
    TIMEOUT = 30
    SCRIPT_TIMEOUT = 9999
    PAGE_LOAD_TIMEOUT = 60

    def __init__(self, options=None, user_agent=None, profile_data=None, **kwargs):
        if not options: options = uc.ChromeOptions()
        
        options.add_argument('--disable-notifications')

        if user_agent or profile_data:
            if user_agent: options.add_argument(f'--user-agent={user_agent}')
                
            if len(profile_data):
                user_dir = profile_data[0]
                options.user_data_dir = user_dir
                options.add_argument(f'--user-data-dir={user_dir}')

                if len(profile_data) > 1: options.add_argument(f'--profile-directory={profile_data[1]}')

        super().__init__(options=options, keep_alive=True, **kwargs)
        
        self.set_script_timeout(self.SCRIPT_TIMEOUT)
        self.set_page_load_timeout(self.PAGE_LOAD_TIMEOUT)

    def send_keys(self, element, value, interval=.08):
        for char in value:
            element.send_keys(char)
            time.sleep(interval)
    
    def get_user_agent(self):
        return self.execute_script('return navigator.userAgent')

    def execute_elements(self, *args):
        def execute(ec, command, **kwargs):
            callback = command['callback']

            result = WebDriverWait(self, self.TIMEOUT).until(ec)
            index = -1

            if 'index' in command: index = command['index']
            if 'index' in kwargs: index = kwargs['index']

            result = result[index] if index != -1 else result

            if 'value' in command:
                callback(result, command['value'])
                return
            
            callback(result)

        for command in args:
            ec = command['ec']
            execute(ec, command)
            
            if 'next' in command:
                for item in command['next']:
                    execute(ec, item,
                    	index=command['index'] if 'index' in command else -1)
                    time.sleep(1)

            time.sleep(1.5)

    def get_cookie_str(self):
        cookies = self.get_cookies()
        result = ''

        for cookie in cookies:
            result += f'{cookie["name"]}={cookie["value"]};'

        return result

    def add_cookie_str(self, value):
        cookie = SimpleCookie()
        cookie.load(value)

        for key, morsel in cookie.items():
            self.add_cookie({
                'name': key,
                'value': morsel.value
            })
                
        time.sleep(.5)
        self.refresh()