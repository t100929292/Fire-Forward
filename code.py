import board
import random
import displayio
import keypad
import terminalio
import digitalio
from adafruit_debouncer import Debouncer
from adafruit_display_text.label import Label
import adafruit_displayio_ssd1306
from adafruit_display_shapes.circle import Circle
import time
#from adafruit_seesaw import seesaw, rotaryio, digitalio


class environment:
    def __init__(self):
        global display_layer
        display_layer = displayio.Group()
        global canvas
        canvas= displayio.Group()
        global sprite_layer
        sprite_layer = displayio.Group()
        global display_size
        display_size = displayio.Bitmap(128, 64, 1)
        global color_palette
        color_palette = displayio.Palette(1)
        self.fuel_display = displayio.Group()
        self.fuel_display_size = displayio.Bitmap(128,9,1)
        self.display_layer = display_layer
        self.canvas = canvas
        self.sprite_layer = sprite_layer
        self.display_size = display_size
        self.color_palette = color_palette
    def bckgnd(self):
        white = 0xFFFFFF
        self.color_palette[0] = white  # White
        bg_sprite = displayio.TileGrid(self.display_size, pixel_shader=self.color_palette, x=0, y=0)
        fuel_pallete = displayio.Palette(1)
        fuel_pallete[0] = 0x000000
        fuel_display_grid = displayio.TileGrid(self.fuel_display_size, pixel_shader=fuel_pallete, x=0, y=55)
        
        fuel_text = displayio.Group(scale=1,x=70,y=60)
        fuel_label = Label(terminalio.FONT, text="FUEL:", color=0xFFFFFF)
        
        self.canvas.append(bg_sprite)
        fuel_text.append(fuel_label)
        self.fuel_display.append(fuel_text)
        self.canvas.append(fuel_display_grid)
        self.canvas.append(self.fuel_display)
        self.display_layer.append(self.canvas)
    def win(self):
        self.win_display = displayio.Group()
        self.win_display_size = displayio.Bitmap(128, 64, 1)
        win_pallete = displayio.Palette(1)
        win_pallete[0] = 0x000000
        self.win_show = True
        win_sprite = displayio.TileGrid(self.win_display_size, pixel_shader=win_pallete, x=0, y=0)
        self.win_display.append(win_sprite)
        win_text = displayio.Group(scale=1,x=40,y=30)
        win_label = Label(terminalio.FONT, text="YOU WIN!!", color=0xFFFFFF)
        win_text.append(win_label)
        self.win_display.append(win_text)
        self.canvas.append(self.win_display)
    def lose(self):
        self.lose_display = displayio.Group()
        self.lose_display_size = displayio.Bitmap(128, 64, 1)
        lose_pallete = displayio.Palette(1)
        lose_pallete[0] = 0x000000
        self.lose_show = True
        lose_sprite = displayio.TileGrid(self.lose_display_size, pixel_shader=lose_pallete, x=0, y=0)
        self.lose_display.append(lose_sprite)
        lose_text = displayio.Group(scale=1,x=40,y=30)
        lose_label = Label(terminalio.FONT, text="YOU LOSE D:", color=0xFFFFFF)
        lose_text.append(lose_label)
        self.lose_display.append(lose_text)
        self.canvas.append(self.lose_display)
        
        
class fuel:
    
    def __init__(self,fuel_number):
        self.fuel_number = fuel_number
        self.f1 = Circle(105, 60, 2, fill=0xFFFFFF, outline=0xFFFFFF)
        self.f2 = Circle(115, 60, 2, fill=0xFFFFFF, outline=0xFFFFFF)
        self.f3 = Circle(125, 60, 2, fill=0xFFFFFF, outline=0xFFFFFF)
    def fuel_gauge(self,Environment, fuel_no):
            
        if fuel_no == 1:
            Environment.fuel_display.append(self.f1)
        elif fuel_no == 2:

            Environment.fuel_display.append(self.f1)
            Environment.fuel_display.append(self.f2)
        elif fuel_no == 3:
            
            Environment.fuel_display.append(self.f1)
            Environment.fuel_display.append(self.f2)
            Environment.fuel_display.append(self.f3)
        elif fuel_no == 0:
            pass
        else:
            pass
    def reset_fuel(self,Environment):
        if self.fuel_number<0:
            self.fuel_number = 0
        elif self.fuel_number>3:
            self.fuel_number = 3
            
        if self.fuel_number == 3:
            Environment.fuel_display.remove(self.f1)
            Environment.fuel_display.remove(self.f2)
            Environment.fuel_display.remove(self.f3)
        elif self.fuel_number == 2:
            Environment.fuel_display.remove(self.f1)
            Environment.fuel_display.remove(self.f2)
        elif self.fuel_number == 1:
            Environment.fuel_display.remove(self.f1)
        else:
            pass
