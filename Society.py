import numpy as np
from Community import Community


class Society:

    def __init__(self, ncom, nage, wordlist, kobj, memorylimit, probinternal):
        """

        :param ncom: Number of Comunities of the society
        :param nage: Number of Agents Per Comunity
        :param wordlist: Number of avalaible words
        :param kobj: Number of Name-Objects per Agent
        :param memorylimit: Number of Max Word save per Agent in the Memory
        :param probinternal: Probability of Comunication Intra-Comunity
        """
        
        comlist = []
        steady_comunities = []

        for i in range(ncom):
            comlist.append(Community(numagents=nage, wordlist=wordlist, kobj=kobj, memorylimit=memorylimit))
            steady_comunities.append(False)

        self.comunities = comlist
        self.numcom = ncom
        self.numage = nage
        self.numobj = kobj
        self.prob = probinternal
        self.numword = wordlist
        self.steady_state = False
        self.num_steady = 0
        self.steady_communities = steady_comunities
        self.steady_time = "not steady yet"

    def one_step_steady(self, comunity, t):

        if not self.steady_communities[comunity]:
            self.num_steady += 1
            self.steady_communities[comunity] = True
            if self.num_steady == self.numcom:
                self.steady_state = True
                self.steady_time = t

    def interact(self, t):

        # print("running {0}".format(t))

        for i in range(self.numobj):

            for c in range(self.numcom):

                if self.steady_state:
                    break

                else:

                    for a in range(self.numage):

                        # Take a type of communication based in probability of internal communication
                        val = np.random.choice(["internal", "external"], 1, p=[self.prob, 1 - self.prob])

                        if val == "internal":

                            # Take a neighbor randomly
                            neighbors = np.arange(self.numage).tolist()
                            neighbors.remove(a)
                            nb = np.random.choice(neighbors, replace=False, size=1)[0]

                            # Start Communication with this neighbor nb
                            self.comunities[c].agents[a].internal_communication(self.comunities[c].agents[nb], i)

                            # Update for Steady State
                            if self.comunities[c].check_steady_state(i):

                                self.comunities[c].forbiden[self.comunities[c].agents[a].objs[i]] = None
                                # define a la palabra convergencia y quedate solo con el primer tiempo de convergencia
                                self.comunities[c].one_step_steady(i, t)

                                for neig in range(self.numage):
                                    self.comunities[c].agents[neig].word_at_steady_steady_state(i,
                                                                                         self.comunities[c].agents[neig].objs[i],
                                                                                         self.comunities[c].forbiden,
                                                                                         self.numword)

                                if self.comunities[c].steady_state:
                                    self.one_step_steady(c, t)

                        else:

                            comunidad_vecina = np.arange(self.numcom).tolist()
                            comunidad_vecina.remove(c)
                            v_com = np.random.choice(comunidad_vecina, replace=False, size=1)[0]

                            # Se la otra comunidad ya convergio en ese objeto ya no escucha
                            if not self.comunities[v_com].steady_words[i]:
                                vec_ext = np.random.choice(np.arange(self.numage), replace=False, size=1)[0]
                                self.comunities[c].agents[a].external_communication(
                                    self.comunities[v_com].agents[vec_ext], i)
