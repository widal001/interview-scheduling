from pprint import pprint

import networkx as nx


class Scheduler:
    def __init__(self, c_availability, p_availability, interviews):
        self.c_availability = c_availability
        self.p_availability = p_availability
        self.candidates = list(c_availability.keys())
        self.positions = list(p_availability.keys())
        self.interviews = []

        for p, matches in interviews.items():
            for c in matches:
                self.interviews.append((p, c))

    def schedule_interviews(self):
        # get variables
        c_availability = self.c_availability.items()
        p_availability = self.p_availability.items()
        interviews = self.interviews

        # creating lists for time nodes and edges
        c_times = [(c, t) for c, times in c_availability for t in times]
        p_times = [(p, t) for p, times in p_availability for t in times]
        c_interviews = [("c", i) for i in interviews]
        p_interviews = [(i, "p") for i in interviews]
        s_edges = [("s", c) for c in c_times]
        i_edges = [(("c", i), (i, "p")) for i in interviews]
        t_edges = [(p, "t") for p in p_times]

        # connects a candidate's time slots to their interviews
        # based on mutual availability with the interviewing partner
        c_edges = []
        for i in c_interviews:
            candidate = i[1][1]
            p = i[1][0]
            for c in c_times:
                time = c[1]
                if candidate == c[0] and time in self.p_availability[p]:
                    c_edges.append((c, i))

        # connects a partner's time slots to their interviews
        # based on mutual availability with the interviewing candidate
        p_edges = []
        for i in p_interviews:
            position = i[0][0]
            c = i[0][1]
            for p in p_times:
                time = p[1]
                if position == p[0] and time in self.c_availability[c]:
                    p_edges.append((i, p))

        pprint(c_edges)
        pprint(p_edges)

        # initialize the graph
        G = nx.DiGraph()

        # add nodes
        G.add_nodes_from(c_times)  # candidate availability partition
        G.add_nodes_from(p_times)  # partner availability partition
        G.add_nodes_from(c_interviews)  # interviews partition
        G.add_nodes_from(p_interviews)
        G.add_nodes_from(["s", "t"])  # source and sink nodes

        # add edges
        G.add_edges_from(s_edges)  # ensures no candidates are double booked
        G.add_edges_from(t_edges)  # ensures no partners are double booked
        G.add_edges_from(c_edges)  # connects c_availability to interviews
        G.add_edges_from(p_edges)  # connects interviews to p_availability
        G.add_edges_from(i_edges)  # ensures no interview is scheduled twice

        # assign graph capacity
        nx.set_edge_attributes(G, 1, "capacity")

        # run the flow and retrieve the matches
        flow_val, flow_dict = nx.maximum_flow(G, "s", "t")
        scheduled = {}
        for i in interviews:
            for time, flow in flow_dict[(i, "p")].items():
                if flow > 0:
                    scheduled[i] = time[1]
        unscheduled = [i for i in interviews if i not in scheduled.keys()]

        self.G = G
        self.scheduled = scheduled
        self.unscheduled = unscheduled
