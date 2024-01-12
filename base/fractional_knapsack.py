def fractional_knapsack(items, capacity):
    # item[1] - value item[0] - capacity
    # Calculate the value-to-weight ratio for each item
    # print('frac_knap',items)
    y=[]
    for item in items:
        # print('item0',item[0])
        # print('item1',item[1])
        x = (int(item[1]) / int(item[0]))
        # print(x)
        y.append(x)
    # print(y)    
    # Sort the items by the value-to-weight ratio in descending order
    sorted_items = [x for _, x in sorted(zip(y, items), reverse=True)]
    selected_items = []
    # print(sorted_items)
    total_value = 0
    for item in sorted_items:
        if capacity >= float(item[0]):
            # Take the whole item
            capacity -= float(item[0])
            total_value += float(item[1])
            selected_items.append(item)
        else:
            # Take a fraction of the item
            fraction = capacity / float(item[0])
            selected_items.append((item,fraction))
            total_value += float(item[1]) * fraction
            break
    # print(total_value,selected_items)    
    return total_value,selected_items

# Example usage
# items = [(60, 10), (100, 20), (120, 30)]
# capacity = 50
# print(fractional_knapsack(items, capacity))
