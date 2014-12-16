#-*-coding:utf-8 -*-
#19263195
#insert into userinfo values('12345','abc','aaa','http','use',2,2,4,datetime('now', 'localtime'))
import sys
from  BaiDu.BaiduParse import BaiDuParse,str2,Max,WriteFd
from  BaiDu.MySqlite   import MySqlite

UkMap={}
ContentMap={}
##########################  MAIN PROGRAM ###################################
if(len(sys.argv) !=2 ):
	  print "Usage Error:Input The Baid Uk Id"
	  exit(-1)
#t=BaiDuParse(sys.argv[1])
db=MySqlite(r'D:\\pycode\\temp\\BaiDuYun.db3')
#print t.GetUk_Id()
#db.InsertIntoUserInfo( [ t.GetUserInfo() ] )
#db.InsertIntoFileInfo( t.GetContent() )
#db.InsertIntoUserInfo(  t.GetFans()   )
#db.InsertIntoUserInfo(  t.GetScript()  )
#db.UpdateUserInfoStatus( t.GetUk_Id() )

sql='Update userinfo set sum_shared_file=?,sum_fans=?,sum_subscripe=? where status in (\'SubFans\',\'SubScript\') and sum_fans=-1 and uk=? '

for r in db.FetchAll('select uk,status,url from userinfo where status in (\'SubFans\',\'SubScript\') and sum_fans=-1 '):
	print r[0]
	tuple_str=BaiDuParse.GetBasicInfo( r[2],r[0] )
	#print tuple_str
	db.Update(sql,tuple_str)
	#break;
#t2=BaiDuParse.GetSoup('http://pan.baidu.com/wap/share/home?third=1&uk='+sys.argv[1])
#t.SetTotalPage(1)
#t.SetTotalSubscript(1)
#t.GetContent()
#t.GetFans()
#t.GetScript()
#print t.GetPages()
#print type(t2)