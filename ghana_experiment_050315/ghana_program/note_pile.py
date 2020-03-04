# Test notes in choice

import Tkinter as tk
import os

class NotePile:
    def __init__(self, BASE, master, grid_row, grid_col):
        self.main = tk.Canvas(master,
                              bg = "gray",
                              height = 100,
                              width = 219,
                              name = "note_stack")
        self.main.grid(row = grid_row, column = grid_col, sticky = "n")

        rupee = tk.PhotoImage(file = os.path.join(BASE, "images", "cedi.gif"))

        labels = [tk.Label(master,
                           image = rupee)
                  for i in range(0, 11)]

        for label in labels:
            label.image = rupee

        self.notes = [self.main.create_window(0, 0,
                                              state = "hidden",
                                              anchor = "nw",
                                              window = lab,
                                              tag = ("note_" +
                                                     str(i)))
                      for i, lab in enumerate(labels, 1)]


        x = range(0, 55, 5)
        y = range(0, 22, 2)

        coords = zip(x, y)

        self.positions = dict(enumerate(coords, 1))
        self.current_nr = tk.IntVar()
        self.current_nr.set(1)

    def get_positions(self, nr):
        n0 = self.current_nr.get()


        if nr >= n0 and nr <= 11:
            nstart = max(n0, 1)
            nrange = range(nstart, nr + 1)
            tags = ["note_" + str(i) for i in nrange]
            positions = [self.positions.get(i)
                         for i in nrange]
            tag_pos = zip(tags, positions)
            self.show(tag_pos)

            self.current_nr.set(nr)

        elif nr < n0:
            nrange = range(nr, n0 + 1)[1:]
            tags = ["note_" + str(i) for i in nrange]
            self.hide(tags)
            self.current_nr.set(nr)

        elif nr > 11:
            pass



    def show(self, labels_positions):
        [self.main.itemconfig(tag, state = "normal")
         for tag, pos in labels_positions]

        [self.main.coords(tag, *position)
         for tag, position in labels_positions]

    def hide(self, labels):
       [self.main.itemconfig(tag, state = "hidden")
        for tag in labels]

# root = tk.Tk()
# simon = NotePile(root)
