class Searching:
    def __init__(self):
        pass
    def perform_binary_search(self, input_array: [], input_element: int):
        left, right = 0, len(input_array) - 1
        while left <= right:
            mid = (left + right)//2
            if input_element == input_array[mid]:
                return mid
            elif input_element < input_array[mid]:
                right = mid - 1
            elif input_element > input_array[mid]:
                left = mid + 1
        return -1