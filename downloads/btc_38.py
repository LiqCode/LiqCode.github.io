#! /usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import time

headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36" }
    
url = {
	'day':'http://www.btc38.com/trade/getTradeDayLine.php?mk_type=CNY&coinname=',
	'hour':'http://www.btc38.com/trade/getTradeTimeLine.php?mk_type=CNY&coinname=',
	'min_5':'http://www.btc38.com/trade/getTrade5minLine.php?mk_type=CNY&coinname=',
	'trades':'http://api.btc38.com/v1/ticker.php?mk_type=cny&c=',	#返回最新报价
	'depth':'http://api.btc38.com/v1/depth.php?mk_type=cny&c=',		#返回当前市场深度（委托挂单），其中 asks 是委卖单, bids 是委买单。返回30条。
	'history':'http://api.btc38.com/v1/trades.php?mk_type=cny&c=',	#返回系统支持的历史成交记录，默认返回最新30条。tid=100 指定返回条数 最多500条

}

coins = ['ppc','bts','zcc','xem','dash','tag','btc','ric','xpm','doge','hlb','blk','xrp','mgc','dgc','vash','mec','src','bost','eac','ncs','xzc','nxt','xlm','emc','bec','ltc','ybc']
coins_obj = {'ddb':'ppc','btg':'bts','zcb':'zcc','xjb':'xem','dsb':'dash','jsb':'tag','btb':'btc','lmb':'ric','zsb':'xpm','ggb':'doge','hlb':'hlb','hb':'blk','rbb':'xrp','zhb':'mgc','smb':'dgc','wb':'vash','mkb':'mec','aqb':'src','zcb':'bost','dqb':'eac','zcg':'ncs','lb':'xzc','wlb':'nxt','hxb':'xlm','jqb':'emc','bab':'bec','ltb':'ltc','ybb':'ybc'}

care = ['dz','lmb','zcb']

def get_data(type='min_5',c='btc'):
	html = requests.get(url[type]+c, headers=headers).text
	return json.loads(html)

def all_trades():
	data = get_data(type='trades',c='all')
	for x in data.keys():
		print x,data[x]['ticker']

def depth_ana(c='hlb'):
	data = get_data(type='depth',c=c)
	for x in data['asks'][::-1]:
		print x[0],'\t',round(x[0]*x[1])
	print ''
	for x in data['bids']:
		print x[0],'\t',round(x[0]*x[1])
	print '卖单资金：',sum(x[0]*x[1] for x in data['asks'])
	print '买单资金：',sum(x[0]*x[1] for x in data['bids'])

def main():
	# all_trades()
	# for x in care:
#	while True:
    depth_ana(c='ncs')
    time.sleep(1)
	# data = get_data(type='history', c='hlb')
	# for x in data:
	# 	print 'date:',time.strftime('%Y-%m-%d %H:%M',time.localtime(x['date'])),' price:',x['price'],'\t',x['type'],'\tamount:',x['price']*x['amount']

if __name__ == '__main__':
	main()
