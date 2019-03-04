from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import json


class Dpspider(object):
    def __init__(self):
        # options = Options()
        # options.set_headless()
        # self.driver = webdriver.Chrome(options=options)
        self.driver = webdriver.Chrome()
        self.num = 1
        self.base_urls = "https://nanjing.newhouse.fang.com/house/s//b9{}/".format(self.num)
     
    def xinfang_list(self, isTure=True):
        # 获取所有房源
        # name = self.driver.find_elements_by_xpath('//*[@class="clearfix"]/div/a')
        name = self.driver.find_elements_by_xpath('//*[@class="nl_con clearfix"]/ul/li/div/div[1]/a')
        house_lst = []
        for i in name:
            href = (i.get_attribute('href'))
            house_lst.append(href)
        data_list = []
        for url in house_lst:
            self.driver.get(url)
            # 获取楼盘点评
            try:
                fangyuan_url = self.driver.find_element_by_xpath("//*[@class='navleft tf']//a[contains(text(),'点评')]")
                href1 = fangyuan_url.get_attribute('href')
                self.driver.get(href1)
                # self.driver.get("https://gongyuanchengzh.fang.com/dianping/")
            except Exception as e:
                fangyuan_url = None
                pass
            try:
                while True:
                    next_page = self.driver.find_element_by_link_text("再显示20条")
                    if next_page != None:
                        next_page.click()
                        sleep(0.2)
                    else:
                        break
            except Exception as e:
                pass
            # 获取点评所有信息
            comment = self.driver.find_elements_by_xpath("//div[@id='dpContentList']/div[contains(@id,'detail')]")
            all_comment_dict = {"_id": url}
            commentJson = []
            href = self.driver.current_url  # 获取前页面的url
            for i in comment:
                data = {}
                data["sourceUrl"] = href  # 评论url
                data["source"] = "房天下"  # 来源
                user_name = i.find_element_by_xpath("./div[2]/div[1]").text
                data["userNick"] = user_name  # 用户名
             
                try:
                    data["content"] = i.find_element_by_xpath('.//a//p').text  # 评论内容
                except Exception as e:
                    data["content"] = None
                data["createDate"] = i.find_element_by_xpath('.//em/span').text  # 评论时间
                data_list.append(data)
                commentJson.append(data)
            commentJson = json.dumps(commentJson, ensure_ascii=False)
            all_comment_dict.update({"commentJson": commentJson})
            print(all_comment_dict)
            self.save_data(all_comment_dict)

    def save_data(self, data_list):
        """保存本地数据"""
        with open('点评10号(南京).jsonlines', 'a', encoding='utf8') as f:
            f.write(json.dumps(data_list, ensure_ascii=False))
            f.write('\n')
            f.close()

    def __del__(self):
        # 退出浏览器
        self.driver.quit()
        pass

    def run(self):
        while True:
            # get请求浏览网页
            self.driver.get(self.base_urls)
            # 解析信息
            self.xinfang_list()
            self.num += 1
       
            self.base_urls = "https://nanjing.newhouse.fang.com/house/s//b9{}/".format(self.num)
            if self.num > 38:
                break
      


if __name__ == '__main__':
    GJS = Dpspider()
    GJS.run()
