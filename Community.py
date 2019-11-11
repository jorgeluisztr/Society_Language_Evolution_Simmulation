from Agent import Agent


class Community:

    def __init__(self, numagents, wordlist, kobj, memorylimit):

        agent_list = []

        for i in range(numagents):
            agent_list.append(Agent(wordlist=wordlist, kobj=kobj, memorylimit=memorylimit))

        self.agents = agent_list

        steady_words = []

        for i in range(kobj):
            steady_words.append(False)

        self.numobj = kobj
        self.steady_words = steady_words
        self.forbiden = {}
        self.steady_state = False
        self.num_steady = 0
        self.steady_time = "not steady yet"


    def check_steady_state(self, nobj):

        counter = 0
        ele = self.agents[0].objs[nobj]

        for age in self.agents:
            if ele == age.objs[nobj]:
                counter += 1

        if counter == len(self.agents):
            return True

        else:
            return False

    def one_step_steady(self, nobj, t):

        if not self.steady_words[nobj]:
            self.num_steady += 1
            self.steady_words[nobj] = True
            if self.num_steady == self.numobj:
                self.steady_state = True
                self.steady_time = t

