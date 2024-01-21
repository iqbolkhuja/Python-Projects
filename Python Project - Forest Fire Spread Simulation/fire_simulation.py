'''
IQBOLKHOJA TEMIRKHOJAEV
CSC170 - Project 3
Forest Fire Simulator
'''

from graphics import *
import random

WIN_Y = 350
WIN_X = 950

class Tree:
    '''
    Represents an individual tree. Starts as an unburned tree, and can be burned through
    repeated calls to object method Tree.burn_more(). Please ensure that the accompanying
    files are in the same directory as this file:
            0_tree.png
            1_little_burn.png
            2_lot_burn.png
            3_charcoal.png
    '''
    tree_imgs = ["0_tree.png", "1_little_burn.png", "2_lot_burn.png", "3_charcoal.png"]

    def __init__(self, Point) -> None:
        #Creates a unburned Tree object centered at anchor_pt.
        self.Point = Point
        self.state = 0
        self.img_name = self.tree_imgs[self.state]
        self.img_obj = Image(Point, self.img_name)


    def burn_more(self, win):
        #Moves the calling Tree object to the next burn state.
        #If the calling Tree object is in the final burn state, it is not modified.

        if self.state == 3:
            return
        self.state += 1
        self.state = self.state
        self.img_obj.undraw()
        self.img_name = self.tree_imgs[self.state]
        self.img_obj = Image(self.Point, self.img_name)
        self.img_obj.draw(win)

    def draw(self, win):
        self.img_obj.draw(win)

    def undraw(self):
        #Removes the Tree object from the graphics window win.
        self.img_obj.undraw()

    def is_on_fire(self):
        #Returns True if the calling Tree object is on fire, False otherwise.
        if self.state > 0 and self.state < 3:
            return True

    def reborn(self, win):
        self.img_obj.undraw()
        self.state = 0
        self.img_name = self.tree_imgs[self.state]
        self.img_obj = Image(self.Point, self.img_name)
        self.img_obj.draw(win)

    def __str__(self) -> str:
        #Returns a string representation of the calling object.
        #This is the string type conversion function, str().
        return f"{self.img}"

    def __repr__(self) -> str:
        #Return a code-like string representation of the calling object.
        #This is the representation function, repr().
        return f"Tree({self.Point})"


class Button(Polygon):
    '''
    Represents a rectangular, clickable button. Has built-in functions which determine if a
    Point object is within the boundary of the Button.
    '''
    def __init__(self, text, height):
        absolute_point = Point(WIN_X * 0.6, WIN_Y * 0.4 + height)
        absolute_point1 = Point(WIN_X * 0.6 + 300, WIN_Y * 0.4 + height + 40)
        rec = Rectangle(absolute_point, absolute_point1)
        rec.setFill("blanched almond")
        centerPoint = rec.getCenter()
        text = Text(centerPoint, text)
        self.text = text
        self.rectangle = rec

    def points_is_inside(self, mouse_position):
        '''
        Returns True if point is within the bounds of the calling Button object, False otherwise.
        '''
        p1 = (self.rectangle).getP1()
        p2 = (self.rectangle).getP2()
        x_range = range(int(p1.getX()), int(p2.getX()))
        y_range = range(int(p1.getY()), int(p2.getY()))
        if mouse_position.getX() in x_range and mouse_position.getY() in y_range:
            return True
        return False

class FireSimulator:
    '''
    Initialized the forest fire simulator class
    along with all values provided
    '''

    def __init__(self, x_grid, y_grid) -> None:
        height_img = 29
        width_img = 29
        forest = []
        bool_forest = []

        for i in range(y_grid):
            temp_row = []
            temp_row2 = []

            for j in range(x_grid):
                point = Point(50 + (j * height_img), (50 + (i * width_img)))
                temp_tree = Tree(point)
                temp_row.append(temp_tree)
                temp_row2.append(False)

            bool_forest.append(temp_row2)
            forest.append(temp_row)

        self.forest = forest
        self.bool_forest = bool_forest
        self.width = x_grid
        self.height = y_grid

    # Will work at the start to draw the forest
    def draw_trees(self, win):
        y_grid = self.height
        x_grid = self.width
        self.win = win
        for i in range(y_grid):
            for j in range(x_grid):
                (self.forest[i][j]).draw(win)


    #Returns a boolean value to check the status of a tree (fire or no-fire)
    def trees_on_fire(self):
        fire = False
        for i in range(self.height):
            for j in range(self.width):
                if self.forest[i][j].is_on_fire():
                    fire = True
        return fire

    # This function is going to update the image of the tree
    def set_on_fire(self, win):
        for i in range(self.height):
            for j in range(self.width):
                if self.bool_forest[i][j]:
                    self.forest[i][j].burn_more(win)

    #This method is goign to check the probabilty
    def check_probabilities(self, probability):
        for i in range(self.height):
            for j in range(self.width):
                if not self.bool_forest[i][j]:
                    self.check_trees_close(i, j, probability)


    def check_trees_close(self, i, j, probability):
        for a in range(-1, 2):
            for b in range(-1, 2):
                if (i + a) in range(0, self.height) and (j + b) in range(0, self.width):
                    if self.bool_forest[i + a][j + b]:
                        self.bool_forest[i][j] = fire_probability(probability)

    #This function is going to remake the forest. Resets the simulation of the project.
    def remake_forest(self, win):
        bool_forest = []
        for i in range(self.height):
            temp_row = []
            for j in range(self.width):
                temp_row.append(False)
                self.forest[i][j].reborn(win)
            bool_forest.append(temp_row)
        self.bool_forest = bool_forest

