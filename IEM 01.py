#!/usr/bin/env python
# coding: utf-8

# In[50]:


# shubham onkar and suraj shirsale 


from gurobipy import *
import numpy as np
import pandas as pd

df = pd.read_csv(r'pretzeldemand.csv',header=None)
d=df.to_numpy()

fp = 3.29 # fresh pretzel selling cost
dop = 0.99 # a day old pretzel selling cost
c = 50 # pretzel production each day

#Indices
I = range(1, len(d)+1)


m = Model("Pretzel Production ")
fs = m.addVars(I, lb=0.0, vtype=GRB.CONTINUOUS, name="fresh sold ") #pretzel produced in a day and sold the same day
snd = m .addVars(I, lb=0.0, vtype=GRB.CONTINUOUS, name="sold next day") #pretzel produced on a day and sold next day


m.setObjective(quicksum(fs[i] * fp + snd[i] * dop for i in I), GRB.MAXIMIZE) 



for i in range(1, len(d)+1):
    m.addConstr(fs[i] + snd[i] <= c)    #production capacity constraint
    
m.addConstr(fs[1] <= d[0])    #demand constraint for day one ; enforces zero opeaning inventory
    
for i in range(2, len(d)):
    m.addConstr(fs[i] + snd[i-1] <= d[i])
    
m.addConstr(snd[len(d)] == 0)    #zero  closing inventory

m.write("Pretzel Production.lp")

m.optimize()

if m.status == GRB.OPTIMAL:
    for v in m.getVars():
        print('%s = %g units' % (v.varName, v.x)) 
    print('Objective =$ %f' % m.objVal)
elif m.status == GRB.INFEASIBLE:
    print('LP is infeasible.')
elif m.status == GRB.UNBOUNDED:
    print('LP is unbounded.')


# In[ ]:




