#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file Calc.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
import csv
import datetime
import time
import re
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
calc_spec = ["implementation_id", "Calc", 
		 "type_name",         "Calc", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "Shinden", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class Calc
# @brief ModuleDescription
# 
# 
class Calc(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_fin = RTC.TimedString(RTC.Time(0,0),"")
		"""
		"""
		self._finIn = OpenRTM_aist.InPort("fin", self._d_fin)
		
		self._d_time = RTC.TimedDouble(RTC.Time(0,0),0.0)
		"""
		"""
		self._timeOut = OpenRTM_aist.OutPort("time", self._d_time)


		self._fin = "fin"#"null"




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
		self.addInPort("fin",self._finIn)
		
		# Set OutPort buffers
		self.addOutPort("time",self._timeOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	

	def onActivated(self, ec_id):
		print("activate Calc")
		return RTC.RTC_OK

	def onDeactivated(self, ec_id):
		print("deactivate Calc")
		return RTC.RTC_OK

	def onExecute(self, ec_id):
		today = datetime.date.today()
		today_str = str(today)
		#終了合図の読み込み
		if self._finIn.isNew():
			self._d_fin = self._finIn.read()
			self._fin = self._d_fin.data
			print("receive", self._fin)
			#時間の呼び出し
		if self._fin == "fin":
			with open("../CsvWrite/data/"+ today_str + ".csv", "r")as f:
				rows = f.readlines()
				print(rows[-1])#最終行
				print(rows[1])#2列目
				rows1_str = str(rows[1])#変換
				rows2_str = str(rows[-1])	
				high = re.split("[,']", rows1_str)#カンマ区切り
				hight = re.split("[,']", rows2_str)
				high1 = float(high[0])#timeの取り出し
				high2 = float(hight[0])
				end = round(high2)#小数点切り
				start = round(high1)
				wow  = (end - start)
				print("time is :", wow)
				self._d_time.data = wow
				f.close()
			self._timeOut.write()
			print(self._d_time.data)
			print(self._timeOut)
			self._fin = "end"

		return RTC.RTC_OK
	
def CalcInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=calc_spec)
    manager.registerFactory(profile,
                            Calc,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    CalcInit(manager)

    # Create a component
    comp = manager.createComponent("Calc")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

