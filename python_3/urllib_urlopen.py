# 向有道翻译发送数据获得翻译结果
from urllib import request
from urllib import parse
import zlib
import json
'''
if __name__ == '__main__':
  req = request.Request('http://fanyi.youdao.com/')
  # 响应
  response = request.urlopen(req)
  # 所有的方法
  print(dir(response))
  # 网页
  # print(response.read())
  # 解码
  print(response.read().decode('utf-8'))
'''
headers = {
  'Accept' : '*/*',
  'Accept-Encoding' : 'gzip, deflate',
  'Accept-Language' : 'zh-CN,zh;q=0.9',
  'Connection' : 'keep-alive',
  'Content-Length' : '127',
  'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
  'Cookie' : 'BAIDUID=BC9BCEDC1E19119DF0263E8CE487A793:FG=1; BIDUPSID=BC9BCEDC1E19119DF0263E8CE487A793; PSTM=1495299092; BDUSS=S1RZjBNUXpKWURxT3gyOVI3azVUeXdVSEo4V202WWRmTS1UOFRRTmVGZXhwRWhaSVFBQUFBJCQAAAAAAAAAAAEAAABGzbJJvdbS17ra0MTS17vSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALEXIVmxFyFZS; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; MCITY=-131%3A; cflag=15%3A3; locale=zh; H_PS_PSSID=1445_21085_25438_25178_20929; PSINO=2; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1514741096,1514742349; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1514742349; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D',
  'Host' : 'fanyi.baidu.com',
  'Origin' : 'http://fanyi.baidu.com',
  'Referer' : 'http://fanyi.baidu.com/?aldtype=16047',
  'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
  'X-Requested-With' : 'XMLHttpRequest',
}

if __name__ == '__main__':
  # 请求的地址
  req_url = 'http://fanyi.baidu.com/v2transapi'
  # post请求的Form_Data参数
  Form_Data = {}
  Form_Data['from'] = 'zh'
  Form_Data['to'] = 'en'
  Form_Data['query'] = '真棒了'
  Form_Data['transtype'] = 'translang'
  Form_Data['simple_means_flag'] = '3'
  Form_Data['sign'] = '108595.346882'
  Form_Data['token'] = '83c812e44d521c8713211e0efd611bdb'
  # 转为utf-8的url参数形式传递
  data = parse.urlencode(Form_Data).encode('utf-8')
  # 构建请求
  req = request.Request(req_url, headers=headers, data=data, method='POST')
  # 发起请求并接收响应
  response = request.urlopen(req)
  html = response.read()
  # Content-Encoding:gzip -> 返回的网页为压缩版，需要解压缩
  dec = zlib.decompress(html, 16+zlib.MAX_WBITS)
  text = dec.decode('utf-8')
  # 转为JSON格式处理
  translate_results = json.loads(text)
  # print(translate_results)
  print('翻译为:' + translate_results['trans_result']['data'][0]['dst'])
