def binary_search(sorted_array, target):
    low, high = 0, len(sorted_array) - 1
    iterations = 0

    while low <= high:
        mid = (low + high) // 2
        mid_value = sorted_array[mid]
        iterations += 1

        if mid_value < target:
            low = mid + 1
        elif mid_value > target:
            high = mid - 1
        else:
            return iterations, mid_value

    # Якщо елемент не знайдено, повертаємо "верхню межу"
    if low < len(sorted_array):
        upper_bound = sorted_array[low]
    else:
        upper_bound = None

    return iterations, upper_bound


# Приклад використання:
sorted_array = [0.1, 0.3, 0.5, 0.7, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
target_value = 1.3

result = binary_search(sorted_array, target_value)
print(result)
