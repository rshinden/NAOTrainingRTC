#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file CsvWrite.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
import re
import csv
import datetime
import time
import math
pattern = re.compile('\d+\,\d+\,\d+')
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
CsvWrite_spec = ["implementation_id", "CsvWrite", 
		 "type_name",         "CsvWrite", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "shinden", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class CsvWrite
# @brief ModuleDescription
# 
# 
class CsvWrite(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		sign_arg = [None] * ((len(RTC._d_TimedString) - 4) / 2)
		self._d_sign = RTC.TimedString(RTC.Time(0,0), "")
		"""
		"""
		self._signIn = OpenRTM_aist.InPort("sign", self._d_sign)
		sensor_arg = [None] * ((len(RTC._d_TimedFloatSeq) - 4) / 2)
		self._d_sensor = RTC.TimedFloatSeq(RTC.Time(0,0), [])
		"""
		"""
		self._sensorIn = OpenRTM_aist.InPort("sensor", self._d_sensor)
		fin_arg = [None] * ((len(RTC._d_TimedString) - 4) / 2)
		self._d_fin = RTC.TimedString(RTC.Time(0,0), "")
		"""
		"""
		self._finIn = OpenRTM_aist.InPort("fin", self._d_fin)


		self._switch = "on"
		self._first = "true"
		self._fin = []
		self._start = 0
		self._nexttime = 0
		self._today = datetime.date.today()
		self._today_str = str(self._today)
		self._t = 0


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		
		# Set InPort buffers
		self.addInPort("sign",self._signIn)
		self.addInPort("sensor",self._sensorIn)
		self.addInPort("fin",self._finIn)
		
		# Set OutPort buffers
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 

	def onActivated(self, ec_id):
		print("activate CSVWrite")
		return RTC.RTC_OK
	
		##
		#
		# The deactivated action (Active state exit action)
		# former rtc_active_exit()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onDeactivated(self, ec_id):
		print("deactivate CsvWrite")
	
		return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):
		#センサ値の取得
		self._d_sensor = self._sensorIn.read()
		line = self._d_sensor.data
		FSR_dic = {}
		i = 0
		#辞書に入れる
		for i in range (1,15,1):
			FSR_dic.setdefault(("FSR" + str(i)), line[i-1])
		#開始の合図取得
		if self._signIn.isNew():
			self._d_sign = self._signIn.read()
			sign = self._d_sign.data
			if sign == "kaishi":
				self._switch = "on"
				print("GO")
		#csvファイルの作成、ヘッダー作成
		if self._switch == "on":
			print("switch is on")
			if self._first == "true":
				self._start = time.time()
				self._nexttime = time.time() - self._start
				with open ("./data/" + self._today_str + ".csv", "w") as f:
					writer = csv.writer(f, lineterminator = '\n')
					writer.writerow(["time","No,1","No,2","No,3","No,4","No,5","No,6","No,7","No,8","No,9","No,10","No,11","No,12","No,13","No,14"])
					print("csv open")
					self._first = "false"
					self._nexttime +=0.1
			self._t =time.time() - self._start 
			if (self._t >= self._nexttime and self._first == "false"):
				#print(">>>>>>")
				#書き込み
				with open ("./data/" + self._today_str + ".csv", "a") as f:
					print("csv_write")
					print(self._t)
					writer = csv.writer(f, lineterminator='\n')
					writer.writerow([self._t,FSR_dic["FSR1" ], FSR_dic["FSR2" ], FSR_dic["FSR3" ], FSR_dic["FSR4" ], FSR_dic["FSR5" ], FSR_dic["FSR6" ], FSR_dic["FSR7" ], FSR_dic["FSR8" ], FSR_dic["FSR9" ], FSR_dic["FSR10" ], FSR_dic["FSR11" ], FSR_dic["FSR12" ], FSR_dic["FSR13" ], FSR_dic["FSR14" ]])
					self._nexttime +=0.1
			#終了合図の読み込み
			if self._finIn.isNew():
				self._d_fin = self._finIn.read()
				self._fin = self._d_fin.data
				print("receive: ", self._fin)
				if self._fin == "fin":
					with open ("./data/" + self._today_str + ".csv", "a") as f:
						#print("csv_write")
						writer = csv.writer(f, lineterminator='\n')
						writer.writerow([self._t,FSR_dic["FSR1" ], FSR_dic["FSR2" ], FSR_dic["FSR3" ], FSR_dic["FSR4" ], FSR_dic["FSR5" ], FSR_dic["FSR6" ], FSR_dic["FSR7" ], FSR_dic["FSR8" ], FSR_dic["FSR9" ], FSR_dic["FSR10" ], FSR_dic["FSR11" ], FSR_dic["FSR12" ], FSR_dic["FSR13" ], FSR_dic["FSR14" ]])
						f.close() 
						self._first = "end"
						print("close csv")
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def CsvWriteInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=CsvWrite_spec)
    manager.registerFactory(profile,
                            CsvWrite,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    CsvWriteInit(manager)

    # Create a component
    comp = manager.createComponent("CsvWrite")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

