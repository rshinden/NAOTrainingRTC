#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file Change.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
import re
import math
import datetime
import time
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
change_spec = ["implementation_id", "Change", 
		 "type_name",         "Change", 
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
# @class Change
# @brief ModuleDescription
# 
# 
class Change(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		rawdata_arg = [None] * ((len(RTC._d_TimedString) - 4) / 2)
		self._d_rawdata = RTC.TimedString(RTC.Time(0,0), "")
		"""
		"""
		self._rawdataIn = OpenRTM_aist.InPort("rawdata", self._d_rawdata)
		data_arg = [None] * ((len(RTC._d_TimedFloatSeq) - 4) / 2)
		self._d_data = RTC.TimedFloatSeq(RTC.Time(0,0), [])
		"""
		"""
		self._dataOut = OpenRTM_aist.OutPort("data", self._d_data)


		


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
		self.addInPort("rawdata",self._rawdataIn)
		
		# Set OutPort buffers
		self.addOutPort("data",self._dataOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	

	def onActivated(self, ec_id):
		print("Activate Change")
	
		return RTC.RTC_OK
	
	def onDeactivated(self, ec_id):
		print("Deactivate Change")
		return RTC.RTC_OK
	

	def onExecute(self, ec_id):
		#アナログ値の読み取り
		if self._rawdataIn.isNew():
			self._d_rawdata = self._rawdataIn.read()
			line = self._d_rawdata.data
			line_str = str(line)
			rawdata = re.split("[,']", line_str)
			FSR_dic = {}
			FSR_value = []
			i = 0
			#名前
			for i in range (1,15,1):
				FSR_dic.setdefault(("FSR" + str(i)), float(rawdata[i-1]))
			#Nに変換
			for i in range (1,15,1):
				if FSR_dic["FSR" + str(i)] == 0:
					FSR_dic["FSR" + str(i)] = 0
				elif (1 <= FSR_dic["FSR" + str(i)]) and (FSR_dic["FSR" + str(i)] < 990):
					FSR_dic["FSR" + str(i)] = 0.069*math.exp(0.0044*FSR_dic["FSR" + str(i)])*9.8 
				elif( 990 <= FSR_dic["FSR" + str(i)]) and (FSR_dic["FSR" + str(i)] <= 1024): 
					FSR_dic["FSR" + str(i)] = 3E-06*math.exp(0.0145*FSR_dic["FSR" + str(i)])*9.8
			FSR_value = [ FSR_dic['FSR1'] , FSR_dic['FSR2'] ,FSR_dic['FSR3'] , FSR_dic['FSR4'] ,FSR_dic['FSR5'], FSR_dic['FSR6'] ,FSR_dic['FSR7'] , FSR_dic['FSR8'] ,FSR_dic['FSR9'], FSR_dic['FSR10'] ,FSR_dic['FSR11'] , FSR_dic['FSR12'] ,FSR_dic['FSR13'], FSR_dic['FSR14']]
			self._d_data.data = FSR_value
			self._dataOut.write()
				
		return RTC.RTC_OK

def ChangeInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=change_spec)
    manager.registerFactory(profile,
                            Change,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    ChangeInit(manager)

    # Create a component
    comp = manager.createComponent("Change")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

