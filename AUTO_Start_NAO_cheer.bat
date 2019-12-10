@echo off

echo ### コンピュータ名取得 ###
FOR /F %%A IN ('hostname.exe') DO SET NAME=%%A
echo %NAME%

echo ### NamingService起動 ###
cd C:\Program Files (x86)\OpenRTM-aist\1.1.2\bin
start /MIN rtm-naming.bat

timeout /T 3

echo ### RTC起動 ###
cd C:\workspaces\SerialConnect
start /MIN SerialConnect.py
cd C:\workspaces\Change
start /MIN Change.py
cd C:\workspaces\Judge3
start /MIN judge3.py
cd C:\workspaces\StandUp
start /MIN StandUp.py
cd C:\workspaces\CsvWrite
start /MIN CsvWrite.py
cd C:\workspaces\Calc
start /MIN Calc.py
cd C:\workspaces\GUI
start /MIN GUI.py
cd C:\Program Files (x86)\OpenHRIAudio\OpenHRIAudio\2.10
start /MIN portaudioinput.exe
cd C:\Program Files (x86)\OpenHRIVoice\OpenHRIVoice\2.10
start /MIN juliusrtc.exe sample.xml
cd C:\Program Files (x86)\SEATSAT\SEATSAT\2.10
start /MIN SEAT.exe sample.seatml
timeout /T 5

echo ### Rtshellを使用準備 ###
set PATH=C:\Python27;C:\Python27\Scripts;%PATH%
rtfind localhost

rem call rtcwd localhost/

rem set RTCTREE_NAMESERVERS=localhost
rem call rtls

echo ### config設定 ###
echo ### IpAddress設定 ###
rem call rtconf /localhost/%NAME%.host_cxt/ApriPocoMotion0.rtc get IPAdress
rem call rtconf /localhost/%NAME%.host_cxt/ApriPocoMotion0.rtc set IPAdress localhost
rem call rtconf /localhost/%NAME%.host_cxt/ApriPocoMotion0.rtc get IPAdress
timeout /T 1

echo ### RTCポート接続 ###
call rtcon /localhost/%NAME%.host_cxt/PortAudioInput0.rtc:AudioDataOut /localhost/%NAME%.host_cxt/JuliusRTC0.rtc:data
call rtcon /localhost/%NAME%.host_cxt/JuliusRTC0.rtc:result /localhost/%NAME%.host_cxt/SEAT0.rtc:speechin
call rtcon /localhost/%NAME%.host_cxt/SEAT0.rtc:speechout /localhost/%NAME%.host_cxt/CsvWrite0.rtc:sign
call rtcon /localhost/%NAME%.host_cxt/SEAT0.rtc:speechout /localhost/%NAME%.host_cxt/Judge30.rtc:sign
call rtcon /localhost/%NAME%.host_cxt/SerialConnect0.rtc:sensor /localhost/%NAME%.host_cxt/Change0.rtc:rawdata
call rtcon /localhost/%NAME%.host_cxt/Change0.rtc:data /localhost/%NAME%.host_cxt/Judge30.rtc:data
call rtcon /localhost/%NAME%.host_cxt/Change0.rtc:data /localhost/%NAME%.host_cxt/StandUp0.rtc:sensor
call rtcon /localhost/%NAME%.host_cxt/Judge30.rtc:result /localhost/%NAME%.host_cxt/StandUp0.rtc:judge
call rtcon /localhost/%NAME%.host_cxt/Judge30.rtc:balance /localhost/%NAME%.host_cxt/StandUp0.rtc:balance
call rtcon /localhost/%NAME%.host_cxt/StandUp0.rtc:fin /localhost/%NAME%.host_cxt/CsvWrite0.rtc:fin
call rtcon /localhost/%NAME%.host_cxt/StandUp0.rtc:fin /localhost/%NAME%.host_cxt/Calc0.rtc:fin
call rtcon /localhost/%NAME%.host_cxt/Calc0.rtc:time /localhost/%NAME%.host_cxt/GUI0.rtc:time
call rtcon /localhost/%NAME%.host_cxt/GUI0.rtc:count /localhost/%NAME%.host_cxt/StandUp0.rtc:count

timeout /T 3


echo ### RTCアクティベート ###
call rtact /localhost/%NAME%.host_cxt/SerialConnect0.rtc
timeout /T 3
call rtact /localhost/%NAME%.host_cxt/PortAudioInput0.rtc
call rtact /localhost/%NAME%.host_cxt/JuliusRTC0.rtc
call rtact /localhost/%NAME%.host_cxt/SEAT0.rtc
call rtact /localhost/%NAME%.host_cxt/Change0.rtc
call rtact /localhost/%NAME%.host_cxt/Judge30.rtc
call rtact /localhost/%NAME%.host_cxt/CsvWrite0.rtc
call rtact /localhost/%NAME%.host_cxt/StandUp0.rtc
call rtact /localhost/%NAME%.host_cxt/Calc0.rtc
call rtact /localhost/%NAME%.host_cxt/GUI0.rtc

REM ### アクティベートがうまくいかないときなど、OpenRTPを起動して手動でアクティベートする
rem set PATH=%PROG%\OpenRTM-aist\1.1.2\bin\jre\bin;%PATH%
rem cd %PROG86%\OpenRTM-aist\1.1.2\utils\OpenRTP
rem start eclipse.exe

timeout /T 3
rem PAUSE


