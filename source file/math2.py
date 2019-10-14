#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file Math.py
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


global today
today = datetime.date.today()


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
Math_spec = ["implementation_id", "Math", 
		 "type_name",         "Math", 
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
# @class Math
# @brief ModuleDescription
# 
# 
class Math(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		sign_arg = [None] * ((len(RTC._d_TimedString) - 4) / 2)
		self._d_sign = RTC.TimedString(*sign_arg)
		"""
		"""
		self._signIn = OpenRTM_aist.InPort("sign", self._d_sign)
		fin_arg = [None] * ((len(RTC._d_TimedString) - 4) / 2)
		self._d_fin = RTC.TimedString(RTC.Time(0,0), "")
		"""
		"""
		self._finIn = OpenRTM_aist.InPort("fin", self._d_fin)
		time_arg = [None] * ((len(RTC._d_TimedDouble) - 4) / 2)
		#self._d_time = RTC.TimedDouble(*time_arg)
		self._d_time = RTC.TimedDouble(RTC.Time(0, 0), 0.0)
		"""
		"""
		self._timeOut = OpenRTM_aist.OutPort("time", self._d_time)


		


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
		self.addInPort("fin",self._finIn)
		#self._timeOut = RTC.TimedDouble(RTC.Time(0,0),0.0)
		#self._outport = OpenRTM_aist.OutPort("time", self._timeOut)
		# Set OutPort buffers
		self.addOutPort("time",self._timeOut)
		
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
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		# 
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):
		print("activate Math")
		global switch
		global today
		global go 
		global today_str
		today_str = str(today)
		switch = "off"
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
		print("deactivate Math")
	
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
		global go
		if self._finIn.isNew():
			self._d_fin = self._finIn.read()
			fin = self._d_fin.data
			print("receve", fin)
			if fin == "fin":
				global today_str
				with open("C:/workspaces/CsvWrite/data/"+ today_str + ".csv", "r")as f:
				#with open("log" + today + ".csv", "r") as f:
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
				#self._timeOut.data = wow
				print(self._d_time.data)
				#self._outport.write()
				print(self._timeOut)
				fin = "end"
				go = "fin"
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
	



def MathInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=Math_spec)
    manager.registerFactory(profile,
                            Math,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    MathInit(manager)

    # Create a component
    comp = manager.createComponent("Math")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

