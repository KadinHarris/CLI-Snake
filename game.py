import msvcrt
import random
import sys
import time

WIDTH = 19
HEIGHT = 17

# init_board() - initializes and draws the first state of the board
def init_board():
    board = [0] * HEIGHT # Board is an array of 0's times the HEIGHT

    for i in range(HEIGHT): # Loop over the Height of the board and create arrays representing the width
        if i == HEIGHT - 1 or i == 0:
            board[i] = ["#"] * WIDTH # A '#' indicates a border cell
        else:
            board[i] = ["."] * WIDTH # '.' indicates an empty cell

        board[i][0] = "#"
        board[i][WIDTH - 1] = "#"

    return board

# draw_board()- Draws the current state of the board to the console
#   board - the board list
def draw_board(board):
    for i in range(HEIGHT):
        for j in range(WIDTH):
            print(board[i][j], end=" ")
        print()

# update_board() - updates the board structure to represent the current position of the snake
#   snake() - the snake list
def update_board(snake, board):
    if len(snake) > 1:
        for i in range(0, len(snake)):
            board[snake[i][1]][snake[i][0]] = "■"

def buffer_board(board, frame, score, length):
    frame = ""
    for row in board:
        row = " ".join(row)
        frame += row + "\n"

    frame += "Score: " + str(score) + "  Length: " + str(length) + "\n"
    return frame


# move() - updates the position data of the head of snakewdd
#   direction - the current direction of the snake
def move(snake, uinput, direction):

    match uinput:
        case "w":
            if direction[1] != 1:
                direction = [0, -1]
        case "a":
            if direction[0] != 1:
                direction = [-1, 0]
        case "s":
            if direction[1] != -1:
                direction = [0, 1]
        case "d":
            if direction[0] != -1:
                direction = [1, 0]
        case "H":
            if direction[1] != 1:
                direction = [0, -1]
        case "K":
            if direction[0] != 1:
                direction = [-1, 0]
        case "P":
            if direction[1] != -1:
                direction = [0, 1]
        case "M":
            if direction[0] != -1:
                direction = [1, 0]
    snake[0][0] += direction[0]
    snake[0][1] += direction[1]

    return snake, direction

# check_collision() - checks if snake has collided with itself or the board barrier
def check_collision(snake):
    for i in range(1, len(snake)):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            return True

    if snake[0][0] == WIDTH - 1 or snake[0][1] == HEIGHT - 1 or snake[0][0] <= 0 or snake[0][1] <= 0:
        return True

    return False

# spawn_food() - spawns the food at a random position within the board bounds
def spawn_food(snake, board):
    x = random.randint(1, WIDTH - 2)
    y = random.randint(1, HEIGHT - 2)

    # If food is in snake get new pos
    while [x, y] in snake:
        x = random.randint(1, WIDTH - 2)
        y = random.randint(1, HEIGHT - 2)

    board[y][x] = '@'

    return x, y

# check_food_collision() - checks if the snake head pos is the same as food
def check_food_collision(snake, x, y):
    if snake[0][0] == x and snake[0][1] == y:
        return True
    else:
        return False

def main():
    # VARIABLES
    snake = [[WIDTH//2, HEIGHT//2], [WIDTH//2, (HEIGHT//2) + 1]]
    board = init_board()
    direction = [0, -1]
    grow = False
    ticker = 0.0
    frame = ""
    score = 0
    length = len(snake)

    # SETUP
    print("\033[H\033[J", end="")  # Clear the screen
    f_x, f_y = spawn_food(snake, board)

    update_board(snake, board)
    frame = buffer_board(board, frame, score, length)
    print(frame, end="")
    sys.stdout.flush()

    u_input = input("Press enter to start... (q to quit): ")

    if u_input == "q":
        exit(1)

    # GAME LOOP
    while True:
        print("\033[H\033[J", end="") #Clear the screen

        if msvcrt.kbhit():
            u_input = msvcrt.getch()
            if u_input in (b'\x00', b'\xe0'):
                u_input = msvcrt.getch()

            u_input = u_input.decode("utf-8")

        if u_input == "q":
            break

        if ticker >= 0.22:
            board[snake[len(snake) - 1][1]][snake[len(snake) - 1][0]] = "."  # remove current tail at current tail pos

            # Get the current pos of the tail for growth
            tail_x = snake[len(snake) - 1][0]
            tail_y = snake[len(snake) - 1][1]
            tail = [tail_x, tail_y]
            # Print the current position of all the snake
            # for i in range(0, len(snake)):
            # print("Snake position: x->", snake[i][0], " y->", snake[i][1])


            # If we're not growing then make the body follow, allowing the body to not follow for one tick when we're
            # growing allows for a simulation of growth in the snaek
            if not grow:
                if len(snake) > 1:
                    # Loop over tail to  head and update body pos to its leading body part
                    for i in range(len(snake) - 1, 0, -1):
                        snake[i][0] = snake[i - 1][0]
                        snake[i][1] = snake[i - 1][1]



            snake, direction = move(snake, u_input, direction) # update snake pos and current direction

            # Check if snake head has collided with food
            if check_food_collision(snake, f_x, f_y):
                # print("ATE FOOD\n")
                grow = True
                snake.append(tail)
                f_x, f_y = spawn_food(snake, board) # f_x, f_x = new food position
                score += 1
                length = len(snake)

            ticker = 0.0


        update_board(snake, board)  # update current state of board with current snake state
        frame = buffer_board(board, frame, score, length)
        print(frame, end="")
        sys.stdout.flush()

        # If snake collides with itself or border you lose
        if check_collision(snake):
            print("YOU LOSE!\n")
            break

        print( )

        grow = False # Growth has happened at this point so set to false
        ticker += 0.01
        time.sleep(0.01)



main()