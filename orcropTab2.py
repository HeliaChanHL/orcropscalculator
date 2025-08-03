import streamlit as st
from farmingData import *
def tab1Content():
    checkedCrops = {}
    container1 = st.container()
    container1.header("Tool Configuration:")
    col1, col2 = container1.columns([1, 3])
    with col1:
        st.write("Harvesting Hoe Type:")
        st.write("Sowing Level:")
        st.write("Yielding Level:")

    with col2:
        # Select hoe type and store it in session state using on_change
        hoeType = st.selectbox(
            "Select Hoe Type:", 
            list(hoeTypes.keys()), 
            index=len(hoeTypes) - 1, 
            key='hoeType',
            on_change=lambda: st.session_state.__setitem__('hoeType', st.session_state.hoeType)
        )
        
        sowingLevel = st.selectbox(
            "Select Sowing Level:", 
            ["None", 1, 2, 3], 
            index=0, 
            key='sowingLevel',
            on_change=lambda: st.session_state.__setitem__('sowingLevel', st.session_state.sowingLevel)
        )
        
        yieldingLevel = st.selectbox(
            "Select Yielding Level:", 
            ["None", 1, 2, 3], 
            index=0, 
            key='yieldingLevel',
            on_change=lambda: st.session_state.__setitem__('yieldingLevel', st.session_state.yieldingLevel)
        )

    # Calculate cropChance based on the selected hoeType
    cropChance = {
        "Default": {"1-Star": 90 - hoeTypes[st.session_state.hoeType], "2-Star": 10 + hoeTypes[st.session_state.hoeType], "3-Star": 0},
        "Soil": {"1-Star": 0, "2-Star": 90 - hoeTypes[st.session_state.hoeType], "3-Star": 10 + hoeTypes[st.session_state.hoeType]},
        "Gold Crop": 1
    }

    container2 = st.container()
    container2.header("Crop Configuration:")
    col1, col2 = container2.columns([1, 3])
    
    with col1:
        for cropName in crops.keys():
            checkbox = st.checkbox(cropName, key=f'checkbox_{cropName}')
            if checkbox:
                checkedCrops[cropName] = {}

    with col2:
        if checkedCrops:
            cropTabs = st.tabs(checkedCrops.keys())
            for cropName, tab in zip(checkedCrops.keys(), cropTabs):
                with tab:
                    st.header(cropName)
                    planterTabs = st.tabs(planterTypes.keys())
                    for planterName, planterTab in zip(planterTypes.keys(), planterTabs):
                        with planterTab:
                            if planterName not in checkedCrops[cropName]:
                                checkedCrops[cropName][planterName] = {}

                            planters = st.number_input(f'Number of {planterName} Setups for {cropName}', min_value=0, max_value=10000, value=0, key=f'planter_{cropName}_{planterName}')
                            checkedCrops[cropName][planterName]['Planters'] = planters

                            soil = st.number_input(f'Number of Setups with Soil for {cropName} [in units of {planterName} ({planterTypes[planterName]})]', min_value=0, max_value=planters, value=0, key=f'soil_{cropName}_{planterName}')
                            checkedCrops[cropName][planterName]['Soil'] = soil

                            fertilizer = st.number_input(f'Number of Setups with Fertilizer for {cropName} [in units of {planterName} ({planterTypes[planterName]})]', min_value=0, max_value=planters, value=0, key=f'fertilizer_{cropName}_{planterName}')
                            checkedCrops[cropName][planterName]['Fertilizer'] = fertilizer

    container3 = st.container()
    container3.header("Miscellaneous:")
    col1, col2 = container3.columns([1, 3])
    
    with col1:
        st.write("Harvests:")
    with col2:
        harvests = st.number_input('Number of Seeds per Planter', min_value=1, max_value=64, value=1)
    st.session_state.CalcPlanter = st.checkbox("Calculate Planter Cost & Supply Count?")
    st.session_state.CalcSprinkler = st.checkbox("Calculate Sprinkler Cost & Supply Count?")
    



    # Calculate button
    if st.button('Calculate (Double Click)'):
        if checkedCrops:
            st.session_state.calc = False
            results = {"Crops": [], "totalProfits": [], "totalIncome": [], "totalCosts": []}
            results2 = {"Crops": [], "totalProfits": [], "totalIncome": [], "totalCosts": []}
            allCostBreakdown = []
            suppliesCount = {crop + " Seed": 0 for crop in crops.keys()}
            suppliesCount.update({"Soil": 0, "Fertilizer": 0, "Planter": 0, "Wooden Sprinkler": 0, "Iron Sprinkler": 0})

            for cropName, attributes in checkedCrops.items():
                totalCropCost = 0
                totalCropIncome = 0
                for planterName, planterAttributes in attributes.items():
                    planters = planterAttributes['Planters']
                    soil = planterAttributes['Soil']
                    fertilizer = planterAttributes['Fertilizer']
                    
                    if planters != 0:
                        suppliesCount[cropName + " Seed"] += planterTypes[planterName] * harvests * planters 
                        suppliesCount["Soil"] += planterTypes[planterName] * harvests * soil
                        suppliesCount["Fertilizer"] += planterTypes[planterName] * harvests * fertilizer
                        if st.session_state.CalcPlanter:
                            suppliesCount["Planter"] += planters * planterTypes[planterName]
                        if st.session_state.CalcSprinkler:
                            if planterName =="Wooden Sprinkler":
                                suppliesCount["Wooden Sprinkler"] += planters
                            elif planterName =="Iron Sprinkler":
                                suppliesCount["Iron Sprinkler"] += planters
                        costBreakdown, totalCost = calculateCost(cropName, planterAttributes, planters, soil, fertilizer, planterName,harvests,st.session_state.sowingLevel)
                        totalIncome = calculateIncome(cropName, planterName, planters, soil, fertilizer,harvests,st.session_state.yieldingLevel)
                        results["Crops"].append(cropName + " " + planterName)
                        results["totalCosts"].append(totalCost)
                        results["totalIncome"].append(totalIncome)
                        results["totalProfits"].append(totalIncome - totalCost)
                        totalCropCost += totalCost
                        totalCropIncome += totalIncome
                        
                        allCostBreakdown.append(costBreakdown)
                if totalCropCost!=0:  
                    results2["Crops"].append(cropName)
                    results2["totalCosts"].append(totalCropCost)
                    results2["totalIncome"].append(totalCropIncome)
                    results2["totalProfits"].append(totalCropIncome - totalCropCost)

            st.session_state.checkedCrops=checkedCrops
            st.session_state.results = results
            st.session_state.results2 = results2
            st.session_state.allCostBreakdown = allCostBreakdown
            st.session_state.suppliesCount = suppliesCount

        else:
            st.warning('Please select at least one crop.')
