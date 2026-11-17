import os

import numpy as np
import pytest

from src.algorithms.ant_system import BasicAntSystem
from src.algorithms.as_rank import ASRank
from src.algorithms.greedy import GreedyCVRPSolver
from src.algorithms.mmas import MMAS
from src.parser import parse_sol_file, parse_vrp_file
from src.utils import (calculate_all_routes_distance, calculate_distance_matrix, calculate_route_distance,
                       calculate_s_max_from_bks, parse_parameters_from_filename)

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
INSTANCE = 'A-n32-k5'


@pytest.fixture(scope='module')
def problem():
    instance = parse_vrp_file(os.path.join(DATA_DIR, f'{INSTANCE}.vrp'))
    bks = parse_sol_file(os.path.join(DATA_DIR, f'{INSTANCE}.sol'))
    distance_matrix = calculate_distance_matrix(instance)
    n, k = parse_parameters_from_filename(f'{INSTANCE}.vrp')
    s_max = calculate_s_max_from_bks(instance, bks.routes, distance_matrix, 1.25)
    return instance, bks, distance_matrix, n, k, s_max


def assert_feasible(solution, instance, distance_matrix, k, s_max):
    depot = instance.depot_id - 1
    served = [node for route in solution.routes for node in route]
    # every customer exactly once, the depot never inside a route
    assert sorted(served) == [i for i in range(instance.dimension) if i != depot]
    assert len(solution.routes) <= k
    for route in solution.routes:
        assert instance.demands[route].sum() <= instance.capacity
        assert calculate_route_distance(route, distance_matrix) <= s_max + 1e-9
    # the reported distance is the real length of the routes, including the way back to the depot
    assert solution.total_distance == pytest.approx(calculate_all_routes_distance(solution.routes, distance_matrix))


def test_parser_reads_instance_and_best_known_solution(problem):
    instance, bks, distance_matrix, n, k, _ = problem
    assert (instance.dimension, instance.capacity, instance.depot_id) == (32, 100, 1)
    assert (n, k) == (32, 5)
    assert len(bks.routes) == 5
    assert bks.total_distance == 784
    # the instance uses rounded Euclidean distances, so the BKS cost matches up to rounding
    assert calculate_all_routes_distance(bks.routes, distance_matrix) == pytest.approx(784, abs=10)


def test_greedy_returns_a_feasible_solution(problem):
    instance, _, distance_matrix, _, k, s_max = problem
    solution = GreedyCVRPSolver(instance, distance_matrix, s_max, k).solve()
    assert_feasible(solution, instance, distance_matrix, k, s_max)


def test_greedy_reports_infeasible_when_vehicles_run_out(problem):
    instance, _, distance_matrix, _, _, s_max = problem
    solution = GreedyCVRPSolver(instance, distance_matrix, s_max, 1).solve()
    assert solution.total_distance == float('inf')


@pytest.mark.parametrize('solver_class', [BasicAntSystem, MMAS, ASRank])
def test_aco_returns_a_feasible_solution_better_than_greedy(problem, solver_class):
    instance, _, distance_matrix, n, k, s_max = problem
    np.random.seed(1)
    params = {'iterations': 30, 'num_ants': n, 'alpha': 1.0, 'beta': 4.0, 'rho': 0.5,
              's_max': s_max, 'num_vehicles': k, 'w_rank': 6, 'record_history': True}
    solution = solver_class(instance, distance_matrix, params).solve()

    assert_feasible(solution, instance, distance_matrix, k, s_max)
    greedy = GreedyCVRPSolver(instance, distance_matrix, s_max, k).solve()
    assert solution.total_distance < greedy.total_distance
    # the best cost found so far never gets worse
    assert len(solution.iteration_history) == 30
    assert all(a >= b for a, b in zip(solution.iteration_history, solution.iteration_history[1:]))


def test_aco_reports_infeasible_instead_of_zero(problem):
    instance, _, distance_matrix, n, _, s_max = problem
    np.random.seed(1)
    params = {'iterations': 3, 'num_ants': 5, 'alpha': 1.0, 'beta': 4.0, 'rho': 0.5,
              's_max': s_max, 'num_vehicles': 1}
    solution = MMAS(instance, distance_matrix, params).solve()
    assert solution.total_distance == float('inf')
    assert solution.routes == []
