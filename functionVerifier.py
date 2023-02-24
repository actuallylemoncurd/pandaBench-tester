# todo: make this file automatically compare results data vs feed data when ran and spit out a pass / fail for the module
# convert only the messages we manipulate into binary, parse that data to verify ocelot did what we want
# make sure the other normal message's made it through the ocelot filter

import csv

GRA_Neu = 0x38A
mACC_GRA_Anziege = 0x56a
mACC_System = 0x368

with open('benchtestResults.csv', 'r') as resultData:
    reader = csv.reader(resultData)
    for row in reader:
        try:
            addr = hex(int(row[0]))
            dat = bin(int(row[1], 16)).ljust(66, '0')
            if addr == hex(GRA_Neu):
                # Message from cruise control stalk, most important to make sure the bitflipping is correct!
                GRA_Kodierinfo = bin((int(dat, 2) >> 48) & int(1))
                GRA_Sender = bin((int(dat, 2) >> 44) & int(3)).ljust(4, '0')
            if addr == hex(mACC_GRA_Anziege):
                # Message from ECU, ocelot module should be filling in the blank signals
                ACA_StaACC = bin((int(dat, 2) >> 53) & int(7)).ljust(5, '0')
                ACA_AnzDisplay = bin((int(dat, 2) >> 46) & int(1))
                ACA_Zeitluecke = bin((int(dat, 2) >> 42) & int(15)).ljust(6, '0')
                ACA_V_Wunsch = bin((int(dat, 2) >> 32) & int(255)).ljust(10, '0')
                ACA_PrioDisp = bin((int(dat, 2) >> 27) & int(3)).ljust(4, '0')
                ACA_gemZeitl = bin((int(dat, 2) >> 20) & int(15)).ljust(6, '0')
                ACA_Aend_Zeitluecke = bin((int(dat, 2) >> 5) & int(1))
            if addr == hex(mACC_System):
                #do some binary ops here to ensure proper ocelot function
                pass
        except Exception as e:
            print("an exception occured" + str(e))