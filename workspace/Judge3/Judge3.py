#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file Judge3.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
import re
import math
import datetime
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
judge3_spec = ["implementation_id", "Judge3", 
		 "type_name",         "Judge3", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "Shinden", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.threshold", "3",
		 "conf.default.addvalue", "10",

		 "conf.__widget__.threshold", "text",
		 "conf.__widget__.addvalue", "text",

         "conf.__type__.threshold", "int"
		 "conf.__type__.addvalue", "int",

		 ""]
# </rtc-template>

##
# @class Judge3
# @brief ModuleDescription
# 
# 
class Judge3(OpenRTM_aist.DataFlowComponentBase):
	
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
		data_arg = [None] * ((len(RTC._d_TimedFloatSeq) - 4) / 2)
		self._d_data = RTC.TimedFloatSeq(RTC.Time(0,0), [])
		"""
		"""
		self._dataIn = OpenRTM_aist.InPort("data", self._d_data)
		result_arg = [None] * ((len(RTC._d_TimedLong) - 4) / 2)
		self._d_result = RTC.TimedLong(RTC.Time(0,0), 0)
		"""
		"""
		self._resultOut = OpenRTM_aist.OutPort("result", self._d_result)
		balance_arg = [None] * ((len(RTC._d_TimedLong) - 4) / 2)
		self._d_balance = RTC.TimedLong(RTC.Time(0,0), 0)
		"""
		"""
		self._balanceOut = OpenRTM_aist.OutPort("balance", self._d_balance)


		self._switch = "off"

		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  threshold
		 - DefaultValue: 12
		"""
		self._threshold = [3]
		"""
		
		 - Name:  addvalue
		 - DefaultValue: 10
		"""
		self._addvalue = [10]
		
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
		self.bindParameter("threshold", self._threshold, "12")
		self.bindParameter("addvalue", self._addvalue, "10")
		
		# Set InPort buffers
		self.addInPort("sign",self._signIn)
		self.addInPort("data",self._dataIn)
		
		# Set OutPort buffers
		self.addOutPort("result",self._resultOut)
		self.addOutPort("balance",self._balanceOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	


	def onActivated(self, ec_id):
		print("Activate Judge3")
		return RTC.RTC_OK
	

	def onDeactivated(self, ec_id):
		print("Deactivate Judge3")
		return RTC.RTC_OK
	

	def onExecute(self, ec_id):
		if self._signIn.isNew():
			self._d_sign = self._signIn.read()
			sign = self._d_sign.data
			print(sign)
			#スイッチON
			if sign == "kaishi":
				self._switch = "on"
				print("on")
		#センサ値の読み込み開始
		if self._switch == "on":
			self._d_data = self._dataIn.read()
			data = self._d_data.data
			i = 0
			sensor_dic = {}
			for i in range (1,15,1):
				sensor_dic.setdefault(("sensor" + str(i)), data[i-1])
			#センサ値による立ち上がり判定
			if (sensor_dic["sensor3"] > int(self._threshold[0]) and sensor_dic["sensor10"] > int(self._threshold[0])) :
				self._d_result.data = 1
				print("Sending: ", self._d_result.data)
				self._resultOut.write()
			else:
				self._d_result.data = 0
				print("Sending: ", self._d_result.data)
				self._resultOut.write()
			#足底センサ左右の差
			self._sensor_left_front =  sensor_dic['sensor1'] + sensor_dic['sensor2'] + sensor_dic['sensor3'] +sensor_dic['sensor4'] + sensor_dic['sensor5']			
			self._sensor_right_front =  sensor_dic['sensor8'] + sensor_dic['sensor9'] + sensor_dic['sensor10'] +sensor_dic['sensor11'] + sensor_dic['sensor12']
			#左右のバランス判定
			if self._sensor_left_front >= (self._sensor_right_front + int(self._addvalue[0])):
				self._d_balance.data = 2
				self._balanceOut.write()
			elif self._sensor_right_front >= (self._sensor_left_front + int(self._addvalue[0])):
				self._d_balance.data = 3
				self._balanceOut.write()
		return RTC.RTC_OK
	



def Judge3Init(manager):
    profile = OpenRTM_aist.Properties(defaults_str=judge3_spec)
    manager.registerFactory(profile,
                            Judge3,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    Judge3Init(manager)

    # Create a component
    comp = manager.createComponent("Judge3")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

