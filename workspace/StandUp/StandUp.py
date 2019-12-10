#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file StandUp.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import math
import argparse
import datetime
import re
from naoqi import ALProxy
from time import sleep
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
		 "conf.default.NAO_IPaddress", "127.0.0.1",
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
		self._d_judge = RTC.TimedLong(RTC.Time(0,0), 0)
		"""
		"""
		self._judgeIn = OpenRTM_aist.InPort("judge", self._d_judge)	
		balance_arg = [None] * ((len(RTC._d_TimedLong) - 4) / 2)
		self._d_balance = RTC.TimedLong(RTC.Time(0,0), 0)
		"""
		"""
		self._balanceIn = OpenRTM_aist.InPort("balance", self._d_balance)		
		count_arg = [None] * ((len(RTC._d_TimedLong) - 4) / 2)
		self._d_count = RTC.TimedLong(RTC.Time(0,0), 0)
		"""
		"""
		self._countIn = OpenRTM_aist.InPort("count", self._d_count)	
		fin_arg = [None] * ((len(RTC._d_TimedString) - 4) / 2)
		self._d_fin = RTC.TimedString(RTC.Time(0,0), "")
		"""
		"""
		self._finOut = OpenRTM_aist.OutPort("fin", self._d_fin)

		self._count = 0
		self._start = "yet"
		self._starttime = 0
		self._endtime = 5
		self._time = 5
		self._count_number = 0
		self._data = 3
		self._FSR_left_front = 0
		self._FSR_right_front = 0
		self._balance = 0
		standtime = self._endtime - self._starttime



		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  NAO_IPaddress
		 - DefaultValue: 127.0.0.1
		"""
		self._NAO_IPaddress = ['127.0.0.1']
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
		self.bindParameter("NAO_IPaddress", self._NAO_IPaddress, "127.0.0.1")
		self.bindParameter("NAO_Port", self._NAO_Port, "9559")
		
		# Set InPort buffers
		self.addInPort("judge",self._judgeIn)
		self.addInPort("balance",self._balanceIn)
		self.addInPort("count",self._countIn)
		
		# Set OutPort buffers
		self.addOutPort("fin",self._finOut)
		
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

		#
	def onActivated(self, ec_id):
		print("activate standUp")	
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
		#カウントの取得
		if self._countIn.isNew():
			self._d_count = self._countIn.read()
			self._count_number = self._d_count.data
			#print("recieve;" ,self._count_number)
			self._start = "true"
			NAO_activate(self._NAO_IPaddress[0], self._NAO_Port[0])
		#バランスの取得
		if self._balanceIn.isNew():
			self._d_balance = self._balanceIn.read()
			self._balance = self._d_balance.data
		#立ち上がり判定の取得
		if self._judgeIn.isNew():
			self._d_judge = self._judgeIn.read()
			self._data = self._d_judge.data
			print("judge is ",self._data)
		#NAOトレーニング開始
		if 0 <= self._count < (self._count_number - 1) :
			print(self._count,"count")
			if self._start == "true":
				if self._data == 1:
					print(self._data,"stand")
					self._endtime = time.time()
					NAO_cheer(self._NAO_IPaddress[0], self._NAO_Port[0])
					self._start = "false"
					print("cheer")
				elif self._data == 0:
					print("sitting")
			if self._start == "false":
				if self._data == 0:
					standtime = self._endtime - self._starttime
					#立ち上がりが早い速度場合
					if (0 <= standtime <2):
						NAO_stand_high(self._NAO_IPaddress[0], self._NAO_Port[0])
						self._starttime = time.time()
						self._start = "true"
						self._count += 1
					#立ち上がりが普通の速度の場合
					elif (2 <= standtime <5):
						NAO_stand(self._NAO_IPaddress[0], self._NAO_Port[0])
						self._starttime = time.time()
						self._start = "true"
						self._count += 1
					#立ち上がりがゆっくりの場合
					else:
						NAO_stand_low(self._NAO_IPaddress[0], self._NAO_Port[0])
						self._starttime = time.time()
						self._count += 1
					self._start = "true"
					print(self._data,"sitting")
				#左右のバランス
				if self._data == 1:
					if self._balance == 2 :
						NAO_left(self._NAO_IPaddress[0], self._NAO_Port[0])
					if self._balance == 3:
						NAO_right(self._NAO_IPaddress[0], self._NAO_Port[0])
			#終了合図
		if ((self._count == (self._count_number - 1)) and (self._data == 1)):
			NAO_end(self._NAO_IPaddress[0], self._NAO_Port[0])
			print("end")
			self._count += 1
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
	speechProxy.say("ぼくの動きのまねをしてね")
	postureProxy.goToPosture("StandInit", 0.1)
	speechProxy.say("さんはい")
	motionProxy.wakeUp()
	
def NAO_end(robotIP, PORT):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
	speechProxy.say("上手に立てたね。目標の立ち上がり回数に到達しました。")
	motionProxy.rest()
	speechProxy.say("今日のトレーニングは、終了です。お疲れさまでした。")
	print("FINISH")

def NAO_stand(robotIP, PORT):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
	speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
	postureProxy.goToPosture("StandInit", 0.25)
	speechProxy.say("ぼくみたいに立ってみよう")
	print("stand up")
	speechProxy.say("さんはい")

def NAO_stand_high(robotIP, PORT):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
	speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
	speechProxy.say("すこしはやくするね、ぼくみたいに立ってみよう")
	postureProxy.goToPosture("StandInit", 0.5)
	speechProxy.say("さんはい")
	print("stand up")

def NAO_stand_low(robotIP, PORT):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
	speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
	speechProxy.say("ゆっくりにするね、ぼくみたいに立ってみよう")
	postureProxy.goToPosture("StandInit", 0.2)
	speechProxy.say("さんはい")
	print("stand up")

def NAO_cheer(robotIP, PORT):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
	speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
	speechProxy.say("上手に立てたね。座ってもう一回がんばろう。")
	motionProxy.rest()

def NAO_cheer_fin(robotIP, PORT):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
	motionProxy.wakeUp()
	speechProxy.say("上手に立てたね")
	speechProxy.say("立ち上がり回数が目標に到達しました")
	motionProxy.rest()

def NAO_left(robotIP, PORT):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
	speechProxy.say("重心が左にかたよっています")
	motionProxy.setAngles(["RShoulderPitch", "RShoulderRoll"], [0.0, 1.0], 0.1)
	print("left")
	motionProxy.rest()

def NAO_right(robotIP, PORT):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
	speechProxy.say("重心が右にかたよっています")
	motionProxy.setAngles(["LShoulderPitch", "LShoulderRoll"], [0.0, 1.0], 0.1)
	print("right")
	motionProxy.rest()

def NAO__ss__aa(robotIP, PORT):
	motionProxy  = ALProxy("ALMotion", robotIP, PORT)
	postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
	speechProxy = ALProxy("ALTextToSpeech", robotIP, PORT)
	motionProxy.wakeUp()
	speechProxy.say("上手に立てたね")
	speechProxy.say("立ち上がり回数が目標に到達しました")
	motionProxy.rest()

if __name__ == "__main__":
	main()

