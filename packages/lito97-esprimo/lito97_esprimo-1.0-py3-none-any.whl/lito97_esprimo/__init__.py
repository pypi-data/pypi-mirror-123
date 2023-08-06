#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 11:30:00 2021

@author: Lito
"""

def primo(n):
	for i in range(2, n):
		es_primo = True
		for j in range(2, i):
			if(i%j == 0):
				es_primo = False
		if(es_primo):
			print(f"{i} es primo")