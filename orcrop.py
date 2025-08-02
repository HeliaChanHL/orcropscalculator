import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Title of the app
st.title('OR Farming Calculator')
custom_css = """
<style>
.st-emotion-cache-z8vbw2 { /* stElementContainer */
  width: 100%;
  max-width: 100%;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

def tab1Content():
    math_explanation = """
### Explanation of Calculations

#### Cost Calculation

1. **Seed Cost**:
   The cost of seeds is calculated by multiplying:
   - The number of planters
   - The number of harvests
   - The base cost of the crop
   - The number of planters per fully set up sprinkler (if applicable)
   - A reduction based on the sowing level enchantment (if applicable).

2. **Soil Cost**:
   The cost for soil is calculated by determining how many packs of soil are needed (based on the number of planters and harvests) and multiplying that by the cost per pack.

3. **Fertilizer Cost**:
   This is determined by multiplying the number of planters by the amount of fertilizer used per harvest and its cost.

4. **Planter Cost**:
   If the planter is being calculated, this cost is the number of planters multiplied by the cost of the planter type.

5. **Sprinkler Cost**:
   If a sprinkler is used (and it's not a regular planter), this cost is calculated by multiplying the number of planters by the cost of the sprinkler.

---

#### Income Calculation

1. **Income Without Soil**:
   This is calculated by taking the chance of producing 1-star and 2-star crops (in percentages) and multiplying them by their respective prices. This is then multiplied by the number of planters minus the amount of soil used.

2. **Income With Soil**:
   Similar to income without soil, but it uses the chances for 2-star and 3-star crops instead, and this is multiplied by the amount of soil.

3. **Total Income**:
   The total income combines both income calculations and applies a reduction based on the gold crop chance. It also adds any income from gold crops directly produced.

4. **Adjustments**:
   The total income is adjusted based on the amount of fertilizer used and any yielding enchantments (if applicable). Finally, it factors in the effectiveness of the planter type and multiplies by the number of harvests.

"""
    st.header("Welcome to the OR Farming Calculator!")
    st.markdown(math_explanation)

# Define global variables for crops, planter types, enchant types, etc.
crops = {
    'Chili': {'costs': 1, 'price': [4, 6, 8, 80]},
    'Lettuce': {'costs': 1, 'price': [4, 6, 8, 80]},
    'Eggplant': {'costs': 2, 'price': [5, 8, 11, 165]},
    'Pineapple': {'costs': 3, 'price': [6, 10, 14, 210]},
    'Corn': {'costs': 3, 'price': [6, 10, 14, 210]},
    'Apple': {'costs': 4, 'price': [4, 12, 17, 255]},
    'Banana': {'costs': 4, 'price': [7, 12, 17, 255]},
    'Mango': {'costs': 4, 'price': [7, 12, 17, 255]}
}

hoeTypes = {"Wood": 10, "Stone": 20, "Iron": 30, "Diamond": 40, 
            "Platinum": 50, "Legendary": 50, "Gold": 55, "Netherite": 60}
planterTypes = {"Planter": 1, "Wooden Sprinkler": 24, "Iron Sprinkler": 48}
enchantTypes = {"Sowing": [0.75, 1.5, 2], "Yielding": [0.5, 0.75, 0.1]}
suppliesCost = {"Soil": 4, "Fertilizer": 6, "Planter": 32, "Wooden Sprinkler": 255, "Iron Sprinkler": 1000}

cropChance = {
    "Default": {"1-Star": 90, "2-Star": 10, "3-Star": 0},
    "Soil": {"1-Star": 0, "2-Star": 90, "3-Star": 10},
    "Gold Crop": 1
}

def tab2Content():
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
    if st.button('Calculate'):
        if checkedCrops:
            results = {"Crops": [], "totalProfits": [], "totalIncome": [], "totalCosts": []}
            barCol = []
            allCostBreakdown = []
            suppliesCount = {crop + " Seed": 0 for crop in crops.keys()}
            suppliesCount.update({"Soil": 0, "Fertilizer": 0, "Planter": 0, "Wooden Sprinkler": 0, "Iron Sprinkler": 0})

            for cropName, attributes in checkedCrops.items():
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
                        barCol.append(f"{cropName} {planterName}s")
                        
                        allCostBreakdown.append(costBreakdown)

            st.session_state.checkedCrops=checkedCrops
            st.session_state.results = results
            st.session_state.barCol = barCol
            st.session_state.allCostBreakdown = allCostBreakdown
            st.session_state.suppliesCount = suppliesCount

            # Switch to the results tab
            set_active_tab('Tab 3')
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
def tab3Content():
    if 'results' in st.session_state:
        checkedCrops=st.session_state.checkedCrops
        results = st.session_state.results
        barCol = st.session_state.barCol
        allCostBreakdown = st.session_state.allCostBreakdown
        suppliesCount = st.session_state.suppliesCount

        sumTotalCost = sum(results["totalCosts"])
        sumTotalIncome = sum(results["totalIncome"])

        st.header("Calculated Results:")
        st.success(f"Total Profit from Farm: {sumTotalIncome - sumTotalCost} rubies.")
        st.success(f"Total Income from All Crops: {sumTotalIncome} rubies.")
        st.success(f"Total Cost of Farm: {sumTotalCost} rubies.")

        # Financial Overview Chart
        fig = go.Figure()
        for category in ['totalProfits', 'totalIncome', 'totalCosts']:
            fig.add_trace(go.Bar(name=category, x=barCol, y=results[category]))

        fig.update_layout(title='Financial Overview of Crops', barmode='group', xaxis_title='Crops', yaxis_title='Amount (in Rubies)', template='plotly')
        st.plotly_chart(fig)

        # Cost Breakdown Chart
        costCategories = list(allCostBreakdown[0].keys())
        costValues = {category: [] for category in costCategories}
        for breakdown in allCostBreakdown:
            for category in costCategories:
                costValues[category].append(breakdown[category])

        fig = go.Figure()
        for category in costCategories:
            fig.add_trace(go.Bar(name=category, x=barCol, y=costValues[category]))

        fig.update_layout(title='Cost Breakdown Overview', barmode='stack', xaxis_title='Crops', yaxis_title='Amount (in Rubies)', template='plotly')
        st.plotly_chart(fig)

        supplies_df = pd.DataFrame({
            "Supply Type": list(suppliesCount.keys()), 
            "Count": list(suppliesCount.values())
        })

        # Calculate stack count and double chest count
        supplies_df["Stack Count"] = supplies_df["Count"] / 64
        supplies_df["Double Chest"] = supplies_df["Count"] / 64 / 54

        # Filter for counts greater than 0
        filtered_supplies_df = supplies_df[supplies_df['Count'] > 0]

        # Display the DataFrame in Streamlit
        st.header("Supplies Count Overview:")
        st.dataframe(filtered_supplies_df)

        st.header("Farm Configuration:")
        st.write(f"You selected: {st.session_state.hoeType}, Sowing: {st.session_state.sowingLevel}, Yielding: {st.session_state.yieldingLevel}")
        st.dataframe(checkedCrops)
    else:
        st.warning('No results to display. Please perform a calculation first.')





# Initialize session state for active tab if it doesn't exist
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'Tab 1'

# Function to set the active tab
def set_active_tab(tab):
    st.session_state.active_tab = tab

# Create columns for buttons
col1, col2, col3 = st.columns(3)
# Create buttons for tabs
with col1:
    st.button("How to Use", on_click=set_active_tab, args=("Tab 1",))
with col2:
    st.button("Crop Calculator", on_click=set_active_tab, args=("Tab 2",))
with col3:
    st.button("Calculated Results", on_click=set_active_tab, args=("Tab 3",))

# Display content based on the active tab
if st.session_state.active_tab == 'Tab 1':
    tab1Content()
elif st.session_state.active_tab == 'Tab 2':
    tab2Content()
elif st.session_state.active_tab == 'Tab 3':
    tab3Content()
