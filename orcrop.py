import streamlit as st
import plotly.graph_objects as go
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

container1 = st.container(border=True)
container1.header("Tool Configuration:")

col1, col2 = container1.columns([1, 3])
with col1:
    st.write("") 
    st.write("Harvesting Hoe Type:")
    st.write("") 
    st.write("Sowing Level:")
    st.write("") 
    st.write("Yielding Level:")

with col2:
    hoeType = st.selectbox("Select Hoe Type:", list(hoeTypes.keys()), index=len(hoeTypes) - 1, key='hoeType')
    sowingLevel = st.selectbox("Select Sowing Level:", ["None", 1, 2, 3], index=0, key='sowingLevel')
    yieldingLevel = st.selectbox("Select Yielding Level:", ["None", 1, 2, 3], index=0, key='yieldingLevel')


cropChance = {"Default":{"1-Star":90-hoeTypes[hoeType],"2-Star":10+hoeTypes[hoeType],"3-Star":0},"Soil":{"1-Star":0,"2-Star":90-hoeTypes[hoeType],"3-Star":10+hoeTypes[hoeType]},"Gold Crop":1}


container2 = st.container(border=True)
container2.header("Select Your Crops:")
col1, col2 = container2.columns([1, 3])
with col1:
    for cropName in crops.keys():
        checkbox = st.checkbox(cropName, key=f'checkbox_{cropName}')
        if checkbox:
            checkedCrops[cropName] = {}

# Create tabs for each checked crop
with col2:
    if checkedCrops:
        cropTabs = st.tabs(checkedCrops.keys())

        for cropName, tab in zip(checkedCrops.keys(), cropTabs):
            with tab:
                st.header(cropName)

                # Create tabs for each planter type
                planterTabs = st.tabs(planterTypes.keys())
                for planterName, planterTab in zip(planterTypes.keys(), planterTabs):
                    with planterTab:
                        if planterName not in checkedCrops[cropName]:
                            checkedCrops[cropName][planterName] = {}

                        planters = st.number_input(
                            f'Number of {planterName} for {cropName}', 
                            min_value=0, 
                            max_value=10000, 
                            value=0, 
                            key=f'planter_{cropName}_{planterName}'
                        )
                        checkedCrops[cropName][planterName]['Planters'] = planters * planterTypes[planterName]

                        soil = st.number_input(
                            f'Soil for {cropName} [in units of {planterName} ({planterTypes[planterName]})]', 
                            min_value=0, 
                            max_value=planters, 
                            value=0, 
                            key=f'soil_{cropName}_{planterName}'
                        )
                        checkedCrops[cropName][planterName]['Soil'] = soil * planterTypes[planterName]

                        fertilizer = st.number_input(
                            f'Fertilizer for {cropName} [in units of {planterName} ({planterTypes[planterName]})]', 
                            min_value=0, 
                            max_value=planters, 
                            value=0, 
                            key=f'fertilizer_{cropName}_{planterName}'
                        )
                        checkedCrops[cropName][planterName]['Fertilizer'] = fertilizer * planterTypes[planterName]
container3= st.container(border=True)
container3.header("Miscellaneous:")
col1, col2 = container3.columns([1, 3])
with col1:
    st.write("")
    st.write("")
    st.write("Harvests:")
with col2:
    harvests = st.number_input('Number of Seeds per Planter',  min_value=1, max_value=64,value=1, key=f'harvests')

# Calculate button
if st.button('Calculate'):
    if checkedCrops:
        results = {"Crops":[],"totalProfits":[],"totalPrices":[],"totalCosts":[]}
        barCol=[]
        priceFormula=""
        costFormula = ""
        for cropName, attributes in checkedCrops.items():
            for planterName, planterAttributes in attributes.items():
                planters = planterAttributes['Planters']
                if planters !=0 :
                    soil = planterAttributes['Soil']
                    fertilizer = planterAttributes['Fertilizer']
                    costs = crops[cropName]['costs']
                    results["Crops"].append(cropName)
                    barCol.append(f"{cropName} {planterName}s")
                    totalCost = harvests*((costs * planters * (1 - (enchantTypes["Sowing"][sowingLevel - 1]/100 if sowingLevel != "None" else 0))) + ((soil + 11) // 12 * suppliesCost["Soil"]) + (fertilizer * suppliesCost["Fertilizer"]))
                    results["totalCosts"].append(totalCost)
                    
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
                    
                    totalPrice= ((incomeWithoutSoil+incomeWithSoil)*(1-cropChance["Gold Crop"]/100) + (cropChance["Gold Crop"]/100 * crops[cropName]['price'][3] * planters) ) * (1 + (fertilizer/planters)*harvests)
                    if yieldingLevel != "None":
                        totalPrice *= (1 + enchantTypes["Yielding"][yieldingLevel - 1]/100)
                    results["totalPrices"].append(totalPrice)
                    results["totalProfits"].append(totalPrice-totalCost)
            sumTotalCost = sum(results["totalCosts"])
            sumTotalPrice = sum(results["totalPrices"])
        if sumTotalCost > 0:
            
            st.header("Calculated Results:")
            st.success(f"Total Profit from Farm: {sumTotalPrice-sumTotalCost}")
            st.success(f"Total Income from All Crops: {sumTotalPrice}")
            st.success(f"Total Cost of Farm: {sumTotalCost}")

            fig = go.Figure()
            categories = ['Crops','totalProfits', 'totalPrices', 'totalCosts']
            for category in categories[1:]:
                fig.add_trace(go.Bar(
                    name=category,
                    x=barCol,
                    y=results[category]
                ))

            # Update layout
            fig.update_layout(
                title='Financial Overview of Crops',
                barmode='group',
                xaxis_title='Crops',
                yaxis_title='Amount (in Rubies)',
                template='plotly'
            )

            # Streamlit app
            st.title("Financial Overview of Crops")

            st.plotly_chart(fig)
            st.write("Total Income for Each Crop:")
            st.markdown(
                "= (((planter-soil)\\*(1-Star% \\* 1-Star\\$ + 2-Star% * 2-Star\\$) + (soil)\\*(2-Star% \\* 2-Star\\$ + 3-Star% \\* 3-Star\\$)) \\* !goldCrop% + goldCrop% \\* goldCrop\\$ \\* planters) \\* (Fertilizer Doubling) \\* (Yielding Doubling) \\* (harvests)"
            )
            st.write("Total Costs for Each Crop:")
            st.markdown(
                "= (Seed Cost \\* Planters) \\* 1-Sowing% + (Rounded Soil Cost) + (Fertilizer Cost \\* Fertilizer) \\* (harvests)"
            )
            st.write("")
            st.header("Farm Configuration:")
            st.write(f"You selected: {hoeType} Sowing: {sowingLevel} Yielding: {yieldingLevel}")
            st.dataframe(checkedCrops)
            st.dataframe(results)
        else:
            st.warning('Please select at least one planter.')
    else:
        st.warning('Please select at least one crop.')