#This method checks the mouse status at the moment to handle actions
def check_mouse(mouse_position):
    absolute_width = int(WIN_X * 0.6)
    absolute_height = int(WIN_Y * 0.4)
    if mouse_position.getX() in range(absolute_width, absolute_width + 300):

        if mouse_position.getY() in range(absolute_height, absolute_height + 40):
            return 1
        elif mouse_position.getY() in range(absolute_height + 40, absolute_height + 90):
            return 2
        elif mouse_position.getY() in range(absolute_height + 90, absolute_height + 140):
            return 3
    return False

#Shows the final label of how many steps does it took to subside the fire
def final_text(steps, win):
    first_point = Point(WIN_X * 0.2, WIN_Y * 0.4)
    second_point = Point(WIN_X * 0.8, WIN_Y * 0.6)
    rec = Rectangle(first_point, second_point)
    rec.setFill("Red")
    centerPoint = rec.getCenter()
    text = Text(centerPoint,
                f"Fire subsided in {steps} steps. Click anywhere to continue")
    label = [rec, text]
    label[0].draw(win)
    label[1].draw(win)
    win.getMouse()
    label[0].undraw()
    label[1].undraw()

#This code is going to popup the invalid input message if some error occurs
def error_text(win):
    first_point = Point(WIN_X * 0.2, WIN_Y * 0.4)
    second_point = Point(WIN_X * 0.8, WIN_Y * 0.6)
    rec = Rectangle(first_point, second_point)
    rec.setFill("Yellow")
    centerPoint = rec.getCenter()
    text = Text(centerPoint,
                f"Invalid input, try with a new one (click anywhere to continue)")
    label = [rec, text]
    label[0].draw(win)
    label[1].draw(win)
    win.getMouse()
    label[0].undraw()
    label[1].undraw()

def fire_probability(probability):
    return random.random() < probability

#Show what tree is one fire - returns either true or false
def which_tree(mouse_position, forest):
    width = forest.width
    height = forest.height
    x_pos = mouse_position.getX()
    y_pos = mouse_position.getY()
    if (x_pos in range(50, 29 * width + 29)
            and y_pos in range(50, 29 * height + 29)):
        tree_position_y = int(y_pos / 29) - 1
        tree_position_x = int(x_pos / 29) - 1
        tree_positions = [tree_position_y, tree_position_x]
        return tree_positions
    return False


def main():
    # Providing the valie of initial trees
    y_grid = 10
    x_grid = 15
    win = GraphWin('Graphics', WIN_X, WIN_Y)

    # Drawing the probability text
    title = Text(Point(WIN_X * 0.75, WIN_Y * 0.22), "Burn Probability:")
    title.setSize(15)
    title.setStyle("italic")
    title.draw(win)

    # Drawing input field for the probability value
    inputBox = Entry(Point(WIN_X * 0.75, WIN_Y * 0.32), 20)
    inputBox.setSize(20)
    inputBox.draw(win)

    # Drawing the buttons
    button1 = Button("Run (Random Start)", 0)
    button1.rectangle.draw(win)
    button1.text.draw(win)

    button2 = Button("Run (Click to start)", 50)
    button2.rectangle.draw(win)
    button2.text.draw(win)

    button3 = Button("Reset Simulation", 100)
    button3.rectangle.draw(win)
    button3.text.draw(win)

    button4 = Button("Close button", 150)
    button4.rectangle.draw(win)
    button4.text.draw(win)

    # Creating the forest with tree with provided dimensions
    forest = FireSimulator(x_grid, y_grid)
    forest.draw_trees(win)
    mouse_position = win.getMouse()

    # Making sure the first tree buttions were clicked to handle the action

    while button4.points_is_inside(mouse_position) == False:
        # This is to get the number

        wtd = check_mouse(mouse_position)
        while True:
            try:
                inputStr = float(inputBox.getText())
                break
            except ValueError:
                inputBox.setText("0")
                error_text(win)
                wtd = False

        if wtd == 1:
            # This method will print the forest in every iteration
            random1 = random.randint(0, 9)
            random2 = random.randint(0, 14)

            (forest.forest[random1][random2]).burn_more(win)
            forest.bool_forest[random1][random2] = True

            steps = 0

            while forest.trees_on_fire():
                forest.check_probabilities(inputStr)
                forest.set_on_fire(win)
                steps += 1

            forest.set_on_fire(win)
            final_text(steps, win)

        elif wtd == 2:
            # This option will start the fire at clicked position
            while True:
                mouse_position = win.getMouse()
                tree_pos = which_tree(mouse_position, forest)
                if tree_pos != False:
                    break

            (forest.forest[tree_pos[0]][tree_pos[1]]).burn_more(win)
            forest.bool_forest[tree_pos[0]][tree_pos[1]] = True
            steps = 0

            while forest.trees_on_fire():
                forest.check_probabilities(inputStr)
                forest.set_on_fire(win)
                steps += 1

            forest.set_on_fire(win)
            final_text(steps, win)

        elif wtd == 3:
            # This option will restart the simulation
            forest.remake_forest(win)

        mouse_position = win.getMouse()


if __name__ == "__main__":
    main()
