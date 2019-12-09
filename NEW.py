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
    # 'http://192.168.31.11:8899': 'https://momodel.cn'
}

# check_url = check_url_dict.get(WEB_ADDR, 'https://momodel.cn')

# check_url = 'http://192.168.31.11:8899'
check_url = 'https://momodel.cn'

# 0 不测试
# 1 本地测试
# 2 rc 或 prod 上测试
debugMode = 1



check_url_name_dict = {
    'https://momodel.cn': 'PROD',
    # 'http://192.168.31.11:8899': 'RC'
}


# check_url_name = check_url_name_dict.get(check_url)


class NotebookTest(unittest.TestCase, TaskSet):
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

    def screen_shot(self):
        driver = self.driver
        picture_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        directory_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        path = '.\\picture'
        # 若目录不存在，创建新目录
        try:
            file_path = path + '\\' + directory_time + '\\'
            if not os.path.exists(file_path):
                os.makedirs(file_path)
                print('新建目录！')
            else:
                pass
        except BaseException as msg:
            print("新建目录失败：%s" % msg)

        # 使用save_screenshot来截图
        try:
            url = driver.save_screenshot(path + '\\' + directory_time + '\\' + picture_time + '.png')
            print("%s ：截图成功！！！" % url)
        except BaseException as pic_msg:
            print("截图失败：%s" % pic_msg)

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
        time.sleep(5)

        # 上去之前改
        # 打开制造错误，测试发邮件
        # driver.find_element_by_xpath("(sakdfkashdf").click()

        logger.warning("点击新建 app 按钮")
        driver.find_element_by_id("Newapp").click()
        time.sleep(3)
        logger.warning("点击确认按钮")
        driver.find_element_by_id("confirmInCreateModal").click()


        # logger.warning("点击从 script 新建 app")
        # driver.find_element_by_css_selector(
        #     "body > div > div > div.ant-modal-wrap > div > div.ant-modal-content > div.ant-modal-body > div > div").click()

        # # 进入第一个项目
        # logger.warning("鼠标悬浮第一个项目")
        # element_to_hover_over = driver.find_element_by_css_selector("#workspace > div > div > div.ant-tabs-content.ant-tabs-content-no-animated.ant-tabs-top-content > div.ant-tabs-tabpane.ant-tabs-tabpane-active > div > div.ant-spin-nested-loading > div > div > a > div")
        #
        # hover = ActionChains(driver).move_to_element(element_to_hover_over)
        # hover.perform()
        #
        # logger.warning("点击进入第一个项目")
        # driver.find_element_by_id("first-project").click()

        logger.warning("切换到 tab 2")
        time.sleep(15)

        for _ in range(3):
            try:
                self.switch_tab(2)
                break
            except:
                pass
            logger.warning('等待 30 s 后重试')
            time.sleep(15)

        logger.warning('进入 notebook 页面')
        for _ in range(3):
            try:
                if self.is_element_present(By.ID, "filebrowser"):
                    break
                else:
                    driver.refresh()
            except:
                pass
            time.sleep(30)

            # 点击进入 launcher 页面

        try:
            logger.warning("点击关闭小提示")
            driver.find_element_by_css_selector(
                'body > div > div > div.ant-modal-wrap > div > div.ant-modal-content > button > span').click()
            time.sleep(3)
        except:
            logger.warning("没有找到小提示，跳过")
            pass

        # 确认 notebook 已打开
        logger.warning("找到 filebrowser 确保 notebook 成功打开")
        driver.find_element_by_css_selector("#filebrowser")

        #
        # 点击进入 launcher 页面
        logger.warning("点击 launcher tab")
        driver.find_element_by_css_selector(
            "#jp-main-dock-panel > div.p-Widget.p-TabBar.p-DockPanel-tabBar.jp-Activity > ul > li:nth-child(1)").click()

        logger.warning('点击新建 notebook')
        time.sleep(3)
        driver.find_element_by_css_selector(
            "* > div > div > div:nth-child(2) > div.jp-Launcher-cardContainer > div").click()

        logger.warning('点击新建 cell')
        time.sleep(3)
        driver.find_element_by_css_selector(
            "* > div > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div.CodeMirror-scroll > div.CodeMirror-sizer > div:nth-child(2) > div").click()
        logger.warning("input code in the cell")

        time.sleep(3)
        #复制代码
        driver.find_element_by_css_selector(
            "* > div.p-Widget.jp-Cell.jp-CodeCell.jp-mod-noOutputs.jp-Notebook-cell.jp-mod-collapsed.jp-mod-active.jp-mod-selected > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div:nth-child(1) > textarea").send_keys(Keys.CONTROL + "v")

        # #hello
        driver.find_element_by_css_selector(
            "* > div.p-Widget.jp-Cell.jp-CodeCell.jp-mod-noOutputs.jp-Notebook-cell.jp-mod-collapsed.jp-mod-active.jp-mod-selected > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div:nth-child(1) > textarea").send_keys(
            "print('helloworld')"
            )
        # time.sleep(3)
        #
        # logger.warning('运行 cell')
        # time.sleep(3)
        # driver.find_element_by_css_selector(
        #     "* > div.p-Widget.jp-Cell.jp-CodeCell.jp-mod-noOutputs.jp-Notebook-cell.jp-mod-collapsed.jp-mod-active.jp-mod-selected > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div:nth-child(1) > textarea").send_keys(
        #     Keys.SHIFT + Keys.ENTER)

        time.sleep(200000)

        # # 输入循环代码
        # logger.warning('点击新建 cell')
        # time.sleep(3)
        # driver.find_element_by_css_selector(
        #     "* > div:nth-child(3) > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div.CodeMirror-scroll > div.CodeMirror-sizer > div:nth-child(2) > div > div > div.CodeMirror-code > pre").click()
        # logger.warning("input for-loop in the cell")
        # time.sleep(3)
        #
        # data = 'sum1=0\nfor i in range(100):\nsum1 += i\n\bprint(sum1)'
        # driver.find_element_by_css_selector(
        #     "* > div.p-Widget.jp-Cell.jp-CodeCell.jp-mod-noOutputs.jp-Notebook-cell.jp-mod-collapsed.jp-mod-active.jp-mod-selected > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div:nth-child(1) > textarea").send_keys(
        #     data)
        # logger.warning('运行 cell')
        # time.sleep(3)
        # driver.find_element_by_css_selector(
        #     "* > div.p-Widget.jp-Cell.jp-CodeCell.jp-mod-noOutputs.jp-Notebook-cell.jp-mod-collapsed.jp-mod-active.jp-mod-selected > div.p-Widget.p-Panel.jp-Cell-inputWrapper > div.p-Widget.jp-InputArea.jp-Cell-inputArea > div.p-Widget.jp-CodeMirrorEditor.jp-Editor.jp-InputArea-editor > div > div:nth-child(1) > textarea").send_keys(
        #     Keys.SHIFT + Keys.ENTER)
        # assert driver.find_element_by_css_selector(
        #     "* > div:nth-child(3) > div.p-Widget.p-Panel.jp-Cell-outputWrapper > div.p-Widget.jp-OutputArea.jp-Cell-outputArea > div > div.p-Widget.jp-RenderedText.jp-mod-trusted.jp-OutputArea-output > pre").text == '4850'

        driver.close()

        # logger.warning('click go back to the detail page')
        # driver.find_element_by_xpath(
        #     "//div[@id='mo-jlContainer']/div/span/span/span[2]/span").click()
        #
        # logger.warning('switch to tab3')
        # time.sleep(10)
        # self.switch_tab(3)
        #
        # for i in range(3):
        #     try:
        #         print('i',
        #               self.is_element_present(By.CLASS_NAME, "main-container"))
        #         if self.is_element_present(By.CLASS_NAME, "main-container"):
        #             break
        #     except:
        #         pass
        #     time.sleep(1)
        # else:
        #     self.fail("time out")
        #
        # time.sleep(5)
        # logger.warning("click delete button")
        # # driver.execute_script('document.querySelector("#LaunchPage_Contain > div > div > div > div > div > div >  div > div > span[title=\"Delete project\"]").click()')
        # driver.find_element_by_css_selector("#LaunchPage_Contain > div > div > div > div > div > div >  div > div > span[title='Delete project']").click()
        #
        # time.sleep(3)
        # logger.warning("click confirm button")
        #
        # try:
        #     # driver.execute_script('document.querySelector("body > div > div > div.ant-modal-wrap > div > div.ant-modal-content > div > div > div > button.ant-btn.ant-btn-primary").click()')
        #     driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div/div[2]/div/div/div[2]/button[2]").click()
        # except:
        #     driver.find_element_by_css_selector(
        #         "body > div > div > div.ant-modal-wrap > div > div.ant-modal-content > div > div > div > button.ant-btn.ant-btn-primary").click()
        #
        # time.sleep(3)
        # driver.close()

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

    def tearDown(self):
        self.screen_shot()
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def switch_tab(self, num):
        driver = self.driver
        handles = driver.window_handles  # 获取当前窗口句柄集合（列表类型）
        driver.switch_to.window(handles[num - 1])  # 跳转到第num个窗口


