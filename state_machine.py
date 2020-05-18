
class state_machine:
    def __init__(self, num_of_states):
        self.cur_state = 0
        self.total_num_of_states = num_of_states

    def next_state(self):
        self.cur_state += 1
        if self.total_num_of_states == self.cur_state:
            self.cur_state = 0

    @property
    def state(self):
        return self.cur_state


