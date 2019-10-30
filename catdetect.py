#!/usr/bin/python3
# Python code for keylogger 
# to be used in linux 
import os 
import pyxhook 
import json 

##Test case
#rolling_buffer = list("[2~]](9999m=[]-[[[[[ft2B9Y']]]]]]]]]]]]]]XXXXXXXXXXXXXXXXXXXXXXXXXxxxxxx444444444444444444444444444444444444444444444444444444444444444444444444$$$$$$$$$$$$$$$$$$$$$$$$$$$$$gggggggggggggIIIIIIIIIIIIIIII8///////8I880")

rolling_buffer = []
if len(rolling_buffer) == 0:
    BUFFER_LENGTH = 30
else:
    BUFFER_LENGTH = len(rolling_buffer)
DETECT_LENGTH = 6

rows = []
rows.append("Escape [269025042] [269025041] [269025043] [269025202] Num_Lock Scroll_Lock Super_L p [269025051] [269025027] [269025026] Print Insert Delete".split())
rows.append("grave 1 2 3 4 5 6 7 8 9 0 minus equal BackSpace".split())
rows.append("Tab q w e r t y u i o p bracketleft bracketright backslash".split())
rows.append("Caps_Lock a s d f g h j k l semicolon apostrophe Return".split())
rows.append("Control_L Super_L Alt_L space Alt_R Control_R Page_Up Up Next".split())
rows.append("null null null null null null null null null null null Left Down Right".split())
# This tells the keylogger where the log file will go. 
# You can set the file path as an environment variable ('pylogger_file'), 
# or use the default ~/Desktop/file.log 
log_file = os.environ.get( 
    'pylogger_file', 
    os.path.expanduser('./file.log') 
) 
# Allow setting the cancel key from environment args, Default: ` 
cancel_key = ord( 
    os.environ.get( 
        'pylogger_cancel', 
        '`'
    )[0] 
) 
  
# Allow clearing the log file on start, if pylogger_clean is defined. 
if os.environ.get('pylogger_clean', None) is not None: 
    try: 
        os.remove(log_file) 
    except EnvironmentError: 
       # File does not exist, or no permissions. 
        pass
  
#creating key pressing event and saving it into log file 
def OnKeyPress(event):
    addToRollingBuffer(event.Key)

def addToRollingBuffer(key):
    global rolling_buffer
    global BUFFER_LENGTH
    if len(rolling_buffer)==BUFFER_LENGTH:
        rolling_buffer = rolling_buffer[int(BUFFER_LENGTH/2):]
    if len(rolling_buffer)<BUFFER_LENGTH:
        rolling_buffer.append(key)
    isCatDetected = isBufferCatty()
    if isCatDetected:
        print('CAT DETECTED')
        rolling_buffer = []
        os.popen('gnome-screensaver-command --lock')

def isBufferCatty():
    global rolling_buffer
    areThereNearbyKeys = 0
    areThereDupes = 0
    #if len(rolling_buffer)>int(BUFFER_LENGTH/3):
    #     areThereNearbyKeys = nearbyKeyDetection(rolling_buffer)
    areThereDupes = dupeDetection(rolling_buffer)
    #print (areThereNearbyKeys, areThereDupes) 
    if areThereNearbyKeys or areThereDupes:
       return 1
    return 0



def nearbyKeyDetection(rolling_buffer):
    nearby = 0
    for i in range(len(rolling_buffer)):
        for row in rows:
            if rolling_buffer[i] in row:
               nearby += (row.index(rolling_buffer[i])+1)
        nearby*=-1
    if nearby<2:
        return 1
    return 0
def dupeDetection(rolling_buffer):
    dupes={};
    for i in range(len(rolling_buffer)):
        dupe = {"count":0}
        if rolling_buffer[i] in dupes:
            dupes[rolling_buffer[i]]['count'] = dupes[rolling_buffer[i]]['count'] + 1;
        else:
            dupes[rolling_buffer[i]] = dupe
    for (key,dupe) in dupes.items():
        #FIX ME  multiple dupes, are there. we are returning when we just get for a single item.
        if dupe['count']>DETECT_LENGTH:
            return 1 
    return 0
# create a hook manager object 
new_hook = pyxhook.HookManager() 
new_hook.KeyDown = OnKeyPress 
# set the hook 
new_hook.HookKeyboard() 
try: 
    new_hook.start()         # start the hook 
except KeyboardInterrupt: 
    # User cancelled from command line. 
    pass
except Exception as ex: 
    # Write exceptions to the log file, for analysis later. 
    msg = 'Error while catching events:\n  {}'.format(ex) 
    pyxhook.print_err(msg) 
    with open(log_file, 'a') as f: 
        f.write('\n{}'.format(msg)) 


