# 基类——对象库层
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self):
        pass

    # 单个元素定位
    # driver 浏览器对象
    # location 定位元素，示例：(By.ID,'key')
    # timeout 最大等待时间
    # poll 检查频率
    def base_find_elt(self,driver, location, timeout=30, poll=0.5):
        return WebDriverWait(driver, timeout, poll).until(lambda el: el.find_element(*location))

    # 多个元素定位
    # driver 浏览器对象
    # location 定位元素，示例：(By.CLASS_NAME,'key')
    # timeout 最大等待时间
    # poll 检查频率
    def base_find_elts(self,driver, location, timeout=30, poll=0.5):
        return WebDriverWait(driver, timeout, poll).until(lambda el: el.find_elements(*location))

    # 查找页面是否存在指定元素
    # driver 浏览器对象
    # location 定位元素，示例：(By.ID,'key')
    # timeout 最大等待时间
    # poll 检查频率
    def base_isExsit_elt(self,driver, location, timeout=30, poll=0.5):
        try:
            WebDriverWait(driver, timeout, poll).until(lambda el: el.find_element(*location))
            return True
        except:
            # print("未找到{}元素！".format(location))
            return False

    # 通过父类元素查找单个元素
    # driver 浏览器对象
    # fatherEL 父元素对象
    # location 定位元素，示例：(By.CLASS_NAME,'key')
    # timeout 最大等待时间
    # poll 检查频率
    def base_find_el_by_fatherEL(self,driver, fatherEL, location, timeout=30, poll=0.5):
        return WebDriverWait(driver, timeout, poll).until(lambda el: fatherEL.find_element(*location))

    # 通过父类元素查找多个元素
    # driver 浏览器对象
    # fatherEL 父元素对象
    # location 定位元素，示例：(By.CLASS_NAME,'key')
    # timeout 最大等待时间
    # poll 检查频率
    def base_find_els_by_fatherEL(self,driver, fatherEL, location, timeout=30, poll=0.5):
        return WebDriverWait(driver, timeout, poll).until(lambda el: fatherEL.find_elements(*location))

    # 切换窗口(句柄)
    # driver 浏览器对象
    # num 窗口列表中的第几个窗口
    def base_swith_window(self,driver, num):
        # 找到当前所有句柄
        list = driver.window_handles
        # 切换句柄
        driver.switch_to.window(list[num])
