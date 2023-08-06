# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 12:02:11 2021

@author: Diomer Algendonis
"""

def primo(n):
	for i in range(2, n):
		es_primo = True
		for j in range(2, i):
			if(i%j == 0):
				es_primo = False
		if(es_primo):
			print(f"{i} es primo")