class Menu:
    def __init__(self):
        menu_display_layer = displayio.Group()
        self.menu_display_layer = menu_display_layer
        self.show = False
        menu_palette = displayio.Palette(1)
        menu_palette[0] = 0x000000  # Black
        menu_background_size = displayio.Bitmap(128, 30, 1)#size of the menu layer
        menu_background = displayio.TileGrid(menu_background_size, pixel_shader=menu_palette, x=0, y=12)#menu position
        menu_display_layer.append(menu_background)
        left_text = Label(terminalio.FONT, text="Forward", color=0xFFFFFF)#text 1 for the menu layer
        left_text_layer = displayio.Group(scale=1,x=5,y=30)#position of text 1 for menu layer
        left_text_layer.append(left_text)
        middle_text = Label(terminalio.FONT, text="Fire", color=0xFFFFFF)#text 2 of the menu layer
        middle_text_layer = displayio.Group(scale=1,x=55,y=30)#position of text 2 for memu layer
        middle_text_layer.append(middle_text)
        right_text = Label(terminalio.FONT, text="Return", color=0xFFFFFF)#text 3 of the menu layer
        right_text_layer = displayio.Group(scale=1,x=87,y=30)#position of the menu layer
        right_text_layer.append(right_text)
        self.menu_display_layer.append(left_text_layer)
        self.menu_display_layer.append(middle_text_layer)
        self.menu_display_layer.append(right_text_layer)
    def Forward(self,Environment, Player):
        Environment.display_layer.remove(self.menu_display_layer)
        self.show = False
        Environment.sprite_layer.remove(Player.inner_sprite)
        Player.inner_sprite = displayio.TileGrid(Player.inner_bitmap, pixel_shader=Player.inner_palette, x=Player.x, y=Player.y-8)
        Environment.sprite_layer.append(Player.inner_sprite)
