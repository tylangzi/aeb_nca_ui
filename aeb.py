"""
获取driver,并访问百度
"""
import sys
import time

import pyautogui
import pyperclip
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

def clear_tripname():
    # 输入tripname
    input_loc = (By.XPATH, "//*/span[contains(text(),'行程名称:')]/../..//input")
    input_ele = WebDriverWait(driver,10,1).until(EC.visibility_of_element_located(input_loc))
    input_ele.send_keys(Keys.CONTROL, 'a')
    input_ele.send_keys(Keys.BACKSPACE)

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
    # time.sleep(1)
    for i in range(2):
        input_dest_ele.send_keys(Keys.CONTROL, 'a')
        time.sleep(0.1)
        input_dest_ele.send_keys(Keys.BACKSPACE)
        time.sleep(0.1)
    # time.sleep(2)
    # 开始输入内容
    input_dest_ele.send_keys(text)
    past_text = "【售后问题】" + pyperclip.paste()
    input_dest_ele.send_keys(past_text)

    return past_text
def create_work_item():
    # time.sleep(3)
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
def scroll_to_element(driver,ele):
    for _ in range(5):
        try:
            time.sleep(0.05)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ele) #拖动到可见的元素去

            # action = ActionChains(driver)
            # action.move_to_element(ele).perform()
            # time.sleep(1)
            # action.scroll_to_element(ele).perform()
            break
        except Exception as e:
            print(e)
            time.sleep(1)

def click_element(driver,ele):
    for _ in range(5):
        try:
            action = ActionChains(driver)
            action.click(ele).perform()
            break
        except Exception as e:
            print(e)
            time.sleep(1)

def input_operator(input_content='pinyihu'):

    operator_loc = (By.XPATH, "//*/span[contains(text(),'经办人')]/../..//*/input")
    operator_ele = WebDriverWait(driver,200,1).until(EC.visibility_of_element_located(operator_loc))
    # 移动到该元素
    scroll_to_element(driver,operator_ele)
    operator_ele.send_keys(input_content)

    item_loc = (By.XPATH,"//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]
    for _ in range(5):
        try:
            content_loc = (By.XPATH, ".//div")
            content_ele = item_ele.find_element(*content_loc)
            break
        except Exception as e:
            print(e)
            time.sleep(0.5)

    while True:
        try:
            print(content_ele.text)
            scroll_to_element(driver,content_ele)
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")
                click_element(driver,content_ele)
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text,f"可见的<div>元素数量: {len(item_ele_list)}")

def business(input_contents="GWM"):


    business_loc = (By.XPATH, "//*/span[contains(text(),'业务线')]/../..//*/input")
    business_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(business_loc))
    # 移动到该元素
    scroll_to_element(driver,business_ele)
    click_element(driver,business_ele)
    for input_content in [input_content for input_content in input_contents.split(' / ')]:
        # business_ele.send_keys(input_content)

        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]

        for _ in range(5):
            try:
                content_loc = (By.XPATH, ".//div")
                content_ele = item_ele.find_element(*content_loc)
                break
            except Exception as e:
                print(e)
                time.sleep(0.5)


        while True:
            try:

                print(content_ele.text)
                scroll_to_element(driver,content_ele)
                if input_content == content_ele.text:
                    print(f"{content_ele.text}为输入的值")

                    click_element(driver,content_ele)
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
    scroll_to_element(driver,priority_ele)

    priority_ele.send_keys(input_content)

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]
    for _ in range(5):
        try:
            content_loc = (By.XPATH, ".//div")
            content_ele = item_ele.find_element(*content_loc)
            break
        except Exception as e:
            print(e)
            time.sleep(0.5)

    while True:
        try:

            print(content_ele.text)
            scroll_to_element(driver,content_ele)
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")

                click_element(driver,content_ele)
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
    scroll_to_element(driver,module_ele)

    module_ele.click()

    item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
    item_ele_list = driver.find_elements(*item_loc)
    item_ele = item_ele_list[-1]

    for _ in range(5):
        try:
            content_loc = (By.XPATH, ".//div")
            content_ele = item_ele.find_element(*content_loc)
            break
        except Exception as e:
            print(e)
            time.sleep(0.5)

    while True:
        try:
            print(content_ele.text)
            scroll_to_element(driver,content_ele)
            if input_content == content_ele.text:
                print(f"{content_ele.text}为输入的值")

                click_element(driver,content_ele)
                break
            else:
                content_loc = (By.XPATH, "./following-sibling::div[1]")
                content_ele = content_ele.find_element(*content_loc)
        except Exception as e:
            print(e)
            print(f"请检查表格中的值{input_content}是否有误")
    print(item_ele.text, f"可见的<div>元素数量: {len(item_ele_list)}")
    # 点击经办人
    operator_loc = (By.XPATH, "//*/span[contains(text(),'经办人')]")
    operator_ele = WebDriverWait(driver, 200, 1).until(EC.visibility_of_element_located(operator_loc))
    # 移动到该元素
    scroll_to_element(driver,operator_ele)
    operator_ele.click()

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



