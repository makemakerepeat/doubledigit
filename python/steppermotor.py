from machine import Pin
import time
DEFAULT_STEPS_PER_ROTATION = 2048
NUM_WIRES = 4
MIDPOINT_POSITION = 10000

class StepperMotor:

    def __init__(self, name, pins, stop_pin, digit_steps, steps_per_rotation = DEFAULT_STEPS_PER_ROTATION):
        self.pins = [Pin(p, Pin.OUT) for p in pins]
        self.stop_pin = Pin(stop_pin, Pin.IN)
        self.name = name
        self.current_step = MIDPOINT_POSITION
        self.digit_steps = digit_steps
        self.num_digit_steps = len(digit_steps)
        self.target_step = 0
        self.steps_per_rotation = steps_per_rotation
        self.steps_per_digit = steps_per_rotation / self.num_digit_steps
        self.gap_stepes = 40
        
        self.current_digit = None
        self.current_digit_index = None

        self.current_stop_value = False
        self.is_initialized = False

    def step_until_condition(self, stop_value, step_delay):
        num_steps = 0
        while self.stop_pin.value() != stop_value:
            self.step_one()
            num_steps += 1
            time.sleep(step_delay)

        return num_steps

    def move_steps(self, num_steps, step_delay):
        while num_steps > 0:
            self.step_one()
            num_steps -= 1
            time.sleep(step_delay)

    def reset(self, step_delay):
        print(self.name, "POS 1")
        self.step_until_condition(True, step_delay)
        print(self.name, "POS 2")
        self.step_until_condition(False, step_delay)

        print("EDGE FOUND")
        print(self.name, "POS 3")
        gap_counter = self.step_until_condition(True, step_delay)

        print("GAP COUNT", gap_counter)
        print(self.name, "POS 4")
        step_counter = self.step_until_condition(False, step_delay)
        print("DISC COUNT", step_counter)
        print("TOTAL", gap_counter, "+", step_counter, "=", gap_counter + step_counter)

        self.steps_per_rotation = gap_counter + step_counter
        self.steps_per_digit = self.steps_per_rotation / self.num_digit_steps
        self.gap_stepes = gap_counter
        self.current_stop_value = bool(self.stop_pin.value()) 

        for _ in range(self.gap_stepes // 2):
            self.step_one()
            time.sleep(step_delay)
        self.set_zero()

    def step_one(self, reverse = False):
        if reverse:
            self.current_step -= 1
        else:
            self.current_step += 1

        step = self.current_step % NUM_WIRES
        for i in range(NUM_WIRES):
            on = (step == i or step == (i+1) % NUM_WIRES )
            self.pins[i].value(step == i) ### NB ###

        if self.is_initialized:
            new_stop_value = bool(self.stop_pin.value()) 
            if new_stop_value != self.current_stop_value:
                old_csv = self.current_step
                if new_stop_value:
                    if reverse:
                        new_current_step = MIDPOINT_POSITION - self.gap_stepes // 2
                    else:
                        new_current_step = MIDPOINT_POSITION + self.gap_stepes // 2
                else:
                    if reverse:
                        new_current_step = MIDPOINT_POSITION + self.gap_stepes // 2
                    else:
                        new_current_step = MIDPOINT_POSITION - self.gap_stepes // 2
                print("CORRECTION", self.name, old_csv, new_current_step)
                self.current_stop_value = new_stop_value

    def set_zero(self):
        self.current_step = MIDPOINT_POSITION
        self.target_step = MIDPOINT_POSITION
        self.current_digit_index = 0
        self.current_digit = 0
        self.is_initialized = True

    # def index_from_current_step(self):
    #     current_digit_index = int((self.current_step + 1 - MIDPOINT_POSITION) // self.steps_per_digit)
    #     while current_digit_index < 0:
    #         current_digit_index += self.num_digit_steps

    #     while current_digit_index >= self.num_digit_steps:
    #         current_digit_index -= self.num_digit_steps

    #     return current_digit_index

    def find_target_index(self, target, start_index, direction):

        dist = 0
        index = start_index
        num_total_steps = 0

        while self.digit_steps[index] != target:
            dist += 1
            index += direction

            if index < 0:
                index = self.num_digit_steps - 1
            if index >= self.num_digit_steps:
                index = 0

            num_total_steps += 1

            if num_total_steps > self.num_digit_steps:
                raise ValueError("Target does not exist" + str(target))

        return index, dist

    def set_target_digit(self, tgt):

        if self.target_step != self.current_step:
            print("DENIED", tgt)
            return

        current_digit_index = self.current_digit_index
        next_index_fwd, fwd_dist = self.find_target_index(tgt, current_digit_index, 1)
        next_index_bwd, bwd_dist = self.find_target_index(tgt, current_digit_index, -1)
        next_index = next_index_fwd if fwd_dist < bwd_dist else next_index_bwd

        neg = int(bwd_dist * self.steps_per_digit)
        pos = int(fwd_dist * self.steps_per_digit)

        if neg < pos:
            self.target_step = self.current_step - neg
        else:
            self.target_step = self.current_step + pos

        self.current_digit_index = next_index
        self.current_digit = tgt

        # print("PN", pos, neg)
        # print("FWD", next_index_fwd, fwd_dist)
        # print("BWD", next_index_bwd, bwd_dist)
        # print("NEW TARGET", tgt, current_digit_index, next_index, self.target_step)

    def step_to_target(self):
        if self.current_step < self.target_step:
            self.step_one(False)
        elif self.current_step > self.target_step:
            self.step_one(True)
        else:
            return True

        return False

    def step_to_destination(self, step_delay):
        while not self.step_to_target():
            time.sleep(step_delay)