from constants import FWD, BWD

class StepControl:

    def __init__(self, digits, steps_per_rotation, gap_steps, slack_steps):
        self.steps_per_rotation = steps_per_rotation
        self.gap_steps = gap_steps
        self.slack_steps = slack_steps
        self.digits = digits
        self.num_digits = len(digits)
        self.steps_per_digit = steps_per_rotation / self.num_digits
        self.current_direction = FWD
        self.current_step = 0
        self.current_digit_index = 0
        self.ignore_steps = 0

    def sync(self, name, new_stop_value, reverse):
        if not new_stop_value:
            if reverse:
                new_current_step = self.gap_steps
            else:
                new_current_step = 0 
        else:
            if reverse:
                new_current_step = 0 
            else:
                new_current_step = self.gap_steps
        print("CORR P", name, self.current_step, "N", new_current_step)
        self.current_step = new_current_step

    def inc_step(self):
        if self.ignore_steps > 0:
            self.ignore_steps -= 1
            return

        self.current_step += 1
        while self.current_step > self.steps_per_rotation:
            self.current_step -= self.steps_per_rotation

    def dec_step(self):
        if self.ignore_steps > 0:
            self.ignore_steps -= 1
            return
            
        self.current_step -= 1
        while self.current_step < 0:
            self.current_step += self.steps_per_rotation

    def find_target_index(self, target, start_index, direction):
        dist = 0
        index = start_index
        num_total_steps = 0

        while self.digits[index] != target:
            dist += 1
            index += direction

            if index < 0:
                index = self.num_digits - 1
            if index >= self.num_digits:
                index = 0

            num_total_steps += 1

            if num_total_steps > self.num_digits:
                raise ValueError("Target does not exist" + str(target))

        return index, dist

    def calculate_steps_to(self, target_digit):
        current_digit_index = self.current_digit_index
        next_index_fwd, fwd_dist = self.find_target_index(target_digit, self.current_digit_index, 1)
        next_index_bwd, bwd_dist = self.find_target_index(target_digit, self.current_digit_index, -1)

        print("B", next_index_bwd, "F", next_index_fwd, "FD", fwd_dist, "BD", bwd_dist)

        next_index = next_index_fwd if fwd_dist < bwd_dist else next_index_bwd
        target_step = next_index * self.steps_per_digit

        steps_to_move = target_step - self.current_step

        if steps_to_move < 0 and abs(steps_to_move) > self.steps_per_rotation /2:
            steps_to_move = self.steps_per_rotation + steps_to_move
        elif steps_to_move > 0 and steps_to_move > self.steps_per_rotation /2:
            steps_to_move = -(self.steps_per_rotation - steps_to_move)

        # if steps_to_move < 0:
        #     steps_to_move = self.steps_per_rotation + steps_to_move
        
        steps_to_move = int(round(steps_to_move))
        self.ignore_steps = 0
        if steps_to_move > 0 and self.current_direction == BWD:
            steps_to_move += self.slack_steps
            self.ignore_steps = self.slack_steps
            self.current_direction = FWD
        elif steps_to_move < 0 and self.current_direction == FWD:
            steps_to_move -= self.slack_steps
            self.ignore_steps = self.slack_steps
            self.current_direction = BWD
        self.current_digit_index = next_index
        return steps_to_move
