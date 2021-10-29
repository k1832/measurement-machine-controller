# -*- coding: utf-8 -*-
from .visaresource import VisaResource
from typing import Final

# WF1967/WF1968
# http://www.nfcorp.co.jp/support/manual/pdf/WF1967_68_InstructionManual003.pdf
class FG(VisaResource):
    HIGH_VOLTAGE: Final[float] = 2.1
    LOW_VOLTAGE: Final[float] = 0.7
    AMPLITUDE: Final[float] = 1.4
    OFFSET: Final[float] = 1.4

    def __init__(self, addr):
        super(FG, self).__init__(addr)

    # SQUare or DC
    def change_function(self, ch=1, fctn="SQUare"):
        self.resource.write(":SOURce{}:FUNCtion {}".format(str(ch), fctn))
    
    def change_offset(self, ch=1, offset=None):
        if offset is None:
            offset = FG.OFFSET
        self.resource.write(":SOURce{}:VOLTage:OFFSet {}V".format(str(ch), str(offset)))
    
    def change_amplitude(self, ch=1, amplitude=None):
        if amplitude is None:
            amplitude = FG.AMPLITUDE
        self.resource.write(":SOURce{}:VOLTage:AMPLitude {}VPP".format(str(ch), str(amplitude)))

    def change_freq(self, ch=1, freq=0.2):
        self.resource.write(":SOURce{}:FREQuency {}MHZ".format(str(ch), str(freq)))
    
    def change_phase(self, ch=1, phase=0):
        self.resource.write(":SOURce{}:PHASe:ADJust {}DEG".format(str(ch), str(phase)))
    
    def sync_chs(self):
        # 基準位相を初期化。WF1968ではResourceの指定によらず2channelとも同じ基準位相になる（同期）。
        self.resource.write(":PHASe:INITiate")

    def turn_on(self, ch=1):
        self.resource.write(":OUTPut{}:STATe ON".format(str(ch)))
    def turn_off(self, ch=1):
        self.resource.write(":OUTPut{}:STATe OFF".format(str(ch)))
    
    def turn_on_all(self):
        self.turn_on(ch=1)
        self.turn_on(ch=2)
    def turn_off_all(self):
        self.turn_off(ch=1)
        self.turn_off(ch=2)

    def ac(self, ch=1):
        self.change_function(ch=ch)
        self.change_offset(ch=ch, offset=FG.OFFSET)
        self.change_amplitude(ch=ch, amplitude=FG.AMPLITUDE)
        self.change_freq(ch=ch)
        self.change_phase(ch=ch)
    
    def dc(self, ch=1, high=True):
        offset = FG.HIGH_VOLTAGE if high else FG.LOW_VOLTAGE
        self.change_function(ch=ch, fctn="DC")
        self.change_offset(ch=ch, offset=offset)
