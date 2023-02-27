import time
import csv
outOfEnvironment = False
try:
    from panda import Panda
    p = Panda()
except:
    outOfEnvironment = True

if not outOfEnvironment:
    w = open('benchtestResults.csv', 'w')
    writer = csv.writer(w)

# addr, data, bus
# can 0 is our feed data onto CAR PT can
# can 1 is our gateway receive can
# can 2 is our extended receive can
# (0, 1, 2) for RX, (128, 129, 130) for TX
# hex(int(row[1], 16)) <- solution for hex data fed to panda if it doesnt like str data

with open('ocelot_j533-testData.csv', 'r') as testData:
    reader = csv.reader(testData)
    if outOfEnvironment:
        for row in reader:
            addr = hex(int(row[0]))
            dat = str(row[1])
            if int(row[0]) == 1386:
                print(addr, f'"{dat}"', 2)
            if int(row[0]) == 906:
                print(addr, f'"{dat}"', 1)
            else:
                print(addr, f'"{dat}"', 0)    
    else:
        p.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
        for row in reader:
            p.can_clear(0xFFFF)
            addr = hex(int(row[0]))
            dat = str(row[1])
            if int(row[0]) == 1386:
                p.can_send(addr, f'"{dat}"', 2)
            if int(row[0]) == 906:
                p.can_send(addr, f'"{dat}"', 1)
            else:
                p.can_send(addr, f'"{dat}"', 0)
            can_recv = p.can_recv()
            time.sleep(0.008) #120ish hz
            if len(can_recv) > 0:
                writer.writerow(can_recv)
        for i in range(500):        # We should see all can activity from ocelot shut off after 2 seconds
            can_recv = p.can_recv()
            time.sleep(0.01) #100hz
            writer.writerow(can_recv)