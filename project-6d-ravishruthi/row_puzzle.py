# Author: Shruthi Ravi
# Date: 02/08/2021
# Description: A row puzzle that starts of at leftmost square and moves either
#              right or left to get to the rightmost square. If it does, returns
#              True. It returns False, if not possible.
#

def shift_right(num_list, index):  # Helper function
    """
        Checks if current index can move right legally.
        Returns true if possible, false if not.
    """
    if index == 0:  # At leftmost index
        return True
    if index + num_list[index] < len(num_list):  # Checks if it goes of right end
        return True
    return False


def shift_left(num_list, index):
    """
        Checks if current index can move left legally.
        Returns true if possible, false if not.
    """
    if index == 0:  # At leftmost index
        return False
    if index - num_list[index] < 0:  # Checks if it goes of left end
        return False
    return True


def row_puzzle(num_list, pos=0, memo=None):
    """
        Takes a list of numbers, a current index (pos) and memo as parameters.
        Checks legal moves and recursively calls function in that direction.
        If it reaches rightmost index, it returns True. False if not.
    """
    # print("index:", pos, " memo:", memo)
    if memo is None:
        memo = {}
    if pos not in memo:  # If pos not in memo, create new key
        memo[pos] = []
    if len(num_list) - 1 in memo:  # At rightmost index
        return True

    right = shift_right(num_list, pos)  # Checks move right
    left = shift_left(num_list, pos)  # Checks move left

    if len(memo[pos]) == 0:  # Makes sure no repetitive recursive calls
        if right and not left:
            memo[pos].append("right")
            memo[pos].append("no left")
            right = row_puzzle(num_list, pos + num_list[pos], memo)
            if right:
                return True
            return False
        elif left and not right:
            memo[pos].append("left")
            memo[pos].append("no right")
            left = row_puzzle(num_list, pos - num_list[pos], memo)
            if left:
                return True
            return False
        elif left and right:
            memo[pos].append("right")
            right = row_puzzle(num_list, pos + num_list[pos], memo)
            memo[pos].append("left")
            left = row_puzzle(num_list, pos - num_list[pos], memo)
            if not left and not right:
                return False
            return True
    if not left and not right:  # If stuck (cannot move left or right)
        return False