class selector:
    def __init__(self,size_x,size_y,init_x,init_y):
        self.size_x = size_x
        self.size_y = size_y
        self.init_x = init_x
        self.init_y = init_y
        self.selector_layer_x = 0
        self.selector_layer = displayio.Group()
        self.selector_1 = 0
        self.selector_2 = 0
        self.selector_3 = 0
        self.selector_4 = 0
        self.selector_5 = 0
        self.selector_6 = 0
        self.selector_pallet = displayio.Palette(1)
        self.selector_pallet[0] = 0xFFFFFF  # White
    def init_first(self):
        
        selector_1_size = displayio.Bitmap(self.size_x, self.size_y, 1)#(9,2,1)
        self.selector_1 = displayio.TileGrid(selector_1_size, pixel_shader=self.selector_pallet, x=self.init_x+self.selector_layer_x, y=self.init_y)#(20,18)
        self.selector_layer.append(self.selector_1)
        selector_2_size = displayio.Bitmap(self.size_x, self.size_y-1, 1)
        self.selector_2 = displayio.TileGrid(selector_2_size, pixel_shader=self.selector_pallet, x=self.init_x+self.selector_layer_x, y=self.init_y)
        self.selector_layer.append(self.selector_2)
        selector_3_size = displayio.Bitmap(self.size_x-2, self.size_y-1, 1)
        self.selector_3 = displayio.TileGrid(selector_3_size, pixel_shader=self.selector_pallet, x=self.init_x+1+self.selector_layer_x, y=self.init_y+1)
        self.selector_layer.append(self.selector_3)
        selector_4_size = displayio.Bitmap(self.size_x-4, self.size_y-1, 1)
        self.selector_4 = displayio.TileGrid(selector_4_size, pixel_shader=self.selector_pallet, x=self.init_x+2+self.selector_layer_x, y=self.init_y+2)
        self.selector_layer.append(self.selector_4)
        selector_5_size = displayio.Bitmap(self.size_x-6, self.size_y-1, 1)
        self.selector_5 = displayio.TileGrid(selector_5_size, pixel_shader=self.selector_pallet, x=self.init_x+3+self.selector_layer_x, y=self.init_y+3)
        self.selector_layer.append(self.selector_5)
        selector_6_size = displayio.Bitmap(self.size_x-8, self.size_y-1, 1)
        self.selector_6 = displayio.TileGrid(selector_6_size, pixel_shader=self.selector_pallet, x=self.init_x+4+self.selector_layer_x, y=self.init_y+4)
        self.selector_layer.append(self.selector_6)
        #Arrow selector sprite ends here
        menu.menu_display_layer.append(self.selector_layer)

    def move(self,):
        selector_1_size = displayio.Bitmap(self.size_x, self.size_y, 1)#(9,2,1)
        self.selector_layer.remove(self.selector_1)
        self.selector_1 = displayio.TileGrid(selector_1_size, pixel_shader=self.selector_pallet, x=self.init_x+self.selector_layer_x, y=self.init_y)#(20,18)
        self.selector_layer.append(self.selector_1)
        selector_2_size = displayio.Bitmap(self.size_x, self.size_y-1, 1)
        self.selector_layer.remove(self.selector_2)
        self.selector_2 = displayio.TileGrid(selector_2_size, pixel_shader=self.selector_pallet, x=self.init_x+self.selector_layer_x, y=self.init_y)
        self.selector_layer.append(self.selector_2)
        selector_3_size = displayio.Bitmap(self.size_x-2, self.size_y-1, 1)
        self.selector_layer.remove(self.selector_3)
        self.selector_3 = displayio.TileGrid(selector_3_size, pixel_shader=self.selector_pallet, x=self.init_x+1+self.selector_layer_x, y=self.init_y+1)
        self.selector_layer.append(self.selector_3)
        selector_4_size = displayio.Bitmap(self.size_x-4, self.size_y-1, 1)
        self.selector_layer.remove(self.selector_4)
        self.selector_4 = displayio.TileGrid(selector_4_size, pixel_shader=self.selector_pallet, x=self.init_x+2+self.selector_layer_x, y=self.init_y+2)
        self.selector_layer.append(self.selector_4)
        selector_5_size = displayio.Bitmap(self.size_x-6, self.size_y-1, 1)
        self.selector_layer.remove(self.selector_5)
        self.selector_5 = displayio.TileGrid(selector_5_size, pixel_shader=self.selector_pallet, x=self.init_x+3+self.selector_layer_x, y=self.init_y+3)
        self.selector_layer.append(self.selector_5)
        selector_6_size = displayio.Bitmap(self.size_x-8, self.size_y-1, 1)
        self.selector_layer.remove(self.selector_6)
        self.selector_6 = displayio.TileGrid(selector_6_size, pixel_shader=self.selector_pallet, x=self.init_x+4+self.selector_layer_x, y=self.init_y+4)
        self.selector_layer.append(self.selector_6)
        #Arrow selector sprite ends here

