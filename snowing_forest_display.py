import random
import time


class SnowFlake:
    symbol = "`"
    snow_flakes = []
    landed_spots = set()
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, canvas):
        direction = random.choice([(1, 1), (0, 1), (-1, 1)])
        new_x = direction[0] + self.x
        new_y = direction[1] + self.y
        
        if 0 > new_x or new_x >= len(canvas[0]) or new_y >= len(canvas):
            SnowFlake.add_snowflake(canvas)
            SnowFlake.snow_flakes.remove(self)
            
        elif canvas[new_y][new_x] != " " and canvas[new_y][new_x] != SnowFlake.symbol:
            SnowFlake.add_snowflake(canvas)
            SnowFlake.landed_spots.add((new_x, new_y))
            SnowFlake.snow_flakes.remove(self)        
        else:
            self.x = new_x
            self.y = new_y
 
    @staticmethod
    def add_snowflake(canvas):
        SnowFlake.snow_flakes.append(SnowFlake(random.randint(0, len(canvas[0]) - 1), random.randint(0, 1)))
        

def get_triangle(height, symbol="#"):
    width = height * 2 - 1
    width_middle = width // 2
    arr = [[" " for _ in range(width)] for _ in range(height)]
    
    for row_index in range(height):
        if row_index == 0:
            arr[row_index][width_middle] = symbol
        elif row_index < height - 1:
            arr[row_index][width_middle - row_index] = symbol
            arr[row_index][width_middle + row_index] = symbol
        else:
            arr[row_index] = [symbol] * width
    return arr


def convert_string_color(full_string, color):
    string_colors = {
                    "white": "10",
                    "red": "31",
                    "green": "32",
                    "brown": "33"
                    }
    
    if len(full_string) > 1:
        string = full_string[5: -4]
    elif full_string == " ":
        return full_string
    else:
        string = full_string
        
    string_color = string_colors[color]
    new_string = f"\033[{string_color}m{string}\033[0m"
    return new_string


def convert_array_color(arr, color):
    for row in arr:
        for i in row:
            temp = convert_string_color(i, color)
            arr[arr.index(row)][row.index(i)] = temp

def print_array(arr):
    for i in arr:
        row_string = "".join(i)
        print(row_string)


def paste_array_to_canvas(arr, canvas, x_padding, y_padding):
    # NOTE - arr MUST be smaller or equal size to canvas
    for y_index in range(len(arr)):
        canvas_y_index = y_padding + y_index
        canvas_x_index_start = x_padding
        canvas_x_index_end = x_padding + len(arr[0])
        canvas[canvas_y_index][canvas_x_index_start:canvas_x_index_end] = arr[y_index]        



def get_christmas_tree(height, symbol="#"):
    tree_stump = 1 # height + tree stump
    triangles = [] # Height of each of the triangles seen on the tree
    
    while True:
        if height - (sum(triangles) + 2) > len(triangles) + 2:
            triangles.append(len(triangles) + 2)
        else:
            if triangles:
                if height - (sum(triangles)) < triangles[-1]:
                    triangles[-1] += height - (sum(triangles))
                    break
            triangles.append(height - (sum(triangles)))
            break
        
    width = triangles[-1] * 2 - 1 # Array width
    arr = [[" " for _ in range(width)] for _ in range(height + tree_stump)]
    
    x_padding = 0 # Starting x index in the tree array
    y_padding = 0 # Starting y index in the tree array

    for triangle_height in triangles:     
        x_padding = (width - (triangle_height * 2 - 1)) // 2
        triangle_arr = get_triangle(triangle_height)    
        paste_array_to_canvas(triangle_arr, arr, x_padding, y_padding)
          
        y_padding += triangle_height # For the next triangle
    
    # Adding the tree stump
    for y in range(tree_stump):
        arr[-1 - y][width // 2] = symbol
    return arr


def decorate_christmas_tree(tree):
    convert_array_color(tree, "green")
    tree[-1][len(tree[0]) // 2] = convert_string_color("#", "brown")


def generate_christmas_tree(canvas_width, canvas_height):
    tree_size_variation = (5, canvas_height - 4) # max and minimum height of trees
    tree = get_christmas_tree(random.randint(tree_size_variation[0], tree_size_variation[1]))
    decorate_christmas_tree(tree)
    return tree


def generate_forest(canvas_width, canvas_height):
    num_of_trees = random.randint(3, 3)
    trees = []
    rightside_newest_tree = 5
    
    for i in range(num_of_trees):
        tree = {}
        tree["arr"] = generate_christmas_tree(canvas_width, canvas_height)
        
        canvas_x_pos = rightside_newest_tree
        canvas_y_pos = canvas_height - len(tree["arr"]) - 1
        tree["pos"] = (canvas_x_pos, canvas_y_pos)
        
        trees.append(tree)
        rightside_newest_tree += + len(tree["arr"][0]) + 5
    return trees

def make_canvas_grid(width, height):
    canvas = [[" " for _ in range(width)] for _ in range(height)]
    return canvas
    
def set_up_terminal_canvas(width, height, elements):
    terminal_canvas = make_canvas_grid(width, height)
    
    # Trees
    for e in elements:
        paste_array_to_canvas(e["arr"], terminal_canvas, e["pos"][0], e["pos"][1])
    
    for s in SnowFlake.snow_flakes:
        terminal_canvas[s.y][s.x] = SnowFlake.symbol
        
        
    for s_p in SnowFlake.landed_spots:
        terminal_canvas[s_p[1]][s_p[0]] = convert_string_color(terminal_canvas[s_p[1]][s_p[0]], "white") 
    
    terminal_canvas[-1] = ["#"] * width
    
    return terminal_canvas
    
    
def main():
    # Constats
    canvas_width = 60
    canvas_height = 20
    FPS = 2
    num_of_snow_flakes = 50
    
    terminal_canvas = make_canvas_grid(canvas_width, canvas_height)
    
    SnowFlake.snow_flakes = [SnowFlake(random.randint(1, canvas_width - 1), random.randint(1, canvas_height - 1)) for _ in range(num_of_snow_flakes)]
    elements = []
    elements.extend(generate_forest(canvas_width, canvas_height))
    
    for frame in range(300):
        # Updating each snow flake for every frame
        for flake in SnowFlake.snow_flakes:
            flake.move(terminal_canvas)  
            
        terminal_canvas = set_up_terminal_canvas(canvas_width, canvas_height, elements)
        
        # This line will clear out the console everytime it is called.
        print("\033[J", end="")
        
        # This line will print out the terminal_canvas to the console every time it is called.
        print_array(terminal_canvas)
        
        time.sleep(1 / FPS)
    
        
main()