# def send_email(log_contents):
#     # 通知开发者
#     if check_url == 'https://momodel.cn' and not debugMode:
#         # emails = ['491730572@qq.com', '949502498@qq.com',
#         #           'chengsi1992@126.com',
#         #           'rainbowgirlanita@gmail.com', 'lzfxxx@gmail.com',
#         #           'jx.li@momodel.ai', 'bingjielei@163.com']
#         emails = ['ming197@qq.com','13035111987@163.com']
#         subject = 'PROD 项目创建异常，请检查网站'
#     else:
#         emails = ['lzfxxx@gmail.com', '491730572@qq.com']
#         subject = 'RC 项目创建异常，请检查网站'

#     text = email_template(
#         title="<div><h3 style='margin-left: 12px; line-height: 1.1;"
#               "color: #000; font-size: 27px;'>{0} 项目创建错误"
#               "<a href= '{1}/workspace' target='_blank' "
#               "style='color: #1980FF !important;"
#               "text-decoration:underline;margin-left: "
#               "24px;font-size: 24px;'>进入网站查看</a></h3></div>".format(
#             check_url_name, check_url),
#         middle="<div style='margin-left: 24px; margin-top: -24px; "
#                "list-style-position: inside;'>"
#                "<div>日志如下:</div>"
#                "<div style='white-space: pre-wrap;'>{0}</div>"
#                "<div>".format(log_contents))

