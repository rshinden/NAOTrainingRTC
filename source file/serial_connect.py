#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file SerialConnect.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
import re
import serial


# Import RTM module
import RTC
import OpenRTM_aist

pattern = re.compile('\d+\,\d+\,\d+')


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
SerialConnect_spec = ["implementation_id", "SerialConnect", 
		 		       "type_name",         "SerialConnect", 
					   "description",       "ModuleDescription", 
					   "version",           "1.0.0", 
					   "vendor",            "Shinden", 
					   "category",          "Category", 
					   "activity_type",     "STATIC", 
					   "max_instance",      "1", 
					   "language",          "Python", 
					   "lang_type",         "SCRIPT",
				       "conf.default.COM", "3",

					   "conf.__widget__.COM", "text",

					   "conf.__type__.COM", "int",

		 ""]
# </rtc-template>

##
# @class SerialConnect
# @brief ModuleDescription
# 
# 
class SerialConnect(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
		self._d_pot_data = RTC.TimedString(
            RTC.Time(0, 0), [])
		self._sensorOut = OpenRTM_aist.OutPort("sensor", self._d_pot_data)

		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		self._COM_num = [3]
		self._serialcon = serial.Serial()
		self._serialcon.baudrate = 9600
		
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
		self.bindParameter("COM", self._COM_num, "3")		
		# Set InPort buffers
		
		# Set OutPort buffers
		self._sensor_dataOut = RTC.TimedString(RTC.Time(0,0),0)
		self._outport = OpenRTM_aist.OutPort("sensor_data", self._sensor_dataOut)

		self.addOutPort("sensor",self._sensorOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
		##
		# 
		# The finalize action (on ALIVE->END transition)
		# formaer rtc_exiting_entry()
		# 
		# @return RTC::ReturnCode_t
	
		# 
	def onFinalize(self):
		print("fin")
		self._serialcon.close()
		return RTC.RTC_OK
	
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
		print("activate SrialConnect")
		self._serialcon.port = "COM" + str(self._COM_num[0])
		print("connecting: "+str(self._serialcon.port))
		self._serialcon.open()

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
		print("deactivate Serial Connect")
		self._serialcon.close()	
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
		#シリアル通信データ
		i = 0
		list_data = []
		num_data = []
		list_data = [0, 0, 0]
		num_data = [0.0, 0.0, 0.0]
		time_data = [0.0]
		#時間取得

		line = self._serialcon.readline()
		#linenew = [time, line]
		print(line)
		#データ送信
		self._d_pot_data.data = line
		print(self._d_pot_data)
		self._sensorOut.write()
		#時間出力
	
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
	
		##
		#
		# The error action in ERROR state
		# former rtc_error_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onError(self, ec_id):
		print("error")
		self._serialcon.close()
		return RTC.RTC_OK
	
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
	



def SerialConnectInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=SerialConnect_spec)
    manager.registerFactory(profile,
                            SerialConnect,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    SerialConnectInit(manager)

    # Create a component
    comp = manager.createComponent("SerialConnect")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