class player:
    def __init__(self, x, y,Environment):
        self.x = x
        self.y = y
        self.curr_pos = 0
        self.inner_bitmap = displayio.Bitmap(8, 7, 1)
        self.inner_palette = displayio.Palette(1)
        self.inner_palette[0] = 0x000000  # Black
        self.inner_sprite = displayio.TileGrid(self.inner_bitmap, pixel_shader=self.inner_palette, x=self.x, y=self.y)
        Environment.sprite_layer.append(self.inner_sprite)
        Environment.display_layer.append(Environment.sprite_layer)
        Environment.display_layer.append(text_layer)
    def move_right(self,my_label,bullet,enemy_queue):
        mvrt = True
        
        for en in enemy_queue:
            #print("player x is: "  + str(self.inner_sprite.x + 8) + " and enemy x is: " + str(en.x))
            #print("player y is: "  + str(self.inner_sprite.y) + " and enemy x is: " + str(en.y-1))
            if self.inner_sprite.x + 8 == en.x and self.inner_sprite.y == (en.y - 1):
                mvrt = False
                
        if self.x<120 and mvrt == True:
            self.x = self.x+8
            if self.x<self.curr_pos+32:
                self.inner_sprite.x = self.inner_sprite.x + 8
                bullet.x = bullet.x + 8
                #my_label.text = str(self.x)
                time.sleep(.1)
            else:
                self.x = self.x-8
                
    def move_left(self,my_label,bullet):
        mvlft = True
        for en in enemy_queue:
            #print("player x is: "  + str(self.inner_sprite.x + 8) + " and enemy x is: " + str(en.x))
            #print("player y is: "  + str(self.inner_sprite.y) + " and enemy x is: " + str(en.y-1))
            if self.inner_sprite.x - 8 == en.x and self.inner_sprite.y == (en.y - 1):
                mvlft = False
        if self.x>0 and mvlft == True:
            self.x = self.x-8
            if self.x>self.curr_pos-32:
                self.inner_sprite.x = self.inner_sprite.x - 8
                bullet.x = bullet.x - 8
                #my_label.text = str(self.x)
                time.sleep(.1)
            else:
                self.x = self.x+8
    def reset(self,x,y,Environment):
        self.x = x
        self.y = y
        self.inner_sprite.x = self.x
        Environment.sprite_layer.remove(self.inner_sprite)
        self.inner_sprite = displayio.TileGrid(self.inner_bitmap, pixel_shader=self.inner_palette, x=self.x, y=self.y)
        Environment.sprite_layer.append(self.inner_sprite)
        
class enemy:
    def __init__(self, x,y, Environment):
        self.x = x
        self.y = y
        self.circle = Circle(self.x+4, self.y+4, 4, fill=0xFF0000, outline=0xFF0000)
        Environment.sprite_layer.append(self.circle)
    
def remove_enemy(enemy, Environment):
    Environment.sprite_layer.remove(enemy.circle)

def generate_enemy_row(pos_queue,enemy_queue,Environment):
    x_val = 0
    for i in range(1,10):
        while x_val == 0:
            x_val = get_new_position()
            if x_val not in pos_queue:
                pos_queue.append(x_val)
                en = enemy(x_val,0,Environment)
                enemy_queue.append(en)
            else:
                x_val = 0
        x_val = 0
def get_new_position():
    x = random.randint(1,15)
    x = x*8
    return x

def move_enemy_forward(Environment,enemy,enemy_queue):
    movement_allowed = False
    if enemy.y==48:
        movement_allowed = True
        Environment.sprite_layer.remove(enemy.circle)
        enemy_queue.remove(enemy)
    else:
        en_test_x = enemy.x
        en_test_y = enemy.y
        #print("enemy test: ")
        #print(en_test_y)
        while movement_allowed == False:
            en_test_y = enemy.y
            if enemy.x == 0:#if the enemy is all the way to the left
                r = random.randint(1,2)#choose either 1 or 2
                r = r
                
                if r == 1:
                    en_test_x = en_test_x+8
                    en_test_y = en_test_y+8

                    
                elif r == 2:
                    en_test_x = en_test_x
                    en_test_y = en_test_y+8

            elif enemy.x == 120:#if the enemy is all the way to the right
                r = random.randint(1,2)
                r = r
                
                if r == 1:
                    en_test_x = en_test_x-8
                    en_test_y = en_test_y+8
  
                    
                elif r == 2:
                    en_test_x = en_test_x
                    en_test_y = en_test_y+8
  
            else:# if the enemy is in any of the middle spaces
                
                r = random.randint(1,3)
                r = r
                
                if r == 1:
                    en_test_x = en_test_x-8
                    en_test_y = en_test_y+8
                    
                elif r == 2:
                    en_test_x = en_test_x
                    en_test_y = en_test_y+8
                    
                elif r == 3:
                    en_test_x = en_test_x+8
                    en_test_y = en_test_y+8
                  
            for en in enemy_queue:#check each enemy in the enemy queue
                if en.x == en_test_x and en.y == en_test_y:#if the 
                    #print("enemy test 1: ")
                    #print(en_test_y) 
                    movement_allowed = False
                    break
                else:
                    #print("enemy test 2: ")
                    #print(en_test_y) 
                    movement_allowed = True
        #print("enemy test end: ")
        #print(en_test_y)            
        enemy.x = en_test_x
        enemy.y = en_test_y
        
        Environment.sprite_layer.remove(enemy.circle)
        enemy.circle = Circle(enemy.x+4, enemy.y+4, 4, fill=0xFF0000, outline=0xFF0000)
        Environment.sprite_layer.append(enemy.circle)
