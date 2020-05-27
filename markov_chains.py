import numpy as np

# markov chain implementation
class Markov_chain:
    def __init__(self, transition_prob):
        self.transition_prob = transition_prob
        self.states = list(transition_prob.keys())

    # return next state
    def next_state(self, current_state):
        return np.random.choice(self.states,
                                p=[self.transition_prob[current_state][next_state] for next_state in self.states])

    # generate sequence of n future states 
    def generate_states(self, current_state, no=10):
        future_states = []
        for _ in range(no):
            next_state = self.next_state(current_state)
            future_states.append(next_state)
            current_state = next_state
        return future_states



''' 
test
transition_prob = {
    'Sunny': {'Sunny': 0.8,
              'Rainy': 0.19,
              'Snowy': 0.01},
    'Rainy': {'Sunny': 0.2,
              'Rainy': 0.7,
              'Snowy': 0.1},
    'Snowy': {'Sunny': 0.1,
              'Rainy': 0.2,
              'Snowy': 0.7},
}

wather_chain = Markov_chain(transition_prob=transition_prob)
print(
  wather_chain.next_state(current_state='Sunny')
)
'''