def the_time(input_contents="白天"):

    if input_contents == "白天":
        the_time_loc = (By.XPATH, "//*/div[text()='白天']")
    elif input_contents == "夜晚":
        the_time_loc = (By.XPATH, "//*/div[text()='夜晚']")
    else:
        print("请输入正确的问题属性")

    the_time_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(the_time_loc))

    # 移动到该元素并点击该元素
    scroll_to_element(driver,the_time_ele)
    click_element(driver,the_time_ele)

def area(input_contents="白天"):

    if input_contents == "白天":
        area_loc = (By.XPATH, "//*/div[text()='白天']")
    elif input_contents == "夜晚":
        area_loc = (By.XPATH, "//*/div[text()='夜晚']")
    else:
        print("请输入正确的问题属性")

    area_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(area_loc))

    # 移动到该元素并点击该元素
    scroll_to_element(driver, area_ele)
    click_element(driver, area_ele)

def child_function(input_contents="纵向功能 / 融合限速 / 隧道限速"):

    fun_loc = (By.XPATH, "//*/span[contains(text(),'子功能')]/../..//div")
    fun_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(fun_loc))

    # 移动到该元素
    scroll_to_element(driver,fun_ele)

    fun_ele.click()

    for input_content in [input_content for input_content in input_contents.split(' / ')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]

        for _ in range(5):
            try:
                content_loc = (By.XPATH, ".//span")
                content_ele = item_ele.find_element(*content_loc)
                break
            except Exception as e:
                print(e)
                time.sleep(0.5)


        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                scroll_to_element(driver,content_ele)
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    click_element(driver,content_ele)
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
    scroll_to_element(driver, road_type_ele)

    road_type_ele.click()

    for input_content in [input_content for input_content in input_contents.split(' / ')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]
        print(item_ele.get_attribute('innerHTML'))

        for _ in range(5):
            try:
                content_loc = (By.XPATH, "./div/div")
                content_ele = item_ele.find_element(*content_loc)
                break
            except Exception as e:
                print(e)
                time.sleep(0.5)


        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                scroll_to_element(driver,content_ele)
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    click_element(driver,content_ele)
                    break
                else:
                    content_loc = (By.XPATH, "./../following-sibling::div[1]/div")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")

