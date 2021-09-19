from __future__ import annotations  # prevents NameErrors for typing
from typing import Dict, Tuple, List

import networkx as nx

Interview = Tuple[str, str]
InterviewTime = Dict[Interview, str]


class Scheduler:
    """Class used to schedule interviews

    Parameters
    ----------
    c_availability: Dict[str, list]
        A dictionary of candidates' availability to interview with the format:
        {"CandidateA": ["Time1", "Time2", "Time3"]}
    p_availability: Dict[str, list]
        A dictionary of partners' availability to interview with the format:
        {"PositionA": ["Time1", "Time2", "Time3"]}
    interviews: Dict[str, list]
        A list of interviews to schedule with the following format:
        {"PositionA": ["CandidateA", "CandidateB", "CandidateC"]}
    """

    def __init__(
        self,
        c_availability: Dict[str, list],
        p_availability: Dict[str, list],
        interviews: List[tuple],
    ) -> None:
        """Inits the Interviews class"""
        self.c_availability = c_availability
        self.p_availability = p_availability
        self.candidates = list(c_availability.keys())
        self.positions = list(p_availability.keys())

        self.interviews = []
        for p, matches in interviews.items():
            for c in matches:
                self.interviews.append((p, c))

        # set by self.schedule_interviews()
        self.G: nx.DiGraph = None
        self.scheduled: InterviewTime = {}
        self.unscheduled: List[Interview]

    def schedule_interviews(self):
        """Assign interviews to time slots depending on mutual availability"""
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
        c_edges = [
            (c, i) for i in c_interviews for c in c_times if i[1][1] == c[0]
        ]
        p_edges = [
            (i, p) for i in p_interviews for p in p_times if i[0][0] == p[0]
        ]
        i_edges = [(("c", i), (i, "p")) for i in interviews]
        t_edges = [(p, "t") for p in p_times]

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
        flow_dict = nx.maximum_flow(G, "s", "t")[1]
        scheduled = {}
        for i in interviews:
            for time, flow in flow_dict[(i, "p")].items():
                if flow > 0:
                    scheduled[i] = time[1]
        unscheduled = [i for i in interviews if i not in scheduled.keys()]

        self.G = G
        self.scheduled = scheduled
        self.unscheduled = unscheduled
