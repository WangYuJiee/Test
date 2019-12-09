# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

from HTMLTestRunner import HTMLTestRunner
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage

import unittest
import datetime
import time, os, sys
import shutil
# from server3.business.user_business import UserBusiness
# from server3.business.project_business import ProjectBusiness
# from server3.entity.project import Project
# from server3.constants import WEB_ADDR
# from server3.email_template import email_template
import schedule

import logging
import io
# 多进程
from locust import HttpLocust, TaskSet, task

logger = logging.getLogger()
logger.level = logging.INFO

# rc 和  proc 互相检测
check_url_dict = {
    'https://momodel.cn': 'https://s.momodel.cn',
    'https://s.momodel.cn': 'https://momodel.cn'
}

# check_url = check_url_dict.get(WEB_ADDR, 'https://momodel.cn')

# check_url = 'https://s.momodel.cn'
check_url = 'https://momodel.cn'

# 0 不测试
# 1 本地测试
# 2 rc 或 prod 上测试
debugMode = 1


check_url_name_dict = {
    'https://momodel.cn': 'PROD',
    'https://s.momodel.cn': 'RC'
}


# check_url_name = check_url_name_dict.get(check_url)


class NotebookTest(unittest.TestCase):
    @task(1)
    def setUp(self):
        # 在服务器上跑改headless模式，测试使用可视化模式
        if debugMode == 1:
            # 可视化模式
            self.driver = webdriver.Chrome()
        else:
            # headless模式
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument("--disable-setuid-sandbox")
            self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True


    def test_notebook(self):
        driver = self.driver
        driver.get(check_url + "/user/login")
        logger.warning("窗口最大化")
        # 将浏览器最大化显示
        driver.maximize_window()
        # self.screen_shot()

        driver.find_element_by_id("username").clear()
        logger.warning("输入用户名")
        driver.find_element_by_id("username").send_keys("luxu99")
        # driver.find_element_by_id("username").send_keys("zhaofengli")
        # driver.find_element_by_id("username").send_keys("coder")
        driver.find_element_by_id("password").clear()
        logger.warning("输入密码")
        driver.find_element_by_id("password").send_keys("123456")
        driver.find_element_by_id("password").send_keys(Keys.RETURN)

        # driver.find_element_by_xpath(
        #     "(.//*[normalize-space(text()) and normalize-space(.)='Password'])[1]/following::button[1]").click()
        logger.warning("登录")
        logger.warning("点击新建 app 按钮")
        driver.find_element_by_id("Newapp").click()
        time.sleep(2)
        logger.warning("点击确认按钮")
        driver.find_element_by_css_selector(
            "body > div > div > div.ant-modal-wrap.create-new-project-modal > div > div.ant-modal-content > div.ant-modal-body > div > div > div >button.ant-btn-primary").click()

        # for _ in range(3):
        #     try:
        #         self.switch_tab(2)
        #         break
        #     except:
        #         pass
        #     logger.warning('等待 30 s 后重试')

        # windows = driver.current_window_handle  # 定位当前页面句柄
        #
        # all_handles = driver.window_handles  # 获取全部页面句柄
        # for handle in all_handles:  # 遍历全部页面句柄
        #     if handle != windows:  # 判断条件
        #      driver.switch_to.window(handle)
        for _ in range(5):
         js = "window.open('https://momodel.cn/workspace?tab=app')"
         driver.execute_script(js)
         for _ in range(3):
            try:
                self.switch_tab(2)
                break
            except:
                pass
            logger.warning('等待 30 s 后重试')
         driver.find_element_by_id("Newapp").click()
         time.sleep(1)
         logger.warning("点击确认按钮")
         driver.find_element_by_css_selector(
            "body > div > div > div.ant-modal-wrap.create-new-project-modal > div > div.ant-modal-content > div.ant-modal-body > div > div > div >button.ant-btn-primary").click()
         time.sleep(5)
        # driver.get(check_url + "/user/login")

        # try:
        #     element = driver.findElement(By.tagName("body"))
        #     element.sendKeys(Keys.CONTROL + "t")
        # except:
        #     print("fail")


        # time.sleep(20)
        # for _ in range(3):
        #     try:
        #         self.switch_tab(2)
        #         break
        #     except:
        #         pass
        #     logger.warning('等待 30 s 后重试')
        #     time.sleep(20)
        #
        # logger.warning('进入 notebook 页面')
        # for _ in range(3):
        #     try:
        #         if self.is_element_present(By.ID, "filebrowser"):
        #             break
        #         else:
        #             driver.refresh()
        #     except:
        #         pass
        #     time.sleep(30)
        #
        #     # 点击进入 launcher 页面
        #
        # try:
        #     logger.warning("点击关闭小提示")
        #     driver.find_element_by_css_selector(
        #         'body > div > div > div.ant-modal-wrap > div > div.ant-modal-content > button > span').click()
        #     time.sleep(3)
        # except:
        #     logger.warning("没有找到小提示，跳过")
        #     pass
        #
        # # 确认 notebook 已打开
        # logger.warning("找到 filebrowser 确保 notebook 成功打开")
        # driver.find_element_by_css_selector("#filebrowser")
        #
        # #
        # # 点击进入 launcher 页面
        # logger.warning("点击 launcher tab")
        # driver.find_element_by_css_selector(
        #     "#jp-main-dock-panel > div.p-Widget.p-TabBar.p-DockPanel-tabBar.jp-Activity > ul > li:nth-child(1)").click()
        #
        # logger.warning('点击新建 notebook')
        # time.sleep(3)
        # driver.find_element_by_css_selector(
        #     "* > div > div > div:nth-child(2) > div.jp-Launcher-cardContainer > div").click()
        #
        # logger.warning('点击新建 cell')
        # time.sleep(3)
        # driver.find_element_by_css_selector(
        #     "* > div > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div.CodeMirror-scroll > div.CodeMirror-sizer > div:nth-child(2) > div").click()
        # logger.warning("input code in the cell")
        #
        # time.sleep(3)
        # driver.find_element_by_css_selector(
        #     "* > div.p-Widget.jp-Cell.jp-CodeCell.jp-mod-noOutputs.jp-Notebook-cell.jp-mod-collapsed.jp-mod-active.jp-mod-selected > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div:nth-child(1) > textarea").send_keys(Keys.CONTROL + "v")
        #
        # logger.warning('运行 cell')
        # time.sleep(3)
        # driver.find_element_by_css_selector(
        #     "* > div.p-Widget.jp-Cell.jp-CodeCell.jp-mod-noOutputs.jp-Notebook-cell.jp-mod-collapsed.jp-mod-active.jp-mod-selected > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div:nth-child(1) > textarea").send_keys(
        #     Keys.SHIFT + Keys.ENTER)




    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to.alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True



    def switch_tab(self, num):
        driver = self.driver
        handles = driver.window_handles  # 获取当前窗口句柄集合（列表类型）
        driver.switch_to.window(handles[num - 1])  # 跳转到第num个窗口






if __name__ == "__main__":
      NotebookTest()