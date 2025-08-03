import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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