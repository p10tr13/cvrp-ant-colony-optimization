from src.algorithms.ant_system import BasicAntSystem
from src.algorithms.mmas import MMAS
from src.algorithms.as_rank import ASRank
from src.experiments_runner import run_solution_quality_test

def main():
    aco_solvers = {
        'BasicAntSystem': BasicAntSystem,
        'MMAS': MMAS,
        'ASRank': ASRank
    }

    run_solution_quality_test(
        data_dir="data/",
        solvers_map=aco_solvers,
        seeds=range(1, 11),
        test_name="solution_quality_test",
        s_max_multiplier=1.25
    )

if __name__ == "__main__":
    main()