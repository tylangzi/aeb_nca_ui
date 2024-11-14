"""
获取driver,并访问百度
"""
import time

import pyautogui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver.driver import driver, Driver
import pandas as pd
from pynput import keyboard
from pynput.keyboard import Controller, Key

def switch_new_window():
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])
def get_driver():
    return Driver().get_driver()
def open_url(driver):
    driver.get("https://drplatform.deeproute.cn/#/diagnosis-management/issue/tag?path=%2Fissue%2Ftag")
    switch_new_window()




def switch_iframe():
    while True:
        try:
            driver.switch_to.frame('opsIframe')
            break
        except Exception as e:
            print(e)
            print("iframe找不到")
            time.sleep(1)


def query_tripname(tripname):
    # 输入tripname
    input_loc = (By.XPATH, "//*/span[contains(text(),'行程名称:')]/../..//input")
    input_ele = WebDriverWait(driver,10,1).until(EC.visibility_of_element_located(input_loc))
    input_ele.send_keys(Keys.COMMAND, 'a')
    input_ele.send_keys(Keys.BACKSPACE)
    input_ele.send_keys(tripname)

    # 点击查询
    time.sleep(1)
    query_loc = (By.XPATH, "//*/span[contains(text(),'查询')]/..")
    query_ele = driver.find_element(*query_loc)
    query_ele.click()

    time.sleep(3)
    # 点击离线诊断，显示等待
    query_loc = (By.XPATH, "//*/span[contains(text(),'离线诊断')]/..")
    while True:
        try:
            query_ele = driver.find_element(*query_loc)
            query_ele.click()
            break
        except Exception as e:
            print(e)
            print('数据未搜索到')
            time.sleep(1)
def click_tag_list():
    tag_list_loc = (By.XPATH, "//*/span[contains(text(),'所属trip的tag列表')]/..")
    while True:
        try:
            tag_list_ele = driver.find_element(*tag_list_loc)
            tag_list_ele.click()
            break
        except Exception as e:
            print(e)
            print("所属trip的tag列表找不到")
            time.sleep(1)
def filter_taglist():
    click_tag_list()
    # type 框
    type_loc = (By.XPATH, "//*/span[contains(text(),'tag类型')]/..//span[contains(text(),'event_trigger')]")
    # type_ele = driver.find_element(*type_loc)
    type_ele = WebDriverWait(driver,100,1).until(EC.visibility_of_element_located(type_loc))
    action = ActionChains(driver)
    # action.move_to_element(type_ele).perform()
    action.click(type_ele).perform()
    # action.scroll_to_element(type_ele).perform()

    time.sleep(1)

    #//*/div[@class='v-vl-visible-items']
    # 差掉 event_trigger
    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele =  WebDriverWait(driver,100,1).until(EC.visibility_of_element_located(item_loc))
    type_loc = (By.XPATH, './div[1]')
    type_ele = item_ele.find_element(*type_loc)
    # 循环遍历下一个兄弟节点
    while True:
        try:
            if type_ele.text in ["event_trigger", "tag"]:
                # 滑动到目标位置了再点击
                action = ActionChains(driver)
                action.scroll_to_element(type_ele).perform()
                type_ele.click()
                # action.click(type_ele).perform()
                # driver.execute_script("arguments[0].click();", type_ele)


                print(f'{type_ele.text}被点击了')
                time.sleep(1)
            print(f'{type_ele.text}没有被点击')
            next_loc = (By.XPATH, "following-sibling::div[1]")
            type_ele = type_ele.find_element(*next_loc)

        except Exception as e:
            print(e)
            print("兄弟节点已经没有了")
            break
    # time.sleep(1000)

