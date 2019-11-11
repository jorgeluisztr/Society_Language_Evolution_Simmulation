import numpy as np


def words(n):
    wordlist = []
    for i in range(n):
        wordlist.append("w" + str(i))

    return wordlist


def objects(k, wordlist):
    objlist = []
    objects = np.random.choice(wordlist, replace=False, size=k)
    for i in range(len(objects)):
        objlist.append(objects[i])

    return objlist


class Agent:

    def __init__(self, wordlist, kobj, memorylimit):

        """

        :param wordlist: list of the available words
        :param kobj: number of name objects by the agent
        :param memorylimit: max number of name-objects that an agent could safe in memory
        """

        self.objs = objects(kobj, words(wordlist))

        memory = []

        for i in range(len(self.objs)):
            memory.append({self.objs[i]: None})

        self.memory = memory
        self.memorylimit = memorylimit
        self.prohibidas = {}

    def word_at_steady_steady_state(self, nobj, word_st, word_bag_steady_state, wordlist):

        """

        :param nobj: number of the object
        :param word_st: word at steady state
        :param word_bag_steady_state: dictionary of words at steady state
        :param wordlist: list of words avalaible
        :return:
        """

        other_objects = np.arange(len(self.objs)).tolist()
        other_objects.remove(nobj)

        for i in other_objects:

            # delete the word at steady state for an object from other possible name-objects
            if word_st in self.memory[i]:
                del (self.memory[i][word_st])
                while self.memory[i] == {}:
                    ele = objects(1, words(wordlist))
                    if ele[0] not in word_bag_steady_state:
                        self.memory[i] = {ele[0]: None}

            # in case of an another object has the same name, take another posible name
            if self.objs[i] == word_st:
                # take another word from memory
                self.objs[i] = np.random.choice(list(self.memory[i].keys()), replace=False, size=1)[0]

    def internal_communication(self, neighbor, nobj):

        """

        :param neighbor: internal neighbor
        :param nobj: number of the object to share
        :return:
        """

        # if the two agents has the same name object then update
        if self.objs[nobj] in neighbor.memory[nobj]:

            # update the object name of the neighbor
            neighbor.objs[nobj] = self.objs[nobj]
            # delete another names from the neighbor's memory
            neighbor.memory[nobj] = {neighbor.objs[nobj]: None}

        # if the two agents has different names for the object the neighbor will keep the name of the agent in its memory
        else:
            # check the steady state words is VERY IMPORTANT
            # add the word in its memory

            neighbor.memory[nobj][self.objs[nobj]] = None

            if len(neighbor.memory[nobj]) > neighbor.memorylimit:
                neighbor.memory[nobj] = {self.objs[nobj]: None}

    def external_communication(self, external_agent,  nobj):

        """

        :param external_agent: external agent
        :param nobj:
        :return: number of the object to share
        """

        if self.objs[nobj] in external_agent.memory[nobj]:

            # update the object name of the external agent
            external_agent.objs[nobj] = self.objs[nobj]
            # delete another names from the external agent's memory
            external_agent.memory[nobj] = {external_agent.objs[nobj]: None}

        else:

            external_agent.memory[nobj][self.objs[nobj]] = None

            if len(external_agent.memory[nobj]) > external_agent.memorylimit:
                external_agent.memory[nobj] = {self.objs[nobj]: None}
