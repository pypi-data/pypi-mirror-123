# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 18:46:09 2021

@author: travis.czechorski@maine.edu

Email:   travis.czechorski@maine.edu
         tjczec01@gmail.com
        
Advisor: thomas.schwartz@maine.edu
       
Github:  https://github.com/tjczec01       

"""

import butchertableau as bt

order = 7
X = bt.butcher(order, 15)
A, B, C = X.radau() 
Ainv = X.inv(A)        
T, TI = X.Tmat(Ainv)  
P = X.P(C)

print(P)