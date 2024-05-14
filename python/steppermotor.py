from machine import Pin
from stepcontrol import StepControl
import time

NUM_WIRES=4

class StepperMotor:

    def __init__(self, name, pins, stop_pin, digit_steps):
        self.pins = [Pin(p, Pin.OUT) for p in pins]
        self.stop_pin = Pin(stop_pin, Pin.IN)
        self.name = name
        self.digit_steps = digit_steps
        self.steps_to_move = 0
        self.current_stop_value = False
        self.step_control = None
        self.current_step = 1000000

    def step_until_condition(self, stop_value, step_delay, reverse=False):
        num_steps = 0
        while self.stop_pin.value() != stop_value:
            self.step_one(reverse)
            num_steps += 1
            time.sleep(step_delay)

        return num_steps

    def move_steps(self, num_steps, step_delay, reverse = False):
        while num_steps > 0:
            self.step_one(reverse)
            num_steps -= 1
            time.sleep(step_delay)

    def reset(self, step_delay):
        self.step_control = None
        self.step_until_condition(True, step_delay, False)
        self.step_until_condition(False, step_delay, False)
        gap_steps = self.step_until_condition(True, step_delay, False)

        return_steps = self.step_until_condition(False, step_delay, True)
        return_steps += self.step_until_condition(True, step_delay, True)

        slack_steps = return_steps - gap_steps

        self.step_until_condition(False, step_delay)
        self.step_until_condition(True, step_delay)
        step_counter = self.step_until_condition(False, step_delay)

        steps_per_rotation = gap_steps + step_counter

        print("CALIBRATION ROTATION : ", steps_per_rotation, "GAP: ", gap_steps, "SLACK: ", slack_steps)

        self.step_control = StepControl(self.digit_steps, steps_per_rotation, gap_steps, slack_steps)

    def step_one(self, reverse = False):
        step = self.current_step % NUM_WIRES
        for i in range(NUM_WIRES):
            on = (step == i or step == (i+1) % NUM_WIRES )
            self.pins[i].value(step == i) ### NB ###

        if reverse:
            self.current_step -= 1
        else:
            self.current_step += 1

        if self.step_control is not None:
            if reverse: self.step_control.dec_step()
            else : self.step_control.inc_step()

            new_stop_value = bool(self.stop_pin.value()) 
            if new_stop_value != self.current_stop_value:
                self.step_control.sync(self.name, new_stop_value, reverse)
                self.current_stop_value = new_stop_value

    def set_target_digit(self, tgt):

        if self.steps_to_move != 0:
            print("DENIED", tgt)
            return

        self.steps_to_move = self.step_control.calculate_steps_to(tgt)
        print(self.name, self.steps_to_move, tgt)

    def step_to_target(self):
        if self.steps_to_move > 0:
            self.step_one(False)
            self.steps_to_move -= 1
        elif self.steps_to_move < 0:
            self.step_one(True)
            self.steps_to_move += 1
        else:
            return True

        return False

    def step_to_destination(self, step_delay):
        while not self.step_to_target():
            time.sleep(step_delay)