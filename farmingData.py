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




tab1Text = """
### Welcome to the OR Farming Calculator!
#### 1. Tool Configuration
- **Harvesting Hoe Type**: 
  - Select the type of hoe you want to use from the dropdown menu. This choice affects your crop yield.
  
- **Sowing Level**: 
  - Choose a level from the dropdown menu that indicates how well you can plant your crops. Higher levels can lead to better results.
  
- **Yielding Level**: 
  - Pick a level that shows how much you can expect to harvest. Again, higher levels are better.

#### 2. Crop Configuration
- **Select Crops**: 
  - In the left column, you’ll see a list of crops available. Check the boxes next to the crops you want to grow.
  
- **Planter Setup**: 
  - For each crop you selected:
    - Click on the crop's tab to access its settings.
    - Inside that tab, you'll see options for different types of planters.
      - **Number of Planters**: Enter how many setups of that planter you want to use for the selected crop.
      - **Soil Setups**: Specify how many of the planter setups will **contain soil**. This indicates the number of setups that are using soil.
      - **Fertilizer Setups**: Indicate how many of the planter setups will **contain fertilizer**. This shows the number of setups that are using fertilizer.

#### 3. Miscellaneous
- **Harvests**: 
  - Enter the number of seeds you plan to plant in each planter. This can be between 1 and 64 seeds.
  
- **Calculate Costs and Supplies**: 
  - You can choose to calculate the costs and supplies needed for planters and sprinklers by checking the boxes at the bottom.

#### Once you have filled out all the necessary information, you can proceed with the calculations or actions related to your crop planning!

---

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