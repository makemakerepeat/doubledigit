from machine import Pin
STEPS_PER_ROTATION = 2048
NUM_WIRES = 4

class StepperMotor:

    def __init__(self, name, pins, stop_pin, digit_steps, steps_per_rotation = STEPS_PER_ROTATION):
        self.pins = [Pin(p, Pin.OUT) for p in pins]
        self.stop_pin = Pin(stop_pin, Pin.IN)
        self.name = name
        self.current_step = 0
        self.digit_steps = digit_steps
        self.num_digit_steps = len(digit_steps)
        self.target_step = 0
        self.steps_per_digit = steps_per_rotation / self.num_digit_steps

    def step_one(self):

        step = self.current_step % NUM_WIRES
        for i in range(NUM_WIRES):
            on = (step == i or step == (i+1))
            if step == 3 and i == 0 : on = True

            self.pins[i].value(step == i)
        self.current_step += 1

    def step_if_zero(self):

        if self.stop_pin.value():
            return True

        self.step_one()
        return False

    def step_if_non_zero(self):
        
        if not self.stop_pin.value():
            return True

        self.step_one()
        return False

    def set_zero(self):
        self.current_step = 0
        self.target_step = 0

    def set_target_digit(self, tgt):

        current_digit_index = int(self.current_step // self.steps_per_digit)
        next_index = current_digit_index

        while next_index < self.num_digit_steps:
            if self.digit_steps[next_index] == tgt:
                break
            next_index += 1

        if next_index >= self.num_digit_steps:
            self.target_step = 0
        else:
            self.target_step = int(next_index * self.steps_per_digit)

        print("NEW TARGET", self.name, current_digit_index, next_index, self.current_step, self.target_step)

    def step_to_target(self):
        if self.target_step == 0:
            if not self.stop_pin.value():
                if self.current_step != 0:
                    print("ROT", self.current_step )
                self.current_step = 0
                return True
            else:
                self.step_one()
        else:
            if self.current_step < self.target_step:
                self.step_one()
            else:
                return True

        return False 