def obstacle(input_contents="障碍物类型 / 小障碍物 / 锥桶 / 倒地锥桶"):

    obstacle_loc = (By.XPATH, "//*/span[contains(text(),'障碍物交互')]/../..//div")
    obstacle_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(obstacle_loc))

    # 移动到该元素
    scroll_to_element(driver,obstacle_ele)

    obstacle_ele.click()

    for input_content in [input_content for input_content in input_contents.split(' / ')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]

        for _ in range(5):
            try:
                content_loc = (By.XPATH, ".//span")
                content_ele = item_ele.find_element(*content_loc)
                break
            except Exception as e:
                print(e)
                time.sleep(0.5)


        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                scroll_to_element(driver,content_ele)
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    click_element(driver,content_ele)
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
    scroll_to_element(driver,task_type_ele)

    task_type_ele.click()

    for input_content in [input_content for input_content in input_contents.split(' / ')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]

        for _ in range(5):
            try:
                content_loc = (By.XPATH, "./div/div")
                content_ele = item_ele.find_element(*content_loc)
                break
            except Exception as e:
                print(e)
                time.sleep(0.5)


        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                scroll_to_element(driver,content_ele)
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    click_element(driver,content_ele)
                    break
                else:
                    content_loc = (By.XPATH, "./../following-sibling::div[1]/div")
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
    scroll_to_element(driver,issue_type_ele)

    issue_type_ele.click()

    for input_content in [input_content for input_content in input_contents.split(' / ')]:
        item_loc = (By.XPATH, "//*/div[@class='v-vl-visible-items']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]

        for _ in range(5):
            try:
                content_loc = (By.XPATH, ".//span")
                content_ele = item_ele.find_element(*content_loc)
                break
            except Exception as e:
                print(e)
                time.sleep(0.5)


        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                scroll_to_element(driver,content_ele)
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    click_element(driver,content_ele)
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
    scroll_to_element(driver,submit_ele)
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
    with open('/home/pinyihu/pyworkspace/diagnosis/index.txt', 'r', encoding='utf-8') as file:
        # 读取文件内容
        content = str(file.read())
    # 打印文件内容
    print(content)
    return content

def read_index_second():
    # 打开文件
    with open('/home/pinyihu/pyworkspace/second/index.txt', 'r', encoding='utf-8') as file:
        # 读取文件内容
        content = str(file.read())
    # 打印文件内容
    print(content)
    return content

def write_index_second(content):
    import fileinput

    # 写入新内容到原文件或新文件
    with open('/home/pinyihu/pyworkspace/second/index.txt', 'w') as file:
        file.write(content)

def write_index(content):
    import fileinput

    # 写入新内容到原文件或新文件
    with open('/home/pinyihu/pyworkspace/diagnosis/index.txt', 'w') as file:
        file.write(content)


def zanting():
    def on_press(key):
        try:
            if key == keyboard.Key.alt:
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


def to_feishu():
    # p判断已经创建成功
    while True:
        try:
            triaged_loc = (By.XPATH, "//*/span[contains(text(),'TRIAGED')]")
            triaged_ele = driver.find_element(*triaged_loc)
            scroll_to_element(driver,triaged_ele)
            click_element(driver,triaged_ele)
            break
        except Exception as e:
            print(e)
            print("未提交成功")
            time.sleep(0.5)
    while True:
        try:
            to_feishu_loc = (By.XPATH,"//*/span[contains(text(),'跳转到飞书工作项')]")
            to_feishu_ele = driver.find_element(*to_feishu_loc)
            scroll_to_element(driver,to_feishu_ele)
            click_element(driver,to_feishu_ele)
            break
        except Exception as e:
            print(e)
            print("找不到飞书工作项目跳转链接")
            time.sleep(1)


def open_new_window(driver):
    while True:
        if len(driver.window_handles) == 1:
            print("没有打开新的窗口")

        else:
            print("打开了新的窗口")
            break
    # time.sleep(2)
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    # time.sleep(1)

    # 重新打开页面

    url = driver.current_url
    return url

    # # 切回主页面
    # driver.switch_to.default_content()

    # zanting()

def large_fanhua(input_contents="客户泛化问题"):
    large_fanhua_loc = (By.XPATH, "//*/span[contains(text(),'大规模泛化标签')]/../../..//div[contains(text(),'待填')]")
    large_fanhua_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(large_fanhua_loc))

    # 移动到该元素
    scroll_to_element(driver, large_fanhua_ele)

    large_fanhua_ele.click()
    time.sleep(1)

    for input_content in [input_content for input_content in input_contents.split(' / ')]:
        item_loc = (By.XPATH, "//*/div[@class='semi-select-option-list']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]

        for _ in range(5):
            try:
                content_loc = (By.XPATH, ".//span")
                content_ele = item_ele.find_element(*content_loc)
                break
            except Exception as e:
                print(e)
                time.sleep(0.5)

        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                scroll_to_element(driver, content_ele)
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    click_element(driver, content_ele)
                    break
                else:
                    content_loc = (By.XPATH, "./../../../../following-sibling::div[1]//span")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")


def issue_from(input_contents="客户泛化问题"):
    issue_from_loc = (By.XPATH, "//*/span[contains(text(),'问题来源')]/../../..//div[contains(text(),'待填')]")
    issue_from_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(issue_from_loc))

    # 移动到该元素
    scroll_to_element(driver, issue_from_ele)

    issue_from_ele.click()
    time.sleep(1)

    for input_content in [input_content for input_content in input_contents.split(' / ')]:
        item_loc = (By.XPATH, "//*/div[@class='semi-select-option-list']")
        item_ele_list = driver.find_elements(*item_loc)
        item_ele = item_ele_list[-1]

        for _ in range(5):
            try:
                content_loc = (By.XPATH, ".//span")
                content_ele = item_ele.find_element(*content_loc)
                break
            except Exception as e:
                print(e)
                time.sleep(0.5)

        while True:
            try:
                print(f"content_ele.text的值为：{content_ele.text.strip()}")
                print(f"input_content的值为：{input_content.strip()}")
                scroll_to_element(driver, content_ele)
                if input_content.strip() == content_ele.text.strip():
                    print(f"{content_ele.text}为输入的值")
                    click_element(driver, content_ele)
                    break
                else:
                    content_loc = (By.XPATH, "./../../../../following-sibling::div[1]//span")
                    content_ele = content_ele.find_element(*content_loc)
            except Exception as e:
                print(e)
                print(f"请检查表格中的值{input_content}是否有误")


