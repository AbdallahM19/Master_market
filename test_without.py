#!/usr/bin/env python3

from Secret.Common_Arithmetic_Operations import *
import os
import json

def sign_in_or_log_up():
    last = {
        'Addition' : addition(),
        'Subtraction' : subtraction(),
        'Multiplication' : multiplication(),
        'Division' : division(),
    }
    for i, operation in last.items():
        print(f"{i}. {operation}")

sign_in_or_log_up()