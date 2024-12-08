import random
import json
import time

# Initialize the tic-tac-toe board
ttt = ["[ ]"] * 9
q_table = {}  # Dictionary to hold the Q-values
learning_rate = 0.1
discount_factor = 0.9
exploration_rate = 0.2

# Function to get the board state as a tuple
def get_state(board):
    return tuple(board)  # The state should be a tuple of board values

# Function to initialize Q-values for a state
def initialize_state(state):
    if state not in q_table:
        q_table[state] = [0] * 9  # One Q-value for each possible move

# Function to choose an action (move) based on exploration/exploitation
def choose_action(state):
    available_moves = [i for i in range(9) if state[i] == "[ ]"]
    if not available_moves:  # If no available moves, return -1 or some error indicator
        return -1  # Returning -1 or a non-valid move in case the board is full
    if random.random() < exploration_rate:  # Explore
        return random.choice(available_moves)
    else:  # Exploit
        q_values = q_table[state]
        return max(available_moves, key=lambda x: q_values[x])

# Function to check if a player has won
def check_winner(board, marker):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    return any(all(board[i] == marker for i in line) for line in win_conditions)

# Function to update Q-values
def update_q_value(prev_state, action, reward, new_state):
    max_future_q = max(q_table[new_state]) if new_state in q_table else 0
    q_table[prev_state][action] += learning_rate * (reward + discount_factor * max_future_q - q_table[prev_state][action])

# Save Q-table to a file (convert keys to strings)
def save_q_table(q_table, filename="q_table.json"):
    # Convert the state (tuple) keys to strings for serialization
    serializable_q_table = {str(key): value for key, value in q_table.items()}
    with open(filename, "w") as file:
        json.dump(serializable_q_table, file)

# Load Q-table from a file (convert string keys back to tuples)
def load_q_table(filename="q_table.json"):
    try:
        with open(filename, "r") as file:
            serializable_q_table = json.load(file)
            # Convert the string keys back to tuples (for valid board states)
            return {tuple(eval(key)): value for key, value in serializable_q_table.items()}
    except json.JSONDecodeError:
        print("Error loading Q-table: Invalid JSON format. Starting fresh.")
        return {}  # Return an empty Q-table if there's a decoding error
    except FileNotFoundError:
        print("Q-table file not found. Starting fresh.")
        return {}  # Return an empty Q-table if file doesn't exist

# Periodically save Q-table every 5 minutes
def auto_save(q_table, interval=300):
    last_save_time = time.time()
    while True:
        time.sleep(1)  # Sleep 1 second to check periodically
        if time.time() - last_save_time >= interval:
            save_q_table(q_table)
            print("Q-table saved!")
            last_save_time = time.time()

# Main game loop for self-play
# Main game loop for self-play
def play_game():
    global q_table
    game_counter = 0

    # Load the Q-table when the program starts
    q_table = load_q_table()

    # Start auto-saving in a separate thread
    import threading
    save_thread = threading.Thread(target=auto_save, args=(q_table, 300))  # Save every 5 minutes (300 seconds)
    save_thread.daemon = True
    save_thread.start()

    while True:
        print("Game:", game_counter + 1)
        # Initialize a new empty board
        ttt = ["[ ]"] * 9

        # Game loop until a winner or draw is found
        while True:
            # Player 1 (AI as 'X') makes a move
            state_player1 = get_state(ttt)
            initialize_state(state_player1)
            action_player1 = choose_action(state_player1)
            if action_player1 == -1:
                break  # No available moves left, end the game
            ttt[action_player1] = "[X]"

            # Check if Player 1 wins
            if check_winner(ttt, "[X]"):
                print("Player 1 (X) wins!")
                reward_player1 = 1
                reward_player2 = -1
                break

            # Player 2 (AI as 'O') makes a move
            state_player2 = get_state(ttt)
            initialize_state(state_player2)
            action_player2 = choose_action(state_player2)
            if action_player2 == -1:
                break  # No available moves left, end the game
            ttt[action_player2] = "[O]"

            # Check if Player 2 wins
            if check_winner(ttt, "[O]"):
                print("Player 2 (O) wins!")
                reward_player1 = -1
                reward_player2 = 1
                break

            # Check for a draw (no empty spaces left)
            if "[ ]" not in ttt:
                print("Draw!")
                reward_player1 = 0
                reward_player2 = 0
                break

        # Update Q-values for both players
        update_q_value(state_player1, action_player1, reward_player1, get_state(ttt))
        update_q_value(state_player2, action_player2, reward_player2, get_state(ttt))

        # Save Q-table after each game
        save_q_table(q_table)

        # Increment game counter and continue
        game_counter += 1

# Run the game loop
if __name__ == "__main__":
    play_game()
