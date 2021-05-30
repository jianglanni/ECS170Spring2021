# Lan Jiang
# ECS170
# HW4

# The perceptron itself and the interface for testing.
def perceptron(threshold, adjust, weights, examples, max_laps):
    print("Starting weights:", weights)
    print("Threshold:", threshold, "Adjustment:", adjust)
    print("")
    # Initialize
    lap = 1  # Start from pass 1
    size = len(weights)  # The amount of inputs
    # Start to run the examples.
    while lap <= max_laps:
        print("Pass", lap)
        print("")
        for i in range(0, len(examples)):
            sum_value = 0.0
            for j in range(0, size):
                if examples[i][1][j] == 1:
                    sum_value += weights[j]  # Calculate the prediction
            result = sum_value > threshold  # Compare the prediction with the threshold
            if result and not examples[i][0]:  # Encounter a false positive
                for k in range(0, size):
                    if examples[i][1][k] == 1:
                        weights[k] -= adjust
            elif not result and examples[i][0]:  # Encounter a false negative
                for k in range(0, size):
                    if examples[i][1][k] == 1:
                        weights[k] += adjust
            print("inputs:", examples[i])
            print("prediction:", result, "answer:", examples[i][0])
            print("adjusted weights:", weights)
        print("")
        lap += 1  # go for the next pass
    return


# learning1 = [[True,  [1,1,1,1,0]], [False, [1,1,1,1,1]], [False, [0,0,0,0,0]], [False, [0,0,1,1,0]],
#             [False, [1,0,1,0,1]], [False, [1,0,1,0,0]], [False, [0,1,0,1,1]], [False,[0,1,0,1,0]],
#             [False, [0,0,1,0,0]], [False, [0,0,0,1,0]]]
# learning2 = [[True, [1,1]], [False, [0,0]], [True, [0,1]], [True, [1,0]]]
#
# perceptron(0.5, 0.1, [-0.5, 0, 0.5, 0, -0.5], learning1, 4)  # Given example 1
# perceptron(0.4, 0.09, [0.3, -0.6], learning2, 10)  # Given example 2
