# -*- coding: utf-8 -*-
from .visaresource import VisaResource

# DSOX 3054T
# https://www.keysight.com/upload/cmc_upload/All/3kT_X-Series_prog_guide.pdf
class Oscillo(VisaResource):
    def __init__(self, addr):
        super(Oscillo, self).__init__(addr)

    def get_value_list(self, average_count=500, target_channel="CHANnel3"):
        self.resource.write(":DISPlay:CLEar")
        self.resource.write(":ACQuire:TYPE AVERage")
        self.resource.write(":MTESt:COUNt:RESet")
        # specify the percentage of acquisition needed to be done
        self.resource.write(":ACQuire:COMPlete 100")
        # specify the number of waves to be averaged
        self.resource.write(":ACQuire:COUNt {}".format(str(average_count)))

        # DIGitize run the instrument until it meets the acquire setting(above).
        # DIGitize also stops after the instrument meets the setting.
        # To collect data, you use the :DIGitize command. This command clears the
        # waveform buffers and starts the acquisition process. Acquisition continues until
        # acquisition memory is full, then stops. The acquired data is displayed by the
        # oscilloscope, and the captured data can be measured, stored in acquisition
        # memory in the oscilloscope, or transferred to the controller for further analysis.
        # Any additional commands sent while :DIGitize is working are buffered until
        # :DIGitize is complete.
        self.resource.write(":DIGitize {}".format(target_channel))

        self.resource.write(":WAVeform:SOURce {}".format(target_channel))
        self.resource.write(":WAVeform:FORMat ASCII")
        ascii_str = self.resource.query(":WAVeform:DATA?")
        header_length = int(ascii_str[1]) + 2
        return [float(s.strip()) for s in ascii_str[header_length:].split(",")]

    def set_trigger(self, ch=1, slope_positive=True, level="+800.50E-03"):
        self.resource.write(":TRIGger:SOURce CHANnel{}".format(str(ch)))
        self.resource.write(":TRIGger:MODE EDGE")
        self.resource.write(":TRIGger:SLOPe {}".format("POSitive" if slope_positive else "NEGative"))
        self.resource.write(":TRIGger:LEVel {}".format(level))
    
    def save_image(self, filename="tmp.png"):
        self.resource.timeout = 30000
        data = self.resource.query_binary_values(':DISPlay:DATA? PNG, COLOR', datatype='B')
        newfile = open(filename,'wb')
        newfile.write(bytearray(data))
        newfile.close()
    
    def change_bwlimit(self, ch=1, set_bwlimit=True):
        self.resource.write(":CHANnel{}:BWLimit {}".format(str(ch), "1" if set_bwlimit else "0"))
