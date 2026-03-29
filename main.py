from src.parser import parse_vrp_file, parse_sol_file
from src.utils import calculate_distance_matrix
from src.visualization import visualize_solution, compare_solutions

def main():
    path = "data/A-n32-k5.vrp"
    instance = parse_vrp_file(path)

    print(f"Instance Name: {instance.name}")
    print(f"Dimension: {instance.dimension}")
    print(f"Capacity: {instance.capacity}")
    print(f"Depot ID: {instance.depot_id}")

    distance_matrix = calculate_distance_matrix(instance)
    print("Distance Matrix:")
    for i in range(instance.dimension):
        for j in range(instance.dimension):
            print(f"{distance_matrix[i][j]:.2f}", end=" ")
        print()

    solution_path = "data/A-n32-k5.sol"
    solution = parse_sol_file(solution_path)
    for i in range(len(solution.routes)):
        print(f"Route {i + 1}: {solution.routes[i]}")
    print(f"Total Distance: {solution.total_distance}")

    visualize_solution(instance, solution)
    compare_solutions(instance, solution, solution)

if __name__ == "__main__":
    main()