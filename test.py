import os, json, sys
import time
import scrapy

import login
import baseinfo
import gongshang
import zhuyao_chengyuan
import gudongxinxi
import duiwaitouzi
import rongzi
import hexintuandui

driver=login.login()
driver.save_screenshot('test.png')
# 搜索
# search=driver.find_element_by_id('home-main-search')
# search.send_keys('腾讯')
# ensure=driver.find_element_by_xpath('//div[@class="js-search-container"]'
#                              '//div[@class="input-group inputV2"]'
#                              '//div[@class="input-group-addon search_button"]')
# ensure.click()

# 也可以直接构造网址
key='摩拜'
url='https://www.tianyancha.com/search?key='+key
driver.get(url)

# 选择第一个公司
select=scrapy.Selector(text=driver.page_source)
url=select.xpath('//div[contains(@class,"search_result")]'
             '/div[@class="search_right_item ml10"]'
             '/div[1]/a/@href').extract_first()
driver.get(url)
time.sleep(3)
try:
    driver.find_element_by_xpath('//div[@id="bannerFooterID"]/img').click()
except:
    pass

select=scrapy.Selector(text=driver.page_source)
company={}
# 获取公司基本信息
company['基本信息']=baseinfo.get_base(select)
# 获取工商信息
company['工商信息']=gongshang.get_gongshang(select)
# 获取公司主要成员
company['主要成员']=zhuyao_chengyuan.get_zhuyao(select)
# 获取股东信息
company['股东信息']=gudongxinxi.get_gudong(select)
# 获取对外投资
company['对外投资']=duiwaitouzi.get_duiwai(select,driver)
# 获取融资历史
company['融资历史']=rongzi.get_rongzi(select,driver)
# 核心团队
company['核心团队']=hexintuandui.get_hexin(select,driver)

driver.close()