def paging():
    # 点击分页按钮

    page_loc = (By.XPATH, "//*/div[contains(text(),'页')]")
    page_ele = WebDriverWait(driver,100,1).until(EC.visibility_of_element_located(page_loc))
    action = ActionChains(driver)
    action.scroll_to_element(page_ele).perform()
    # action.click(page_ele).perform()
    # 使用JavaScript执行点击操作
    driver.execute_script("arguments[0].click();", page_ele)
    # time.sleep(1)





    # 点击100页面
    page_100_loc = (By.XPATH, "//*/div[contains(text(),'100 / 页')]")
    page_100_ele = WebDriverWait(driver,100,1).until(EC.visibility_of_element_located(page_100_loc))
    action = ActionChains(driver)
    action.scroll_to_element(page_100_ele).perform()
    action.click(page_100_ele).perform()


    # 划到最底部
    for i in range(3):
        try:
            action = ActionChains(driver)
            action.scroll_to_element(page_100_ele).perform()
            action.scroll_to_element(page_100_ele).perform()
        except Exception as e:
            print("滑动到最底部失败，尝试重新滑动")


    time.sleep(4)





def diagnosis_list(id=2):
    # 定义循环结束的标识
    flag = False

    # 获取页面的数量
    count_num = get_num_of_page()
    for n in range(count_num):
        # 如果找到了就结束循环
        if flag == True:
            break
        # 点击某一页
        n_count = n + 1
        if n != 0:
            click_one_page(n_count)
            time.sleep(5)

        # 开始进行后面的操作
        tbody_loc = (By.XPATH, "//*/tbody[@class='n-data-table-tbody']")
        tbody_ele = WebDriverWait(driver,200,1).until(EC.visibility_of_element_located(tbody_loc))
        tr_loc = (By.XPATH, "./tr[1]")
        tr_ele = tbody_ele.find_element(*tr_loc)

        # event_id
        event_id_loc = (By.XPATH, "./td[@data-col-key='eventId']")
        event_id_ele = tr_ele.find_element(*event_id_loc)
        print("到这里了")
        try:
            while True:
                action = ActionChains(driver)
                action.scroll_to_element(event_id_ele).perform()
                print(event_id_ele.text)
                if int(id) == int(event_id_ele.text):
                    print(f"id找到了{event_id_ele.text}")

                    # 开始诊断
                    diagnosis_loc = (By.XPATH, "./td[@data-col-key='action']/button")
                    diagnosis_ele = tr_ele.find_element(*diagnosis_loc)
                    diagnosis_ele.click()
                    flag = True
                    break
                # 没有找到，开始找下一个
                next_loc = (By.XPATH, "following-sibling::tr[1]")
                tr_ele = tr_ele.find_element(*next_loc)
                event_id_loc = (By.XPATH, "./td[@data-col-key='eventId']")
                event_id_ele = tr_ele.find_element(*event_id_loc)


        except Exception as e:
            print(e)
            print("找不到这个ID，可能是数据诊断结束或者数据丢失")



def input_desc(text="【[NCA]第一轮城区泛化测试-7.8】城区，多车道直行路段，自车向左变道过程中，点刹，影响体感"):
    # 将页面滑动可以诊断信息，为了让页面可见
    diagnosis_info_loc = (By.XPATH, "//*/div[contains(text(),'诊断信息')]")
    diagnosis_info_ele = driver.find_element(*diagnosis_info_loc)
    driver.execute_script('arguments[0].scrollIntoView();', diagnosis_info_ele)

    # 把内容清空
    input_dest_loc = (By.XPATH, "//*/span[contains(text(),'描述')]/../..//*/textarea")
    input_dest_ele = WebDriverWait(driver,200,1).until(EC.visibility_of_element_located(input_dest_loc))
    time.sleep(1)
    for i in range(10):
        input_dest_ele.send_keys(Keys.COMMAND, 'a')
        time.sleep(0.1)
        input_dest_ele.send_keys(Keys.BACKSPACE)
        time.sleep(0.1)
    # time.sleep(2)
    # 开始输入内容
    input_dest_ele.send_keys(text)
    time.sleep(2)
