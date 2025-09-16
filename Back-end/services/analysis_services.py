def run_analysis(roof_area, dwellers, open_space, location_data):
    """
    Performs the core rainwater harvesting analysis.
    
    Args:
        roof_area (float): The roof area in square meters.
        dwellers (int): Number of people in the household.
        open_space (float): Available open ground space in square meters.
        location_data (dict): A dictionary containing local environmental data
                              like rainfall, aquifer type, etc.

    Returns:
        dict: A dictionary containing all the calculated results.
    """
    # --- Constants and Assumptions ---
    # Runoff coefficient (e.g., for a tiled roof). Varies from 0.7 to 0.95.
    RUNOFF_COEFFICIENT = 0.85
    # Average daily water need per person in liters (as per Indian standards)
    WATER_NEED_PER_PERSON_LPCD = 135
    # Cost per cubic meter for excavation (can be refined for different regions)
    COST_PER_CUBIC_METER_INR = 500 


    # --- 1. Potential Analysis ---
    annual_rainfall_mm = location_data.get("avgAnnualRainfall", 1470)
    annual_rainfall_m = annual_rainfall_mm / 1000.0

    # Calculate total harvestable water
    annual_harvestable_water = roof_area * annual_rainfall_m * RUNOFF_COEFFICIENT * 1000 # in Liters

    # Calculate household water needs
    daily_household_need = dwellers * WATER_NEED_PER_PERSON_LPCD
    annual_household_need = daily_household_need * 365

    # Calculate the percentage of needs met by harvested water
    if annual_household_need > 0:
        percentage_of_needs_met = min(100, (annual_harvestable_water / annual_household_need) * 100)
    else:
        percentage_of_needs_met = 100

    # --- 2. System Recommendation ---
    # Simple logic: if enough open space, recommend a pit, otherwise a trench.
    # This can be expanded with soil type, etc.
    if open_space >= 10:
        recommended_system = "Recharge Pit"
        # Dimensions are based on a typical design for a 100-150 sq.m roof
        pit_diameter = 1.5 # meters
        pit_depth = 3.0 # meters
        pit_volume = 3.14159 * ((pit_diameter / 2)**2) * pit_depth
        dimensions = {"diameter_m": pit_diameter, "depth_m": pit_depth}
        system_volume = pit_volume
    else:
        recommended_system = "Recharge Trench"
        # Typical dimensions
        trench_width = 0.5 # meters
        trench_depth = 1.5 # meters
        trench_length = 4.0 # meters
        dimensions = {"width_m": trench_width, "depth_m": trench_depth, "length_m": trench_length}
        system_volume = trench_width * trench_depth * trench_length

    # --- 3. Cost & Benefit Analysis ---
    estimated_cost = system_volume * COST_PER_CUBIC_METER_INR
    # Assume a cost of water (e.g., from municipal supply or tankers)
    cost_per_1000_liters_inr = 25
    annual_savings = (annual_harvestable_water / 1000) * cost_per_1000_liters_inr

    if annual_savings > 0:
        roi_years = estimated_cost / annual_savings
    else:
        roi_years = float('inf') # Indicates no return if no savings


    return {
        "potentialAnalysis": {
            "annualHarvestableWaterLiters": round(annual_harvestable_water),
            "percentageOfNeedsMet": round(percentage_of_needs_met, 2),
        },
        "systemRecommendation": {
            "name": recommended_system,
            "dimensions": dimensions,
            "reason": f"A {recommended_system.lower()} is suitable for your available open space of {open_space} sq. meters.",
        },
        "costBenefitAnalysis": {
            "estimatedCostINR": round(estimated_cost),
            "annualSavingsINR": round(annual_savings),
            "roiYears": (
                round(roi_years, 1) if roi_years != float('inf') else "N/A"
            ),
        },
        "locationData": location_data,
    }
