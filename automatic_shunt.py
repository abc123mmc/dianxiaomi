import currency
import re,requests

class automaticShunt(currency.starUpChrome):
    def new_page(self):
        '''在新页面打开店小蜜，并切换焦点到索引[1]'''
        self.driver.execute_script('window.open("https://dianxiaomi.taobao.com/#/xinsight/xinsightAuto/xinsight_573");')
        currency.time.sleep(5)
        self.driver.switch_to_window(self.driver.window_handles[1])

    def go_dianxiaomi(self,latest_date=''):
        '''传入最近跟新时间latest_date，跳转到店小蜜页，如果已经更新则返回最新，否则返回传入值'''
        self.driver.get('https://dianxiaomi.taobao.com/#/xinsight/xinsightAuto/xinsight_573')
        body=self.driver.find_element_by_css_selector('body')
        for i in range(5):
            body.click()
            body.send_keys(currency.Keys.ESCAPE)
        currency.time.sleep(2)
        latest_date1=self.driver.find_element_by_xpath("//div[contains(text(),'更新到今天')]").text
        if latest_date != latest_date1: return latest_date1
        else: return latest_date

    def get_wangwang(self):
        '''读取 xiazai 文件夹下单 文件的B列并返回，同时删除下载的文件'''
        li=currency.dirlist('xiazai')
        excel_cols1=[]
        for i in li:
            l=currency.weiExcel(i,'detail').e_read(1,'lieB')[1:]
            excel_cols1+=l
            currency.os.remove(i)            
        return excel_cols1

    def go_shunt(self):
        '''转到分流页，并设置没页条数（大于336条则每页168条，低于336条则分为2页）'''
        t=currency.time.localtime()
        self.driver.get('https://zizhanghao.taobao.com/subaccount/qianniu/OfflineDispatch.htm?date=%d-%02d-%02d'%(t[0],t[1],t[2]))
        currency.time.sleep(5)
        weichuli='td:nth-child(7)>a>span[title="服务助手接待后未转接到人工客服且后续没有和人工客服沟通过的买家"]'
        weichuli=self.driver.find_element_by_css_selector(weichuli)
        weichuli=int(re.findall('\d{1,10}',weichuli.text)[0])
        weichuli=int(weichuli/2+1)
        if weichuli>168:  weichuli=168
        xianshitiaoshu=self.driver.find_element_by_xpath("//span[contains(text(),'每页')] //input")
        xianshitiaoshu.clear()
        xianshitiaoshu.click()
        xianshitiaoshu.send_keys(str(weichuli))
        xianshitiaoshu.send_keys(currency.Keys.ENTER)
        currency.time.sleep(3)

    def all_shunt(self):
        '''全部分流'''
        self.driver.find_element_by_xpath("//a[contains(text(),'一键分配当天全部')]").click()
        currency.time.sleep(1)
        self.driver.find_element_by_xpath("//a[contains(text(),'一键分配当天全部')]/div/a[1]").click()

    def part_shunt(self,wangwang):
        '''部分流'''
        b=slh.driver.find_elements_by_css_selector('#J_records>tbody>tr>td:nth-child(1)')
        for i in b:
            if i.text in wangwang: i.find_elements_by_css_selector('input').click()
        self.driver.find_element_by_xpath("//a[contains(text(),'批量分配')]").click()
        currency.time.sleep(1)
        self.driver.find_element_by_xpath("//a[contains(text(),'批量分配')]/div/a[1]").click()

    def part_shunt1(self,wangwang):
        '''部分流'''
        t=currency.time.localtime()
        data={'group':'' ,
            'intention':'' ,
            'pageSize':'10' ,
            'status':'1' ,
            'beginTime':'%d-%02d-%02d 00:00'%(t[0],t[1],t[2]),
            'endTime':'%d-%02d-%02d 24:00'%(t[0],t[1],t[2]) ,
            'site':'0'}
        headers={'accept':'application/json, text/javascript, */*; q=0.01' ,
            'accept-encoding':'gzip, deflate, br' ,
            'accept-language':'zh-CN,zh;q=0.8' ,
            'content-length':'115' ,
            'content-type':'application/x-www-form-urlencoded; charset=UTF-8' ,
            'origin':'https://zizhanghao.taobao.com' ,
            'referer':'https://zizhanghao.taobao.com/subaccount/qianniu/OfflineDispatch.htm?date=2019-10-07' ,
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36' ,
            'x-requested-with':'XMLHttpRequest'}
        cookies=self.driver.get_cookies()
        cookies1=[]
        for i in cookies:
            kv=f"{i['name']}={i['value']}"
            cookies1+=[kv]
            if i['name']=='_tb_token_':
                url=f'https://zizhanghao.taobao.com/subaccount/qianniu/offlineDispatchAjaxHandler.htm?method=doGetOfflineDispathRecords&{kv}'
                url1=f'https://zizhanghao.taobao.com/subaccount/qianniu/offlineDispatchAjaxHandler.htm?method=doReDispatch&{kv}'
        headers['cookie']='; '.join(cookies1)
        li=[]
        pagenum=1
        while 1:
            data['currentPage']=f'{pagenum}'
            req=requests.post(url,data=data,headers=headers).json()
            for i in req['data']['list']:
                if i['account'] in wangwang: li+=[i['id']]
            print(f"第{pagenum}页，共有数据{len(req['data']['list'])}条")
            if len(req['data']['list'])<10: break
            pagenum+=1
        print(len(li),103)
        for i in li:
            data1={'site':'','ids':i}
            requests.post(url1,data=data1,headers=headers)

    def page_turning(self):
        '''翻页'''
        next_page=self.driver.find_element_by_xpath("//a[contains(text(),'下一页')]")
        if 'disabled' in next_page.find_element_by_xpath('./..').get_attribute('outerHTML'):return '末页'
        else: next_page.click()

    def run(self,x1,x2,x3,x4):
        if x4:
            qbfl=True#全部分流
        else:
            qbfl=False
            if x1:
                self.driver.find_element_by_xpath("//span[contains(text(),'下载下单未付款名单')]").click()
                currency.time.sleep(5)
            if x2:
                self.driver.find_element_by_xpath("//span[contains(text(),'下载下单未付款名单')]").click()
                currency.time.sleep(5)
            if x3:
                self.driver.find_element_by_xpath("//span[contains(text(),'下载下单未付款名单')]").click()
                currency.time.sleep(5)
            excel_cols1=self.get_wangwang()#调用获取旺旺
        currency.time.sleep(60*5)#******等待时间5分钟
        self.go_shunt()#调用转到分流
        if qbfl: self.all_shunt()#调用全部分流
        else:
            self.part_shunt1(excel_cols1)#调用部分分流
        currency.time.sleep(10)

    def cs001(self):
        '''当前逻辑测试'''
        latest_date=''
        x1=x2=x3=1
        x4=0
        while 1:
            currency.time.sleep(3)
            try:latest_date2=self.go_dianxiaomi(latest_date='')
            except:pass
            if latest_date!=latest_date2:
                self.run(x1,x2,x3,x4)
                latest_date=latest_date2


if __name__ == "__main__":
    slh=automaticShunt()#实例化类
    slh.star_driver()#启动浏览器
    #slh.cs001()
    #slh.new_page()#打开新网页标签并跳转
    #slh.go_dianxiaomi(latest_date='')#跳转到店小蜜，并判断是否更新
    #slh.run(x1,x2,x3,x4)
    pass