def create_work_item():
    time.sleep(3)
    create_loc = (By.XPATH,"//*/span[contains(text(),'创建飞书工作项')]/..")
    create_ele = driver.find_element(*create_loc)
    while True:
        try:
            status_loc = (By.XPATH,"//*/span[contains(text(),'创建飞书工作项')]/preceding-sibling::span[1]")
            driver.find_element(*status_loc)
            print("还在加载中，请等待。。。")
            time.sleep(1)
        except Exception as e:
            print("加载成功")
            break

    create_ele.click()


def input_operator(input_content='pinyihu'):

    operator_loc = (By.XPATH, "//*/span[contains(text(),'经办人')]/../..//*/input")
    operator_ele = WebDriverWait(driver,200,1).until(EC.visibility_of_element_located(operator_loc))
    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(operator_ele).perform()
    operator_ele.send_keys(input_content)

    item_loc = (By.XPATH,"//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]
    content_loc = (By.XPATH, ".//div")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:
            print(content_ele.text)
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")
                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text,f"可见的<div>元素数量: {len(item_ele_list)}")

def business(input_content="GWM"):


    business_loc = (By.XPATH, "//*/span[contains(text(),'业务线')]/../..//*/input")
    business_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(business_loc))
    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(business_ele).perform()

    business_ele.send_keys(input_content)

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]

    content_loc = (By.XPATH, ".//div")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:

            print(content_ele.text)
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")

                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text, f"可见的<div>元素数量: {len(item_ele_list)}")
def priority(input_content="P0"):


    priority_loc = (By.XPATH, "//*/span[contains(text(),'优先级')]/../..//*/input")
    priority_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(priority_loc))
    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(priority_ele).perform()

    priority_ele.send_keys(input_content)

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]

    content_loc = (By.XPATH, ".//div")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:

            print(content_ele.text)
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")

                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text, f"可见的<div>元素数量: {len(item_ele_list)}")
def module(input_content="prediction"):


    module_loc = (By.XPATH, "//*/span[contains(text(),'问题所属模块')]/../following-sibling::div[1]//div")
    module_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(module_loc))
    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(module_ele).perform()

    module_ele.click()

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]

    content_loc = (By.XPATH, ".//div")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:
            print(content_ele.text)
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")

                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div[1]")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text, f"可见的<div>元素数量: {len(item_ele_list)}")

def what_time(input_content="白天"):


    what_time_loc = (By.XPATH, "//*/span[contains(text(),'时间')]/../..//*/input[@placeholder != '请从prophet拷贝对应时间戳']")
    what_time_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(what_time_loc))
    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(what_time_ele).perform()

    what_time_ele.send_keys(input_content)

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]

    content_loc = (By.XPATH, ".//div")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:

            print(content_ele.text)
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")

                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div[1]")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text, f"可见的<div>元素数量: {len(item_ele_list)}")

def area(input_content="城区"):

    area_loc = (By.XPATH, "//*/span[contains(text(),'区域')]/../..//*/input")
    area_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(area_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(area_ele).perform()

    area_ele.send_keys(input_content)

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]

    content_loc = (By.XPATH, ".//div")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:

            print(content_ele.text)
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")
                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div[1]")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text, f"可见的<div>元素数量: {len(item_ele_list)}")

def whether(input_content="晴天"):


    whether_loc = (By.XPATH, "//*/span[contains(text(),'天气')]/../..//*/input")
    whether_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(whether_loc))
    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(whether_ele).perform()

    whether_ele.send_keys(input_content)

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]

    content_loc = (By.XPATH, ".//div")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:

            print(content_ele.text)
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")
                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div[1]")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text, f"可见的<div>元素数量: {len(item_ele_list)}")


