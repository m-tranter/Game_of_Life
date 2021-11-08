# gol.py - game of life
from random import randrange
from tkinter import *
import time

def main():
    columns, delay, h = 30, 0, 10 
    gol = Gol(columns, delay, h)
    gol.run() 

class Gol():
    def __init__(self, size, delay, h):
        """Constructor. Set up some initial variables."""
        self.size, self.delay, self.h = size, delay, h
        self.generating = self.generations = 0 
        self.alive = []
        self.message = "Ready."
  
    def run(self):
        """Set up the GUI and start the loop."""
        self.root = Tk()
        self.gol = Frame(self.root)
        self.gol.grid()
        self.root.title("Game of Life")
        self.cells = [[] for x in range(self.size)]
        # use an image for the Cell, so we can specify size in pixels
        empty = PhotoImage(width=1, height=1, master=self.root)
        # create the cells
        for row, col in [(row, col) for row in range(self.size) for col in range(self.size)]:
            self.cells[row].append(Cell(self.gol, image=empty, height=self.h, width=self.h, relief="flat", bg="grey", activebackground="green"))
            self.cells[row][col].grid(row=row,column=col)
            self.cells[row][col].initialise(self, row, col)
        
        # buttons
        self.start = Button(self.gol, text = "Start")
        self.start["command"] = lambda: self.generate()
        self.start.grid(row=0, column = self.size+1,rowspan=3)

        self.stop = Button(self.gol, text = "Stop")
        self.stop["command"] = lambda: self.stopped()
        self.stop.grid(row=4, column = self.size+1,rowspan=3)

        self.reset = Button(self.gol, text = "Reset")
        self.reset["command"] = lambda: self.clear()
        self.reset.grid(row=8, column = self.size+1, rowspan=3)

        self.random = Button(self.gol, text = "Random")
        self.random["command"] = lambda: self.randomise()
        self.random.grid(row=12, column = self.size+1, rowspan=3)

        # labels
        self.gens = Label(self.gol,text = "Generations:\n0", fg="blue")
        self.gens.grid(row=14, column = self.size+1, rowspan=5, padx=3)

        self.alert = Label(self.gol, text=self.message, fg="blue")
        self.alert.grid(row=17, column = self.size+1, rowspan=5,padx=3)

        self.active = Label(self.gol, text= "Population:\n0", fg="blue")
        self.active.grid(row=20, column = self.size+1, rowspan=5,padx=3)
        
        self.allCells = self.flatten() 
        for cell in self.allCells:
            cell.addNeighbours(self)
        self.relevant = {}
        self.root.mainloop()
        
    def flatten(self):
        """Returns a one-dimensional array of all of the cells."""
        return list(cell for row in self.cells for cell in row)

    def randomise(self):
        """Randomly activate some cells"""
        self.clear()
        for cell in self.allCells:
            if not randrange(5):
                cell.toggle(self)
    
    def clear(self):
        """Clear all cells."""
        self.generating = self.generations = 0
        self.message="Cleared."

        #This is weird. This works.
        # while self.alive:
            # for c in self.alive:
                # c.toggle(self)
        # But this doesn't and I don't know why
        for c in self.alive:
            c.toggle(self)
        self.refresh()


    def refresh(self):
        """Update labels."""
        self.gens.config(text = "Generations:\n" + str(self.generations))
        self.alert.config(text = self.message)
        
    def stopped(self):
        """The command bound to the stop button."""
        self.generating = False
        self.message = "Paused."
        
    def buttonsOn(self):
        """Make the buttons clickable."""
        for cell in self.allCells:
            cell.config(state="normal")
            
    def buttonsOff(self):
        """Stop buttons from being clickable."""
        for cell in self.allCells:
            cell.config(state="disabled")
        
    def generate(self):
        """Start the simulation."""
        self.generating = True
        self.message = "Running."
        self.buttonsOff()
        while self.generating:
            self.getData()
            self.nextGen()
            self.gol.update()
            self.refresh()
            self.gol.after(self.delay)
        self.buttonsOn()
        
    def getData(self):
        """Collect information about relevant cells."""
        self.relevant = set(self.alive) 
        for cell in self.alive:
            self.relevant = self.relevant.union(cell.neighbours)
        for cell in self.relevant: 
            cell.nCount = 0
            for n in cell.neighbours:
                cell.nCount += self.cells[n.row][n.col].status
            if cell.status and cell.nCount == 2:
                cell.next = 1
            elif cell.nCount == 3:
                cell.next = 1
            else:
                cell.next = 0  
          
    def nextGen(self):
        """Make changes to display next generation."""
        self.changed = False
        for cell in self.relevant:
            if cell.status != cell.next:
                cell.toggle(self)
                self.changed = True
        if not self.changed:
            if not self.alive:
                self.message = "Extinction"
            else:
                self.message = "Stasis"
            self.generating = False
        else:
             self.generations +=1

class Cell(Button):
    """Cell class inherits from Button class."""
    def initialise(self, parent, row, col):
        """Associate the cell's command with toggle()."""
        self["command"] = lambda: self.toggle(parent)
        self.nCount = self.next = self.status = 0
        self.row, self.col = row, col

    def addNeighbours(self, parent):
        rowAbove = (self.row - 1) % parent.size
        rowBelow = (self.row + 1) % parent.size
        colLeft = (self.col - 1) % parent.size
        colRight = (self.col + 1) % parent.size
        self.neighbours = {parent.cells[rowAbove][colLeft],
                parent.cells[rowAbove][self.col], 
                parent.cells[rowAbove][colRight],
                parent.cells[self.row][colLeft], 
                parent.cells[self.row][colRight], 
                parent.cells[rowBelow][colLeft], 
                parent.cells[rowBelow][self.col], 
                parent.cells[rowBelow][colRight]}

    def toggle(self, parent):
        """Toggle cells, update count of living cells, update population label."""
        if not self.status:
            self.status = 1
            parent.alive.append(self)
            self.configure(bg="green")
        else:
            self.status = 0
            parent.alive.remove(self)
            self.configure(bg="grey")
        parent.active.config(text="Population:\n" + str(len(parent.alive)))

if __name__ == "__main__":
    main()
