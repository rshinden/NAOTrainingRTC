#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file GUI.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
import Tkinter
import ttk
import tkFont as font
import os
import re
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


global data
global txt1
global switch
global count
global a
a = "end"
switch = "on"

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
gui_spec = ["implementation_id", "GUI", 
		 "type_name",         "GUI", 
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
# @class GUI
# @brief ModuleDescription
# 
# 
class GUI(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		time_arg = [None] * ((len(RTC._d_TimedDouble) - 4) / 2)
		self._d_time = RTC.TimedDouble(RTC.Time(0, 0), 0.0)
		"""
		"""
		self._timeIn = OpenRTM_aist.InPort("time", self._d_time)
		count_arg = [None] * ((len(RTC._d_TimedLong) - 4) / 2)
		self._d_count = RTC.TimedLong(*count_arg)
		"""
		"""
		self._countOut = OpenRTM_aist.OutPort("count", self._d_count)


		


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
		self.addInPort("time",self._timeIn)
		
		# Set OutPort buffers
		self.addOutPort("count",self._countOut)
		
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
		print("activate GUI")
		global switch
		global nina 
		switch = "on"
		nina = "poo"
	
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
		print("deactivate")

	
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
		global switch
		global data
		global count
		global a
		global frame2
		if switch == "on":
			print("on")
			#立ち上がり回数のGUI
			frame1 = Tkinter.Tk()
			frame1.title("トレーニング")
			frame1.geometry('400x300')
			frame1.grid()
			font1 = font.Font(family = "Helvetica", size = 10)
			label1 = Tkinter.Label(frame1, text = "立ち上がり回数を入力してください")
			label1.place(x = 90, y = 40)
			global txt1
			txt1 = Tkinter.Entry(width = 30)
			txt1.place(x = 90, y = 70)
			
			button1 = Tkinter.Button(frame1, text = "入力", command = btn1_callback)
			
			button1.place(x = 160, y = 100)
			#global i
			#self._d_count.data = i
			#self._countOut.write()
			frame1.mainloop()
			global a 
			switch = "off"
			
		if self._timeIn.isNew():
			print("receive time")
			#立ち上がり時間の取得
			self._d_time = self._timeIn.read()
			jikan = self._d_time.data
			print(jikan)
				#時間表示のGUI作成
			global nina
			if nina == "poo":
				frame2 = Tkinter.Toplevel()
				frame2.attributes("-topmost", True)
				frame2.title("結果表示")
				frame2.state('zoomed')
				#frame2.geometry('600x300')
				font3 = font.Font(family='Helvetica', size=30, weight='bold')
				label3 = Tkinter.Label(frame2, text = "今回の立ち上がり時間は" ,font = font3, anchor='e', justify='left')
				label3.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
				label6 = Tkinter.Label(frame2, text = "過去の立ち上がり時間は" ,font = font3, anchor='e', justify='left')
				label6.grid(row=11, column=0, columnspan=2, padx=5, pady=5)
				font2 = font.Font(family='Helvetica', size=20, weight='bold')
				label2 = Tkinter.Label(frame2, text = jikan ,font = font2)
				label2.grid(row=5, column=5, padx=5, pady=5)
				label7 = Tkinter.Label(frame2, text = "秒" ,font = font2)
				label7.grid(row=5, column=8, padx=5, pady=5)
				label8 = Tkinter.Label(frame2, text = "表示する過去のデータを選んでください" ,font = font3)
				label8.grid(row=8, column=0, padx=5, pady=5)
				frame2.grid()
					#過去呼び出しのコンボボックス
				post = os.listdir("C:/workspaces/CsvWrite/data")
				global txt
				txt = Tkinter.StringVar()
				cb = ttk.Combobox(frame2, textvariable=txt)
				cb.bind('<<ComboboxSelected>>' , select_cb)
				cb['values']=(post)
				cb.grid(row=8, column=5, padx=5, pady=5)
				#cb.set("コンボテキスト2")
				#cb.grid(row=3, column=3)
				cb.grid_configure(padx=100, pady=100)
				nina = "iiiii"
				frame2.mainloop()

		if a == "start":
			global i
			self._d_count.data = i
			self._countOut.write()
			print("send data", self._d_count)
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
	



def GUIInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=gui_spec)
    manager.registerFactory(profile,
                            GUI,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    GUIInit(manager)

    # Create a component
    comp = manager.createComponent("GUI")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

def gui():
	"""
	root = Tkinter.Tk()
	root.title(u"トレーニング")
	root.geometry("400x300")
	root.attributes("-topmost", True)
	font1 = font.Font(family = "Helvetica", size = 10)
	label1 = Tkinter.Label(root, text = "立ち上がり回数を入力してください")
	label1.place(x = 90, y = 40)
	global txt1
	txt1 = Tkinter.Entry(width = 30)
	txt1.place(x = 90, y = 70)
	button1 = Tkinter.Button(root, text = "入力", command = btn1_callback)
	button1.place(x = 160, y = 100)
	root.mainloop()	
	"""

def btn1_callback():
	global data
	global txt1
	global count
	data= txt1.get()
	print(data)
	#data_int = int(data)
	#count = data_int.isdecimal()
	#s = input()

	if data.isdigit():
		global i
		global a
		i = int(data)
		print("data:",i)
		a = "start"

		#self._d_count.data = i
		#self._countOut.write()

def select_cb(event):
	#print(txt.get())
	global txt
	global frame2
	postdata = txt.get()
	print(postdata)
	with open("C:/workspaces/CsvWrite/data/"+ postdata, "r")as f:
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
		print("posttime is :", wow)
		font3 = font.Font(family='Helvetica', size=20, weight='bold')
		label4 = Tkinter.Label(frame2, text = wow ,font = font3)
		label4.grid(row=11, column=5, padx=5, pady=5)
		label5 = Tkinter.Label(frame2, text = "秒" ,font = font3)
		label5.grid(row=11, column=8, padx=5, pady=5)


def gui2():
	"""
	root1 = Tkinter.Tk()
	root1.title(u"トレーニング")
	root1.geometry("400x300")
	root1.attributes("-topmost", True)
	font1 = font.Font(family = "Helvetica", size = 10)
	label2 = Tkinter.Label(root1, text = "もう一回入力してください")
	label2.place(x = 90, y = 40)
	root1.mainloop()
	"""
if __name__ == "__main__":
	main()

