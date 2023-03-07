from panda import Panda
p = Panda()

p.can_send(0x38A, "ed01ec00", 1)
can_recv = p.can_recv()
print(can_recv)