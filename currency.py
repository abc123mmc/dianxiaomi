#currency通用
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import os,shutil,time
import traceback#用于错误处理
import os,re
import xlrd
import xlwt
from xlutils.copy import copy

class starUpChrome():#生意参谋_流量
    def star_driver(self):#启动浏览器
        mkpath=os.getcwd()+'\\xiazai'#保存目录
        try:
            shutil.rmtree(mkpath)
            os.makedirs(mkpath)
        except:pass
        chromeOptions = webdriver.ChromeOptions()
        prefs ={'profile.default_content_settings.popups':0,"download.default_directory":mkpath}#设置默认下载路径
        chromeOptions.add_experimental_option("prefs",prefs)
        self.driver= webdriver.Chrome(options=chromeOptions)
        self.driver.get('https://login.taobao.com/member/login.jhtml?')
        self.driver.maximize_window()

    def drop_down(self,Keys01):#滚动  Keys.DOWN、Keys.UP、Keys.HOME、Keys.END
        self.driver.find_element_by_xpath("//body").send_keys(Keys01)
        time.sleep(1)

class Ri_zhi():#日志和记录
    def __init__(self):
        self.timeArray = time.localtime(int(time.time()))
        self.otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S",self.timeArray)
        if traceback.format_exc()!='NoneType: None\n':
            with open(r"执行日志.txt",'a') as f:
                traceback.print_exc(file=f)
                f.write('********************%s********************\n\n'% self.otherStyleTime)

class weiExcel:
    '''在excel的最后一行写入列表DataList，如果excel文件（或者表名）不存在的话会自动创建'''
    def __init__(self,filename,sheet_name):
        '''初始化表：传入filename(Excel文件名及路径)、sheet_name（表名）'''
        self.filename=filename
        self.sheet_name=sheet_name
        try:self.workbook = xlrd.open_workbook(self.filename, formatting_info=True)
        except:
            wk=xlwt.Workbook()
            wk.add_sheet(sheet_name)
            wk.save(self.filename)
            self.workbook = xlrd.open_workbook(self.filename, formatting_info=True)
        self.sheet = self.workbook.sheet_by_name(sheet_name)
    def e_write(self,DataList=None,Header=None):
        if DataList is None:DataList = []
        newbook = copy(self.workbook)
        newsheet = newbook.get_sheet(self.sheet_name)
        nrows = self.sheet.nrows#获取行数
        ncols = self.sheet.ncols#获取列数
        if ncols==nrows==0:
            for i in range(len(Header)):newsheet.write(0,i,Header[i])
            nrows+=1
        for i in range(len(DataList)):newsheet.write(nrows,i,DataList[i])# 在末尾增加新行
        newbook.save(self.filename)# 覆盖保存
        self.workbook = xlrd.open_workbook(self.filename, formatting_info=True)
        self.sheet = self.workbook.sheet_by_name(self.sheet_name)
    def e_read(self,num=0,type1='hang'):
        '''传入num(第几行或列)，type1（类型hang或者其他）'''
        if type1=='hang':return self.sheet.row_values(num)#获取整行数据
        else:return self.sheet.col_values(num)#获取整列数据

def dirlist(mainpath, allfilelist=[]):
    '''获取路径mainpath下的所有文件'''
    try:filelist = os.listdir(mainpath)#返回目录下的所有文件、文件名
    except:filelist=[]
    for filename in filelist:
        filepath = os.path.join(mainpath, filename)#连接文件名、文件夹名
        if os.path.isdir(filepath):dirlist(filepath, allfilelist)#如果上部合并的是文件夹，调用本函数
        else:allfilelist.append(filepath)#是文件则加入列表
    return allfilelist

import configparser#配置文件
class weiConfig:
    '''配置文件ini增删改查'''
    def __init__(self,file_path_name):
        self.file_path_name=file_path_name+'.ini'
        content = open(self.file_path_name,'rb').read()
        content=content.decode(encoding='UTF-8')
        content=re.sub('\ufeff','',content)
        open(self.file_path_name,'wb').write(bytes(content, encoding='utf-8'))
        self.config=configparser.ConfigParser()
        self.config.read(self.file_path_name,encoding='UTF-8')#读文件
    def c_read(self,Section,Key):
        '''传入项(Section)和键(Key),查询值(value)'''
        return self.config[Section][Key]
    def c_change(self,Section,dict1):
        '''传入项(Section)和字典(dict1)，进行增和修改'''
        for i in dict1:
            try:self.config.add_section(Section)
            except:pass
            self.config[Section][i]=dict1[i]
        with open(self.file_path_name,'w',encoding='UTF-8') as f:self.config.write(f)
    def c_del(self,Section,Key):
        '''传入项(Section)和键(Key)，进行删除'''
        self.config.remove_option(Section,Key) #删除一个配置项
        with open(self.file_path_name,'w',encoding='UTF-8') as f:self.config.write(f)
#配置文件如果含有换行用TAB缩进就可以。

if __name__ == "__main__":
    pass
