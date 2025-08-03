import streamlit as st
import pandas as pd
import plotly.graph_objects as go
def tab2Content():
    if 'results' in st.session_state:
        checkedCrops=st.session_state.checkedCrops
        results = st.session_state.results
        results2 = st.session_state.results2
        allCostBreakdown = st.session_state.allCostBreakdown
        suppliesCount = st.session_state.suppliesCount

        sumTotalCost = sum(results["totalCosts"])
        sumTotalIncome = sum(results["totalIncome"])

        st.header("Calculated Results:")
        st.success(f"Total Profit from Farm: {sumTotalIncome - sumTotalCost} rubies.")
        st.success(f"Total Income from All Crops: {sumTotalIncome} rubies.")
        st.success(f"Total Cost of Farm: {sumTotalCost} rubies.")
        
        incomeOverview(results,results2)

        costBreakdownChart(results["Crops"],allCostBreakdown)

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


def incomeOverview(results,results2):
    if 'show_per_crop' not in st.session_state:
        st.session_state.show_per_crop = True  # Default to showing per crop
    # Button to toggle between graphs
    if st.button("Toggle Financial Overview"):
        st.session_state.show_per_crop = not st.session_state.show_per_crop
    # Display the selected graph
    if st.session_state.show_per_crop:
        fig = go.Figure()
        colors = ['#8CD9C2', '#D88C8C', '#D1D54D']

        for category, color in zip(['totalIncome', 'totalCosts', 'totalProfits'], colors):
            fig.add_trace(go.Bar(name=category, x=results2["Crops"], y=results2[category], marker=dict(color=color)))

        fig.update_layout(title='Financial Overview per Crop', barmode='group', 
                          xaxis_title='Crops', yaxis_title='Amount (in Rubies)', 
                          template='plotly')
        st.plotly_chart(fig)
    else:
        fig = go.Figure()
        colors = ['#8CD9C2', '#D88C8C', '#D1D54D']
        for category, color in zip(['totalIncome', 'totalCosts', 'totalProfits'], colors):
            fig.add_trace(go.Bar(name=category, x=results["Crops"], y=results[category], marker=dict(color=color)))

        fig.update_layout(title='Financial Overview per Crop Planter Type', barmode='group', 
                          xaxis_title='Crops', yaxis_title='Amount (in Rubies)', 
                          template='plotly')
        st.plotly_chart(fig)

def costBreakdownChart(col,allCostBreakdown):
    costCategories = list(allCostBreakdown[0].keys())
    costValues = {category: [] for category in costCategories}
    for breakdown in allCostBreakdown:
        for category in costCategories:
            costValues[category].append(breakdown[category])

    fig = go.Figure()
    cost_colors = ['#B8E4A0', '#DE9B23', '#7FC7D4', '#E4C679', '#F26F6D']

    for category, color in zip(costCategories, cost_colors):
        fig.add_trace(go.Bar(name=category, x=col, y=costValues[category], marker=dict(color=color)))

    fig.update_layout(title='Cost Breakdown Overview', barmode='stack', 
                      xaxis_title='Crops', yaxis_title='Amount (in Rubies)', 
                      template='plotly')
    st.plotly_chart(fig)