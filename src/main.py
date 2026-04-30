"""The main driver file of this program."""

import pygame as pg
import pygame_gui
import colony
import plotter
import button

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1088

class Game:
    def __init__(self, resolution: tuple, frame_rate: int) -> None:
        pg.init()
        pg.display.set_caption("Conway's Game of Life")
        self.screen = pg.display.set_mode(resolution)
        self.clock = pg.time.Clock()
        self.running = True
        self.frame_rate = frame_rate
        self.colony = colony.Colony(resolution[0], resolution[1])
        self.selected_cell = None
        self.plot = plotter.Plotter()
        self.manager = pygame_gui.UIManager(resolution)

    def draw_colony(self) -> None:
        for row in range(self.colony.rows):
            for column in range(self.colony.columns):
                color = ""
                if self.colony.get_cell(row, column).is_alive:
                    color = "black"
                elif self.colony.get_cell(row, column) == self.selected_cell:
                    color = "grey"
                else:
                    color = "white"

                pg.draw.rect(
                        self.screen,
                        color,
                        pg.Rect(self.colony.get_cell(row, column).calculate_screen_coordinates(),
                                (16, 16))
                        )

    def _draw_button(self, left_corner: tuple, dimensions: tuple, color: str) -> None:
        button_to_draw = pg.Rect(left_corner, dimensions)
        pg.draw.rect(self.screen, color, button_to_draw)


    def main(self) -> None:
        in_gui = True
        in_game = False

        print(pg.display.get_window_size()[0])
        button_width = 100
        button_height = 50
        button_size = (button_width, button_height)
        restart_button_pos = (pg.display.get_window_size()[0]-button_width, 0)
        start_button_gui = pygame_gui.elements.UIButton(relative_rect=pg.Rect((0,0), button_size),
                                                        text='Start',
                                                        manager=self.manager)
        restart_button_gui = pygame_gui.elements.UIButton(relative_rect=pg.Rect(restart_button_pos, button_size),
                                                        text='Restart',
                                                        manager=self.manager)

        while self.running:

            time_delta = self.clock.tick(60)/1000.0

            # Exit the loop if the the player quits.
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button_gui:
                        in_gui = False
                        in_game = True
                    elif event.ui_element == restart_button_gui:
                        self.colony.wipe_colony()
                        in_gui = True
                        in_game = False

                self.manager.process_events(event)

            self.manager.update(time_delta)

            # Entry point to select cells
            if in_gui:

                # Render buttons.
                self.draw_colony()

                # Determine the cell under the cursor.
                mouse_pos = pg.mouse.get_pos()
                mouse_row = int(mouse_pos[0]/16)
                mouse_column = int(mouse_pos[1]/16)
                self.selected_cell = self.colony.get_cell(mouse_column, mouse_row)

                # Determine if left mouse button is clicked.
                mouse_clicked = pg.mouse.get_pressed()
                left_clicked = mouse_clicked[0]

                if left_clicked:
                    self.selected_cell.resurect_cell()


            elif in_game:
                self.draw_colony()

                mouse_pos = pg.mouse.get_pos()
                mouse_clicked = pg.mouse.get_pressed()

                self.plot.update_cell_count_list(self.colony)
                self.colony.bit_map_determine_fate()
                self.colony.kill_and_resurect_cells()

            self.manager.draw_ui(self.screen)
            pg.display.flip()

            self.clock.tick(self.frame_rate)
            
        pg.quit()
        self.plot.save_plot()


game_of_life = Game((SCREEN_WIDTH, SCREEN_HEIGHT), 30)
game_of_life.main()
