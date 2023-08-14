import numpy as np
import scipy

def load_input_file(file_name):
    with open(file_name, 'r') as file:
        n, H = map(int, file.readline().split())
        tile_types = np.zeros((n, n), dtype=int)
        tile_values = np.zeros((n, n), dtype=int)

        for i in range(n * n):
            if i == 0:
                continue  # the initial tile is zero type with zero value
            x, y, t, v = map(int, file.readline().split())
            tile_types[x][y] = t
            tile_values[x][y] = v

    return n, H, tile_types, tile_values


def print_tile_data(tile_types, tile_values):
    print("Tile Types:")
    print(tile_types)
    print("\nTile Values:")
    print(tile_values)


def DP(n, H, tile_types, tile_values, n1, n2, protection = False, multiplier = 1, memo=[]):
    # TODO
    # Placeholder function - implement your logic here
    # Your code to check whether it is possible to reach the bottom-right
    # corner without running out of HP should go here.
    # You should use dynamic programming to solve the problem.
    # Return True if possible, False otherwise.

    # By defualt we return False
    if H < 0: return False
    elif (n1 == n-1) and (n2 == n-1): return True
    if (H in memo.keys()) and (memo[H][n1][n2][int(protection)][multiplier-1] != -1): return memo[H][n1][n2][int(protection)][multiplier-1]

    Downval = tile_values[min(n1+1, n-1)][n2]
    Rightval = tile_values[n1][min(n2+1, n-1)]
    Downtype = tile_types[min(n1+1, n-1)][n2]
    Righttype = tile_types[n1][min(n2+1, n-1)]
    Downval = Downval * (Downtype == 1) - Downval * (Downtype == 0)
    Rightval = Rightval * (Righttype == 1) - Rightval * (Righttype == 0)
    if Downtype == 3:
        Down = DP(n, (H if n1<(n-1) else -1), tile_types, tile_values, min(n1+1, n-1), n2, protection=protection, multiplier=2, memo=memo)
    if Righttype == 3:
        Right = DP(n, (H if n2<(n-1) else -1), tile_types, tile_values, n1, min(n2+1, n-1), protection=protection, multiplier=2, memo=memo)
    if protection:
        Down = DP(n, (H+(Downval>0)*Downval*multiplier if n1<(n-1) else -1), tile_types, tile_values, min(n1+1, n-1), n2, protection=(Downval>0), multiplier=(multiplier if (Downval<0) else 1), memo=memo) 
        Right = DP(n, (H+(Rightval>0)*Rightval*multiplier if n2<(n-1) else -1), tile_types, tile_values, n1, min(n2+1, n-1), protection=(Rightval>0), multiplier=(multiplier if (Rightval<0) else 1), memo=memo)
    else:
        Down = DP(n, (H+(Downval>0)*Downval*multiplier+(Downval<0)*Downval if n1<(n-1) else -1), tile_types, tile_values, min(n1+1, n-1), n2, protection=(Downtype==2), multiplier=(multiplier if (Downval<0) else 1), memo=memo)
        Right = DP(n, (H+(Rightval>0)*Rightval*multiplier+(Rightval<0)*Rightval if n2<(n-1) else -1), tile_types, tile_values, n1, min(n2+1, n-1), protection=(Righttype==2), multiplier=(multiplier if (Rightval<0) else 1), memo=memo)
    
    # TODO you should change this
    res = Down or Right
    try: memo[H][n1][n2][int(protection)][multiplier-1] = res
    except:
        memo[H] = np.ones((n, n, 2, 2)) * -1
        memo[H][n1][n2][int(protection)][multiplier-1] = res
    return res


def write_output_file(output_file_name, result):
    with open(output_file_name, 'w') as file:
        file.write(str(int(result)))


def main(input_file_name):
    n, H, tile_types, tile_values = load_input_file(input_file_name)
    print_tile_data(tile_types, tile_values)
    memo={}
    result = DP(n, H, tile_types, tile_values, 0, 0, protection = False, multiplier = 1, memo=memo)
    print("Result: " + str(result))
    output_file_name = input_file_name.replace(".txt", "_out.txt")
    write_output_file(output_file_name, result)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python kill_Down_with_Trojans.py a_file_name.txt")
    else:
        main(sys.argv[1])
    #main("test_3.txt")