class popup:
    def __init__(self, written_text):
        popup_display_layer = displayio.Group()
        self.popup_display_layer = popup_display_layer
        self.show = False
        popup_palette = displayio.Palette(1)
        popup_palette[0] = 0x000000  # Black
        popup_background_size = displayio.Bitmap(128, 30, 1)#size of the menu layer
        popup_background = displayio.TileGrid(popup_background_size, pixel_shader=popup_palette, x=0, y=12)#menu position
        popup_display_layer.append(popup_background)
        popup_text = Label(terminalio.FONT, text=written_text, color=0xFFFFFF)#text 1 for the menu layer
        popup_text_layer = displayio.Group(scale=1,x=5,y=30)#position of text 1 for menu layer
        popup_text_layer.append(popup_text)
        self.popup_display_layer.append(popup_text_layer)
        
        
    
    
displayio.release_displays()
i2c = board.I2C()

display_bus = displayio.I2CDisplay(i2c, device_address=0x3d)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)


#button declarations
left = digitalio.DigitalInOut(board.D12)
left.direction = digitalio.Direction.INPUT
left.pull = digitalio.Pull.UP
left_button = Debouncer(left, interval=0.001)
right = digitalio.DigitalInOut(board.D11)
right.direction = digitalio.Direction.INPUT
right.pull = digitalio.Pull.UP
right_button = Debouncer(right, interval=0.001)
action = digitalio.DigitalInOut(board.D9)
action.direction = digitalio.Direction.INPUT
action.pull = digitalio.Pull.UP
action_button = Debouncer(action)


Environment = environment()
Environment.bckgnd()
display.root_group = Environment.display_layer #display to screen
board_layer_show = False

#make menu layer starts here
menu = Menu()
#make menu selector

selector = selector(9,2,20,18)
selector.init_first()
selector_val = 0

text_layer = displayio.Group(scale=1,x=4,y=5)
my_label = Label(terminalio.FONT, text="", color=0x000000)
#text_layer.append(my_label)

# Draw a smaller inner rectangle
#this is the main character

Player = player(56,47,Environment)

#enemy sprite starts
# enemy_pos = 48
# enemy_len = 8
# enemy_alive = True
# circle = Circle(enemy_pos+4, enemy_len+4, 4, fill=0xFF0000, outline=0xFF0000)
# Environment.sprite_layer.append(circle)

#bullet layer starts here
bullet_len = Player.y
bullet_pallet = displayio.Palette(1)
bullet_pallet[0] = 0x000000  # Black
bullet_layer = displayio.Group()
bullet_size = displayio.Bitmap(5, 5, 1)

bullet = displayio.TileGrid(bullet_size, pixel_shader=bullet_pallet, x=Player.x+2, y=bullet_len)
bullet_layer.append(bullet)
Environment.display_layer.append(bullet_layer)
#bullet layer ends here

display.root_group = Environment.display_layer
board_layer_show = True

print("starting")
# seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
# button = digitalio.DigitalIO(seesaw, 24)
# button_held = False#set the button prssed vairable to false

enemy_queue = []
pos_queue = []
generate_enemy_row(pos_queue,enemy_queue,Environment)
Fuel = fuel(2)
Fuel.fuel_gauge(Environment,Fuel.fuel_number)
Player_turn = True
Enemy_turn = False
Fired = False
Forward = False
Popup = popup("No fuel. Try to fire")
game_lose = False
game_win = False

