# todo: now that all the signals are here, add some conditionals to parse their outputs
#       give a pass fail for module functionality

import csv

GRA_Neu = 0x38A
mACC_GRA_Anziege = 0x56a
mACC_System = 0x368

# init all signal counters
kodierCounter = 0
senderCounter = 0
staACCCounter = 0
accSystemCounter = 0
ststinfoCounter = 0

with open('benchtestResults.csv', 'r') as resultData:
    reader = csv.reader(resultData)
    for row in reader:
        try:
            addr = hex(int(row[0]))
            dat = bin(int(row[1], 16)).ljust(66, '0')
            if addr == hex(GRA_Neu):
                # Message from cruise control stalk, most important to make
                # sure the bitflipping is correct!
                GRA_Kodierinfo = bin((int(dat, 2) >> 48) & int(1))[2]
                GRA_Sender = bin((int(dat, 2) >> 44) & int(3)).ljust(4, '0')[2:4]
            if addr == hex(mACC_GRA_Anziege):
                # Message from ECU, ocelot module should be filling in the blank signals
                ACA_StaACC = bin((int(dat, 2) >> 53) & int(7)).ljust(5, '0')[2:5]
                ACA_AnzDisplay = bin((int(dat, 2) >> 46) & int(1))[2]
                ACA_Zeitluecke = bin((int(dat, 2) >> 42) & int(15)).ljust(6, '0')[2:6]
                ACA_V_Wunsch = bin((int(dat, 2) >> 32) & int(255)).ljust(10, '0')[2:10]
                ACA_PrioDisp = bin((int(dat, 2) >> 27) & int(3)).ljust(4, '0')[2:4]
                ACA_gemZeitl = bin((int(dat, 2) >> 20) & int(15)).ljust(6, '0')[2:6]
                ACA_Aend_Zeitluecke = bin((int(dat, 2) >> 5) & int(1))[2]
            if addr == hex(mACC_System):
                accSystemCounter = accSystemCounter + 1
                # Message entirely from ocelot
                ACS_Zaehler = bin((int(dat, 2) >> 52) & int(15)).ljust(6, '0')[2:6]
                ACS_Sta_ADR = bin((int(dat, 2) >> 50) & int(3)).ljust(4, '0')[2:4]
                ACS_StSt_Info = bin((int(dat, 2) >> 46) & int(3)).ljust(4, '0')[2:4]
                ACS_MomEingriff = bin((int(dat, 2) >> 45) & int(1))[2]
                ACS_Typ_ACC = bin((int(dat, 2) >> 43) & int(3)).ljust(4, '0')[2:4]
                ACS_FreigSollB = bin((int(dat, 2) >> 40) & int(1))[2]
                ACS_Sollbeschl = bin((int(dat, 2) >> 29) & int(2045)).ljust(13, '0')[2:13]
                ACS_zul_Regelabw = bin((int(dat, 2) >> 20) & int(255)).ljust(10, '0')[2:10]
                ACS_max_AendGrad = bin((int(dat, 2) >> 8) & int(255)).ljust(10, '0')[2:10]
            # increment signal incorrect counters
            if str(GRA_Kodierinfo) != '1': kodierCounter = kodierCounter + 1
            if str(GRA_Sender) != '01': senderCounter = senderCounter + 1
            if str(ACA_StaACC) == '000': staACCCounter = staACCCounter + 1
            if str(ACS_StSt_Info) == '1': ststinfoCounter = ststinfoCounter + 1
        except Exception as e:
            pass
            #print("an exception occured " + str(e))
    # if matrix for pass / fail
    # 1000 = 10 seconds of collective faults (100hz)
    if kodierCounter >= 1000:
        print("GRA_Kodierinfo was wrong "+f'{kodierCounter}'+" times")
    else:
        print("GRA_Kodierinfo PASS")
    if senderCounter >= 1000:
        print("GRA_Sender was wrong "+f'{senderCounter}'+" times")
    else:
        print("GRA_Sender PASS")
    if staACCCounter >= 1000:
        print("mACC_GRA_Anziege was wrong "+f'{staACCCounter}'+" times")
    else:
        print("mACC_GRA_Anziege PASS")
    if accSystemCounter <= 1000:
        print("mACC_System FAIL, MSG MISSING")
    else:
        print("mACC_System PRESENT")
    if ststinfoCounter <= 1000 and accSystemCounter >= 1000:
        print("ACS_StSt_Info was wrong "+f'{ststinfoCounter}'+" times")
    if ststinfoCounter >= 1000:
        print("ACS_StSt_Info PASS")