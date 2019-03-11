from cdkkPyGameApp import *

anim = Animation_Counter()
anim.setup(5, ANIMATE_LOOP, 3)
print("--- ANIMATE_LOOP ---")
sequence = [anim.current_image]
for i in range(50):
    anim.next_loop()
    sequence.append(anim.current_image)
print(sequence)

anim.setup(5, ANIMATE_ONCE, 3)
print("--- ANIMATE_ONCE ---")
sequence = [anim.current_image]
for i in range(50):
    anim.next_loop()
    sequence.append(anim.current_image)
print(sequence)

anim.setup(5, ANIMATE_SHUTTLE, 3)
print("--- ANIMATE_SHUTTLE ---")
sequence = [anim.current_image]
for i in range(50):
    anim.next_loop()
    sequence.append(anim.current_image)
print(sequence)

anim.setup(5, ANIMATE_LOOP+ANIMATE_REVERSE, 3)
print("--- ANIMATE_LOOP + ANIMATE_REVERSE ---")
sequence = [anim.current_image]
for i in range(50):
    anim.next_loop()
    sequence.append(anim.current_image)
print(sequence)

anim.setup(5, ANIMATE_SHUTTLE+ANIMATE_REVERSE, 3)
print("--- ANIMATE_SHUTTLE + ANIMATE_REVERSE ---")
sequence = [anim.current_image]
for i in range(50):
    anim.next_loop()
    sequence.append(anim.current_image)
print(sequence)

anim.setup(5, ANIMATE_ONCE+ANIMATE_REVERSE, 3)
print("--- ANIMATE_ONCE + ANIMATE_REVERSE ---")
sequence = [anim.current_image]
for i in range(50):
    anim.next_loop()
    sequence.append(anim.current_image)
print(sequence)

anim.setup(5, ANIMATE_SHUTTLE_ONCE, 3)
print("--- ANIMATE_SHUTTLE_ONCE ---")
sequence = [anim.current_image]
for i in range(50):
    anim.next_loop()
    sequence.append(anim.current_image)
print(sequence)

anim.setup(5, ANIMATE_SHUTTLE_ONCE+ANIMATE_REVERSE, 3)
print("--- ANIMATE_SHUTTLE_ONCE + ANIMATE_REVERSE ---")
sequence = [anim.current_image]
for i in range(50):
    anim.next_loop()
    sequence.append(anim.current_image)
print(sequence)


anim.setup(5, ANIMATE_MANUAL, 3)
print("--- ANIMATE_MANUAL ---")
sequence = [anim.current_image]
for i in range(50):
    anim.next_loop()
    sequence.append(anim.current_image)
print(sequence)

anim.setup(5, ANIMATE_MANUAL+ANIMATE_REVERSE, 3)
print("--- ANIMATE_MANUAL + ANIMATE_REVERSE ---")
sequence = [anim.current_image]
for i in range(50):
    anim.next_loop()
    sequence.append(anim.current_image)
print(sequence)


anim.setup(5, ANIMATE_MANUAL, 3)
print("--- ANIMATE_MANUAL --- 6 Next --- 6 Prev ---")
sequence = [anim.current_image]
for i in range(6):
    anim.next_image()
    sequence.append(anim.current_image)
for i in range(6):
    anim.prev_image()
    sequence.append(anim.current_image)
print(sequence)
