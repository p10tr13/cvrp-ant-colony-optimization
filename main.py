import argparse
import os

import numpy as np

from src.algorithms.ant_system import BasicAntSystem
from src.algorithms.as_rank import ASRank
from src.algorithms.greedy import GreedyCVRPSolver
from src.algorithms.mmas import MMAS
from src.experiments_runner import run_h3_convergence_test, run_solution_quality_test
from src.parser import parse_sol_file, parse_vrp_file
from src.utils import calculate_distance_matrix, calculate_s_max_from_bks, parse_parameters_from_filename

ACO_SOLVERS = {
    'BasicAntSystem': BasicAntSystem,
    'MMAS': MMAS,
    'ASRank': ASRank,
}


def s_max_multiplier(value: str) -> float:
    return float('inf') if value.lower() == 'inf' else float(value)


def run_demo(args):
    vrp_path = os.path.join(args.data, f"{args.instance}.vrp")
    sol_path = os.path.join(args.data, f"{args.instance}.sol")
    instance = parse_vrp_file(vrp_path)
    distance_matrix = calculate_distance_matrix(instance)
    n, k = parse_parameters_from_filename(os.path.basename(vrp_path))
    bks = parse_sol_file(sol_path) if os.path.exists(sol_path) else None

    if args.smax == float('inf') or bks is None:
        s_max = float('inf')
    else:
        s_max = calculate_s_max_from_bks(instance, bks.routes, distance_matrix, args.smax)

    greedy = GreedyCVRPSolver(instance, distance_matrix, s_max, k).solve()
    greedy.algorithm_name = 'Greedy'

    np.random.seed(args.seed)
    params = {
        'iterations': args.iterations,
        'num_ants': n,
        'alpha': 1.0,
        'beta': 4.0,
        'rho': 0.5,
        's_max': s_max,
        'num_vehicles': k,
        'w_rank': 6,
    }
    aco = ACO_SOLVERS[args.algorithm](instance, distance_matrix, params).solve()

    print(f"Instance {args.instance}: {n} nodes, {k} vehicles, S_max = {s_max:.1f}")
    if bks is not None:
        print(f"  Best known solution: {bks.total_distance:.1f}")
    for solution in (greedy, aco):
        gap = f" (gap {100 * (solution.total_distance / bks.total_distance - 1):.1f}%)" if bks and np.isfinite(solution.total_distance) else ""
        result = f"{solution.total_distance:.1f}{gap}" if np.isfinite(solution.total_distance) else "no feasible solution"
        print(f"  {solution.algorithm_name:<15} {result}, {solution.computation_time:.1f} s")

    feasible = [s for s in (greedy, aco) if np.isfinite(s.total_distance)]
    if args.plot and feasible:
        from src.visualization import plot_solutions_side_by_side
        plot_solutions_side_by_side(instance, feasible, title=f"{args.instance}, S_max multiplier {args.smax}", path=args.save)


def main():
    parser = argparse.ArgumentParser(description="Ant Colony Optimization for the distance-constrained CVRP.")
    parser.add_argument('--data', default='data/', help="folder with the .vrp and .sol files (default: data/)")
    subparsers = parser.add_subparsers(dest='command', required=True)

    demo = subparsers.add_parser('demo', help="solve one instance with Greedy and an ACO variant and plot the routes")
    demo.add_argument('--instance', default='A-n32-k5')
    demo.add_argument('--algorithm', choices=ACO_SOLVERS, default='MMAS')
    demo.add_argument('--iterations', type=int, default=200)
    demo.add_argument('--seed', type=int, default=1)
    demo.add_argument('--smax', type=s_max_multiplier, default=1.25, help="S_max as a multiple of the longest BKS route, or 'inf'")
    demo.add_argument('--no-plot', dest='plot', action='store_false', help="only print the distances")
    demo.add_argument('--save', help="save the plot to this file instead of showing it")

    quality = subparsers.add_parser('quality', help="solution quality test (H1, H2, H4): Greedy and all ACO variants on every instance")
    quality.add_argument('--smax', type=s_max_multiplier, default=1.25)
    quality.add_argument('--seeds', type=int, default=10)

    convergence = subparsers.add_parser('convergence', help="convergence test (H3): best cost per iteration of AS and AS-rank")
    convergence.add_argument('--smax', type=s_max_multiplier, default=1.25)
    convergence.add_argument('--seeds', type=int, default=10)

    args = parser.parse_args()

    if args.command == 'demo':
        run_demo(args)
    elif args.command == 'quality':
        run_solution_quality_test(args.data, ACO_SOLVERS, seeds=range(1, args.seeds + 1),
                                  test_name="solution_quality_test", s_max_multiplier=args.smax)
    else:
        run_h3_convergence_test(args.data, ACO_SOLVERS, seeds=range(1, args.seeds + 1), s_max_multiplier=args.smax)


if __name__ == "__main__":
    main()
