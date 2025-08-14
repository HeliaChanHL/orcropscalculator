import streamlit as st
import pandas as pd
from fishingData import *
import plotly.graph_objects as go
from plotly import colors
def fishperBiome(fishTypes):
    biome_counts = {}
    for attr in fishTypes.values():
        for biome in attr["biomes"]:
            if biome not in biome_counts:
                biome_counts[biome] = 0
            biome_counts[biome] += 1
    return biome_counts

# Calculate biome counts
biome_counts = fishperBiome(fishTypes)

def calcOdds(fish,j):
	fishbiome=0
	rarity = fishTypes[fish["Fish"]]["rarity"]
		
	for biome in st.session_state.bestBiomeMapping.keys():
		if fish["Fish"] in st.session_state.bestBiomeMapping[biome]:
			fishbiome=biome
			break
	return (sizeOdds[fish["Size"][j].lower()] / 100) * rarityOdds[rarity] * (1 /biome_counts[fishbiome])

def calcPrices(fish,j):
    model = fishTypes[fish["Fish"]]["model"]
    size = sizeList[model][fish["Size"][j].lower()]
    return priceList[size]+rarityList[fishTypes[fish["Fish"]]["rarity"]]

def display():
    st.header("Results:")
    st.markdown("---")
    st.subheader("Fishing Locations")
    st.write(f"Best combination with {st.session_state.minBiomesFound} unique biomes:")

    df_biome_fish = pd.DataFrame(
        st.session_state.bestBiomeMapping.items(),
        columns=["Biome Category", "Fish"]
    )
    st.dataframe(df_biome_fish)
    st.write(f"Specific Biomes in Biome categories:")
    data = [
        (
           item,
           [' '.join(word.capitalize() for word in j.split(":")[1].replace('_', ' ').split()) for j in fishingBiomes[item]]
        )
        for item in st.session_state.bestBiomeMapping.keys()

    ]

    df_inputs = pd.DataFrame(data, columns=["Biome Category","Biomes"])
    st.dataframe(df_inputs)
    st.markdown("---")
    st.subheader("Fish Income")

    data = [
        (
            item["Fish"],
            item["Size"][j],
            item["Amount"][j],
            calcPrices(item, j),
            item["Amount"][j] * calcPrices(item, j)
        )
        for item in st.session_state.inputs.values()
        for j in range(len(item["Size"]))
    ]
    df_inputs = pd.DataFrame(data, columns=["Fish", "Size", "Amount", "Price", "Total Price"])
    total_income = df_inputs["Total Price"].sum()
    st.success(f"Total Income from Selling Fish: {total_income} rubies")
    st.dataframe(df_inputs)

    st.write("Total Income per Fish Type")
    tab1, tab2, tab3 = st.tabs(["Unsorted", "By Type", "By Value"])
    with tab1:
        fishChart(df_inputs)
    with tab2:
        fishChart2(df_inputs)
    with tab3:
        fishChart3(df_inputs)
    
    st.markdown("---")
    st.subheader("Fish Odds:")

    data = [
        (
            item["Fish"],
            fishTypes[item["Fish"]]["biomes"],
            item["Size"][j],
            calcOdds(item,j),
        )
        for item in st.session_state.inputs.values()
        for j in range(len(item["Size"]))
    ]

    df_inputs = pd.DataFrame(data, columns=["Fish", "Biomes", "Size", "Catch Odds % per Fish"])
    st.dataframe(df_inputs)

    with st.expander("Raw Inputs:", expanded=False):
        st.write(st.session_state.inputs)

def fishChart(df_inputs):
    fig = go.Figure()
    default_colors = colors.DEFAULT_PLOTLY_COLORS
    for index, fish in enumerate(df_inputs['Fish'].unique()):
        fish_data = df_inputs[df_inputs['Fish'] == fish]
        
        combined_x = [f"{fish} - {size}" for size in fish_data['Size']]
        
        fig.add_trace(go.Bar(
            x=combined_x, 
            y=fish_data['Total Price'],
            name=fish,
            marker_color=default_colors[index % len(default_colors)]
        ))

    # Update layout
    fig.update_layout(
        title='Total Income per Fish Type - (Raw Input)',
        xaxis_title='Fish Type - Size',
        yaxis_title='Total Price',
        barmode='group'  # Group bars by fish type
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

def fishChart2(df_inputs):
    # Initialize the figure
    fig = go.Figure()
    added_fish_names = set()
    # Get unique fish types and sorted size types
    unique_fish = sorted(df_inputs['Fish'].unique())
    sorted_size_types = list(sizeOdds.keys())  # Assuming sizeOdds is defined elsewhere
    default_colors = colors.DEFAULT_PLOTLY_COLORS

    for index, fish in enumerate(unique_fish):
        fish_data = df_inputs[df_inputs['Fish'] == fish]
        sorted_dict = [None for _ in sorted_size_types]  # Use None for uninitialized values
        
        for j, size_type in enumerate(sorted_size_types):
            for i in range(len(fish_data)):
                if size_type.capitalize() == fish_data["Size"].iloc[i]:
                    sorted_dict[j] = (fish_data["Size"].iloc[i], fish_data["Total Price"].iloc[i])
                    break

        for sizeAmount in sorted_dict:
            if sizeAmount is not None:
                size, totalprice = sizeAmount
                show_legend = fish not in added_fish_names
                if show_legend:
                    added_fish_names.add(fish)
                fig.add_trace(go.Bar(
                    x=[f"{fish} - {size}"], 
                    y=[totalprice], 
                    name=fish,
                    marker_color=default_colors[index % len(default_colors)],
                    showlegend=show_legend
                ))

    fig.update_layout(
        title='Total Income per Fish Type - (Sorted by Fish)',
        xaxis_title='Fish Type - Size',
        yaxis_title='Total Price',
        barmode='group' 
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

def fishChart3(df_inputs):
    # Create a new DataFrame with fish, size, and total price
    data = []
    for fish in df_inputs['Fish'].unique():
        fish_data = df_inputs[df_inputs['Fish'] == fish]
        for _, row in fish_data.iterrows():
            data.append({'Fish': fish, 'Size': row['Size'], 'Total Price': row['Total Price']})

    # Convert to DataFrame
    fish_df = pd.DataFrame(data)

    # Sort by total price
    fish_df = fish_df.sort_values(by='Total Price', ascending=True)
    # Initialize figure
    fig = go.Figure()
    default_colors = colors.DEFAULT_PLOTLY_COLORS
    added_fish_names = set()
    index=-1
    for fish in fish_df.iterrows():
        show_legend = fish[1]['Fish'] not in added_fish_names
        if show_legend:
            index+=1
            added_fish_names.add(fish[1]['Fish'])

        fig.add_trace(go.Bar(
            x=[f"{fish[1]['Fish']} - {fish[1]['Size']}"], 
            y=[fish[1]['Total Price']], 
            name=fish[1]['Fish'],
            marker_color=default_colors[index % len(default_colors)],
            showlegend=show_legend
        ))

    # Update layout
    fig.update_layout(
        title='Total Price per Fish Type - (Sorted by Value)',
        xaxis_title='Fish Type - Size',
        yaxis_title='Total Price',
        barmode='group'  # Group bars by fish type
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)