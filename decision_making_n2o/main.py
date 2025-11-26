# main.py
from .quantitative import Quotes
from .qualitative import QualitativeScores

def main():
    # Quantitative scores
    costs = Quotes()
    costs.init_from_user_input()
    costs.calculate_CostScores()

    # Qualitative scores
    q = QualitativeScores(costs)
    q.criterion_scores()
    q.get_scenario_qualitative_scores()
    q.compute_topsis()

    # Print results
    costs.print_summary_quantitative()
    q.print_summary_qualitative()

if __name__ == "__main__":
    main()
