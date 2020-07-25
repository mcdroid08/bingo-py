import sys
from random import randint, shuffle
from time import sleep

class Bingo :

    #constructor
    def __init__(self, size, show_comp_board) :
        self.show_comp_board = show_comp_board
        self.size = size #size of board
        self.user_moves = self.make_empty_board() #1 means move left 0 means position left for user to play
        self.comp_moves = self.make_empty_board() # for comp moves
        self.moves_to_play = [i for i in range(1,size*size+1)] #stores the all moves left for baord
        shuffle(self.moves_to_play) #shuffle array for comp moves 
        self.user_board = self.create_random_board() #create board for user
        self.comp_board = self.create_random_board() #create board for comp

        self.player = "user" # keep track of which one's  move it is
        self.user_lines = 0 #number of lines user has formed
        self.comp_lines = 0 #number of lines comp has formed
        self.SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉") # to convert number for better visiblity
    

    #overriding function for print
    def __str__(self) :
        #print("Moves to play : ", self.moves_to_play)
        #print("user : ", self.user_moves)
        #print("comp : ", self.comp_moves)
        res = "==========================================================\nUser Board :\n"

        # create string for user board
        for i in range(self.size) :
            #for each row
            for j in range(self.size) :
                if self.user_moves[i][j] == 1 :
                    res += "X" + 7 * " "  #add X for visited ones
                else :
                    res += str(self.user_board[i][j]).translate(self.SUB) + (8-len(str(self.user_board[i][j])))*" " #add small number for number in board
            res += "\n"

        res += "\n"
        
        if self.show_comp_board : #if computer board have visible activated
            res += "Computer Board :\n"
            #for comp board
            for i in range(self.size) :
                #for each row
                for j in range(self.size) :

                    if self.comp_moves[i][j] == 1 :  #add X for visited
                        res += "X" + 7 * " "
                    else :
                        res += "-" + 7 * " " #add  - for unvisited

                res += "\n"

        res += "=========================================================="
        
        return res

    
    #make empty board with size by size
    def make_empty_board(self) :
        board = [] #create list
        for i in range(self.size) :
            board.append([0]*self.size) #append list times size to board with 0's
        return board


    #generate a size by size board with random values
    def create_random_board(self):
        board = [] #final board
        possible_values = [i for i in range(1, self.size*self.size+1)] # all possible values ie for size = 5 , values are 1..25
        shuffle(possible_values) #randomize vaules

        for i in range(self.size): #iterate for all possible indeces
            board.append([]) 
            for j in range(self.size) :
                board[i].append(possible_values.pop()) # add value to board
        return board


    # given a number and player return pair of index for (i,j) for that player's board
    def get_index(self, move, player) :
        #select board to find
        cur_board = self.user_board if player == "user" else self.comp_board 
        #initiaize positon pair
        pos = []

        for i in range(self.size) :
            for j in range(self.size) :  # find in whole board

                if cur_board[i][j] == move : # when number found 
                    pos.append(i) # add pos to pair
                    pos.append(j)

        return pos #return pair


    #make move for user or comp
    def make_move(self) :

        is_winner_found = False #keep track of is game completed on not

        #if current payer is user
        if self.player == "user" :

            user_move = input("Enter move to play : ") #get user move
            #if move is valid ie (its a digit, its within board range, its avaiable on board) if not return here
            if (not user_move.isdigit()) or (int(user_move) > self.size * self.size) or (int(user_move) not in self.moves_to_play):
                return False

            self.update_move(int(user_move)) # upadate that move on both boards
            self.moves_to_play.remove(int(user_move)) #remove user move from comp all moves, so comp wont play it 
            print("Upadting ", user_move, "in both boards...") #show status of pick

            is_winner_found = self.check_win() #check if user won

            print(f"Lines completed - User : {self.user_lines} Comp : {self.comp_lines}") #show status for lines can be made

            self.player = "comp" #set player for next move that will be computer

        else :

            comp_move = self.moves_to_play.pop() # get move for computer to play

            self.update_move(comp_move)  #update that on both boards

            print("Computer selected : ", comp_move, ", updating in both boards...") #show pick to user

            is_winner_found =  self.check_win() # check if computer won 

            print(f"Lines completed - User : {self.user_lines} Comp : {self.comp_lines}") #show status of lines can be made

            self.player = "user" #set player for next move for user

        return is_winner_found #return if game ended

    
    #update move on both boards
    def update_move(self, move_to_play):
        index = self.get_index(move_to_play, "user") #get index for next move of user
        self.user_moves[index[0]][index[1]] = 1 #set move for user
        index = self.get_index(move_to_play, "comp") #get index for next move of comp
        self.comp_moves[index[0]][index[1]] = 1 #set move for comp


    #check if our cur player won the game & update the number of lines for user and comp
    def check_win(self) :
        lines = 0 # total lines that can be made on board
        for i in range(self.size) : # for each row and col
            if self.check_col(i) : # for each col
                lines += 1
            if self.check_row(i) : # for each row
                lines += 1

        #check diagonals
        if self.check_left_diagonals() :
            lines += 1
        if self.check_right_diagonals() :
            lines += 1


        #update the line numbers
        if self.player == "user" :
            self.user_lines = lines
        else :
            self.comp_lines = lines

        #return weather game is won by some player or not
        if lines >= 3 :
            return True

        return False


    #for given row, check weather it is fully checked for current player
    def check_row(self, row_num) :
        cur_moves = self.user_moves if self.player == "user" else self.comp_moves #select cur user
        for i in range(self.size) : 
            if cur_moves[row_num][i] == 0 : #if row num have any zero, means cannot make line
                return False
        return True
            
    
    #for given col, check weather it is fully checked for current player
    def check_col(self, col_num) :
        cur_moves = self.user_moves if self.player == "user" else self.comp_moves #select current user
        for i in range(self.size) :
            if cur_moves[i][col_num] == 0 : #if col num have any zero, means cannot make line
                return False
        return True

    
    #check weather left diagonal is funlly checked for current user
    def check_left_diagonals(self) :
        cur_moves = self.user_moves if self.player == "user" else self.comp_moves #select current user
        for i in range(self.size) : 
            if cur_moves[i][i] == 0 :  # left diagonal is when (i,j) i==j
                return False
        return True
    

    #check weather right diagonal is fully checked for current user
    def check_right_diagonals(self) :
        cur_moves = self.user_moves if self.player == "user" else self.comp_moves #select current player
        for i in range(self.size) :
            if cur_moves[i][self.size - i - 1] == 0 : # right diagonal is when (i,j) i=i, and j = len-i
                return False
        return True


    #return which user won the game
    def get_winner(self) :
        return "User" if self.player == "comp" else "Computer" #need to swap as player will swap at end of make move funciton



def main():

    #get board size
    size = 0
    if len(sys.argv) > 1 and sys.argv[1].isdigit() and int(sys.argv[1]) > 2 and int(sys.argv[1]) <21: # if command lne argument is passed & valid
        size = int(sys.argv[1])
    else :
        size = 5

    #create game object
    game = Bingo(size, True)

    print(game)

    #while moves can be made
    while not game.make_move() : 
        print(game)
        sleep(0.5)
        
    print(game)
    print(game.get_winner() + " won the game.")

if __name__ == "__main__":
    main()
