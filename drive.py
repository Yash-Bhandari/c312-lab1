
#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MoveSteering, OUTPUT_A, OUTPUT_D, MoveTank

tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

def main():
    # Using readlines()
    file1 = open('Lemniscate.txt', 'r')
    Lines = file1.readlines()

    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        v_l, v_r, TimeStep = line.split(' ')
        tank_drive.on_for_seconds(v_l, v_r, TimeStep[:-1])


if __name__ == "__main__":
    main()
