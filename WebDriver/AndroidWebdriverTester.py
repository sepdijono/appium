# Yusep Budijono Al Yoyon
# sepdijono@gmail.com

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import pyy_utils as pyy
import threading
from io import BytesIO
import cv2
import numpy as np
from PIL import Image
from time import sleep

class AWDSettings:

    def __init__(self, is_avd: bool):
        self.cap = []
        self.cap.append({
            "platformName": "android",
            "appium:udid": "192.168.100.61:42383",
            "appium:platformVersion": "13",
            "appium:deviceName": "GalTab7",
            "appium:automationName": "UIAutomator2",
            "appium:newCommandTimeout": 2500,
            "appium:ensureWebviewsHavePages": True,
            "appium:nativeWebScreenshot": True,
            "appium:connectHardwareKeyboard": True,
            "appium:unlockType": "pattern",
            "appium:unlockKey": "7415963",
            "appium:appPackage": "com.sec.android.app.camera",
            "appium:appActivity": "com.sec.android.app.camera.Camera"
        })
        self.cap.append({
            "platformName": "android",
            "appium:udid": "emulator-5554",
            "appium:platformVersion": "13",
            "appium:deviceName": "AVD",
            "appium:automationName": "UIAutomator2",
            "appium:newCommandTimeout": 2500,
            "appium:ensureWebviewsHavePages": True,
            "appium:nativeWebScreenshot": True,
            "appium:connectHardwareKeyboard": True,
            "appium:noReset": True,
            "appium:appPackage": "com.android.camera2",
            "appium:appActivity": "com.android.camera.CameraLauncher"
        })
        self.is_AVD = is_avd
        self.ss_folder = pyy.get_ss_path().strip()
        pyy.create_ss_dir()
        self.appium_server_url = "http://127.0.0.1:4752"
        if not is_avd:
            self.cap = self.cap[0]
        else:
            self.cap = self.cap[1]
        self.driver = webdriver.Remote(self.appium_server_url, self.cap)
        self.driver.implicitly_wait(10)

class AWDScreenshot:
    def __init__(self, driver):
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.take_screenshot)
        self.driver = driver

    def take_screenshot(self):
        while not self.stop_event.is_set():
            try:
                screenshot = self.driver.get_screenshot_as_png()

                image = Image.open(BytesIO(screenshot))

                open_cv_image = np.array(image)

                open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)

                cv2.imshow("Screenshot", open_cv_image)
                cv2.waitKey(2)
            except Exception as e:
                print(f"Error taking screenshot: {e}")

    def start(self):
        if not self.thread.is_alive():
            self.thread=threading.Thread(target=self.take_screenshot)
            self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()
        cv2.destroyAllWindows()

class AWDAndroidTester:
    def __init__(self, is_avd):
        self.MC2 = AWDSettings(is_avd)
        self.SS = AWDScreenshot(self.MC2.driver)

    def fbe_id(self, element_id):
        return self.MC2.driver.find_element(by=AppiumBy.ID, value=element_id)

    def ui_scroller(self, visible_text):
        return self.MC2.driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                        value="new UiScrollable(new UiSelector().scrollable(true).instance("
                                              "0)).scrollIntoView(new "
                                              "UiSelector().textContains(\"" + visible_text + "\").instance(0))")

    def tc_cam_check(self):
        try:
            el1 = WebDriverWait(self.MC2.driver, 20).until(
                ec.presence_of_element_located((MobileBy.ID, "com.sec.android.app.camera:id/btn_turn_on"))
            )
            el1.click()
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            return f"Terjadi kesalahan: {e}"

    # 1055, 305, 1055, 34
    def tc_swipe_up(self, x, y, x1, y1):
        try:
            self.MC2.driver.execute_script('mobile: pressKey', {"keycode": 187})
            actions = ActionChains(self.MC2.driver)
            actions.w3c_actions = ActionBuilder(self.MC2.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(x, y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(x1, y1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            return f"Terjadi kesalahan: {e}"

    def tc_back_cam(self):
        try:
            el5 = self.MC2.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Kamera")
            el5.click()
            el6 = self.MC2.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Beralih ke kamera belakang")
            el6.click()
            el7 = self.MC2.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Ambil gambar")
            el7.click()
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            return f"Terjadi kesalahan: {e}"


    def tc_front_cam(self):
        try:
            el2 = self.MC2.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Beralih ke kamera depan")
            el2.click()
            el3 = self.MC2.driver.find_element(by=AppiumBy.ID, value="com.sec.android.app.camera:id/color_tone_tips_bright")
            el3.click()
            el4 = self.MC2.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Ambil gambar")
            el4.click()
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            return f"Terjadi kesalahan: {e}"

    def tc_kill_app(self):
        try:
            self.MC2.driver.execute_script('mobile: pressKey', {"keycode": 187})

            # Temukan aplikasi yang ingin dihentikan di daftar aplikasi latar belakang
            target_app = self.MC2.driver.find_element(AppiumBy.XPATH,
                                             '//android.widget.FrameLayout[@content-desc="Kamera"]')
            # Dapatkan lokasi dan ukuran elemen aplikasi
            location = target_app.location
            size = target_app.size

            # Hitung koordinat tengah elemen untuk swipe
            start_x = location['x'] + size['width'] / 2
            start_y = location['y'] + size['height'] / 2
            end_x = start_x  # Koordinat X tidak berubah untuk swipe vertikal
            end_y = start_y - 800  # Menggeser elemen ke atas untuk menutup aplikasi

            # Lakukan swipe untuk menutup aplikasi
            self.MC2.driver.swipe(start_x, start_y, end_x, end_y, 500)  # durasi swipe

            print("Aplikasi berhasil dihentikan dari latar belakang.")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            self.MC2.driver.execute_script('mobile: pressKey', {"keycode": 3})

    def tc_runAll(self):
        self.SS.start()
        self.tc_cam_check()
        self.tc_front_cam()
        self.tc_kill_app()
        self.tc_back_cam()
        self.tc_kill_app()
        self.MC2.driver.lock()
        self.SS.stop()

if __name__ == "__main__":
    a = AWDAndroidTester(False)
    a.tc_runAll()
