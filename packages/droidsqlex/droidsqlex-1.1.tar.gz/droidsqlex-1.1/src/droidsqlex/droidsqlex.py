import pickle
import random
import os
import copy



def listToCsv(database):
	if not isinstance(database,list):
		raise TypeError('type must be list')
	string=''
	current_row=0
	for row in database:
		rowLen=len(row)
		current_col=0
		for col in row:
			string+=str(col)
			if current_col+1==rowLen:
				if current_row+1!=len(database):
					string+='\n'
			else:
				string+=','
			current_col+=1
		current_row+=1
	return string
		
				

def dictToCsv(dic):
	if not isinstance(dic,dict):
		raise TypeError('type must be dict')
	#判断每项元素数量是否相同
	last_length=''
	for row in dic.values():
		if isinstance(row,str):
			raise TypeError('value must be list')
		if last_length=='':
			last_length=len(row)
			continue
		else:
			if len(row)!=last_length:
				raise ValueError('arrays must be the same length')
	string=''
	#设置列名
	current_col=0
	current_row=0
	for key in dic:
		string+=str(key)
		if current_row+1==len(dic):
			string+='\n'
		else:
			string+=','
		current_row+=1
	#添加元素(按列)
	current_row=0
	for _ in range(0,len(dic[key])):
		for values in dic.values():
			string+=str(values[current_col])
			if current_row+1==len(dic):
				if current_col+1!=len(dic[key]):
					string+='\n'
			else:
				string+=','
			current_row+=1
		current_row=0
		current_col+=1
	return string



class NewSeesion:
	
	
	
	def __init__(self):
		self.database=[]
		self.path=''
		
		
		
	def access(self,path,autoComplete=True):
		if autoComplete:
			path='/sdcard/'+path
		with open(path,'rb') as file:
			database=pickle.load(file)
		self.database=database
		self.path=path
		return database
		
		
		
	def openCsv(self,path,autoComplete=True):
		if autoComplete:
			path='/sdcard/'+path
		with open(path,'r')as f:
			file=f.readlines()
		database=[]
		for line in file:
			line=line.replace('\n','')
			database1=line.split(',')
			database.append(database1)
		self.database=database
		self.path=path
		return database
		
		
		
	def openKv(self,path,autoComplete=True):
		if autoComplete:
			if '/sdcard/'not in path or '/storage/emulated/0/' not in path:
				path='/sdcard/'+path
			if '.kv' not in path:
				path+='.kv'
		with open(path,'r')as f:
			text=f.read()
		kvList0=text.split(';')
		kvList1=[]
		for dic in kvList0:
			kvList=dic.split(':')
			kvList1.append(kvList)
		kv={}
		for _kv in kvList1:
			kv[_kv[0]]=_kv[1]
		return kv
		
		
		
	def saveList(self,path='',autoComplete=True):
		if path=='':
			path=self.path
		else:
			if autoComplete:
				path='/sdcard/'+path
		with open(path,'wb')as f:
			pickle.dump(self.database,f)
			
			
			
	def saveCsv(self,path,database='',autoComplete=True):
		if autoComplete:
			if '/storage/emulated/0/' not in path or '/sdcard/' not in path:
				path='/sdcard/'+path
			if '.csv' not in path:
				path+='.csv'
		if database=='':
			database=self.database
		if isinstance(database,list):
			csv=listToCsv(database)
		elif isinstance(database,dict):
			csv=dictToCsv(database)
		else:
			raise TypeError('type must be list or dict')
		with open(path,'w')as f:
			f.write(csv)
			
			
	
	def show(self,database=''):
		if database=='':
			database=self.database
		for row in database:
			rowLen=len(row)
			currentCol=0
			for col in row:
				if col=='':
					print(' ',end='')
				else:
					print(col,end='')
				if currentCol+1==rowLen:
					print('')
				else:
					print('  ',end='')
				currentCol+=1
				
				
	
	def despiteIndex(self,replace=False):
		database=copy.deepcopy(self.database)
		database.pop(0)
		database0=[]
		for row in database:
			row.pop(0)
			database0.append(row)
		if replace:
			self.database=database0
		return database0
		
		
		
	def get(self):
		return self.database
	
	
	
	def data(self,pos,database='',specifiedType=''):
		if database=='':
			database=self.database
		if isinstance(pos[0],str) or isinstance(pos[1],str) or specifiedType=='name':
			pos=(str(pos[0]),str(pos[1]))
			results=[]
			current_row=0
			current_col=0
			for row in database:
				if row[0]==pos[0]:
					for col in self.database[0]:
						if col==pos[1]:
							results.append(database[current_row][current_col])
						current_col+=1
				current_row+=1
			if len(results)==0:
				return 'No findings'
			elif len(results)==1:
				return results[0]
			else:
				return results
		elif isinstance(pos[0],int) and isinstance(pos[1],int) or specifiedType=='coordinate':
			return database[pos[0]][pos[1]]
			
			
			
	def locateData(self,givenData,database='',intToStr=True):
		if database=='':
			database=self.database
		if isinstance(givenData,int) and intToStr:
			givenData=str(givenData)
		results=[]
		currentRow=0
		for row in database:
			currentCol=0
			if givenData in row:
				for col in row:
					if col==givenData:
						results.append((currentRow,currentCol))
					currentCol+=1
			currentRow+=1
		return results
		
		
		
	def getLine(self,lineName,database='',mode='col'):
		if database=='':
			database=copy.deepcopy(self.database)
		if not isinstance(database,list):
			raise TypeError('database type must be list')
		results=[]
		if mode=='col':
			targetCols=[]
			currentCol=0
			for title in database[0]:
				if title==lineName:
					targetCols.append(currentCol)
				currentCol+=1
			for targetCol in targetCols:
				datas=[]
				currentRow=0
				for row in database:
					if currentRow==0:
						currentRow+=1
						continue
					datas.append(row[targetCol])
					currentRow+=1
				results.append(datas)
		elif mode=='row':
			results=[]
			currentRow=0
			for row in database:
				if row[0]==lineName:
					database[currentRow].pop(0)
					results.append(database[currentRow])
				currentRow+=1
		if len(results)==1:
			results=results[0]
		return results