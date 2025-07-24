import streamlit as st
import pandas as pd

def orbucksmaxxing(itemsCount, current_value=0, current_index=0, current_cost=0):
    total_orbucks = (current_value + original)
    total_bundles = total_orbucks / bundleCost
    
    # Base case: check if we have a valid combination
    if total_orbucks % bundleCost == 0 and current_value > 0 and current_cost<convMaxPayment:
        if total_bundles not in valid_bundles:
            valid_costs.append(current_cost)
            valid_counts.append(itemsCount.copy())
            valid_bundles.append(total_bundles)
            return current_cost, itemsCount
        else:
            index = valid_bundles.index(total_bundles)
            if valid_costs[index] > current_cost:
                valid_counts[index] = itemsCount.copy()
                valid_costs[index] = current_cost
            return current_cost, itemsCount

    # Base case: check if we have exhausted all items
    if current_index >= len(items) or current_cost>convMaxPayment:
        return float('inf'), []  # No valid combination found

    # Initialize minimum cost
    min_cost = float('inf')
    best_count = None

    for count in range(0, 101): 
        itemsCount[current_index] = count
        cost, count_result = orbucksmaxxing(
            itemsCount.copy(),
            current_value + count * items[current_index][0],
            current_index + 1,
            current_cost + count * items[current_index][1]
        )
        # Update minimum cost if a better option is found
        if cost < min_cost:
            min_cost = cost
            best_count = count_result

    # Exclude the current item
    exclude_item_cost, exclude_itemsCount = orbucksmaxxing(
        itemsCount,
        current_value,
        current_index + 1,
        current_cost
    )

    # Return minimum cost between including and excluding the current item
    if exclude_item_cost < min_cost:
        return exclude_item_cost, exclude_itemsCount
    else:
        return min_cost, best_count

st.title("ORBucks Maximization")

# Default items (value in ORBucks, cost in USD)
items = [(6250, 44.99), (2750, 21.99), (1000, 8.99)]

for i in range(len(items)):
    st.write(f"Item {i+1}:", items[i])

# Other inputs
bundleCost = st.number_input("Bundle Cost (in ORBucks)", min_value=1, value=1800)
original = st.number_input("Original Value (in ORBucks)", min_value=0, value=2000)
maxPayment = st.number_input("Max Payment (in IRL Currency)", min_value=1, value=500)
sale = st.number_input("Sale %", min_value=0, max_value=100, value=25)
currencyName = st.text_input("Currency Name", value="Euro")
conversionFromUSD = st.number_input(f"Conversion Rate from USD to {currencyName}", min_value=0.0, value=0.85)
vat = st.number_input("VAT % (optional)", min_value=0, max_value=100, value=0)

convMaxPayment = (( (maxPayment / conversionFromUSD)/ ((100 - sale) / 100)) / (1 + vat / 100))
# Run the calculation when the button is pressed
if st.button("Calculate"):
    valid_costs = []
    valid_counts = []
    valid_bundles = []

    items_count = [0] * len(items)
    result, final_items_count = orbucksmaxxing(items_count)

    if valid_costs:
        # Prepare data for display
        output_data = []
        total_value = original + sum(count * item[0] for count, item in zip(final_items_count, items))
        
        st.success(f"The minimum cost for a total value divisible by {bundleCost} is: {result * ((100-sale)/100) * conversionFromUSD * (1 + vat/100):.2f} {currencyName} at {sale}% Sale")
        st.write("Total ORBucks: ", total_value)
        st.write("Total Bundles: ", total_value // 1800)
        
        # Prepare detailed results
        for i in range(len(valid_costs)):
            total_value = original + sum(valid_counts[i][j] * items[j][0] for j in range(len(items)))
            total_cost = valid_costs[i] * ((100 - sale) / 100) * conversionFromUSD * (1 + vat / 100)
            output_data.append({
                "Cost": f"{total_cost:.2f} {currencyName}",
                "Number of 6250 ORBucks Bundles": valid_counts[i][0],
                "Number of 2750 ORBucks Bundles": valid_counts[i][1],
                "Number of 1000 ORBucks Bundles": valid_counts[i][2],
                "Total ORBucks": total_value,
                "Total Bundles": int(valid_bundles[i])
            })

        # Create a DataFrame and display it as a table
        if output_data:
            df = pd.DataFrame(output_data)
            st.table(df)
        else:
            st.warning("No valid combinations found within the max payment limit.")

    else:
        st.warning("No combination of items can achieve a total value divisible by the bundle cost.")