import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

class FieldUI(tk.Tk):
    def __init__(self, size):
        super().__init__()
        self.size = size
        self.title("Board Game")
        self.canvas = tk.Canvas(self, width=160*size, height=160*size)
        self.canvas.pack()
        self.cells = [[None for _ in range(size)] for _ in range(size)]
        self.images = [[[] for _ in range(size)] for _ in range(size)]
        self.create_board()

    def create_board(self):
        for i in range(self.size):
            for j in range(self.size):
                x0, y0 = i * 160, j * 160
                x1, y1 = x0 + 160, y0 + 160
                self.cells[i][j] = self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
                self.canvas.tag_bind(self.cells[i][j], "<Button-1>", lambda event, x=i, y=j: self.on_click(x, y))

    def on_click(self, x, y):
        if len(self.images[x][y]) < 3:
            image_path = filedialog.askopenfilename(title="Select Image", filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*")))
            if image_path:
                self.load_image(image_path, x, y)

    def load_image(self, path, x, y):
        image = Image.open(path)
        image = image.resize((50, 50), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.images[x][y].append(photo)
        offset = len(self.images[x][y]) - 1
        if offset == 0:
            self.canvas.create_image(x*160 + 80, y*160 + 80, image=photo)
        elif offset == 1:
            self.canvas.create_image(x*160 + 40, y*160 + 120, image=photo)
        elif offset == 2:
            self.canvas.create_image(x*160 + 120, y*160 + 120, image=photo)

if __name__ == "__main__":
    size = 5  # Change the size of the board here
    app = FieldUI(size)
    app.mainloop()