#     # 发送邮件
#     for email in emails:
#         UserBusiness.send_email(email, subject, text)

# def send_email():
#     # 邮件发送
#     sender = 'a498593970@163.com'
#     sendpswd = 'qweasdzxc123'
#     receivers = ['498593970@qq.com']
#
#     msg = MIMEMultipart()
#
#     # 附件
#
#     # html测试报告
#     report_dir = 'C:\\Users\\12546\Desktop\\selenium\\htmlReport\\' + time.strftime("%Y-%m-%d",
#                                                                                     time.localtime(time.time()))
#     # 获取路径下的文件
#     lists = os.listdir(report_dir)
#     new_report = os.path.join(report_dir, lists[-1])
#     htmlApart = MIMEApplication(open(new_report, 'rb').read())
#     htmlApart.add_header('Content-Disposition', 'attachment', filename=(
#     'utf-8', '', time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time())) + "_report.html"))
#     msg.attach(htmlApart)
#     shutil.rmtree(report_dir)
#     print('htmlReport本地文件删除成功！')
#
#     # 错误截图
#     image_dir = 'C:\\Users\\12546\Desktop\\selenium\\picture\\' + time.strftime("%Y-%m-%d", time.localtime(time.time()))
#     pictures = os.listdir(image_dir)
#     imageFile = os.path.join(image_dir, pictures[-1])
#     imageApart = MIMEImage(open(imageFile, 'rb').read(), imageFile.split('.')[-1])
#     imageApart.add_header('Content-Disposition', 'attachment', filename=(
#     'utf-8', '', time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time())) + '_screen_shot.png'))
#     msg.attach(imageApart)
#     shutil.rmtree(image_dir)
#     print('screen本地文件删除成功！')
#
#     # log日志文件
#     logFile_dir = 'C:\\Users\\12546\Desktop\\selenium\\logFile\\' + time.strftime("%Y-%m-%d",
#                                                                                   time.localtime(time.time()))
#     logs = os.listdir(logFile_dir)
#     logFile = os.path.join(logFile_dir, logs[-1])
#     with open(logFile, 'r', encoding='utf-8') as f:
#         body_main = f.read()
#     logApart = MIMEApplication(open(logFile, 'rb').read())
#     logApart.add_header('Content-Disposition', 'attachment', filename=(
#     'utf-8', '', time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time())) + '_logFile.txt'))
#     msg.attach(logApart)
#     shutil.rmtree(logFile_dir)
#     print('logFile本地文件删除成功！')
#
#     # 邮件内容
#     text = MIMEText(u'日志文件：\n' + body_main)
#     msg.attach(text)
#
#     # 邮箱登录
#     smtp = smtplib.SMTP()
#     smtp.connect('smtp.163.com')
#     smtp.login(sender, sendpswd)
#
#     # 邮件标题
#     msg['Subject'] = Header('自动化测试报告', 'utf-8')
#     msg['From'] = sender
#
#     # 邮件发送
#     for receiver in receivers:
#         msg['To'] = receiver
#         smtp.sendmail(sender, receiver, msg.as_string())


