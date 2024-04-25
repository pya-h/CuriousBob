import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
# from field.logic import FieldLogic

class FieldGUI(tk.Tk):
    def __init__(self, width: int = 5, height: int = 5):
        super().__init__()
        self.height = height
        self.width = width
        
        self.title("Smart Agent Game")
        self.cell_size = 200
        self.canvas = tk.Canvas(self, width=self.cell_size*size, height=self.cell_size*size)
        self.canvas.pack()
        self.cells = [[None for _ in range(size)] for _ in range(size)]
        self.images = [[[] for _ in range(size)] for _ in range(size)]
        self.create_board()

    def create_board(self):
        for i in range(self.height):
            for j in range(self.width):
                x0, y0 = i * self.cell_size, j * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                self.cells[i][j] = self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
                self.canvas.tag_bind(self.cells[i][j], "<Button-1>")

    def load_image(self, path, x, y):
        image = Image.open(path)
        image = image.resize((50, 50), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.images[x][y].append(photo)
        offset_x = (len(self.images[x][y]) - 1) % 2 * 60
        offset_y = (len(self.images[x][y]) - 1) // 2 * 60
        self.canvas.create_image(x*self.cell_size + 80 + offset_x, y*self.cell_size + 80 + offset_y, image=photo)

    def show(self):
        self.mainloop()


# class Field(FieldLogic):

#     def __init__(self, width: int = 5, height: int = 5) -> None:
#         super().__init__(width, height)
#         self.gui = FieldGUI(self.width)
        
#     def show(self):
#         self.gui.show()
        
        
if __name__ == "__main__":
    size = 5  # Change the size of the board here
    app = FieldGUI()

    app.show()
