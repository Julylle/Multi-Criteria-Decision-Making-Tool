from Quotes import Quotes
from QualitativeScores import QualitativeScores


# Quantitative scores
costs = Quotes()
costs.init_from_user_input()
costs.calculate_CostScores()

# Qualitative scores
QualitativeCriteria = QualitativeScores(costs)
QualitativeCriteria.criterion_scores()
QualitativeCriteria.get_scenario_qualitative_scores()
QualitativeCriteria.compute_topsis()

# Print results
costs.print_summary_quantitative()
QualitativeCriteria.print_summary_qualitative()
