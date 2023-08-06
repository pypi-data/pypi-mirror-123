"""
编程api通用请求模块
"""
import requests
from xes import common, uploader

"""
通用请求接口
参数:
  api - string，接口地址
  params - dictionary，参数字典
返回值:
  结果字典
"""
def request(api, params):
    cookies = common.getCookies()
    headers = {"Cookie": cookies}
    rep = requests.get(api, params=params, headers=headers)
    repDic = common.jsonLoads(rep.text)
    return repDic

"""
文件上传
参数:
  fileName - string，文件名，例如"abc.png"
返回值:
  结果字典
"""
def upload(fileName):
    return uploader.XesUploader().upload(fileName)