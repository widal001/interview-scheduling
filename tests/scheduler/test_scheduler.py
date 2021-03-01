from pprint import pprint

from utils.scheduler import Scheduler
from tests.scheduler.scheduler_data import (
    INTERVIEWS,
    AVAIAILABILITY,
    SCHEDULE,
)


class TestInit:
    def test_init(self):
        # setup
        c_availability = AVAIAILABILITY["candidates"]
        p_availability = AVAIAILABILITY["positions"]
        candidates = ["Alice", "Bob", "Charlie"]
        positions = ["Position 1", "Position 2", "Position 3"]
        schedule = SCHEDULE
        interviews = list(schedule.keys())

        # execution
        s = Scheduler(c_availability, p_availability, INTERVIEWS)

        print("EXPECTED")
        pprint(interviews)
        print("ACTUAL")
        pprint(s.interviews)
        print(interviews == s.interviews)

        # validation
        assert s.c_availability == c_availability
        assert s.p_availability == p_availability
        assert s.candidates == candidates
        assert s.positions == positions
        assert set(s.interviews) == set(interviews)


class TestScheduleInterviews:
    def test_complete(self):

        # setup
        c_availability = AVAIAILABILITY["candidates"]
        p_availability = AVAIAILABILITY["positions"]
        schedule = SCHEDULE

        # execution
        s = Scheduler(c_availability, p_availability, INTERVIEWS)
        s.schedule_interviews()

        print("SCHEDULED")
        pprint(s.scheduled)
        print("GRAPH")

        # validation
        assert s.scheduled == schedule
        assert s.unscheduled == []
