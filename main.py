from src.algorithms.ant_system import BasicAntSystem
from src.algorithms.mmas import MMAS
from src.algorithms.as_rank import ASRank
from src.experiments_runner import run_h3_convergence_test

def main():
    aco_solvers = {
        'BasicAntSystem': BasicAntSystem,
        'MMAS': MMAS,
        'ASRank': ASRank
    }

    run_h3_convergence_test(
        data_dir="data/",
        solvers_map=aco_solvers,
        seeds=range(1, 11),
        s_max_multiplier=1.25
    )

if __name__ == "__main__":
    main()