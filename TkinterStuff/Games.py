from tkinter import *
from tkinter import messagebox

import random
import time

class GameOfLifeFrame(Frame):

    def __init__(self, parent, width: int, height: int):
        # initialize super
        Frame.__init__(self, parent)
        # flags
        self.halt_flag = False
        # create the button grid
        ButtonFrame = Frame(self)
        ButtonFrame.grid(row = 0,column = 0)
        self.cell_grid = [[Cell(i, j, False, self, ButtonFrame) for j in range(0, height)] for i in range(0, width)]
        # create the control buttons
        CtrlFrame = Frame(self)
        CtrlFrame.grid(row = 1, column = 0)
        # the scale and button for a given number of ticks
        self.tickBtn = Button(master = CtrlFrame, text = 'tick', command = self.__tick, padx = 50, pady = 1)
        self.tickBtn.grid(row = 0, column = 0)
        self.runBtn = Button(master = CtrlFrame, text = 'run', command = self.run_btn_click, padx = 50, pady = 1)
        self.runBtn.grid(row = 0, column = 1)
        self.tickScale = Scale(master = CtrlFrame, from_ = 1, to = 100, orient = HORIZONTAL)
        self.tickScale.grid(row = 0, column = 2)
    
    def __count_alive_neighbors(self, row: int, column: int):
        # the output counter
        counter = 0
        # flags for possiable neighbor locations
        inz = row > 0
        jnz = column > 0
        istw = row < len(self.cell_grid) - 1
        jsth = column < len(self.cell_grid[0]) - 1
        # count all alive neighbors
        if inz and self.cell_grid[row - 1][column].is_alive():
            counter += 1
        if jnz and self.cell_grid[row][column - 1].is_alive():
            counter += 1
        if istw and self.cell_grid[row + 1][column].is_alive():
            counter += 1
        if jsth and self.cell_grid[row][column + 1].is_alive():
            counter += 1
        if inz and jnz and self.cell_grid[row - 1][column - 1].is_alive():
            counter += 1
        if inz and jsth and self.cell_grid[row - 1][column + 1].is_alive():
            counter += 1
        if istw and jnz and self.cell_grid[row + 1][column - 1].is_alive():
            counter += 1
        if istw and jsth and self.cell_grid[row + 1][column + 1].is_alive():
            counter += 1
        # return the number of alive neighbors
        return counter

    def __tick(self):
        # if halt flag raised skip operation
        if self.halt_flag:
            return
        # count the amount of changes done
        change_counter = 0
        # construct the next time step
        new_statuses = []
        for i in range(0, len(self.cell_grid)):
            new_statuses.append([])
            for j in range(0, len(self.cell_grid[0])):
                alive_neighbors = self.__count_alive_neighbors(i, j)
                new_statuses[i].append((alive_neighbors == 2 and self.cell_grid[i][j].is_alive()) or alive_neighbors == 3)
                if new_statuses[i][j] != self.cell_grid[i][j].is_alive():
                    change_counter += 1
        # update the grid
        for i in range(0, len(self.cell_grid)):
            for j in range(0, len(self.cell_grid[0])):
                self.cell_grid[i][j].set_alive(new_statuses[i][j])
        # turn on the halt flag and relese the buttons if no changes were made
        if change_counter == 0:
            self.halt_flag = True
            self.__enable_buttons(True)

    def run_btn_click(self):
        ticks = self.tickScale.get()
        self.halt_flag = False
        self.__enable_buttons(False)
        for i in range(0, ticks):
            self.after(200 * i, self.__tick)
        self.after(200 * ticks, lambda: self.__enable_buttons(True))
    
    def __enable_buttons(self, value: bool):
        # reset buttons
        new_state = NORMAL if value else DISABLED
        self.runBtn.configure(state = new_state)
        self.tickBtn.configure(state = new_state)
        for i in range(0, len(self.cell_grid)):
            for j in range(0, len(self.cell_grid[0])):
                self.cell_grid[i][j].enable_button(value)

