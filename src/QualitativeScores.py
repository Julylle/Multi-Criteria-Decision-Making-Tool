import pandas as pd
import numpy as np

class QualitativeScores:
    def __init__(self, costs):
        self.costs = costs

    def _ask_user_niche_scores(self, specific, elaboration):
        while True:
            try:
                user_input = input(
                    f"\nEnter niche scores for the two methods in terms of {specific}. "
                    "Please use the format [number1, number2], for example, [1, 1]. "
                    "'number1' corresponds to the liquid-based method, and 'number2' corresponds to the gas-based method."
                    f"\n{elaboration}\n"
                )

                # Safely convert string input to a Python list
                import ast
                specific_niche_score = ast.literal_eval(user_input)

                # Validate result
                if (
                    isinstance(specific_niche_score, list)
                    and len(specific_niche_score) == 2
                    and all(isinstance(x, (int, float)) for x in specific_niche_score)
                ):
                    break
                else:
                    print("Please enter exactly two numbers in the format [number1, number2].")

            except Exception:
                print("Invalid input. Please try again using the correct format, e.g., [1, 2].")

        criterion_specific = {
            "Liquid-based method": specific_niche_score[0],
            "Gas-based method": specific_niche_score[1],
        }

        return criterion_specific


    def _get_default_niches_scores(self, specific):
        criterion_specific = {
            "Liquid-based method": self.niche_scores[f'{specific}'][0],
            "Gas-based method": self.niche_scores[f'{specific}'][1],
        }

        return criterion_specific


    def _specific_scores(self, criterion_specific, coverage_factor, time_factor):

        # Coverage levels (3 levels)
        coverage = ["Minimal coverage", "Moderate coverage", "Extensive coverage"]

        # Expand values per method
        specific_base = {}
        for i, (method,base) in enumerate(criterion_specific.items()):
            if coverage_factor[i] != 1:
                levels = range(1, len(coverage) + 1)  # → 1, 2, 3
            else:
                levels = [1] * len(coverage)          # → 1, 1, 1 (no scaling)

            specific_base[method] = [base * level for level in levels]

        # Time scales and their multipliers
        time_scales = ["Short-term", "Intermediate-term", "Long-term", "Extra-long-term"]
        # time_factor = [1, 2, 3, 4]

        # MultiIndex: (Time scale, Coverage)
        idx = pd.MultiIndex.from_product(
            [time_scales, coverage],
            names=["Time scale", "Coverage"]
        )

        specific_scores = pd.DataFrame(index=idx)
        
        expanded = []
        # Fill values for each method
        for i, (method, values) in enumerate(specific_base.items()):
            expanded = [x for j in time_factor[i] for x in (np.array(values) * j)]
            specific_scores[method] = expanded

        return specific_scores
    
    
    def _run_qualitative_assessment(self):
        # Use a dictionary to save results
        all_criteria_specifics = {
            "Monitoring device setup": None,
            "Auxiliary equipment": None,
            "Initial calibration": None,
            "Regular calibration": None,
            "Extra service": None,
            "Emission calculation": None,
            "Calibration of key parameters": None,
        }
        
        coverage_factors = { 
            "Monitoring device setup": [2,2], # [liquid, gas]
            "Auxiliary equipment": [2,1],
            "Initial calibration": [2,1],
            "Regular calibration": [2,1],
            "Extra service": [2,1],
            "Emission calculation": [2,2],
            "Calibration of key parameters": [2,1],
        }
        
        time_factors = {
            "Monitoring device setup": [[1,1,1,1],[1,1,1,1]], # [liquid, gas]
            "Auxiliary equipment": [[1,1,1,1],[1,1,1,1]],
            "Initial calibration": [[1,1,1,1],[1,1,1,1]],
            "Regular calibration": [[1,2,4,8],[1,1,1,1]],
            "Extra service": [[1,2,4,8],[1,2,4,8]],
            "Emission calculation": [[1,2,4,8],[1,2,4,8]],
            "Calibration of key parameters": [[1,2,4,8],[1,1,1,1]],
        }

        self.niche_scores = {
            "Monitoring device setup": [1,2],
            "Auxiliary equipment": [1,2],
            "Initial calibration": [1,1],
            "Regular calibration": [2,1],
            "Extra service": [1,2],
            "Emission calculation": [1,2],
            "Calibration of key parameters": [2,1],
        }

        # criteria_specifics_scores = pd.DataFrame()
        self.scoringOption = self.costs._ask_user_option(
            "The remaining three criteria (i.e., commissioning, maintenance, and complexity) are qualitative in nature. "
            "This study introduces an innovative scoring system to quantify these qualitative criteria. First, under each "
            "criterion, the liquid-based method and gas-based method are compared across all relevant perspectives. Under the "
            "niche scenario with a 6-month monitoring duration and 2 monitoring locations, the niche scores for all perspectives "
            "are defined such that the superior method receives a score of 1 and the inferior method receives a score of 2. "
            "Second, multiplicative adjustments are applied to these basic scores to account for changes in monitoring duration "
            "or the number of monitoring locations. The final score for each qualitative criterion is then calculated by summing "
            "the specific scores of all perspectives under that criterion. To avoid over-complicating the calculation, this tool "
            "provides the flexibility to customise the niche scores. Enter '0' to use the default niche scores, or enter '1' to " \
            "customise your own."
        )

        elaborations = {
            "Monitoring device setup": "The liquid-based method uses the liquid probe and the gas-based method uses "
                                        "floating hood as monitoring devices. Which one do you think is more difficult to deploy?",
            "Auxiliary equipment": "The liquid-based method has only controller, while the gas-based has chimney, assembled gas "
                                    "analyser, drying unit, sampling unit, switching device and numerical recorder, etc. Which one "
                                    "do you think is more difficult to set up?",
            "Initial calibration": "The liquid-based method necessitates to conduct two-point calibration for each probe, while the "
                                    "gas-based method requires standard gas calibration for a single analyser. Which one "
                                    "do you think is more difficult to calibration after commissioning?",
            "Regular calibration": "The liquid probe needs conduct two-point calibration every two months, while the "
                                    "gas analyser is equipped with auto daily calibration. Which one do you think is more difficult "
                                    "to conduct regular calibration during the whole monitoring periods?",
            "Extra service": "The liquid-based method requires cleaning and drift checking, while maintenance of the gas-based method includes: "
                            "span and zero checks of the gas analyser; adjustment of NDIR optical components, inspection of critical components "
                            "of both the analyser and the sampling unit, replacement of sample filters and the mist catcher in the sampling unit, "
                            "regulator pressure checks and adjustments, replacement of sample pumps in the sampling unit, and verification of the "
                            "sampling unit’s flow rate. Which one do you think is more difficult to conduct extra services?", 
            "Emission calculation": "The liquid-based method needs to calculate liquid to gas transfer nased on estimated kLa values, and the gas-based "
                                    "method needs flux calculation with hoods switching. Which one do you think is more difficult to calculate?",
            "Calibration of key parameters": "The liquid-based method requires extra cross validation to verify or correct kLa estimates, while the "
                                            "gas-based method does not required to implement any calibration test. Which one "
                                            "do you think is more difficult to implement?",
        }

        for specific in all_criteria_specifics.keys():
            if self.scoringOption == 1:
                # ask about realtive scores for each criterion and specific criteria
                criterion_specific = self._ask_user_niche_scores(specific, elaborations[specific])
            else:
                criterion_specific = self._get_default_niches_scores(specific)
            
            coverage_factor = coverage_factors[specific]
            time_factor = time_factors[specific]
            all_criteria_specifics[specific] = self._specific_scores(criterion_specific, coverage_factor, time_factor)
            
        self.criteria_specifics_scores = all_criteria_specifics

    
    def criterion_scores(self):
        self._run_qualitative_assessment()
        self.Commissioning_scores = self.criteria_specifics_scores["Monitoring device setup"] + self.criteria_specifics_scores["Auxiliary equipment"] + self.criteria_specifics_scores["Initial calibration"]
        self.Maintenance_scores = self.criteria_specifics_scores["Regular calibration"] + self.criteria_specifics_scores["Extra service"]
        self.Complexity_scores = self.criteria_specifics_scores["Emission calculation"] + self.criteria_specifics_scores["Calibration of key parameters"]
    

    def get_scenario_qualitative_scores(self):
        """Extract scenario row for all three qualitative criteria."""
        idx = int(self.costs.scenario) - 1

        self.scenario_qualitative_scores = {
            "Commissioning": self.Commissioning_scores.iloc[idx, :],
            "Maintenance": self.Maintenance_scores.iloc[idx, :],
            "Complexity": self.Complexity_scores.iloc[idx, :]
        }

        """Normalize all qualitative criteria into weighted 5-point scores."""
        self.weighted = {}
        self.PIS, self.NIS = {}, {}

        for key, df in {
            "Commissioning": self.Commissioning_scores,
            "Maintenance": self.Maintenance_scores,
            "Complexity": self.Complexity_scores
        }.items():

            s = self.scenario_qualitative_scores[key]
            w = self.costs.weights[key]

            max_val = df.max().max()
            min_val = df.min().min()

            # Weighted scores
            self.weighted[key] = s / max_val * 5 * w

            # TOPSIS ideal/nadir solutions
            self.PIS[key] = min_val / max_val * 5 * w
            self.NIS[key] = 5 * w        # because max/max = 1

    
    def compute_topsis(self):
        """Compute TOPSIS final score for Liquid vs Gas."""

        # Build vectors in correct order
        PIS_vec = [
            self.costs.PIS_EquipmentCost,
            self.costs.PIS_ConsumablesCost,
            self.PIS["Commissioning"], 
            self.PIS["Maintenance"], 
            self.PIS["Complexity"]
        ]

        NIS_vec = [
            self.costs.NIS_EquipmentCost,
            self.costs.NIS_ConsumablesCost,
            self.NIS["Commissioning"], 
            self.NIS["Maintenance"], 
            self.NIS["Complexity"]
        ]

        Liquid_vec = [
            self.costs.EquipmentCost_Score["Liquid-based method"],
            self.costs.ConsumablesCost_Score["Liquid-based method"],
            self.weighted["Commissioning"]["Liquid-based method"],
            self.weighted["Maintenance"]["Liquid-based method"],
            self.weighted["Complexity"]["Liquid-based method"]
        ]

        Gas_vec = [
            self.costs.EquipmentCost_Score["Gas-based method"],
            self.costs.ConsumablesCost_Score["Gas-based method"],
            self.weighted["Commissioning"]["Gas-based method"],
            self.weighted["Maintenance"]["Gas-based method"],
            self.weighted["Complexity"]["Gas-based method"]
        ]

        # Euclidean distances
        Liquid_D_PIS = np.linalg.norm(np.array(Liquid_vec) - np.array(PIS_vec))
        Liquid_D_NIS = np.linalg.norm(np.array(Liquid_vec) - np.array(NIS_vec))
        Gas_D_PIS = np.linalg.norm(np.array(Gas_vec) - np.array(PIS_vec))
        Gas_D_NIS = np.linalg.norm(np.array(Gas_vec) - np.array(NIS_vec))

        # TOPSIS final scores
        self.Liquid_Final = Liquid_D_NIS / (Liquid_D_PIS + Liquid_D_NIS)
        self.Gas_Final = Gas_D_NIS / (Gas_D_PIS + Gas_D_NIS)

        


    def print_summary_qualitative(self):
        print("-------------------------------------------------------------------------------------")
        print("Step 4: Score qualitative criteria")
        # print("\n--- Commissioning scores acorss all scenarios---")
        # print(self.Commissioning_scores)
        # print("\n--- Maintenance scores acorss all scenarios ---")
        # print(self.Maintenance_scores)
        # print("\n--- Complexity scores acorss all scenarios ---")
        # print(self.Complexity_scores)
        # Print extracted scores
        for name, s in self.scenario_qualitative_scores.items():
            print(f"\n*{name} scores:")
            print(
                f"  Liquid-based method: {s['Liquid-based method']} "
                f"=> Weighted scores: {self.weighted[name]['Liquid-based method']:.4f}"
            )
            print(
                f"  Gas-based method: {s['Gas-based method']} "
                f"=> Weighted scores: {self.weighted[name]['Gas-based method']:.4f}"
            )

        print("\nFinal Scores:")
        print(f"  Liquid-based method: {self.Liquid_Final:.4f}")
        print(f"  Gas-based method: {self.Gas_Final:.4f}")

        if self.Liquid_Final < self.Gas_Final:
            print("\nRecommended method: Gas-based method")
        elif self.Gas_Final < self.Liquid_Final:
            print("\nRecommended method: Liquid-based method")
        else:
            print("\nBoth methods are equally recommended")