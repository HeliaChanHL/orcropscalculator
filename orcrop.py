import streamlit as st

# Title of the app
st.title('OR Farming Calculator')

# Crop data stored in a dictionary
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

# Dictionary to hold checked crops and their attributes
checkedCrops = {}
# Hoe type selection
st.header("Tool Configuration:")
col = st.columns([1, 3])
with col[0]:
    st.write("")
    st.write("")
    st.write("Harvesting Hoe Type:")
    st.write("")
    st.write("")
    st.write("")
    st.write("Sowing Level:")
    st.write("")
    st.write("")
    st.write("")
    st.write("Yielding Level:")
with col[1]:
    hoeType = st.selectbox("", list(hoeTypes.keys()), index=len(hoeTypes) - 1, key='hoeType')
    sowingLevel = st.selectbox("", ["None", 1, 2, 3], index=0, key='sowingLevel')
    yieldingLevel = st.selectbox("", ["None", 1, 2, 3], index=0, key='yieldingLevel')

cropChance = {"Default":{"1-Star":90-hoeTypes[hoeType],"2-Star":10+hoeTypes[hoeType],"3-Star":0},"Soil":{"1-Star":0,"2-Star":90-hoeTypes[hoeType],"3-Star":10+hoeTypes[hoeType]},"Gold Crop":1}
# Create a tab for crop selection
st.header("Select Your Crops:")
col = st.columns([1, 3])
with col[0]:
    for cropName in crops.keys():
        checkbox = st.checkbox(cropName, key=f'checkbox_{cropName}')
        if checkbox:
            checkedCrops[cropName] = {}  # Initialize entry for the crop

# Create tabs for each checked crop
with col[1]:
    if checkedCrops:
        cropTabs = st.tabs(checkedCrops.keys())

        for cropName, tab in zip(checkedCrops.keys(), cropTabs):
            with tab:
                st.header(cropName)

                # Create tabs for each planter type
                planterTabs = st.tabs(planterTypes.keys())
                for planterName, planterTab in zip(planterTypes.keys(), planterTabs):
                    with planterTab:
                        # Initialize a dictionary for each planter type
                        if planterName not in checkedCrops[cropName]:
                            checkedCrops[cropName][planterName] = {}

                        planters = st.number_input(
                            f'Number of {planterName} for {cropName}', 
                            min_value=0, 
                            max_value=10000, 
                            value=0, 
                            key=f'planter_{cropName}_{planterName}'
                        )
                        checkedCrops[cropName][planterName]['Planters'] = planters

                        soil = st.number_input(
                            f'Soil for {cropName} [in units of {planterName} ({planterTypes[planterName]})]', 
                            min_value=0, 
                            max_value=planters, 
                            value=0, 
                            key=f'soil_{cropName}_{planterName}'
                        )
                        checkedCrops[cropName][planterName]['Soil'] = soil

                        fertilizer = st.number_input(
                            f'Fertilizer for {cropName} [in units of {planterName} ({planterTypes[planterName]})]', 
                            min_value=0, 
                            max_value=planters, 
                            value=0, 
                            key=f'fertilizer_{cropName}_{planterName}'
                        )
                        checkedCrops[cropName][planterName]['Fertilizer'] = fertilizer

# Calculate button
if st.button('Calculate'):
    if checkedCrops:
        totalPrices=[]
        totalCosts = []
        priceFormula=""
        costFormula = ""
        for cropName, attributes in checkedCrops.items():
            for planterName, planterAttributes in attributes.items():
                planters = planterAttributes['Planters']
                if planters !=0 :
                    soil = planterAttributes['Soil']
                    fertilizer = planterAttributes['Fertilizer']
                    costs = crops[cropName]['costs']
                    
                    totalCost = ((costs * planters * (1 - (enchantTypes["Sowing"][sowingLevel - 1]/100 if sowingLevel != "None" else 0))) + ((soil + 11) // 12 * suppliesCost["Soil"]) + (fertilizer * suppliesCost["Fertilizer"]))
                    totalCosts.append(totalCost)
                    
                     # Calculate income without soil
                    incomeWithoutSoil = (
                        (cropChance["Default"]["1-Star"]/100 * crops[cropName]['price'][0] +
                         cropChance["Default"]["2-Star"]/100 * crops[cropName]['price'][1]) *
                        (planters - soil) 
                    )

                    # Calculate income with soil
                    incomeWithSoil = (
                        (cropChance["Soil"]["2-Star"]/100 * crops[cropName]['price'][1] +
                         cropChance["Soil"]["3-Star"]/100 * crops[cropName]['price'][2]) *
                        soil
                    )
                    
                    totalPrice= ((incomeWithoutSoil+incomeWithSoil)*(1-cropChance["Gold Crop"]/100) + (cropChance["Gold Crop"]/100 * crops[cropName]['price'][3] * planters) ) * (1 + (fertilizer/planters))
                    if yieldingLevel != "None":
                        totalPrice *= (1 + enchantTypes["Yielding"][yieldingLevel - 1]/100)
                    totalPrices.append(totalPrice)
                    costFormula += (
                        f"Total Cost for {cropName} with {planters} {planterName} = \n\n"
                        f"({costs} × {planters} - Seeds from Sowing {sowingLevel}) + \n"
                        f"({((soil + 11) // 12) * suppliesCost['Soil']}) + \n"
                        f"({fertilizer} × {suppliesCost['Fertilizer']}) = {totalCost} \n\n"
                    )
                    priceFormula += (
                        f"Total Income for {cropName} with {planters} {planterName} = \n\n"
                        f"  (((1-Star Chance% × {crops[cropName]['price'][0]} × ({planters} - {soil})) + \n"
                        f"  (2-Star Chance% × {crops[cropName]['price'][1]} × ({planters} - {soil})) + \n\n"
                        f"  (2-Star Chance% × {crops[cropName]['price'][1]} × {soil}) + \n"
                        f"  (3-Star Chance% × {crops[cropName]['price'][2]} × {soil})) × 1-Gold Crop Chance% + \n\n"
                        f"  (Gold Crop Chance% × {crops[cropName]['price'][3]} × {planters})) × \n\n"
                        f"  (1 + Fertilizer Doubling%:({fertilizer / planters})) × (1 + Yielding %) \n\n"
                        f"= Total Income: {totalPrice} \n\n"
                    )
            sumTotalCost = sum(totalCosts)
            sumTotalPrice = sum(totalPrices)
        if sumTotalCost > 0:
            st.header("Calculated Results:")
            st.success(f"Total Profit from Farm: {sumTotalPrice-sumTotalCost}")
            st.success(f"Total Income from All Crops: {sumTotalPrice}")
            st.success(f"Total Cost of Farm: {sumTotalCost}")
            st.write("Total Income for Each Crop:")
            st.write("= (incomeWithoutSoil + incomeWithSoil + goldCrop) x (Fertilizer Doubling) x (Yielding Doubling)\n")
            st.markdown(priceFormula)
            st.write("Total Costs for Each Crop:")
            st.write("= (Base Cost × Planters) + (Rounded Soil Cost) + (Fertilizer Cost × Fertilizer)  \n")
            st.markdown(costFormula)
            st.write("")
            st.header("Farm Configuration:")
            st.write(f"You selected: {hoeType}")
            st.write(checkedCrops)
        else:
            st.warning('Please select at least one planter.')
    else:
        st.warning('Please select at least one crop.')