class Cell:

    """
    A class used to represent an cell in the game of life

    ...

    Attributes
    ----------
    btn: Button
        the button associated with this cell
    alive: bool
        the status of the current cell alive/dead

    Methods
    -------
    toggle() -> void
        changes the cell from alive to dead and vice versa
    is_alive() -> bool
        returns if the cell is alive or not
    set_alive(alive) -> void
        a method to set the state of the cell (alive / dead)
    """

    def __init__(self, cell_row: int, cell_column: int, alive: bool, contoller: GameOfLifeFrame, parent):
        """
        Parameters
        ----------
        cell_row: int
            The row this cell is located at
        cell_column: int
            The column this cell is located at
        parent
            The parent frame/tk of this cell
        """
        self.__btn = Button(master = parent, bg = 'yellow' if alive else 'white', command = self.toggle, padx = 10, pady = 5)
        self.__btn.grid(row = cell_row, column = cell_column)
        self.contoller = contoller
        self.__alive = alive

    def toggle(self):
        """
        changes the cell from alive to dead and vice versa
        """
        self.contoller.halt_flag = False
        self.set_alive(not self.__alive)

    def is_alive(self):
        """
        returns if the cell is alive or not

        Returns
        -------
        true if the cell is alive, otherwise false
        """
        return self.__alive == 1
    
    def set_alive(self, alive: bool):
        """
        a method to set the state of the cell (alive / dead)

        Parameters
        ----------
        alive: bool
            true for alive, false for dead
        """
        self.__alive = alive
        if self.__alive:
            self.__btn.config(bg = 'yellow')
        else: self.__btn.config(bg = 'white')

    def enable_button(self, value: bool):
        """
        a method to enable/disable to cell button

        Parameters
        ----------
        value: bool
            true for enable, false for disable
        """
        new_state = NORMAL if value else DISABLED
        self.__btn.configure(state = new_state)

class TickTacToeFrame(Frame):

    def __init__(self, parent):
        # initialize super
        Frame.__init__(self, parent)
        # create button grid
        btn_frame = Frame(self)
        self.btn_grid = []
        for i in range(0, 3):
            self.btn_grid.append([])
            for j in range(0, 3):
                btn = Button(master = btn_frame, padx = 30, pady = 20, command = lambda row = i, col = j: self.__on_click(row, col))
                btn.grid(row = i, column = j)
                self.btn_grid[i].append(btn)
        btn_frame.grid(row = 0, column = 0)
        # create reset button
        Button(master = self, padx = 15, pady = 1, command = self.__reset_game, text = 'Reset game').grid(row = 1, column = 0)
        # set turn counter to 0
        self.turn_counter = 0

    def __on_click(self, i: int, j: int):
        # draw X / O according to the turn counter
        if self.turn_counter % 2 == 0:
            self.btn_grid[i][j].config(text = 'X')
        else: 
            self.btn_grid[i][j].config(text = 'O')
        # disable the button and increment turn counter
        self.btn_grid[i][j].config(state = DISABLED)
        self.turn_counter += 1
        # check if game is won
        if self.turn_counter >= 5:
            self.__check_win_condition()
    
    def __reset_game(self):
        # enable all buttons
        for i in range(0, 3):
            for j in range(0, 3):
                self.btn_grid[i][j].config(state = NORMAL)
                self.btn_grid[i][j].config(text = '')
        # set turn counter to 0
        self.turn_counter = 0
    
    def __lock_btns(self):
        # lock all buttons
        for i in range(0, 3):
            for j in range(0, 3):
                self.btn_grid[i][j].config(state = DISABLED)

    def __check_win_condition(self):
        # flags for diagnel lines
        diag1 = self.btn_grid[0][0]['text']
        diag2 = self.btn_grid[0][2]['text']
        for i in range(0, 3):
            # check the diagnel lines
            if self.btn_grid[i][i]['text'] != diag1:
                diag1 = -1
            if self.btn_grid[i][2 - i]['text'] != diag2:
                diag2 = -1
            # flags for row and column
            row = self.btn_grid[i][i]['text']
            column = self.btn_grid[i][i]['text']
            # skip blank box
            if row == '':
                continue
            for j in range(0, 3):
                # check the rows and columns
                if self.btn_grid[i][j]['text'] != column:
                    column = -1
                if self.btn_grid[j][i]['text'] != row:
                    row = -1
            # check for win condition
            if row != -1:
                messagebox.showinfo("Game over", row + " won!")
                self.__lock_btns()
            elif column != -1:
                messagebox.showinfo("Game over", column + " won!")
                self.__lock_btns()
        # check for win condition
        if diag1 != -1 and diag1 != '':
            messagebox.showinfo("Game over", diag1 + " won!")
            self.__lock_btns()
        elif diag2 != -1 and diag2 != '':
            messagebox.showinfo("Game over", diag2 + " won!")
            self.__lock_btns()
        elif self.turn_counter == 9:
            messagebox.showinfo("Game over", "tie!")