def calculateCost(cropName, planterAttributes, planters, soil, fertilizer, planterName,harvests,sowingLevel):
    costBreakdown = {
        "Seed Cost": 0,
        "Soil Cost": 0,
        "Fertilizer Cost": 0,
        "Planter Cost": 0,
        "Sprinkler Cost": 0,
    }
    
    costBreakdown["Seed Cost"] = (planters * harvests * planterTypes[planterName] * crops[cropName]['costs'] * (1 - (enchantTypes["Sowing"][sowingLevel - 1] / 100 if sowingLevel != "None" else 0))) 
    costBreakdown["Soil Cost"] = ((planterTypes[planterName] * soil * harvests + 11) // 12 * suppliesCost["Soil"]) 
    costBreakdown["Fertilizer Cost"] = (planterTypes[planterName] * fertilizer * harvests * suppliesCost["Fertilizer"]) 
    if st.session_state.CalcPlanter:
        costBreakdown["Planter Cost"] = (planterTypes[planterName] * planters * suppliesCost["Planter"])
    if planterName != "Planter" and st.session_state.CalcSprinkler:
        costBreakdown["Sprinkler Cost"] = planters * suppliesCost[planterName]

    totalCost = sum(costBreakdown.values())
    return costBreakdown, totalCost

def calculateIncome(cropName, planterName, planters, soil, fertilizer,harvests,yieldingLevel):
    incomeWithoutSoil = (
        (cropChance["Default"]["1-Star"] / 100 * crops[cropName]['price'][0] +
         cropChance["Default"]["2-Star"] / 100 * crops[cropName]['price'][1]) *
        (planters - soil)
    )

    incomeWithSoil = (
        (cropChance["Soil"]["2-Star"] / 100 * crops[cropName]['price'][1] +
         cropChance["Soil"]["3-Star"] / 100 * crops[cropName]['price'][2]) *
        soil
    )

    totalIncome = (incomeWithoutSoil + incomeWithSoil) * (1 - cropChance["Gold Crop"] / 100)
    totalIncome += (crops[cropName]['price'][3] * planters * cropChance["Gold Crop"] / 100)
    totalIncome *= (1 + (fertilizer / planters))
    totalIncome *= (1 + (enchantTypes["Yielding"][yieldingLevel - 1] / 100 if yieldingLevel != "None" else 0))
    totalIncome *= planterTypes[planterName]
    totalIncome *= harvests

    return totalIncome