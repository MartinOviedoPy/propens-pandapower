# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 00:02:46 2022

@author: thoug
"""

import numpy as np
import pandas as pd
import pandapower as pp


import Adv_network_only as addnet


import openpyxl as oxl 
from io import StringIO

net = addnet.net

text='-'
h_line = text.rjust(100,'-')

"""
By Calling Anal(net) function, now I can call all the sub function all at once
"""

########################################################

def Anal(net):
    Anal_Bus_Voltage(net.res_bus)
    Anal_Trafo_Loading(net.res_trafo)
    Anal_Trafo3w_Loading(net.res_trafo3w)
    Anal_Line_Loading_Better(net.res_line)
    
#####################################################3
#####################################################3

def Anal_xl():
    Bus_Voltage_Sum = Anal_Bus_Voltage(net.res_bus)
    Trafo_Loading_Sum = Anal_Trafo_Loading(net.res_trafo)
    Trafo3w_Loading_Sum = Anal_Trafo3w_Loading(net.res_trafo3w)
    Line_Loading_Sum = Anal_Line_Loading_Better(net.res_line)
    
    
    
    return Bus_Voltage_Sum, Trafo_Loading_Sum, Trafo3w_Loading_Sum, Line_Loading_Sum

#####################################################3
#####################################################3

def Anal_Bus_Voltage(x):
    s = x['vm_pu']
    under_bus = []
    under_value = []
    under_voltage=[]
    over_bus =[]
    over_value=[]
    over_voltage =[]
    
    """
    Store the value of Bus and p.u. of voltage and save it in a list, and return it 
    """
    
    for i in range(0, len(x)):
        if s[i] <0.95:
          print(f"bus %d is undervoltage, it is {format(s[i], '.4f')} p.u. now" % i)            #Based on Data of Map, maybe I can make function to color this node RED sth like that in case
          under_bus.append(i)
          under_value.append(s[i])
          under_voltage = [[under_bus],[under_value]]
          #return under_voltage
          #print(under_voltage)
        elif s[i]>1.03:
            print(f"bus %d is overvoltage, it is {format(s[i], '.4f')} p.u. now" % i)           #In case of over voltage, value is still arbitrary
            over_bus.append(i)
            over_value.append(s[i])
            over_voltage = [[over_bus],[over_value]]
            #return over_voltage
            
        elif all(i < 1.0 for i in s) == True:   #Incase when all are in standard, give one line of notice all are good
            print("All Bus Voltage is in standard")
    
    
    return under_voltage, over_voltage
    print('----------Bus Analysis Over----------------')
    
#####################################################3


def Anal_Trafo_Loading(x):
    s = x['loading_percent']
    
    over_trafo_index = []
    over_trafo_value = []
    over_trafo = []
               
    for i in range(0, len(x)):
        if s[i]>100.0:
            print(f"Transformer %d is overloaded, it is {format(s[i], '.4f')} percent used" % i,  )
            over_trafo_index.append(i)
            over_trafo_value.append(s[i])
            over_trafo = [[over_trafo_index],[over_trafo_value]]          
        elif all(i < 100 for i in s) == True:
            print("All Transformer is in standard")
    
    
    return over_trafo
    print('----------Transformer Analysis Over----------------')    
         
#####################################################3

def Anal_Trafo3w_Loading(x):
    s = x['loading_percent']
    a = all(s)
   
    over_trafo3w_index = []
    over_trafo3w_value = []
    over_trafo3w = []
    
    for i in range(0, len(x)):
        if s[i]>100.0:
            print(f"3-winding Transformer %d is overloaded, it is {format(s[i], '.4f')} percent used" % i,  )
            over_trafo3w_index.append(i)
            over_trafo3w_value.append(s[i])
            over_trafo3w = [[over_trafo3w_index],[over_trafo3w_value]]      
        elif all(i < 100 for i in s) == True:
            print("All 3-winding Transformer is in standard")
            
    return over_trafo3w
    print('----------3 Winding Transformer Analysis Over----------------')
   
#####################################################3
#####################################################3

def Anal_Line_Loading_Better(x):
    s = x['loading_percent']
    
    over_line_index = []
    over_line_value = []
    over_line = []
    
    for i in range(0, len(x)):
        if all(i<100 for i in s) == False:
            print(h_line)
            print("There are issues in loading of the line")
            print()
            print("| Line     State      Percentage|")
            print("_________________________________")
            
            break
          
    
    for i in range(0, len(x)):
        if s[i]>100.0:
            print(f"|line %d  overloadedd" %i, end='') 
            print(f": {format(s[i], '.4f')}%|" )
            over_line_index.append(i)
            over_line_value.append(s[i])
            over_line = [[over_line_index],[over_line_value]]
        elif all(i < 100 for i in s) == True:
            print("|All line is in standard|")
            
    return over_line
    print('----------Line Analysis Over----------------')
   
      
#####################################################3