def copy_link():
    copy_link_loc = (By.XPATH, "//*[name()='svg' and @data-icon='GlobalLinkOutlined']")
    copy_link_ele = WebDriverWait(driver, 20, 1).until(EC.visibility_of_element_located(copy_link_loc))

    # 移动到该元素
    scroll_to_element(driver, copy_link_ele)

    copy_link_ele.click()
def get_cur_window(driver):
    cur = driver.current_window_handle
    return cur


def issue_zhenduan():
    zhenduan_loc = (By.XPATH, "//*[@id='app']/div/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]")
    zhenduan_ele = driver.find_element(*zhenduan_loc)
    click_element(driver, zhenduan_ele)


def meb():
    driver = get_driver()
    switch_iframe()

    # 输入描述
    pasttext = input_desc("")

    create_work_item()
    if "轨迹" in pasttext and "不准" in pasttext and "误" in pasttext:
        name = "shengmingmei"
    elif "误" in pasttext:
        name = "jingsongzhang"
    else:
        name = "zenengshe"
    input_operator(name)
    # 业务线
    business("GWM / C01")
    priority("P0")
    module("AEB")
    child_function("MEB")
    if "轨迹" in pasttext or "小车横穿" in pasttext or "车辆横穿" in pasttext or "电动车横穿" in pasttext:
        road_type_text = "城区/直道"
    elif "路沿" in pasttext:
        road_type_text = "乡村道路"

    else:
        road_type_text = "特殊路段/停车场"
    road_type(road_type_text)
    if "行人" in pasttext and "横穿" in pasttext:
        obstacle_text = "车对行人 / 后方成人横穿"
    elif "行人" in pasttext:
        obstacle_text = "车对行人 / 后方静止成人"
    elif "小车" in pasttext and "横穿" in pasttext:
        obstacle_text = "车对车 / 后向车辆横穿"
    elif "电动车" in pasttext and "横穿" in pasttext:
        obstacle_text = "车对车 / 后向车辆横穿"
    elif "墙体" in pasttext or "充电桩" in pasttext or "箱" in pasttext or "柱" in pasttext or "卷闸门" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对墙柱"
    elif "桶" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对圆柱"
    elif "电动车" in pasttext or "小车" in pasttext:
        obstacle_text = "车对车 / 后方车辆接近"
    elif "拖车" in pasttext:
        obstacle_text = "车对车 / 车辆上拖车"
    elif "雪糕筒" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对雪糕筒"
    elif "路沿" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对路沿"
    elif "石墩" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对路边石墩"
    elif "栏" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对栏杆"
    else:
        obstacle_text = "无干扰行驶"
    obstacle(obstacle_text)
    task_type("泛化测试")
    if "位置" in pasttext and "误" in pasttext:
        issue_type_text = "误制动 / 感知问题 / box不稳定"
    elif "误" in pasttext and "雪糕筒" in pasttext:
        issue_type_text = "误制动 / 感知问题 / 误检锥桶/三角架/雪糕筒"
    elif "误检" in pasttext and "行人" in pasttext:
        issue_type_text = "误制动 / 感知问题 / 误检VRU"
    elif "轨迹" in pasttext and "不" in pasttext:
        issue_type_text = "误制动 / 感知问题 / 物体方向不准"
    elif "误" in pasttext:
        issue_type_text = "误制动 / 感知问题 / 误检一般障碍物"
    else:
        issue_type_text = "正触发"
    issue_type(issue_type_text)

    # 暂停检查
    zanting()

    # 提交飞书工作项
    submit()
    # 打开飞书项目
    to_feishu()

    # 获取当前句柄
    cur0 = driver.current_window_handle

    # 切换窗口
    url = open_new_window(driver)
    # time.sleep(1)



    # 写入url
    write_index_second(str(url))

    # 清空形成名称


    # 判断 second是否执行完毕

    while True:
        index = read_index()
        if index is None or not index:
            time.sleep(1)
            print("没有内容")
        else:
            print("有内容")
            write_index("")
            time.sleep(1)
            # 关闭飞书页面并返回最开始的页面
            driver.close()
            driver.switch_to.window(cur0)

            # 点击问题诊断
            issue_zhenduan()

            #清空内容
            clear_tripname()





            break


    # # 结束程序
    # sys.exit()

    #
    # driver.switch_to_default_content()
    # # 再次打开
    # open_again(driver, url)
    #
    #
    # # 勾选标签
    # large_fanhua("客户泛化问题")
    #
    # # 问题来源
    # issue_from("主动安全case")
    #
    # #复制链接
    #
    # copy_link()
    #
    #
    # # 再次打开诊断页面
    # driver.get("https://drplatform.deeproute.cn/#/diagnosis-management/diagnosis?path=%2Fissue%2Ftag")
    #
    #
    # 结束程序
    # sys.exit()


