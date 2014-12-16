#-*-coding:utf-8-*-             
import sqlite3
class MySqlite:
	def __init__(self,db_name):
		self.db_name=db_name
		self.conn=sqlite3.connect(db_name)
		#self.conn.isolation_level = None
		self.cx=self.conn.cursor()

	def InsertIntoUserInfo(self,list_tuple):
			for t_str in list_tuple:
				self.cx.execute('insert into UserInfo(UK,UK_NAME,UK_REMARK,URL,STATUS,SUM_SHARED_FILE,SUM_FANS,SUM_SUBSCRIPE,THREAD_ID,PARENT_UK,UK_TYPE,UK_SUBTYPE) values(?,?,?,?,?,?,?,?,?,?,?,?)',t_str)
			self.conn.commit()
	
	def InsertIntoFileInfo(self,list_tuple):
		for t_str in list_tuple:
			self.cx.execute('insert into FileInfo(UK,FILE_NAME,URL) values(?,?,?)',t_str)
		self.conn.commit()

	def UpdateUserInfoStatus(self,uk_id):
		self.cx.execute('update UserInfo set status=\'Complete\' where status=\'Processing\' and UK=? ',(uk_id,) )
		self.conn.commit()
	def FetchAll(self,sql):
		cursor=self.cx.execute(sql)
		return cursor.fetchall()

	def GetCursor(self):
		return self.cx
	def Update(self,sql,tuple_str):
		self.cx.execute(sql,tuple_str)
		self.conn.commit()
