from src.parser import parse_vrp_file, parse_sol_file
from src.utils import calculate_distance_matrix
from src.visualization import compare_solutions, visualize_solution
from src.algorithms.greedy import GreedyCVRPSolver
from src.algorithms.ant_system import BasicAntSystem
from src.algorithms.mmas import MMAS
from src.algorithms.as_rank import ASRank

def main():
    path = "data/A-n32-k5.vrp"
    instance = parse_vrp_file(path)
    number_of_vehicles = 5

    print(f"Instance Name: {instance.name}")
    print(f"Dimension: {instance.dimension}")
    print(f"Capacity: {instance.capacity}")
    print(f"Depot ID: {instance.depot_id}")

    distance_matrix = calculate_distance_matrix(instance)

    params = {'s_max': 300, 'iterations': 200, 'alpha': 1, 'beta': 3.0, 'rho': 0.2, 'num_vehicles': number_of_vehicles, 'num_ants': 32, 'w_rank': 6}

    base_ant_system_solution = BasicAntSystem(instance, distance_matrix, params).solve()
    mmas_solution = MMAS(instance, distance_matrix, params).solve()
    as_rank_solution = ASRank(instance, distance_matrix, params).solve()
    greedy_solution = GreedyCVRPSolver(instance, distance_matrix, s_max=300, num_vehicles=number_of_vehicles).solve()

    solution_path = "data/A-n32-k5.sol"
    best_solution = parse_sol_file(solution_path)

    visualize_solution(instance, best_solution)
    compare_solutions(instance, greedy_solution, base_ant_system_solution)
    compare_solutions(instance, mmas_solution, as_rank_solution)

if __name__ == "__main__":
    main()