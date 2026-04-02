import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from src.parser import parse_vrp_file, parse_sol_file
from src.utils import calculate_distance_matrix, parse_parameters_from_filename, calculate_s_max_from_bks
from src.algorithms.greedy import GreedyCVRPSolver

def run_solution_quality_test(data_dir, solvers_map, seeds, test_name, s_max_multiplier=1.25):
    """
    Starts a solution quality test for a given CVRP instance, running multiple algorithms with specified parameters and seeds.
    Saves results to a CSV file.
    """
    all_results = []
    
    files = [f for f in os.listdir(data_dir) if f.endswith('.vrp')]

    total_runs = len(files) * len(solvers_map) * len(seeds)
    pbar = tqdm(total=total_runs, desc="Running solution quality tests", unit="run")
    
    for filename in files:
        pbar.set_description(f"File: {filename}")
        
        path = os.path.join(data_dir, filename)
        instance = parse_vrp_file(path)
        distance_matrix = calculate_distance_matrix(instance)
        n, k = parse_parameters_from_filename(filename)

        if k is None or n is None:
            print('Not able to parse filename')
            continue
        
        if s_max_multiplier == float('inf'):
            s_max_value = float('inf')
        else:
            sol_path = path.replace('.vrp', '.sol')
            bks_solution = parse_sol_file(sol_path) if os.path.exists(sol_path) else None
            s_max_value = calculate_s_max_from_bks(instance, bks_solution.routes, distance_matrix, s_max_multiplier)
        
        aco_params = {
            'iterations': 200,
            'num_ants': n,
            'alpha': 1.0,
            'beta': 4.0,
            'rho': 0.5,
            's_max': s_max_value,
            'num_vehicles': k,
            'w_rank': 6
        }

        greedy_solver = GreedyCVRPSolver(instance, distance_matrix, s_max_value, k)
        res_greedy = greedy_solver.solve()
        
        all_results.append({
            'Instance': filename,
            'Algorithm': 'Greedy',
            'Seed': 0,
            'Distance': res_greedy.total_distance,
            'Time': res_greedy.computation_time,
            'S_max': s_max_value
        })

        for algo_name, SolverClass in solvers_map.items():
            for seed in tqdm(seeds, desc=f"  -> {algo_name}", leave=False, unit="run"):
                np.random.seed(seed)
                
                solver = SolverClass(instance, distance_matrix, aco_params)
                result = solver.solve()
                
                all_results.append({
                    'Instance': filename,
                    'Algorithm': algo_name,
                    'Seed': seed,
                    'Distance': result.total_distance,
                    'Time': result.computation_time,
                    'S_max': s_max_value
                })

                pbar.update(1)

    pbar.close()

    df = pd.DataFrame(all_results)
    
    output_filename = f"{test_name}_smax_{s_max_multiplier}.csv"
    if not os.path.exists("results"):
        os.makedirs("results")
        
    save_path = os.path.join("results", output_filename)
    df.to_csv(save_path, index=False)
    
    print(f"\nTESTS ENDED. Results saved in: {save_path}")
    return df