import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from field.logic import FieldLogic
from agent import Agent
from typing import List
from entity import Entity
from resources.avatar import Avatar
from threading import Timer


class FieldGUI(tk.Tk):
    def __init__(self, width: int = 5, height: int = 5):
        super().__init__()
        self.height = height
        self.width = width
        
        self.title("Smart Agent Game")
        self.cell_size = 125
        self.canvas = tk.Canvas(self, width=self.cell_size*self.width, height=self.cell_size*self.height)
        self.canvas.pack()
        self.cells = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.images = [[[] for _ in range(self.width)] for _ in range(self.height)]
        self.create_board()
    
    def create_board(self):
        for i in range(self.height):
            for j in range(self.width):
                x0, y0 = i * self.cell_size, j * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                self.cells[i][j] = self.canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black")
                self.canvas.tag_bind(self.cells[i][j], "<Button-1>")

    def load_entity(self, entity: Entity):
        avatar = entity.avatar
        x, y = entity.position.convert_to_indices()
        image = Image.open(avatar.path)
        image = image.resize((avatar.size, avatar.size), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.images[x][y].append(photo)
        distance_between_images = self.cell_size / 3
        offset_x = (len(self.images[x][y]) - 1) % 2 * distance_between_images
        offset_y = (len(self.images[x][y]) - 1) // 2 * distance_between_images
        offset_delta = self.cell_size / 3
        return self.canvas.create_image(x*self.cell_size + offset_delta + offset_x, y*self.cell_size + offset_delta + offset_y, image=photo)

    def update_ui(self, cells_data: List[List[List[Entity]]],  agent: Agent):
        '''Show the graphical user interface for illustration of the simulation; TODO: agent field is temprory'''
        for row in cells_data:
            for cell in row:
                if not cell:
                    continue
                for entity in cell:
                    if not entity:
                        continue
                    entity.avatar.canvas_id = self.load_entity(entity)
        agent.avatar.canvas_id = self.load_entity(agent)


class Field(FieldLogic):

    def __init__(self, width: int = 5, height: int = 5) -> None:
        super().__init__(width, height)
        self.gui = FieldGUI(self.width, self.height)

    def clear_field(self):
        for row in self.cells:
            for cell in row:
                if not cell:
                    continue
                for entity in cell:
                    if not entity or not entity.avatar.canvas_id:
                        continue
                    entity.clear_canvas(self.gui.canvas)

    def update_ui(self, agent: Agent):
        self.gui.update_ui(self.cells, agent)
        
    def go_for_next_move(self, game):
        self.clear_field()
        self.update_ui(game.agent)
        game.do_next_move()

    def run(self, game):
        # Timer(1, self.go_for_next_move, args=(game,)).run()
        self.check_for_events(game)
        self.gui.mainloop()
        return self
    
    def check_for_events(self, game):
        self.gui.update()  # Process events
        self.go_for_next_move(game)
        self.gui.after(1000, self.check_for_events, game)  # Check again after 100ms

if __name__ == "__main__":
    size = 5  # Change the size of the board here
    app = FieldGUI()
    app.run().show()