def open_again(driver,url):
    driver.get(url)
    driver.switch_to.window(driver.window_handles[-1])


def close_other():
    keyboard = Controller()
    # 按下并释放组合键 'Ctrl+T'
    # with keyboard.pressed(Key.ctrl):
    #     keyboard.press('2')
    #     keyboard.release('2')
    # time.sleep(2)
    # 按下并释放组合键 'Ctrl+T'
    with keyboard.pressed(Key.ctrl):
        keyboard.press('w')
        keyboard.release('w')



def test():
    driver = get_driver()
    switch_iframe()

    time.sleep(1)





    # 获取当前句柄
    cur0 = driver.current_window_handle
    # 切换窗口
    url = open_new_window(driver)

    # 关闭飞书页面并返回最开始的页面
    driver.close()
    driver.switch_to.window(cur0)


    # 再次打开
    open_again(driver,url)

    large_fanhua("客户泛化问题")

    # 问题来源
    issue_from("主动安全case")

    #复制链接
    copy_link()

    # 再次打开诊断页面
    driver.get("https://drplatform.deeproute.cn/#/diagnosis-management/diagnosis?path=%2Fissue%2Ftag")


    # 结束程序
    sys.exit()


def data_filter_meb(pasttext):
    data = {}
    # 名字
    if "轨迹" in pasttext and "不准" in pasttext and "误" in pasttext:
        input_operator = "shengmingmei"
    elif "误" in pasttext:
        input_operator = "jingsongzhang"
    else:
        input_operator = "zenengshe"
    data["input_operator"] = input_operator

    # 业务线
    data["business"] = "GWM / C01"

    # 优先级
    data["priority"] = "P0"

    # 所属模块
    data["module"] = "AEB"

    # 子功能
    data["child_function"] = "MEB"

    # 道路类型
    if "轨迹" in pasttext or "小车横穿" in pasttext or "车辆横穿" in pasttext or "电动车横穿" in pasttext:
        road_type_text = "城区/直道"
    elif "路沿" in pasttext:
        road_type_text = "乡村道路"
    else:
        road_type_text = "特殊路段/停车场"
    data["road_type"] = road_type_text

    # 障碍物
    if "行人" in pasttext and "横穿" in pasttext:
        obstacle_text = "车对行人 / 后方成人横穿"
    elif "行人" in pasttext:
        obstacle_text = "车对行人 / 后方静止成人"
    elif "小车" in pasttext and "横穿" in pasttext:
        obstacle_text = "车对车 / 后向车辆横穿"
    elif "电动车" in pasttext and "横穿" in pasttext:
        obstacle_text = "车对车 / 后向车辆横穿"
    elif "墙体" in pasttext or "充电桩" in pasttext or "箱" in pasttext or "柱" in pasttext or "卷闸门" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对墙柱"
    elif "桶" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对圆柱"
    elif "电动车" in pasttext or "小车" in pasttext:
        obstacle_text = "车对车 / 后方车辆接近"
    elif "拖车" in pasttext:
        obstacle_text = "车对车 / 车辆上拖车"
    elif "雪糕筒" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对雪糕筒"
    elif "路沿" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对路沿"
    elif "石墩" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对路边石墩"
    elif "栏" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对栏杆"
    else:
        obstacle_text = "无干扰行驶"
    data["obstacle"] = obstacle_text

    # 测试任务
    data["task_type"] = "泛化测试"

    # 问题类型
    if "位置" in pasttext and "误" in pasttext:
        issue_type_text = "误制动 / 感知问题 / box不稳定"
    elif "误" in pasttext and "雪糕筒" in pasttext:
        issue_type_text = "误制动 / 感知问题 / 误检锥桶/三角架/雪糕筒"
    elif "误检" in pasttext and "行人" in pasttext:
        issue_type_text = "误制动 / 感知问题 / 误检VRU"
    elif "轨迹" in pasttext and "不" in pasttext:
        issue_type_text = "误制动 / 感知问题 / 物体方向不准"
    elif "误" in pasttext:
        issue_type_text = "误制动 / 感知问题 / 误检一般障碍物"
    else:
        issue_type_text = "正触发"
    data["issue_type"] = issue_type_text

    return data


