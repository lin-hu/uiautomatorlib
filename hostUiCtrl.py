'''
hostUiCtrl: wrapper for Python uiautomator to provide RobotFramework Keyword.

"uiautomator" is a Python wrapper of Android uiautomator testing framework. 
install: pip install uiautomator

Created on 04/11/2019

@author: lhu

'''
import bellagio.SystemLib.testbed_logging.testbedlog as tblog
from bellagio.SystemLib.TestbedException.BellagioError import BellagioError
from robot.libraries.BuiltIn import BuiltIn

class hostUiCtrl(object):
    '''
    provide robotframework keyword for UI control through uiautomator
    '''
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    _instance = None
    dev = None
   
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(hostUiCtrl, cls).__new__(cls, *args, **kwargs)
        #tblog.warnLog("hostUiCtrl instance: 0x{0:x}" .format(id(cls._instance)))
        return cls._instance  

    def __init__(self):
        if self.dev is None:
            try:
                from uiautomator import device as d
            except Exception as e:
                raise BellagioError("Uiautomator Python wrapper not found: {0}" .format(e))
            self.dev = d
        '''
            tblog.warnLog("init 1st time!!!")
        else:
            tblog.warnLog("init multiple times!!!")
        '''

    def text_on_screen(self, string):
        '''
        Check if current screen contains string
        '''
        ret = self.dev.exists(textContains=string)
        if ret==False :
            tblog.errorLog("Text \"{0}\" not found" .format(string))
        #raise BellagioError("Text {0} not found: {1}" .format(string, e))
        return ret
    
    def text_click(self, string):
        '''
        click object contains specific string
        '''
        try:
            self.dev(textContains=string).click()
        except Exception as e:
            #raise BellagioError("Failed to click {0} {1}" .format(txt, e))
            tblog.errorLog(str(e))

    def search_and_click(self, searchStr, parentClass="android.widget.LinearLayout", childClass="android.widget.TextView"):
        '''
        scroll and search text and click it 
        '''
        try:
            self.dev(className=parentClass).child_by_text(searchStr, allow_scroll_search=True, className=childClass).click()
        except Exception as e:
            #raise BellagioError("Failed to click {0} {1}" .format(txt, e))
            tblog.errorLog(str(e))

    def text_click_obj_around(self, searchStr, around="right", objectAround="android.widget.Switch"):
        '''
        search
        '''
        try:
            if around == "right":
                self.dev(textContains="OK Google").right(className=objectAround).click()
            elif around == "left":
                self.dev(textContains="OK Google").left(className=objectAround).click()
        except Exception as e:
            #raise BellagioError("Failed to click {0} {1}" .format(txt, e))
            tblog.errorLog(str(e))

    def calculate_logcat_interval(self, start_time, end_time):
        '''
        calculate logcat style(h:m:s.ms) time interval
        '''
        tblog.traceLog(self.calculate_logcat_interval, start_time, end_time) 
        try:
            start_hr = int(start_time.split(":", 1)[0])
            start_min = int((start_time.split(":", 1)[1]).split(":")[0])
            start_sec = int((start_time.split(":", 2)[2]).split(".")[0])
            start_ms = int(start_time.split(".")[1])
            print(start_hr, start_min, start_sec, start_ms)
            
            end_hr = int(end_time.split(":", 1)[0])
            end_min = int((end_time.split(":", 1)[1]).split(":")[0])
            end_sec = int((end_time.split(":", 2)[2]).split(".")[0])
            end_ms = int(end_time.split(".")[1])
            print(end_hr, end_min, end_sec, end_ms)
        except LookupError as e:
            print("Failed to find time pattern: {0}" .format(e))
            raise BellagioError("Failed to find time pattern: {0}" .format(e))
            return -1
            
        if end_ms < start_ms:
            end_ms += 1000
            end_sec -= 1
        interval_ms = end_ms - start_ms
        if end_sec < start_sec:
            end_sec += 60
            end_min -= 1
        interval_sec = end_sec - start_sec
        if end_min < start_min:
            end_min += 60
            end_hr -= 1
        interval_min = end_min - start_min
        if end_hr < start_hr:
            print("Time error {}/{}!" .format(start_time, end_time))
            raise BellagioError("Time error {}/{}!" .format(start_time, end_time))
            return -1
        interval_hr = end_hr - start_hr
        return interval_hr, interval_min, interval_sec, interval_ms
    
    def logcat_time_interval(self, log, start, end):
        '''
        get time interval between start/end string in logcat message
        '''
        tblog.traceLog(self.logcat_time_interval, start, end)
        if start in log and end in log:
            for line in log.splitlines():
                if start in line:
                    start_time = line.split()[1]
                    #print(start + ": " + start_time)
                if end in line:
                    end_time = line.split()[1]
                    #print(end + ": " + end_time)
                    break   #FIXME: only check first pair
        else:
            print("No {0}/{1} event found!!!" .format(start, end))
            tblog.errorLog("Failed to find event string in logcat")
            return("0:0:0.0")
            #raise BellagioError("Failed to find event string in logcat")
        
        interval_hr, interval_min, interval_sec, interval_ms = self.calculate_logcat_interval(start_time, end_time)
        return(start_time, end_time, "{}:{}:{}.{}" .format(interval_hr, interval_min, interval_sec, interval_ms))

if __name__ == '__main__':
    print("start")
    h = hostUiCtrl()
    '''
    h.text_click("Google")
    print("Search...")
    h.dev(className="android.widget.LinearLayout").child_by_text(r"Search, Assistant & Voice", allow_scroll_search=True,className="android.widget.TextView").click()
    '''
    #h.text_click("Voice")
    #h.text_click("Voice Match")
    #h.dev(textContains="Ok Google").right(className="android.widget.Switch").click()
    #h.text_click("Ok Google")
    if h.text_on_screen("adb"):
        print("TEXT found!")
    else:
        print("Failed to find TEXT!")
    print("done!")
    #h.text_click("CHRE")
    #interval_hr, interval_min, interval_sec, interval_ms = h.calculate_logcat_interval("00:37:14.948", "00:37:15.120")
    #print("{}:{}:{}.{}" .format(interval_hr, interval_min, interval_sec, interval_ms))
    '''
    log_file = "c:\\workspace\\linhu\\logcat.txt"
    event_str_pair = [("+tear_buffer_route", "-tear_buffer_route"),
                      ("+tear_bargein_mic_route+","-tear_bargein_mic_route-")]
    with open(log_file, "r") as fp:
        logcat = fp.read()
        for i in range(len(event_str_pair)):
            start, end, interval = h.logcat_time_interval(logcat, event_str_pair[i][0], event_str_pair[i][1])
            print("{0}:{3}/{2}:{4} ... {1}" .format(event_str_pair[i][0], interval, event_str_pair[i][1], start, end))
    '''
     
