import time
import csv
from panda import Panda
p = Panda()

f = open('benchtestResults.csv', 'w')
writer = csv.writer(f)

# addr, data, bus
# can 0 is our feed data onto CAR PT can
# can 1 is our gateway receive can
# can 2 is our extended receive can
# (0, 1, 2) for RX, (128, 129, 130) for TX

while True:
    p.can_clear(0xFFFF)
    p.set_safety_mode(Panda.SAFETY_ALLOUTPUT)
    # GRA_Neu SETCRUISE
    p.can_send(0x38a, "0d010c00", 0)
    p.can_send(0x38a, "2d012c00", 0)
    # Motor_2
    p.can_send(0x288, "327f300400536600", 0)
    p.can_send(0x288, "327f200400536600", 0)
    p.can_send(0x38a, "2d012c04", 0)
    # Bremse_3
    p.can_send(0x4A0, "b804ba04aa04b604", 0)
    p.can_send(0x4A0, "60045e044e045c04", 0)

    # GRA_Neu LEVEL CANCEL
    p.can_send(0x38a, "0d010c00", 0)
    p.can_send(0x38a, "2d012c00", 0)
    # Motor_2
    p.can_send(0x288, "327f300400536600", 0)
    p.can_send(0x288, "327f200400536600", 0)
    p.can_send(0x38a, "2d112c00", 0)
    # Bremse_3
    p.can_send(0x4A0, "b804ba04aa04b604", 0)
    p.can_send(0x4A0, "60045e044e045c04", 0)

    can_recv = p.can_recv()
    time.sleep(0.01)
    if len(can_recv) > 0:
        writer.writerow(can_recv)