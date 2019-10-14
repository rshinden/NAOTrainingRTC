#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file StandUp.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
import argparse
from naoqi import ALProxy
from time import sleep
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
StandUp_spec = ["implementation_id", "StandUp", 
		 "type_name",         "StandUp", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "shinden", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.NAO_IPaddress", "169.254.14.64",
		 "conf.default.NAO_Port", "9559",

		 "conf.__widget__.NAO_IPaddress", "text",
		 "conf.__widget__.NAO_Port", "text",

         "conf.__type__.NAO_IPaddress", "string",
         "conf.__type__.NAO_Port", "int",

		 ""]
# </rtc-template>

##
# @class StandUp
# @brief ModuleDescription
# 
# 
class StandUp(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		judge_arg = [None] * ((len(RTC._d_TimedLong) - 4) / 2)
		self._d_judge = RTC.TimedLong(*judge_arg)
		"""
		"""
		self._judgeIn = OpenRTM_aist.InPort("judge", self._d_judge)
		count_arg = [None] * ((len(RTC._d_TimedString) - 4) / 2)
		self._d_count = RTC.TimedLong(*count_arg)
		"""
		"""
		self._countIn = OpenRTM_aist.InPort("count", self._d_count)
		fin_arg = [None] * ((len(RTC._d_TimedLong) - 4) / 2)
		self._d_fin = RTC.TimedString(RTC.Time(0,0), "")
		"""
		"""
		self._finOut = OpenRTM_aist.OutPort("fin", self._d_fin)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  NAO_IPaddress
		 - DefaultValue: 169.254.14.64
		"""
		self._NAO_IPaddress = ['169.254.14.64']
		"""
		
		 - Name:  NAO_Port
		 - DefaultValue: 9559
		"""
		self._NAO_Port = [9559]
		
		
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
		self.bindParameter("NAO_IPaddress", self._NAO_IPaddress, "169.254.14.64")
		self.bindParameter("NAO_Port", self._NAO_Port, "9559")
		
		# Set InPort buffers
		self.addInPort("judge",self._judgeIn)
		self.addInPort("count",self._countIn)
		
		# Set OutPort buffers
		self.addOutPort("fin",self._finOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports

		#global
		global count
		global start

		count = 1
		start = "true"

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
		print("activate standUp")
		global start
		NAO_activate(self._NAO_IPaddress[0], self._NAO_Port[0])
	
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
		print("deactivate StandUp")
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
		global count
		global start
		#print("start")
		if self._countIn.isNew():
			self._d_count.data = self._countIn.read()
			count_number = self._d_count.data
			print("recieve;" ,count_number)
			#while count <= count_number.data:
		while count < 5:
			print(count)
			print(start)

			if start == "true":
				data = self._judgeIn.read()

				if data.data == 1:
					if count == 4:
						start = "false"
					else:
						print(data,"standing")
						NAO_cheer(self._NAO_IPaddress[0], self._NAO_Port[0])
						start = "false"
				elif data.data == 0:
					print("sitting")
				elif data.data == 2:
					NAO_left(self._NAO_IPaddress[0], self._NAO_Port[0])
					start = "false"
				elif data.data == 3:
					NAO_right(self._NAO_IPaddress[0], self._NAO_Port[0])
					start = "false"


			if start == "false":
				data = self._judgeIn.read()

				if data.data ==0 :
					if count == 4:
						print(start)
						count += 1
					else:
						NAO_stand(self._NAO_IPaddress[0], self._NAO_Port[0])
						start = "true"
						print(data,"sitting")
						count += 1
				if data.data == 1:
					print("standing")

			if count == 5:
				NAO_end(self._NAO_IPaddress[0], self._NAO_Port[0])
				print("end")
				count += 1
				end = "fin"
				self._d_fin.data = end
				self._finOut.write()
				print(self._d_fin.data)

	
	
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
	



def StandUpInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=StandUp_spec)
    manager.registerFactory(profile,
                            StandUp,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    StandUpInit(manager)

    # Create a component
    comp = manager.createComponent("StandUp")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()
	
def NAO_activate(robotIP, PORT):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
	speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
	motionProxy.wakeup
	speechProxy.say("今日も頑張ろう")
	postureProxy.goToPosture("StandInit", 0.5)
	#motionProxy.wakeup
	speechProxy.say("ぼくの動きのまねをしてね")
	

def NAO_end(robotIP, PORT):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	#postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
	speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
	motionProxy.rest()
	#motionProxy.wakeup()
	speechProxy.say("今日のトレーニングは、終了です。お疲れさまでした")
	print("FINISH")

def NAO_stand(robotIP, PORT):

	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
	speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
	postureProxy.goToPosture("StandInit", 0.5)
	#motionProxy.wakeup
	speechProxy.say("ぼくみたいに立ってみよう")
	print("stand up")

def NAO_cheer(robotIP, PORT):

	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
	speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
	motionProxy.wakeUp()
	speechProxy.say("上手に立てたね")
	speechProxy.say("もう一回頑張ろう")
	#postureProxy = ALProxy("ALRobotPosture", "localhost", 9559)
	#postureProxy.goToPosture("StandZero", 1.0)

	#motionProxy.setAngles("HeadYaw", -90.0*(2*math.pi/360.0), 1.0)
	#time.sleep(1.0)
	#motionProxy.setAngles("HeadYaw", 90.0*(2*math.pi/360.0), 1.0)
	#time.sleep(1.0)
	#motionProxy.setAngles("HeadYaw", 0, 1.0)
	#time.sleep(1.0)
	motionProxy.rest()

def NAO_left(robotIP, PORT):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	#postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
	speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
	#motionProxy.wakeup()
	speechProxy.say("重心が左にかたよっています")
	motionProxy.setAngles(["RShoulderPitch", "RShoulderRoll"], [0.0, 1.0], 0.1)
	print("left")
	motionProxy.rest()

def NAO_right(robotIP, PORT):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	#postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
	speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
	#motionProxy.wakeup()
	speechProxy.say("重心が右にかたよっています")
	motionProxy.setAngles(["LShoulderPitch", "LShoulderRoll"], [0.0, 1.0], 0.1)
	print("right")
	motionProxy.rest()

if __name__ == "__main__":
	main()

