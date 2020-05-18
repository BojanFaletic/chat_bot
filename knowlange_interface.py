import json
from state_machine import state_machine


class knowledge_interface:

    def __init__(self):
        self.knowledge = {}
        self.sm = state_machine(3)

    def add_ref_key(self, key):
        if self.sm.state == 0:
            self.tmp_kn = {key: {'ask': [], 'answer': []}}
            self.sm.next_state()
            return True
        else:
            return False

    def add_question(self, question):
        if self.sm.state == 1:
            if isinstance(question, (list, str)):
                if isinstance(question, (str)):
                    question = [question]
                key = list(self.tmp_kn)[0]
                self.tmp_kn[key]['ask'] += question
                self.sm.next_state()
                return True
        return False

    def add_answer(self, answer):
        if self.sm.state == 2:
            if isinstance(answer, (list, str)):
                if isinstance(answer, (str)):
                    answer = [answer]
                key = list(self.tmp_kn)[0]
                self.tmp_kn[key]['answer'] += answer
                
                self.knowledge.update(self.tmp_kn)

                self.sm.next_state()
                return True
        return False



'''
test

kn = knowledge_interface()

kn.add_ref_key('potato')
kn.add_question('price of potato')
kn.add_answer('price is 35 dolars')

kn.add_ref_key('bird')
kn.add_question('price of bird')
kn.add_answer('price is 20 dolars')


print(kn.knowledge)
'''