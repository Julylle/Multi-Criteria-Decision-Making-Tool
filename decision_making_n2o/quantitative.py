import math
import tkinter as tk
from tkinter import ttk

class Quotes:
    def __init__(self):
        # Liquid-based system
        self.liquid_items = {
            "Sensor head": 1815,
            "Sensor Body": 3795,
            "Probe dip/rail assembly": 1000,
            "Controller": 12095,
            "Probe calibration kit for calibration": 68,
        }

        # Gas-phase system
        self.gas_items = {
            "Hood fabrication": 2639,
            "Hood positioning (fixings, weights, ropes and consumables)": 750,
            "Switching device floats": 1400,
            "Airflow meters": 2000,
            "Gas analyser": 21194,
            "Switching device - hardware": 14500,
            "Gas Conditioning Unit": 13639,
            "Drying unit gas tube (Nafion gas drying tube, MD-110-144CS-4)": 1150,
            "Data logger system": 6610,
            "Gas system service consumables for calibration": 179,
        }

    # ---------------------------
    # Liquid-phase subsystem sums
    # ---------------------------
    def probe_set_sum(self):
        return (
            self.liquid_items["Sensor head"]
            + self.liquid_items["Sensor Body"]
            + self.liquid_items["Probe dip/rail assembly"]
        )

    def controller_set_sum(self):
        return self.liquid_items["Controller"]

    # --------------------------
    # Gas-phase subsystem sums
    # --------------------------
    def hood_set_sum(self):
        return (
            self.gas_items["Hood fabrication"]
            + self.gas_items["Hood positioning (fixings, weights, ropes and consumables)"]
            + self.gas_items["Switching device floats"]
            + self.gas_items["Airflow meters"]
        )

    def analyser_set_sum(self):
        return (
            self.gas_items["Gas analyser"]
            + self.gas_items["Switching device - hardware"]
            + self.gas_items["Gas Conditioning Unit"]
            + self.gas_items["Drying unit gas tube (Nafion gas drying tube, MD-110-144CS-4)"]
            + self.gas_items["Data logger system"]
        )
    

    def _gui_input(prompt):
        def submit():
            nonlocal user_input
            user_input = entry.get()
            window.destroy()

        window = tk.Tk()
        window.title("Input Required")

        # Fix window size
        window.geometry("500x200")  # width x height
        window.resizable(False, False)

        # Multi-line prompt text
        label = ttk.Label(
            window,
            text=prompt,
            wraplength=480,       # wrap text to fit window
            justify="left"
        )
        label.pack(pady=10)

        # Input box
        entry = ttk.Entry(window, width=50)
        entry.pack(pady=5)

        # Submit button
        user_input = None
        ttk.Button(window, text="OK", command=submit).pack(pady=10)

        window.mainloop()
        return user_input


    
    def _ask_user_for_input(self, content, label):
        """Ask user for a single numeric input."""
        while True:
            try:
                value = float(self._gui_input(f"Enter {content} for '{label}': "))
                return value
            except ValueError:
                print("Invalid number. Please enter a numeric value.")


    def _ask_user_option(self, question):
        """Ask user for a single numeric input."""
        while True:
            try:
                value = float(self._gui_input(f"{question}"))
                return value
            except ValueError:
                print("Invalid number. Please enter a numeric value.")


    def init_from_user_input(self):
        # Monitroring parameters
        self.duration = self._ask_user_option("Please enter the planned monitoring duration in the unit of months:")
        self.nLocation = self._ask_user_option("Please enter the planned number of monitoring locations:")


        # Determine monitoring scenario (1-12)
        self.scenario = min(math.log2(math.ceil(self.duration/6)), 3) *3 + min(math.ceil(self.nLocation / 2), 3)
        
        # Criteria weights
        
        self.weights = {
            "Equipment Cost": 0.25,
            "Commissioning": 0.20,
            "Consumables Cost": 0.20,
            "Maintenance": 0.25,
            "Complexity": 0.1,
        }

        self.weightOption = self._ask_user_option(
            "Five criteria including equipment cost, consumables cost, commissioning, maintenance, and complexity" \
            "are considered in this evaluation. Default weights are provided. Enter '0' to use the default weights," \
            "or enter '1' to define your own. When entering custom weights, each value must be a decimal between 0 and 1. " \
            "You will be asked to enter the first four criteria, and the final criterion will be calculated as 1 minus " \
            "the sum of the four entered weights. Please ensure that the sum of the four entered weights does not exceed 1."
        )
        
        if self.weightOption == 1:
            for criterion in list(self.weights.keys())[:-1]:
                self.weights[criterion] = self._ask_user_for_input("weight", criterion)
            self.weights["Complexity"] = 1 - sum([self.weights[criterion] for criterion in list(self.weights.keys())[:-1]])
        else:
            pass

        self.priceOption = self._ask_user_option(
            "Among the five criteria, equipment cost and consumables cost are quantitative criteria that are strongly "
            "influenced by equipment prices. This tool provides default prices based on Australian suppliers. Enter '0' "
            "to use these default prices, or enter '1' to input your own prices from local suppliers."
        )

        if self.weightOption == 1:
            for item in self.liquid_items.keys():
                self.liquid_items[item] = self._ask_user_for_input("price",item)
            for item in self.gas_items.keys():
                self.gas_items[item] = self._ask_user_for_input("price", item)
        else:
            pass
        
    def _roma(self, num):
        val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        syms = ["M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"]
        roman = ""
        i = 0
        while num > 0:
            for _ in range(num // val[i]):
                roman += syms[i]
                num -= val[i]
            i += 1
        return roman


    def total_liquid_system_cost(self):
        return self.probe_set_sum() + self.controller_set_sum() + self.liquid_items["Probe calibration kit for calibration"]

    def total_gas_system_cost(self):
        return self.hood_set_sum() + self.analyser_set_sum() + self.gas_items["Gas system service consumables for calibration"]


    def _calculate_EquipmentCost_limits(self, weight_EquipmentCost):
        # liquid-based system equipment min: 2 proble sets + 1 controller
        liquid_min = 2 * self.probe_set_sum() + self.controller_set_sum()
        # liquid-based system equipment max: 6 proble sets + 3 controller
        liquid_max = 6 * self.probe_set_sum() + 3*self.controller_set_sum()
        # gas-based system equipment min: 2 hood sets + 1 anaylser set
        gas_min = 2 * self.hood_set_sum() + self.analyser_set_sum()
        # gas-based system equipment max: 6 hood sets + 1 anaylser set
        gas_max = 6 * self.hood_set_sum() + self.analyser_set_sum()
        
        maxEquipmentCost = max(liquid_max, gas_max)
        minEquipmentCost = min(liquid_min, gas_min)

        PIS_EquipmentCost = minEquipmentCost / maxEquipmentCost * 5 * weight_EquipmentCost
        NIS_EquipmentCost = maxEquipmentCost / maxEquipmentCost * 5 * weight_EquipmentCost

        return (PIS_EquipmentCost, NIS_EquipmentCost, maxEquipmentCost)
    
    def _calculate_ConsumablesCost_limits(self, weight_ConsumablesCost):
        # liquid-based system equipment min: 0 sensor head + 6 Probe calibration kit for calibration
        liquid_min = 0 * self.liquid_items["Sensor head"] + 6*self.liquid_items["Probe calibration kit for calibration"]
        # liquid-based system equipment max: 6 proble sets + 3 controller
        liquid_max = 42 * self.liquid_items["Sensor head"] + 144*self.liquid_items["Probe calibration kit for calibration"]
        # gas-based system equipment min: 2 hood calibration kits
        gas_min = 2 * self.gas_items["Gas system service consumables for calibration"]
        # gas-based system equipment max: 6 hood sets + 1 anaylser set
        gas_max = 16 * self.gas_items["Gas system service consumables for calibration"]

        maxConsumablesCost = max(liquid_max, gas_max)
        minConsumablesCost = min(liquid_min, gas_min)

        PIS_ConsumablesCost = minConsumablesCost / maxConsumablesCost * 5 * weight_ConsumablesCost
        NIS_ConsumablesCost = maxConsumablesCost / maxConsumablesCost * 5 * weight_ConsumablesCost

        return (PIS_ConsumablesCost, NIS_ConsumablesCost, maxConsumablesCost)

    

    def calculate_CostScores(self):

        self.PIS_EquipmentCost, self.NIS_EquipmentCost, self.maxEquipmentCost = self._calculate_EquipmentCost_limits(self.weights["Equipment Cost"])
        self.PIS_ConsumablesCost, self.NIS_ConsumablesCost, self.maxConsumablesCost = self._calculate_ConsumablesCost_limits(self.weights["Consumables Cost"])
        

        self.N_probeSet = self.nLocation
        self.N_controllerSet = math.ceil(self.nLocation / 2)
        self.N_probeHeads = self.nLocation * (math.floor(self.duration / 6)-1)
        self.N_liqCalibrationKits = self.nLocation * math.floor(self.duration / 2)
        self.liquid_EquipmentCost = self.N_probeSet * self.probe_set_sum() + self.N_controllerSet * self.controller_set_sum()
        self.liquid_ConsumablesCost = self.N_probeHeads * self.liquid_items["Sensor head"] + self.N_liqCalibrationKits * self.liquid_items["Probe calibration kit for calibration"]

        self.N_hoodSets = self.nLocation
        self.N_analyserSets = 1
        self.N_gasCalibrationKits = math.floor(self.duration/3)
        self.gas_EquipmentCost = self.N_hoodSets * self.hood_set_sum() + self.N_analyserSets * self.analyser_set_sum()
        self.gas_ConsumablesCost = self.N_gasCalibrationKits * self.gas_items["Gas system service consumables for calibration"]
        
        self.liquid_EquipmentCost_Score = (self.liquid_EquipmentCost / self.maxEquipmentCost) * 5 * self.weights["Equipment Cost"]
        self.liquid_ConsumablesCost_Score = (self.liquid_ConsumablesCost / self.maxConsumablesCost) * 5 * self.weights["Consumables Cost"]
        self.gas_EquipmentCost_Score = (self.gas_EquipmentCost / self.maxEquipmentCost) * 5 * self.weights["Equipment Cost"]
        self.gas_ConsumablesCost_Score = (self.gas_ConsumablesCost / self.maxConsumablesCost) * 5 * self.weights["Consumables Cost"]

        self.EquipmentCost_Score = {
            "Liquid-based method": self.liquid_EquipmentCost_Score,
            "Gas-based method": self.gas_EquipmentCost_Score, 
        }
        self.ConsumablesCost_Score = {
            "Liquid-based method": self.liquid_ConsumablesCost_Score,
            "Gas-based method": self.gas_ConsumablesCost_Score, 
        }
        
    

    def print_summary_quantitative(self):
            print("\n=== Multi-criteria Decision Making Evaluation Summary ===")
            print("-------------------------------------------------------------------------------------")
            print("\nStep 1: Identify monitoring scenario")
            print(f"  Monitoring duration: {self.duration} months")
            print(f"  Number of monitoring locations: {self.nLocation}")
            print(f"  Monitoring scenario (I-XII): {self._roma(int(self.scenario)):4}")
    
            print("-------------------------------------------------------------------------------------")
            print("\nStep 2: Decide criteria weights")
            for criterion, weight in self.weights.items():
                print(f"  {criterion:20}: {weight:.3f}")

            print("-------------------------------------------------------------------------------------")
            print("\nStep 3: Score quantitative criteria")

            
            print("\nStep 3-1: Liquid-based quantification system cost breakdown")
            for i, (item, price) in enumerate(self.liquid_items.items()):
                print(f"  {self._roma(i+1):4} {item:60} {price:>6}")
            print(f"{'  *Sub1: Probe set sum (=I+II+III)':60} {self.probe_set_sum():>6}")
            print(f"{'  *Sub2: Controller set sum (=IV)':60} {self.controller_set_sum():>6}")
            
            print("\nStep 3-2: Gas-phase quantification system cost breakdown")
            for i, (item, price) in enumerate(self.gas_items.items()):
                print(f"  {self._roma(i+1):4} {item:60} {price:>6}")
            print(f"{'  *Sub1: Hood set sum (=I+II+III+IV)':60} {self.hood_set_sum():>6}")
            print(f"{'  *Sub2: Analyser set sum (=V+VI+VII+VIII+IX)':60} {self.analyser_set_sum():>6}")

            print(f"\nStep 3-3: Total costs and corresponding scores under scenario {self._roma(int(self.scenario)):4}")
            print("\n*Equipment Costs and Scores:")

            print(f"  Liquid-based method: ${self.liquid_EquipmentCost} => Weighted scores: {self.EquipmentCost_Score['Liquid-based method']:.4f}")
            print(f"  Gas-based method: ${self.gas_EquipmentCost} => Weighted scores: {self.EquipmentCost_Score['Gas-based method']:.4f}")

            print("\n*Consumables Costs and Scores:")
            print(f"  Liquid-based method: ${self.liquid_ConsumablesCost} => Weighted scores: {self.ConsumablesCost_Score['Liquid-based method']:.4f}")
            print(f"  Gas-based method: ${self.gas_ConsumablesCost} => Weighted scores: {self.ConsumablesCost_Score['Gas-based method']:.4f}")