def data_filter_aeb(pasttext):
    data = {}
    # 名字
    if "轨迹" in pasttext and "不准" in pasttext and "误" in pasttext:
        input_operator = "shengmingmei"
    elif "误" in pasttext:
        input_operator = "jingsongzhang"
    else:
        input_operator = "zenengshe"
    data["input_operator"] = input_operator

    # 业务线
    data["business"] = "GWM / C01"

    # 优先级
    data["priority"] = "P0"

    # 所属模块
    data["module"] = "AEB"

    # 子功能
    data["child_function"] = "MEB"

    # 道路类型
    if "轨迹" in pasttext or "小车横穿" in pasttext or "车辆横穿" in pasttext or "电动车横穿" in pasttext:
        road_type_text = "城区/直道"
    elif "路沿" in pasttext:
        road_type_text = "乡村道路"
    else:
        road_type_text = "特殊路段/停车场"
    data["road_type"] = road_type_text

    # 障碍物
    if "行人" in pasttext and "横穿" in pasttext:
        obstacle_text = "车对行人 / 后方成人横穿"
    elif "行人" in pasttext:
        obstacle_text = "车对行人 / 后方静止成人"
    elif "小车" in pasttext and "横穿" in pasttext:
        obstacle_text = "车对车 / 后向车辆横穿"
    elif "电动车" in pasttext and "横穿" in pasttext:
        obstacle_text = "车对车 / 后向车辆横穿"
    elif "墙体" in pasttext or "充电桩" in pasttext or "箱" in pasttext or "柱" in pasttext or "卷闸门" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对墙柱"
    elif "桶" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对圆柱"
    elif "电动车" in pasttext or "小车" in pasttext:
        obstacle_text = "车对车 / 后方车辆接近"
    elif "拖车" in pasttext:
        obstacle_text = "车对车 / 车辆上拖车"
    elif "雪糕筒" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对雪糕筒"
    elif "路沿" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对路沿"
    elif "石墩" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对路边石墩"
    elif "栏" in pasttext:
        obstacle_text = "车对静态障碍物 / 车对栏杆"
    else:
        obstacle_text = "无干扰行驶"
    data["obstacle"] = obstacle_text

    # 测试任务
    data["task_type"] = "泛化测试"

    # 问题类型
    if "位置" in pasttext and "误" in pasttext:
        issue_type_text = "误制动 / 感知问题 / box不稳定"
    elif "误" in pasttext and "雪糕筒" in pasttext:
        issue_type_text = "误制动 / 感知问题 / 误检锥桶/三角架/雪糕筒"
    elif "误检" in pasttext and "行人" in pasttext:
        issue_type_text = "误制动 / 感知问题 / 误检VRU"
    elif "轨迹" in pasttext and "不" in pasttext:
        issue_type_text = "误制动 / 感知问题 / 物体方向不准"
    elif "误" in pasttext:
        issue_type_text = "误制动 / 感知问题 / 误检一般障碍物"
    else:
        issue_type_text = "正触发"
    data["issue_type"] = issue_type_text

    return data


