#-*-coding:utf-8 -*-
import urllib
import urllib2
import sys
import re
from   bs4 import BeautifulSoup as bs

def str2(s,c):
	return s.encode(c)

def Max(a,b):
	if a>=b:
		return a
	else:
		return b

def WriteFd(str,fd=None):
	try:
		if fd==None:
			sys.stdout.write(str+"\n")
		else:
			fd.write(std+"\n")
	except Exception,e:
		pass

class BaiDuParse:
	urlrequesthead=r'http://pan.baidu.com'
	def __init__(self,uk_id):
		self.uk=uk_id
		self.url_fans=BaiDuParse.urlrequesthead+'/wap/share/home/fans?third=1&uk='+uk_id
		self.url_content=BaiDuParse.urlrequesthead+'/wap/share/home?third=1&uk='+uk_id
		self.url_script=BaiDuParse.urlrequesthead+'/wap/share/home/followers?third=1&uk='+uk_id
		try:
			url=urllib2.urlopen(self.url_content,timeout=10)
		except Exception,e:
			print str(e)
			exit(-1)
		content=url.read()
		url.close()
		self.soup=bs(content)
		self.title=self.soup.title.string
		em=self.soup.findAll('em')
		
		self.sharenum=int(em[0].text)
		self.totalpage=self.sharenum/20+1
		
		self.subscription=int(em[1].text)
		self.totalsubscription=self.subscription/20+1
		
		self.fans=int(em[2].text)
		self.totalfans=self.fans/20+1

		if self.totalpage>=120:
			self.totalpage=119
		if self.totalfans>=120:
			self.totalfans=119
		if self.totalsubscription>=120:
			self.totalsubscription=119

	def GetPages(self):
		return self.sharenum,self.subscription,self.fans,self.totalpage,self.totalsubscription,self.totalfans
	
	def GetUserInfo(self):
		'''uk,uk_name,uk_remark,url,status,sum_shared_file,sum_fans,sum_subscript,thread_id,parent_uk,uk_type,uk_subtype'''
		#return self.uk,self.title,'NULL',self.url_content,'Processing',self.totalpage,self.totalfans,self.totalsubscription,'NULL','NULL','MAIN_ID','NULL' 
		return (self.uk,self.title.replace('\n',''),'NULL',self.url_content,'Processing',self.totalpage,self.totalfans,self.totalsubscription,'NULL','NULL','MAIN_ID','NULL')
	
	def GetUk_Id(self):
		return self.uk
	@staticmethod
	def GetSoup(url):
		try:
			url=urllib2.urlopen(url,timeout=10)
		except Exception,e:
			print str(e)

		content=url.read()
		url.close()
		soup=bs(content)
		return soup
	@staticmethod

	def GetBasicInfo(url,uk):
		#r=re.match(r'(?:.*)uk=(\d{10})',url)
		#uk=''
		#if r:
		#	uk=r.group(0)
		try:
			url=urllib2.urlopen(url,timeout=10)
		except Exception,e:
			print str(e)
			exit(-1)
		content=url.read()
		url.close()
		soup=bs(content)
		em=soup.findAll('em')
		sharenum=int(em[0].text)
		subscription=int(em[1].text)
		fans=int(em[2].text)
		return sharenum,fans,subscription,uk

	def GetContent(self):
		j=0
		increase=0
		ret_list=[]
		for idx_start in range(self.totalpage):
			increase=increase+20
			soup=BaiDuParse.GetSoup(self.url_content+"&start="+str(increase))
			ul=soup.findAll('li')
			for i in range(len(ul)):
				j=j+1
				#WriteFd(ul[i]['data-fn']+':'+':'+'=>:'+BaiDuParse.urlrequesthead+ul[i].a["href"] )
				#uk,file_name,url
				ret_list.append(  (self.uk,ul[i]['data-fn'],BaiDuParse.urlrequesthead+ul[i].a["href"] )  )
			print self.url_content+"&start="+str(increase)
		print "total : "+str(j)
		return ret_list

	def GetFans(self):
		j=0
		increase=0
		ret_list=[]
		for idx_start in range(self.totalfans):
			increase=increase+20
			soup=BaiDuParse.GetSoup(self.url_fans+"&start="+str(increase))
			#print soup.text.encode('gbk').decode('utf8')
			ul=soup.findAll('li')
		 	for i in range(len(ul)):
		 		j=j+1
		 		#print ul[i].prettify()
		 		#WriteFd(ul[i].a['data-uk']+':'+ul[i].a.h3.text+":"+ul[i].a.p.text+"=>:"+BaiDuParse.urlrequesthead+ul[i].a["href"] )
		 		# return self.uk,self.title,'NULL',self.url_content,'Processing',self.totalpage,self.totalfans,self.totalsubscription,'NULL','NULL','MAIN_ID','NULL'
		 		ret_list.append( (ul[i].a['data-uk'],ul[i].a.h3.text.replace('\n',''),ul[i].a.p.text.replace('\n',''),BaiDuParse.urlrequesthead+ul[i].a["href"],'SubFans',-1,-1,-1,'NULL',self.uk,'FANS_ID','NULL',)  )
			print self.url_fans+"&start="+str(increase)
		print "total : "+str(j)
		return ret_list

	def GetScript(self):
		j=0
		increase=0
		ret_list=[]
		for idx_start in range(self.totalsubscription):
			increase=increase+20
			soup=BaiDuParse.GetSoup(self.url_script+"&start="+str(increase))
			ul=soup.findAll('li')
			for i in range(len(ul)):
				j=j+1
				#print ul[i].prettify()
				#WriteFd(ul[i].span['data-uk']+':'+ul[i].a.h3.text+':'+ul[i].a.p.text+"=>:"+self.urlrequesthead+ul[i].a["href"] )
				ret_list.append( (ul[i].span['data-uk'],ul[i].a.h3.text.replace('\n',''),ul[i].a.p.text.replace('\n',''),BaiDuParse.urlrequesthead+ul[i].a["href"],'SubScript',-1,-1,-1,'NULL',self.uk,'SCRIPT_ID','NULL',)  )
			print self.url_script+"&start="+str(increase)
		print "total : "+str(j)
		return ret_list

	def SetTotalFans(self,value):
		self.totalfans=value
	def SetTotalPage(self,value):
		self.totalpage=value
	def SetTotalSubscript(self,value):
		self.totalsubscription=value