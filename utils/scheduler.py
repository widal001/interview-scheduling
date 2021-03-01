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
        s_edges = [("s", p) for p in p_times]
        t_edges = [(i, "t") for i in interviews]
        time_edges = [
            (p, c)
            for p in p_times
            for c in c_times
            if (p[0], c[0]) in interviews and p[1] == c[1]
        ]
        interview_edges = [(t, i) for i in interviews for t in c_times if i[1] == t[0]]
        pprint(interview_edges)

        # initialize the graph
        G = nx.DiGraph()

        # add nodes
        G.add_nodes_from(c_times)  # candidate availability partition
        G.add_nodes_from(p_times)  # partner availability partition
        G.add_nodes_from(interviews)  # interviews partition
        G.add_nodes_from(["s", "t"])  # source and sink nodes

        # add edges
        G.add_edges_from(s_edges)  # edges from source to partner availability
        G.add_edges_from(t_edges)  # edges from interviews to sink
        G.add_edges_from(time_edges)  # edges between mutually availabile times
        G.add_edges_from(interview_edges)  # edges from candidates to interviews

        # assign graph capacity
        nx.set_edge_attributes(G, 1, "capacity")

        # run the flow and retrieve the matches
        flow_val, flow_dict = nx.maximum_flow(G, "s", "t")
        scheduled = {}
        print("FULL DICT")
        pprint(flow_dict)
        for interview in interviews:
            # print(interview)
            # print(flow_dict[interview])
            for time, flow in flow_dict[interview].items():
                if flow > 0:
                    scheduled[interview] = time[1]
        unscheduled = [i for i in interviews if i not in scheduled.keys()]

        self.G = G
        self.scheduled = scheduled
        self.unscheduled = unscheduled