def child_function(input_contents="纵向功能 / 融合限速 / 隧道限速"):

    fun_loc = (By.XPATH, "//*/span[contains(text(),'子功能')]/../..//div")
    fun_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(fun_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(fun_ele).perform()

    fun_ele.click()

    for input_content in [input_content for input_content in input_contents.split(' / ')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]

        content_loc = (By.XPATH, ".//span")
        content_ele = item_ele.find_element(*content_loc)
        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                action = ActionChains(driver)
                action.scroll_to_element(content_ele).perform()
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    action.click(content_ele).perform()
                    break
                else:
                    content_loc = (By.XPATH, "./../following-sibling::div[1]/span")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")


def road_type(input_contents="道路用途 / 汇入汇出 / 匝道内选道 / 宽车道一分二选车道"):

    road_type_loc = (By.XPATH, "//*/span[contains(text(),'道路类型')]/../..//div")
    road_type_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(road_type_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(road_type_ele).perform()

    road_type_ele.click()

    for input_content in [input_content for input_content in input_contents.split('/')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]

        content_loc = (By.XPATH, ".//span")
        content_ele = item_ele.find_element(*content_loc)
        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                action = ActionChains(driver)
                action.scroll_to_element(content_ele).perform()
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    action.click(content_ele).perform()
                    break
                else:
                    content_loc = (By.XPATH, "./../following-sibling::div[1]/span")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")

def obstacle(input_contents="障碍物类型 / 小障碍物 / 锥桶 / 倒地锥桶"):

    obstacle_loc = (By.XPATH, "//*/span[contains(text(),'障碍物交互')]/../..//div")
    obstacle_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(obstacle_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(obstacle_ele).perform()

    obstacle_ele.click()

    for input_content in [input_content for input_content in input_contents.split(' / ')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]

        content_loc = (By.XPATH, ".//span")
        content_ele = item_ele.find_element(*content_loc)
        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                action = ActionChains(driver)
                action.scroll_to_element(content_ele).perform()
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    action.click(content_ele).perform()
                    break
                else:
                    content_loc = (By.XPATH, "./../following-sibling::div[1]/span")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")

def task_type(input_contents="专项测试 / 场景验证"):

    task_type_loc = (By.XPATH, "//*/span[contains(text(),'任务类型')]/../..//div")
    task_type_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(task_type_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(task_type_ele).perform()

    task_type_ele.click()

    for input_content in [input_content for input_content in input_contents.split(' / ')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]

        content_loc = (By.XPATH, ".//span")
        content_ele = item_ele.find_element(*content_loc)
        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                action = ActionChains(driver)
                action.scroll_to_element(content_ele).perform()
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    action.click(content_ele).perform()
                    break
                else:
                    content_loc = (By.XPATH, "./../following-sibling::div[1]/span")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")

def secondary(input_contents="VRU / VRU横穿点刹\急刹\过度礼让"):

    secondary_loc = (By.XPATH, "//*/span[contains(text(),'问题类别（二级）')]/../..//div")
    secondary_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(secondary_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(secondary_ele).perform()

    secondary_ele.click()

    for input_content in [input_content for input_content in input_contents.split(' / ')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]

        content_loc = (By.XPATH, ".//span")
        content_ele = item_ele.find_element(*content_loc)
        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                action = ActionChains(driver)
                action.scroll_to_element(content_ele).perform()
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    action.click(content_ele).perform()
                    break
                else:
                    content_loc = (By.XPATH, "./../following-sibling::div[1]/span")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")


def issue_type(input_contents="程序功能相关 / 策略合理性 / 车辆长时间靠右车道行驶"):

    issue_type_loc = (By.XPATH, "//*/span[text()='问题类别']/../..//div[@class='n-cascader']")
    issue_type_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(issue_type_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(issue_type_ele).perform()

    issue_type_ele.click()

    for input_content in [input_content for input_content in input_contents.split(' / ')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]

        content_loc = (By.XPATH, ".//span")
        content_ele = item_ele.find_element(*content_loc)
        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                action = ActionChains(driver)
                action.scroll_to_element(content_ele).perform()
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    action.click(content_ele).perform()
                    break
                else:
                    content_loc = (By.XPATH, "./../following-sibling::div[1]/span")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")


def takeover(input_contents="是 / 被动接管 / 功能性"):
    takeover_loc = (By.XPATH, "//*/span[text()='是否接管']/../..//div")
    takeover_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(takeover_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(takeover_ele).perform()

    takeover_ele.click()

    for input_content in [input_content for input_content in input_contents.split(' / ')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]
        content_loc = (By.XPATH, ".//span")
        content_ele = item_ele.find_element(*content_loc)
        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                action = ActionChains(driver)
                action.scroll_to_element(content_ele).perform()
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    action.click(content_ele).perform()
                    break
                else:
                    content_loc = (By.XPATH, "./../following-sibling::div[1]/span")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")
def issue_atribute(input_contents="合规"):

    if input_contents == "安全":
        issue_atribute_loc = (By.XPATH, "//*/div[text()='安全']")
    elif input_contents == "合规":
        issue_atribute_loc = (By.XPATH, "//*/div[text()='合规']")
    elif input_contents == "舒适":
        issue_atribute_loc = (By.XPATH, "//*/div[text()='舒适']")
    elif input_contents == "智能":
        issue_atribute_loc = (By.XPATH, "//*/div[text()='智能']")
    elif input_contents == "非问题":
        issue_atribute_loc = (By.XPATH, "//*/div[text()='非问题']")
    else:
        print("请输入正确的问题属性")

    issue_atribute_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(issue_atribute_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(issue_atribute_ele).perform()

    action.click(issue_atribute_ele).perform()

def related_plan(input_content="0725封板冒烟测试"):
    related_plan_loc = (By.XPATH, "//*/span[text()='关联计划']/../../div")
    related_plan_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(related_plan_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(related_plan_ele).perform()

    related_plan_ele.click()

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]
    content_loc = (By.XPATH, "./div/div[@class='n-base-select-option__content']")
    content_ele = item_ele.find_element(*content_loc)
    while True:
        try:
            print(f"content_ele.text的值为：{content_ele.text.strip()}")
            print(f"input_content的值为：{input_content.strip()}")
            action = ActionChains(driver)
            action.scroll_to_element(content_ele).perform()
            if input_content.strip() == content_ele.text.strip():
                print(f"{content_ele.text}为输入的值")
                action.click(content_ele).perform()
                break
            else:
                content_loc = (By.XPATH, "./../following-sibling::div[1]/div")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")

def submit():
    submit_loc = (By.XPATH, "//*/span[text()='提交飞书工作项']/..")
    submit_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(submit_loc))

    # 移动到该元素
    action = ActionChains(driver)
    action.scroll_to_element(submit_ele).perform()
    # 提交
    submit_ele.click()

    while True:
        try:
            submit_loc = (By.XPATH, "//*/span[text()='提交飞书工作项']/..")
            submit_ele = driver.find_element(*submit_loc)
            print("问题提交中")
            time.sleep(1)
        except Exception as e:
            print(e)
            print("提交成功")
            break


def read_excell():
    # 指定Excel文件路径
    file_path = '/Users/tianyalangzi/Downloads/行车-指标统计-0721.xlsx'
    # 读取Excel文件
    data_frame = pd.read_excel(file_path)
    # 打印读取的数据
    for index,row in data_frame.iterrows():
        content = read_index()
        print(f"index的值为{content}")
        if int(index) == int(content):
            desc_item = f"【{row['关联计划']}】{row['描述']}"
            trip_name_item = row['Trip']
            tag_id_item = row['Tag_id']
            operator_item = row['经办人 ']
            priority_item = row['优先级']
            business_item = row['业务线']
            what_time_item = row['时间']
            module_item = row['问题所属模块']
            area_item = row['区域']
            whether_item = row['天气']
            child_func_item = row['子功能']
            road_type_item = row['道路类型']
            obstacle_item = row['障碍物交互']
            task_type_item = row['任务类型']
            secondary_item = row['问题类别（二级）']
            issue_type_item = row['问题类别']
            issue_atribute_item = row['问题属性']
            take_over_item = row['是否接管']
            related_plan_item = row['关联计划']


            # 执行
            driver = get_driver()

            open_url(driver)
            switch_iframe()
            query_tripname(tripname=trip_name_item)
            # filter_taglist()
            click_tag_list()
            time.sleep(4)
            paging()
            diagnosis_list(tag_id_item)

            # 输入描述
            input_desc(desc_item)
            # 点击创建飞书项目
            create_work_item()
            input_operator(operator_item)


            # 选择业务线
            business(business_item)
            # 设置优先级
            priority(priority_item)

            # 问题所属模块
            module(module_item)

            # 时间
            what_time(what_time_item)

            # 区域
            area(area_item)

            # 天气
            whether(whether_item)

            # 子功能
            child_function(child_func_item)

            # 道路类型

            road_type(road_type_item)

            # 障碍物
            obstacle(obstacle_item)

            # 任务类型
            task_type(task_type_item)


            # 二级分类
            secondary(secondary_item)

            #问题类别

            issue_type(issue_type_item)

            # 问题属性

            issue_atribute(issue_atribute_item)

            # 是否接管

            takeover(take_over_item)


            # 关联计划
            related_plan(related_plan_item)

            # 提交
            submit()

            i = int(content) + 1
            print(f"i的值为{str(i)}")

            write_index(str(i))
            print("index + 1")

            keyboard = Controller()
            # 按下并释放组合键 'Ctrl+T'
            with keyboard.pressed(Key.cmd):
                keyboard.press('t')
                keyboard.release('t')
            time.sleep(2)
            # 按下并释放组合键 'Ctrl+T'
            with keyboard.pressed(Key.cmd):
                keyboard.press('1')
                keyboard.release('1')
            time.sleep(2)
            # 按下并释放组合键 'Ctrl+T'
            with keyboard.pressed(Key.cmd):
                keyboard.press('w')
                keyboard.release('w')
            time.sleep(3)

            break




            # driver.refresh()
            # driver.close()



        # return desc,tag_id,operator,business,what_time,area,whether,child_func,road_type,obstacle,task_type,secondary,issue_type,issue_atribute,take_over,related_plan

    print(data_frame)

def read_index():
    # 打开文件
    with open('index.txt', 'r', encoding='utf-8') as file:
        # 读取文件内容
        content = int(file.read())
    # 打印文件内容
    print(content)
    return content
def write_index(content):
    import fileinput

    # 写入新内容到原文件或新文件
    with open('index.txt', 'w') as file:
        file.write(content)


def zanting():
    def on_press(key):
        try:
            if key == keyboard.Key.esc:
                print("按下了esc键盘")
                return False
        except AttributeError:
            print('按下特殊键: {0}'.format(key))

    def on_release(key):
        print('释放键: {0}'.format(key))
        if key == keyboard.Key.esc:
            return False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
def get_num_of_page():
    count_loc = (By.XPATH, "//*/div[contains(text(),'共')]")
    count_ele = WebDriverWait(driver,100,1).until(EC.visibility_of_element_located(count_loc))
    count_num = int(int(count_ele.text.replace("共","").replace("条","").strip()) / 100) + 1
    print("countnum的个数为",count_num)

    return count_num
def click_one_page(count_num):
    xpath_pre = "//*/div[contains(text(),'{}') and @class='n-pagination-item n-pagination-item--clickable']".format(count_num)
    click_page_loc = (By.XPATH,xpath_pre)
    print("表达式",xpath_pre)
    click_page_ele = WebDriverWait(driver,100,1).until(EC.visibility_of_element_located(click_page_loc))
    action = ActionChains(driver)
    action.scroll_to_element(click_page_ele).perform()
    time.sleep(1)
    action.click(click_page_ele).perform()
def excell_get():
    df = pd.DataFrame({"id": [1, 2, 3], "name": ["Nick", "Bob", "Tom"]})
    df.to_excel("data.xlsx")

if __name__ == '__main__':
    # zanting()
    # while True:
    #     read_excell()
    # read_index()
    # write_index("2")
    excell_get()
