#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any
import pyvisa as visa
from dataclasses import InitVar, dataclass, field
import atexit

@dataclass
class VisaResource:
    addr: InitVar[str]
    visa_path: InitVar[str] = "C:\\Windows\\system32\\visa64.dll"
    rm: Any = field(init= False)
    resource: Any = field(init= False)

    def __post_init__(self, addr, visa_path):
        self.rm = visa.ResourceManager(visa_path)
        # Always close the resource at exit
        atexit.register(self.close_resource)
        self.resource = self.rm.open_resource(addr)
        self.resource.timeout = 10 * 1000
        print("DEVICE:", self.resource.query("*IDN?"))
    def close_resource(self):
        print("Closing the resource manager...")
        self.rm.close()
