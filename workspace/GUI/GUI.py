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
import Tkinter as tk
import ttk
import tkFont as font
from PIL import Image, ImageTk
import os
import re
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

riha_count = 0
rcv_time = 0
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


		self._d_time = RTC.TimedDouble(RTC.Time(0,0),0.0)
		self._timeIn = OpenRTM_aist.InPort("time", self._d_time)

		self._d_count = RTC.TimedLong(RTC.Time(0,0),0.0)
		self._countOut = OpenRTM_aist.OutPort("count", self._d_count)

		self._flag_act = True
		#self._txt = ""#tk.StringVar
		
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
	

	def onActivated(self, ec_id):
		print("activate GUI")
	
		return RTC.RTC_OK
	

	def onDeactivated(self, ec_id):
		print("deactivate GUI")
		return RTC.RTC_OK
	

	def onExecute(self, ec_id):

		if self._timeIn.isNew():
			self._d_time = self._timeIn.read()
			global rcv_time
			rcv_time = self._d_time.data
			print("receive time: ", self._d_time.data)

		if self._flag_act == True and riha_count > 0:
			self._d_count.data = riha_count
			self._countOut.write()
			print("out data: ",self._d_count.data)
			self._flag_act = False

		time.sleep(0.5)
		
		return RTC.RTC_OK

class GUI_disp:

	def __init__(self):
		self._frame = tk.Tk()
		self._font_set = font.Font(family = "Helvetica" ,size = 30 ,weight = "bold" )

	def input_form(self):
		
		str_var = tk.StringVar
		self._frame.title("立ち上がり回数の決定")
		self._frame.attributes("-topmost", True)
		self._frame.state("zoomed")

		label1 = tk.Label(self._frame, text = "立ち上がり回数を入力してください" ,font = self._font_set)
		label1.grid(row=2, column=5)
			
		img = Image.open("./cheer.png")
		img = ImageTk.PhotoImage(img)
			
		canvas = tk.Canvas(bg = "black", width = 1700, height = 1000)
		canvas.place( relheight=1.0, relwidth=1.0)
		canvas.create_image(700,350, image = img)
		
		txt1 = tk.Entry(width = 30)
		txt1.place (relheight=0.08, relwidth=0.1, relx=0.6, rely=0.7)
			
		textbox = tk.Entry(self._frame, textvariable=txt1)
		textbox.place (relheight=0.08, relwidth=0.1, relx=0.6, rely=0.7)

		button1 = tk.Button(self._frame, text = "入力", height = 1, width = 1)

		input_val = 0

		def btn1_callback(event):
			input_val = textbox.get()
			print(input_val)
			global riha_count
			riha_count = int(input_val)
			label5 = tk.Label(self._frame, text=input_val, font=self._font_set)
			label5.place(relheight=0.08, relwidth=0.1, relx= 0.8, rely= 0.7)
			
		#if data.isdigit():
		#	i = int(data)
		#	print("data is :",i)
		
		button1.bind("<Button-1>",btn1_callback)
		button1.place(relheight=0.08, relwidth=0.1, relx = 0.6, rely = 0.8)

		self._frame.grid()

		#######################################
		frame2 = tk.Toplevel()
		str_var = tk.StringVar
		font_set2 = font.Font(family = "Helvetica" ,size = 30 ,weight = "bold" )

		"""	
			while True:
				time.sleep(1)
				print("stay")
				if display_flag == True:
					break
		"""
		frame2.attributes("-topmost", True)
		frame2.title("結果表示")
		frame2.state("zoomed")

		label2 = tk.Label(frame2, text = "今回の立ち上がり時間は" ,font = font_set2)
		label2.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
		label3 = tk.Label(frame2, text = "過去の立ち上がり時間は" ,font = font_set2)
		label3.grid(row=11, column=0, columnspan=2, padx=5, pady=5)
		
		label4 = tk.Label(frame2, text = "0" ,font = font_set2)
		label4.grid(row=5, column=5, padx=5, pady=5)

		label5 = tk.Label(frame2, text = "秒" ,font = font_set2)
		label5.grid(row=5, column=8, padx=5, pady=5)
		label6 = tk.Label(frame2, text = "表示する過去のデータを選んでください" ,font = font_set2)
		label6.grid(row=8, column=0, padx=5, pady=5)

		frame2.grid()
		#過去呼び出しのコンボボックス
		post = os.listdir("../CsvWrite/data")
		txt2 = tk.StringVar()

		def select_cb(event):
				postdata = txt2.get()
				print(postdata)
				dif = 0
				
				with open("../CsvWrite/data/"+ postdata, "r")as f:
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
					dif  = (end - start)
					print("posttime is :", dif)

					font_set3 = font.Font(family='Helvetica', size=20, weight='bold')

					label7 = tk.Label(frame2, text = dif ,font = font_set3)
					label7.grid(row=11, column=5, padx=5, pady=5)
					label8 = tk.Label(frame2, text = "秒" ,font = font_set3)
					label8.grid(row=11, column=8, padx=5, pady=5)

		cb = ttk.Combobox(frame2, textvariable=txt2)
		cb.bind('<<ComboboxSelected>>' , select_cb)
		cb['values']=(post)
		cb.grid(row=8, column=5, padx=5, pady=5)
		#cb.set("コンボテキスト2")
		#cb.grid(row=3, column=3)s
		cb.grid_configure(padx=100, pady=100)

		def update():
			label4.configure(text=rcv_time)
			frame2.after(500,update)
		
		update()

		self._frame.mainloop()



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
	mgr.runManager(True)
	

if __name__ == "__main__":
	main()
	gui = GUI_disp()
	gui.input_form()
