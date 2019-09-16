#!/usr/bin/env python
import sys, os, json, time

# import MySQLdb
import re

# import mysql.connector
import psycopg2


# mycursor.execute("CREATE DATABASE mydatabase")
def filterData(text):
	# return ''.join([i if ord(i) < 128 else ' ' for i in text])
	reqStr = re.sub(r'[^\x00-\x7F]+',' ', text)
	reqStr = reqStr.replace('\xe2\x94\xac\xc3\xa1', '')
	return reqStr

def conn_db():
	mydb = psycopg2.connect(database = "bank", user = "postgres", password = "toor", host = "127.0.0.1")#, port = "5432")
	print("Opened database successfully")

	mycursor = mydb.cursor()
	return mydb, mycursor

def bank_update():
	mydb, mycursor = conn_db()

	with open("/home/ec2-user/ajay_fyle/bank.csv", 'r') as fp:
		lineNo = 0
		errorCount = 0
		for eachLine in fp:
			lineNo += 1
			# print(eachLine)
			splitLine 	= eachLine.split("\t")
			# print(splitLine)
			bankName 	= splitLine[0]
			branchCode 	= splitLine[1].strip('\n')
			print(bankName, branchCode)
			# mycursor.execute(r"\c bank;")
			INSERT_Q_DB= """INSERT INTO bank_d_banks (name,bankid) VALUES ('%s', %s);"""%(bankName, branchCode )
			# print(INSERT_Q_DB)
			mycursor.execute(INSERT_Q_DB)
			
			# sys.exit()
		mydb.commit()

			

def main():
	# mydb = mysql.connector.connect(
	#   host="localhost",
	#   user="root",
	#   passwd="toor"
	# )

	# mycursor = mydb.cursor()
	# # mycursor.execute("CREATE DATABASE mydatabase")
	# # print("mycursor:", mycursor)

	mydb, mycursor = conn_db()

	with open("/home/ec2-user/ajay_fyle/bank_branches.csv", 'r') as fp:
		lineNo = 0
		errorCount = 0
		for eachLine in fp:
			lineNo += 1
			if lineNo < 2:
				continue
			# print eachLine
			try:
				splitQuote = eachLine.split('"')
				if len(splitQuote) < 2:
					continue
				splitQuote[1] = splitQuote[1].replace(',', ".")
				normanlLine = "".join(splitQuote)
				# print normanlLine
				normanlLine = normanlLine.split(',')
				# ifsc,bank_id,branch,address,city,district,state,bank_name
				INSERT_Q_DB= """INSERT INTO bank_d_branches(ifsc,bank_id,branch,address,city,district,state) VALUES ('%s', %s, '%s', '%s' ,'%s', '%s', '%s') ;"""%(
									filterData(normanlLine[0]).replace("'",""),
									filterData(normanlLine[1]).replace("'",""),
									filterData(normanlLine[2]).replace("'",""),
									filterData(normanlLine[3]).replace("'",""),
									filterData(normanlLine[4]).replace("'",""),
									filterData(normanlLine[5]).replace("'",""),
									filterData(normanlLine[6]).replace("'",""),
									# normanlLine[7],
									)
				# print("INSERT_Q_DB:", INSERT_Q_DB)
				mycursor.execute(INSERT_Q_DB)
				# time.sleep(2)
				# sys.exit()
			except Exception as e:
				errorCount += 1
				print( e)
				print (INSERT_Q_DB)
				# time.sleep(2)
				# print splitQuote, normanlLine
				# exc_type, exc_obj, exc_tb = sys.exc_info()
				# fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				# print(exc_type, fname, exc_tb.tb_lineno)
			# sys.exit()
			mydb.commit()
		print( "errorCount:",errorCount)
		print("success count:", lineNo)

if __name__ == "__main__":
	main()
	# bank_update()