def data_filter(pasttext):
    # 定义空字典
    data = {}
    # MEB 数据
    if "meb" in pasttext or "MEB" in pasttext:
        data = data_filter_meb(pasttext)
    elif "aeb" in pasttext or "AEB" in pasttext:
        data = data_filter_aeb(pasttext)
    return data

def aeb():
    switch_iframe()
    # 输入描述
    pasttext = input_desc("")
    # 获取具体的输入数据
    data = data_filter(pasttext)
    print(data)
    create_work_item()
    input_operator(data["input_operator"])
    # 业务线
    business(data["business"])
    priority(data["priority"])
    module(data["module"])
    child_function(data["child_function"])
    road_type(data["road_type"])
    obstacle(data["obstacle"])
    task_type(data["task_type"])
    issue_type(data["issue_type"])
    # 暂停检查
    zanting()
    # 提交飞书工作项
    submit()
    # 打开飞书项目
    to_feishu()
    # 获取当前句柄
    cur0 = driver.current_window_handle
    # 切换窗口
    url = open_new_window(driver)
    # 写入url
    write_index_second(str(url))

    while True:
        index = read_index()
        if index is None or not index:
            time.sleep(1)
            print("没有内容")
        else:
            print("有内容")
            write_index("")
            time.sleep(1)
            # 关闭飞书页面并返回最开始的页面
            driver.close()
            driver.switch_to.window(cur0)

            # 点击问题诊断
            issue_zhenduan()

            #清空内容
            clear_tripname()
            break


if __name__ == '__main__':
     aeb()