class ChaosTheoryFrame(Frame):

    def __tick(self):
        anchor = random.sample(self.anchor_list, 1)[0]
        target_x = int((self.starting_point[0] + anchor[0]) / 2)
        target_y = int((self.starting_point[1] + anchor[1]) / 2)
        self.canvas.create_rectangle(target_x, target_y, target_x + 4, target_y + 4, fill = 'white')
        self.starting_point = (target_x, target_y)

    def __set_busy_flag(self, value: bool):
        self.busy_flag = value

    def __run(self, tick_delay: int):
        if self.starting_point == None or len(self.anchor_list) == 0 or self.busy_flag:
            return
        ticks = self.tick_slider.get()
        self.__set_busy_flag(True)
        for i in range(0, ticks):
            if self.halt_flag:
                break
            self.after(tick_delay * i, self.__tick)
        if self.halt_flag:
            self.__set_busy_flag(False)
        else:
            self.after(tick_delay * ticks, lambda: self.__set_busy_flag(False))

    def __reset(self):
        if self.busy_flag:
            return
        self.canvas.delete("all")
        self.starting_point = None
        self.anchor_list = []

    def __draw(self, event):
        # draw anchor point
        if self.draw_mode == 0:
            self.canvas.create_rectangle(event.x, event.y, event.x + 4, event.y + 4, fill = 'orange')
            self.anchor_list.append((event.x, event.y))
        # move and draw the starting point
        elif self.draw_mode == 1:
            if self.starting_point is not None:
                self.canvas.create_rectangle(self.starting_point[0], self.starting_point[1], self.starting_point[0] + 4, self.starting_point[1] + 4, fill = 'black')
            self.canvas.create_rectangle(event.x, event.y, event.x + 4, event.y + 4, fill = 'white')
            self.starting_point = (event.x, event.y)

    def __set_draw_mode(self, draw_mode: int):
        self.draw_mode = draw_mode

    def __init__(self, parent, width: int, height: int):
        # initialize super
        Frame.__init__(self, parent)
        # create the canvas
        self.canvas = Canvas(master = self, bg = 'black', width = width, height = height)
        self.canvas.grid(row = 0, column = 0)
        self.canvas.bind("<Button-1>", self.__draw)
        # Define the button space
        buttonSpace = Frame(self)
        buttonSpace.grid(row = 1, column = 0)
        # create radio buttons
        radioFrame = Frame(buttonSpace)
        radioFrame.grid(row = 0, column = 0, padx = (10, 100))
        # the title
        label = Label(master = radioFrame, text = "Currently drawing").grid(row = 0, column = 0)
        # option 1
        anchorRadio = Radiobutton(master = radioFrame, text="Anchor points", value = 0, command = lambda: self.__set_draw_mode(0))
        anchorRadio.grid(row = 1, column = 0)
        anchorRadio.deselect()
        # option 2
        startRadio = Radiobutton(master = radioFrame, text="Starting point", value = 1, command = lambda: self.__set_draw_mode(1))
        startRadio.grid(row = 2, column = 0)
        startRadio.select()
        # create action buttons
        actionFrame = Frame(buttonSpace)
        actionFrame.grid(row = 0, column = 1, padx = (100, 10))
        # slider for tick amount
        self.tick_slider = Scale(master = actionFrame, from_ = 1, to = 3000, orient = HORIZONTAL, length = width / 3)
        self.tick_slider.grid(row = 0, column = 0)
        # a sub frame for buttons
        ctrlFrame = Frame(actionFrame)
        ctrlFrame.grid(row = 1, column = 0)
        # reset / run buttons
        runBtn = Button(master = ctrlFrame, text = 'run', command = lambda: self.__run(10), padx = 50, pady = 1).grid(row = 0, column = 0)
        resetBtn = Button(master = ctrlFrame, text = 'reset', command = self.__reset, padx = 50, pady = 1).grid(row = 0, column = 1)
        # set deafult values for internal variables
        self.draw_mode = 1
        self.starting_point = None
        self.anchor_list = []
        self.busy_flag = False
        self.halt_flag = False
    