def run_all_test():
    # 只在 prod 和 rc 上开启测试
    # if WEB_ADDR not in ['https://momodel.cn', 'https://s.momodel.cn']:
    #     return
    # 最多尝试 3 次，
    all_test_times = 1
    log_capture_string = io.StringIO()
    stream_handler = logging.StreamHandler(log_capture_string)
    logger.addHandler(stream_handler)
    for i in range(all_test_times):
        logger.warning(
            '------------------第 {i} 次测试------------------')
        logger.warning(
            '------  时间: {0} ------'.format(
                datetime.datetime.now()))

        # 生成html报告
        htmlReport_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        directory_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        path = '.\\htmlReport'
        # 若目录不存在，创建新目录
        try:
            file_path = path + '\\' + directory_time + '\\'
            if not os.path.exists(file_path):
                os.makedirs(file_path)
                print('新建目录！')
            else:
                pass
        except BaseException as msg:
            print("新建目录失败：%s" % msg)

        filename = path + '\\' + directory_time + '\\' + htmlReport_time + '_result.html'
        fp = open(filename, 'wb')
        suite = unittest.TestLoader().loadTestsFromTestCase(NotebookTest)
        test_result = HTMLTestRunner(stream=fp, title=u'测试报告', description=u'用例执行情况：').run(suite)
        fp.close()
        print("%s ：html报告生成成功！！！" % filename)

        # 生成log文件
        log_contents = log_capture_string.getvalue()
        # print(log_contents)

        log_time = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        directory_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        path = '.\\logFile'
        # 若目录不存在，创建新目录
        try:
            file_path = path + '\\' + directory_time + '\\'
            if not os.path.exists(file_path):
                os.makedirs(file_path)
                print('新建目录！')
            else:
                pass
        except BaseException as msg:
            print("新建目录失败：%s" % msg)

        filename = path + '\\' + directory_time + '\\' + log_time + '_logFile_' + str(i) + '.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(log_contents)

        # 如果报错，记录错误，并等待 300 秒后重试一次或发送错误邮件
        # if test_result.errors:
        #     # test, errors = test_result.errors[0]
        #     # all_errors.append(errors)
        #
        #     # 如果是最后一次，发送错误邮件通知
        #     if i == all_test_times - 1:
        #         send_email()
        #     # 否则，五分钟后再次尝试
        #     else:
        #         time.sleep(300)
        # else:
        #     break
    log_capture_string.close()
    logger.removeHandler(stream_handler)
    # user = UserBusiness.get_by_username('luxu99')
    # projects = Project.objects(user=user, type='app')
    # for key, e in enumerate(projects):
    #     if 'luxu' in e.display_name:
    #         ProjectBusiness.remove_project_by_id(str(e.id), user.user_ID)
    #         time.sleep(2)


class RunAll(TaskSet):
    @task(1)
    def runAll(self):
        run_all_test()


class websitUser(HttpLocust):
    task_set = RunAll
    min_wait = 0  # 单位毫秒
    max_wait = 0  # 单位毫秒
    host = "随便写"


if __name__ == "__main__":
    if debugMode:
        r = websitUser()
        r.run()
    else:
        schedule.every().hour.do(websitUser.run())
        while True:
            schedule.run_pending()
            time.sleep(1)

