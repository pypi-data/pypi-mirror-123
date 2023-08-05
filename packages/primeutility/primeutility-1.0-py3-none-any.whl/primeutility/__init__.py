#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Oct 11 2021

@author: Santiago Movilla

""" 

def primo(n):
	for i in range(2, n):
		es_primo = True
		for j in range(2, i):
			if(i%j == 0):
				es_primo = False
		if(es_primo):
			print(f"{i} es primo")