##############################################
############ CODE STARTS HERE ################
##############################################
while True:
    Player.curr_pos = Player.x
    while Player_turn == True:
        left_button.update()
        right_button.update()
        action_button.update()
        en_pos = True
        en_y_queue = []
        #for en in enemy_queue:
        #    en_y_queue.append(en.y)
        #print(en_y_queue)
        #print(Player.y)
        for en in enemy_queue:#check to see if there are any enemies in front of the player
            if Player.y < en.y and Fuel.fuel_number == 0:
                #print("help")
                en_pos = False
            else:  
                en_pos = True
            
        #print(game_lose)
        if en_pos == False:
            game_lose = True
            Player_turn = False
            Enemy_turn = True
        
            
        #this is how you move the main character to the right
        if right_button.rose == True and board_layer_show == True:
            #print("right")
            Player.move_right(my_label,bullet,enemy_queue)
            
            
        #this is how you move the main character to the left
        elif left_button.rose == True and board_layer_show == True:#if the current position is not the saem as the last position and the main board is up 
            #print("left")
            Player.move_left(my_label,bullet)
            
      
        #if the menu layer is on the screen 
        if menu.show == True and board_layer_show == False:
            if right_button.rose:
                selector_val = selector_val + 1
                
                if selector_val > 2:
                    selector_val = 2
                selector.selector_layer_x = selector_val*40
                selector.move()
                
                
            elif left_button.rose:
                selector_val = selector_val - 1
                if selector_val < 0:
                    selector_val = 0
                selector.selector_layer_x = selector_val*40
                #move menu selector left
                selector.move()
                
        
        #menu control

        if action_button.rose:
            
            #print("Button released")
            if menu.show == False and board_layer_show == True:
                
                menu.show = True
                board_layer_show = False
                Environment.display_layer.append(menu.menu_display_layer)
                
            elif menu.show == True and board_layer_show == False:# menu forward
                if selector_val == 0:
                    Forward = True
                    if Fuel.fuel_number >0:
                        menu.Forward(Environment,Player)
                        board_layer_show = True
                        Fuel.reset_fuel(Environment)
                        Fuel.fuel_number = Fuel.fuel_number - 1
                        
                        #print(Fuel.fuel_number)
                        Fuel.fuel_gauge(Environment, Fuel.fuel_number)
                        bullet_layer.remove(bullet)
                        bullet = displayio.TileGrid(bullet_size, pixel_shader=bullet_pallet, x=Player.x+2, y=bullet_len-8)
                        bullet_layer.append(bullet)
                        bullet_len = bullet_len-8
                        Player.y = Player.y-8
                        #print(Player.y)
                        Player_turn = False
                        Enemy_turn = True
                        if Player.y < 0:
                            game_win = True
                            #print("you win")
                    else:
                        menu.show = False
                        board_layer_show = True
                        Environment.display_layer.remove(menu.menu_display_layer)
                        Popup.show = True
                        Environment.display_layer.append(Popup.popup_display_layer)
                        while Popup.show == True:
                            action_button.update()
                            if action_button.rose:
                                Popup.show = False
                                Environment.display_layer.remove(Popup.popup_display_layer)
                elif selector_val == 1:# menu fire
                    #print("fired!")
                    Environment.display_layer.remove(menu.menu_display_layer)
                    menu.show = False
                    board_layer_show = True
                    bullet_len = Player.y
                    new_enemy_queue = []
                    for en in enemy_queue:
                        if Player.x == en.x:
                            new_enemy_queue.append(en)
                    while bullet.y > 0:
                       
                        bullet.y = bullet.y - 1
                        
                        #print("bullet len is " + str(bullet.y))
                        time.sleep(.03)
                        bullet_layer.remove(bullet)
                        bullet = displayio.TileGrid(bullet_size, pixel_shader=bullet_pallet, x=Player.x+2, y=bullet.y)
                        bullet_layer.append(bullet)
                        for new_en in new_enemy_queue:
                            
                            if Player.x == (new_en.x) and new_en.y == bullet.y:
                                
                                if Fuel.fuel_number == 3:
                                    Fuel.reset_fuel(Environment)
                                    bullet_layer.remove(bullet)
                                    bullet_len = Player.y
                                    bullet = displayio.TileGrid(bullet_size, pixel_shader=bullet_pallet, x=Player.x+2, y=bullet_len)
                                    bullet_layer.append(bullet)
                                    Fuel.fuel_number = 3
                                    
                                    Fuel.fuel_gauge(Environment, Fuel.fuel_number)
                                    remove_enemy(new_en, Environment)
                                    enemy_queue.remove(new_en)
                                    enemy_alive = False
                                    Player_turn = False
                                    Enemy_turn = True
                                    Fired = True
                                    break
                                else:
                                    Fuel.reset_fuel(Environment)
                                    bullet_layer.remove(bullet)
                                    bullet_len = Player.y
                                    bullet = displayio.TileGrid(bullet_size, pixel_shader=bullet_pallet, x=Player.x+2, y=bullet_len)
                                    bullet_layer.append(bullet)
                                    Fuel.fuel_number = Fuel.fuel_number + 1
                                    
                                    Fuel.fuel_gauge(Environment, Fuel.fuel_number)
                                    remove_enemy(new_en, Environment)
                                    enemy_queue.remove(new_en)
                                    enemy_alive = False
                                    Player_turn = False
                                    Enemy_turn = True
                                    Fired = True
                                    break
                            elif bullet.y < 0:
                                bullet_len = Player.y
                                bullet_layer.remove(bullet)
                                bullet = displayio.TileGrid(bullet_size, pixel_shader=bullet_pallet, x=Player.x+2, y=bullet_len)
                                bullet_layer.append(bullet)
                                Player_turn = False
                                Enemy_turn = True
                        if Fired == True:
                            break
                elif selector_val == 2:# menu back
                    Environment.display_layer.remove(menu.menu_display_layer)
                    menu.show = False
                    board_layer_show = True
        if bullet.y <= 0 and game_win == False:
            print("bullet_now")
            bullet_len = Player.y
            bullet_layer.remove(bullet)
            bullet = displayio.TileGrid(bullet_size, pixel_shader=bullet_pallet, x=Player.x+2, y=bullet_len)
            bullet_layer.append(bullet)

        if Player.x<0:
            Player.x= 0
            bullet.x = Player.x+2
            Player.inner_sprite.x = Player.x
            
        if Player.x>120:
            Player.x = 120
            bullet.x = Player.x+2
            Player.inner_sprite.x = Player.x
        ####################################    
        ###### Player turn ends here #######
        ####################################
    if game_win == True:
        game_win = False
        Forward = False
        Fired = False
        time.sleep(.5)
        Environment.win()
        for en in enemy_queue:
            Environment.sprite_layer.remove(en.circle)
        while Environment.win_show == True:
            action_button.update()
            if action_button.rose:
                Environment.win_show = False
        Environment.canvas.remove(Environment.win_display)
        Player.reset(56,47,Environment)
        enemy_queue = []
        pos_queue = []
        generate_enemy_row(pos_queue,enemy_queue,Environment)
        bullet.x = Player.x - 4
        bullet_layer.remove(bullet)
        bullet = displayio.TileGrid(bullet_size, pixel_shader=bullet_pallet, x=Player.x+2, y=Player.y)
        bullet_layer.append(bullet)
        bullet.y = Player.y
        Fuel.reset_fuel(Environment)
        Fuel.fuel_gauge(Environment,2)
        Fuel.fuel_number = 2
    
    ##################################################
    ########## Enemy Turn Starts Here ################
    ##################################################
    while Enemy_turn == True:
        if Forward == True:
            Forward = False
            for en in enemy_queue:
                move_enemy_forward(Environment,en,enemy_queue)
        
        if Fired == True:
            Fired  = False
            ### function to move each enemy south 1 unit
            for en in enemy_queue:
                move_enemy_forward(Environment,en,enemy_queue)
            pos_queue = []
            generate_enemy_row(pos_queue,enemy_queue,Environment)
        
        Enemy_turn = False
   #######################Game Lost##########     
    
    for en in enemy_queue:

        if Player.x == en.x and Player.y == (en.y - 1):
            
            game_lose = True
            break
    if game_lose == True:
        print("you lose")
        game_lose = False
        Forward = False
        Fired = False
        time.sleep(.25)
        Player.reset(56,47,Environment)
        bullet.x = Player.x - 4
        bullet_layer.remove(bullet)
        bullet = displayio.TileGrid(bullet_size, pixel_shader=bullet_pallet, x=Player.x+2, y=Player.y)
        bullet_layer.append(bullet)
        bullet.y = Player.y
        bullet_len = Player.y
        Environment.lose()
        
        
        for en in enemy_queue:
            Environment.sprite_layer.remove(en.circle)
        while Environment.lose_show == True:
            action_button.update()
            if action_button.rose:
                Environment.lose_show = False
        Environment.canvas.remove(Environment.lose_display)
        
        enemy_queue = []
        pos_queue = []
        generate_enemy_row(pos_queue,enemy_queue,Environment)
        
        Fuel.reset_fuel(Environment)
        Fuel.fuel_gauge(Environment,2)
        Fuel.fuel_number = 2
    Player_turn = True
