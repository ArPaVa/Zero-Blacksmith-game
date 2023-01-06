import pygame
from pygame_texteditor import TextEditor
import pickle
import time

from pygame.locals import (RLEACCEL,KEYDOWN,K_INSERT,K_SPACE,MOUSEBUTTONDOWN,K_ESCAPE)
def string_to_list(string:str, size):
    result = []
    i=0
    while True:
        if i + size >= len(string):
            result.append(string[i:])
            return result
        result.append(string[i:i+size])
        i += size
        
class Save():
    forge_level = 1
    def read_save():
        file = open("save.bin","rb")
        save = pickle.load(file)
        file.close()
        return save
    def write_save(self):
        file = open("save.bin","wb")
        pickle.dump(self,file)
        file.close()
        
class Quest():                                #Quizas el q
    def __init__(self,npc:str,title:str,description:str,monster_list,reward:int,rank:int):
        self.npc = npc
        self.title = title
        self.description = description
        self.monster_list = monster_list
        self.completed = False
        self.reward = reward
        self.rank = rank
   
    def Paint(self):
        """ Paint quest title and the quest info"""
        title_font = pygame.font.SysFont("Arial",40)
        font = pygame.font.SysFont("Arial",26)
        quest_image_path = "resources\quest_board.png"
        image = pygame.image.load(quest_image_path).convert()
        title = title_font.render(self.title,True, (5,5,5),(0,0,0))
        title.set_colorkey((0,0,0), RLEACCEL)
        title_rect = title.get_rect()
        title_rect.centerx = 640
        title_rect.centery = 150
        image.blit(title,title_rect)
        description = string_to_list(self.description,60)
        text_y = 200
        for i in range(len(description)):
            text = font.render(description[i],True, (5,5,5),(0,0,0))
            text.set_colorkey((0,0,0),RLEACCEL)
            text_rect = text.get_rect()
            text_rect.centerx = 640
            text_rect.centery = text_y
            image.blit(text,text_rect)
            text_y += 30
        image.set_colorkey((0,0,0),RLEACCEL)
        return image
        
class Screen ():    
    name = ""
    #Every screen needs to know how to draw it self
    def Paint(self):
        pass

class Main_screen (Screen):
    name = "main_screen"
    def __init__(self, forge_level:int):
        self.forge_level = forge_level
        quest_sign_path = "resources\quest_sign.png"
        quest_sign = pygame.image.load(quest_sign_path).convert()
        if forge_level == 1:
            self.quest_rect = quest_sign.get_rect()#603, 167
            self.quest_rect.centerx = 603
            self.quest_rect.centery = 167
        if forge_level == 2 or forge_level == 3:
            self.quest_rect = quest_sign.get_rect() #633, 172
            self.quest_rect.centerx = 633
            self.quest_rect.centery = 172
        if forge_level == 4:
            self.quest_rect = quest_sign.get_rect() #431, 203 
            self.quest_rect.centerx = 431
            self.quest_rect.centery = 203
  
    def Paint(self):
        if self.forge_level == 0:
            path = "resources\state_1.png"
            view = pygame.image.load(path).convert()
            return view
        else:
            path = "resources\state_" + str(self.forge_level) + ".png"
            view = pygame.image.load(path).convert()
            quest_sign_path = "resources\quest_sign.png"
            quest_sign = pygame.image.load(quest_sign_path).convert()
            quest_sign.set_colorkey((0,0,0),RLEACCEL)
            view.blit(quest_sign,self.quest_rect)
            return view

class Quest_screen (Screen):
    name = "quest_screen"
    #init tiene que aceptar en su constructor un logic.Save , del cual va a tomar las misiones pendientes para pintarlas
    def __init__(self,forge_level):
        self.forge_level= forge_level
        file = open("quests.bin","rb")
        quests = pickle.load(file)
        file.close()
        self.quests = []
        for q in quests:
            if quests[q].rank == self.forge_level:
                self.quests.append(quests[q])
        self.max_index = len(quests)//3
        if len(quests)%3 != 0:
            self.max_index+=1
        self.index = 1
        self.selected = None
        self.detailed_back_rect = None
        self.detailed_forge_rect = None
        self.small_back_buttom_rect = None
        self.small_next_buttom_rect = None
        self.main_screen_buttom_rect = None
    
    def wait(self):
        cont = True
        while(cont):
          self.Paint()
          for event in pygame.event.get():
               if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                        if self.selected is None:
                            butt , cont = self.OnClick_quest_list(pygame.mouse.get_pos())
                        else:
                            butt, cont = self.OnClick_detailed(pygame.mouse.get_pos())
        return butt
            
    def pager(self):
        start = 3 * (self.index - 1)
        if start >= len(self.quests):
            raise IndexError('Too much index, and not enough quests')
        result = []
        size = min(3, len(self.quests)-start) # possible error by +-1
        for i in range(size):
            result.append(self.quests[start + i])
        return result
        
    def Paint(self):
        font = pygame.font.SysFont("Arial",26)
        quest_board_path = "resources\quest_board.png"
        quest_board = pygame.image.load(quest_board_path).convert()
        quest_board.set_colorkey((0,0,0),RLEACCEL)
        self.quest1 = None
        self.quest_rect1 = None
        self.quest2 = None
        self.quest_rect2 = None
        self.quest3 = None
        self.quest_rect3 = None
        self.main_screen_buttom_rect = None
        if self.selected == None:
            # paint quests list, back button and paging buttons
            quests = self.pager() # quests to paint
            
            main_screen_buttom_path = "resources/buttom.png"
            main_buttom_image = pygame.image.load(main_screen_buttom_path).convert()
            main_buttom_image.set_colorkey((0,0,0),RLEACCEL)
            self.main_screen_buttom_rect = main_buttom_image.get_rect()
            self.main_screen_buttom_rect.centerx = 700
            self.main_screen_buttom_rect.centery = 670
            quest_board.blit(main_buttom_image,self.main_screen_buttom_rect)
            text = font.render("Main Screen",True, (5,5,5),(0,0,0))
            text.set_colorkey((0,0,0), RLEACCEL)
            text_rect = text.get_rect()
            text_rect.centerx = 700
            text_rect.centery = 670
            quest_board.blit(text,text_rect)
            
            if self.index != 1:
                small_back_buttom_path = "resources\small_back_buttom.png"
                small_back_buttom = pygame.image.load(small_back_buttom_path).convert()
                small_back_buttom.set_colorkey((0,0,0),RLEACCEL)
                self.small_back_buttom_rect = small_back_buttom.get_rect()
                self.small_back_buttom_rect.centerx = 320
                self.small_back_buttom_rect.centery = 670
                quest_board.blit(small_back_buttom,self.small_back_buttom_rect)
            if self.index != self.max_index:
                small_next_buttom_path = "resources\small_next_buttom.png"
                small_next_buttom = pygame.image.load(small_next_buttom_path).convert()
                small_next_buttom.set_colorkey((0,0,0),RLEACCEL)
                self.small_next_buttom_rect = small_next_buttom.get_rect()
                self.small_next_buttom_rect.centerx = 520
                self.small_next_buttom_rect.centery = 670
                quest_board.blit(small_next_buttom,self.small_next_buttom_rect)
            small_buttom_path = "resources\small_buttom.png"
            small_buttom = pygame.image.load(small_buttom_path).convert()
            small_buttom.set_colorkey((0,0,0),RLEACCEL)
            small_buttom_rect = small_buttom.get_rect()
            small_buttom_rect.centerx = 420
            small_buttom_rect.centery = 670
            quest_board.blit(small_buttom,small_buttom_rect)
            index = font.render(str(self.index),True, (5,5,5),(0,0,0))
            index.set_colorkey((0,0,0), RLEACCEL)
            index_rect = index.get_rect()
            index_rect.centerx = 420
            index_rect.centery = 670
            quest_board.blit(index,index_rect)
            # first quest center
            centerx = 630
            centery = 220
            for n in range(len(quests)):            
                quest:Quest = quests[n]
                quest_path = "resources\Characters/" + quest.npc + "_quest.png"
                quest_image = pygame.image.load(quest_path).convert()
                quest_image.set_colorkey((0,0,0),RLEACCEL)
                quest_rect = quest_image.get_rect()
                quest_rect.centerx = centerx 
                quest_rect.centery = centery + n * 160 
                # save quests rect for OnClick
                if n == 0:
                    self.quest_rect1 = quest_rect 
                    self.quest1 = quests[n]
                elif n == 1:
                    self.quest_rect2 = quest_rect
                    self.quest2 = quests[n]            
                elif n == 2:
                    self.quest_rect3 = quest_rect
                    self.quest3 = quests[n]
                # quest title
                quest_board.blit(quest_image,quest_rect)
                title = font.render(quest.title,True, (5,5,5),(0,0,0))
                title.set_colorkey((0,0,0),RLEACCEL)
                title_rect = title.get_rect()
                title_rect.centerx = centerx
                title_rect.centery = centery + n * 160
                quest_board.blit(title,title_rect)
            pygame.display.get_surface().blit(quest_board,(0,0))
            pygame.display.flip()
        else:
            # showing the quest details                    
            # self.display.blit(board_view,(0,0))
            quest_image = self.selected.Paint()
            image_rect = quest_image.get_rect()
            quest_board.blit(quest_image, image_rect)
            # self.display.blit(image,image_rect)
            
            # paint back button            
            back_buttom_path = "resources/back_buttom.png"
            back_buttom_image = pygame.image.load(back_buttom_path).convert()
            back_buttom_image.set_colorkey((0,0,0),RLEACCEL)
            back_buttom_rect = back_buttom_image.get_rect()
            back_buttom_rect.centerx = 700
            back_buttom_rect.centery = 650
            self.detailed_back_rect = back_buttom_rect
            quest_board.blit(back_buttom_image,back_buttom_rect)
            # self.display.blit(back_buttom_image,back_buttom_rect)
            
            # paint forge button
            forge_buttom_path = "resources/forge_buttom.png"
            forge_buttom_image = pygame.image.load(forge_buttom_path).convert()
            forge_buttom_image.set_colorkey((0,0,0),RLEACCEL)
            forge_buttom_rect = forge_buttom_image.get_rect()
            forge_buttom_rect.centerx = 900
            forge_buttom_rect.centery = 650
            self.detailed_forge_rect = forge_buttom_rect
            quest_board.blit(forge_buttom_image,forge_buttom_rect)
            # self.display.blit(forge_buttom_image,forge_buttom_rect)
            pygame.display.get_surface().blit(quest_board,(0,0))
            pygame.display.flip()
   
    def OnClick_quest_list(self,mouse_pos:tuple):
        if self.quest_rect1 != None and self.quest_rect1.collidepoint(mouse_pos):
            self.selected = self.quest1
            return self.selected,True
        if self.quest_rect2 != None and self.quest_rect2.collidepoint(mouse_pos):
            self.selected = self.quest2
            return self.selected,True
        if self.quest_rect3 != None and self.quest_rect3.collidepoint(mouse_pos):
            self.selected = self.quest3
            return self.selected,True
        if self.main_screen_buttom_rect != None and self.main_screen_buttom_rect.collidepoint(mouse_pos):
            return "main_screen" , False
        if self.small_back_buttom_rect != None and self.small_back_buttom_rect.collidepoint(mouse_pos) and self.index != 1:
            self.index -=1
        if self.small_next_buttom_rect != None and self.small_next_buttom_rect.collidepoint(mouse_pos) and self.index != self.max_index:
            self.index +=1
        return self.selected,True
    
    def OnClick_detailed(self,mouse_pos:tuple):
        if self.detailed_back_rect.collidepoint(mouse_pos):
            self.selected = None
            return 'back', True
        if self.detailed_forge_rect.collidepoint(mouse_pos):
            self.selected = None
            return 'forge', False
        return '', True

class Forge_screen(Screen):
    def __init__(self):
        self.TX = TextEditor(30,30,1100,740,pygame.display.get_surface())
        self.TX.set_line_numbers(True)
        self.main_screen_buttom_rect = None
  
    def wait(self):
        running = True
        while running:
            # capture input
            pygame_events = pygame.event.get() 
            pressed_keys = pygame.key.get_pressed() 
            mouse_x, mouse_y = pygame.mouse.get_pos() 
            mouse_pressed = pygame.mouse.get_pressed()
            for event in pygame_events:
                if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                        butt , running = self.OnClick(pygame.mouse.get_pos())                   
            # display editor functionality once per loop 
            self.Paint(pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed) 
        return butt
        
    def Paint(self,pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed):
        font = pygame.font.SysFont("Arial",26)
        main_screen_buttom_path = "resources/buttom.png"
        main_buttom_image = pygame.image.load(main_screen_buttom_path).convert()
        main_buttom_image.set_colorkey((0,0,0),RLEACCEL)
        self.main_screen_buttom_rect = main_buttom_image.get_rect()
        self.main_screen_buttom_rect.centerx = 1250
        self.main_screen_buttom_rect.centery = 100
        pygame.display.get_surface().blit(main_buttom_image,self.main_screen_buttom_rect)
        text = font.render("Main Screen",True, (5,5,5),(0,0,0))
        text.set_colorkey((0,0,0), RLEACCEL)
        text_rect = text.get_rect()
        text_rect.centerx = 1250
        text_rect.centery = 100
        pygame.display.get_surface().blit(text,text_rect)
        self.TX.display_editor(pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed) 
        # update pygame window 
        pygame.display.flip()

    def OnClick(self,mouse_pos):
        if self.main_screen_buttom_rect != None and self.main_screen_buttom_rect.collidepoint(mouse_pos):
            return "main_screen" , False
        return "", True
        
class Tutorial():
    def __init__(self,display:pygame.Surface):
        self.ended = False
        self.display = display
        self.font = pygame.font.SysFont("Arial",26)
        self.step_1()
    def step_1(self):
        #Quizas se puede optimizar uniendo las dos imagenes (background y msg_view)
        background_path = "resources/tutorial_screen.jpg"
        background = pygame.image.load(background_path).convert()
        self.display.blit(background,(0,0))
        
        msg_path = "resources\msg.png"
        msg_view = pygame.image.load(msg_path).convert()
        msg_view.set_colorkey((0,0,0),RLEACCEL)
        self.display.blit(msg_view,(0,0))
        
        image = self.font.render("En un mundo donde las matemáticas son tan importantes",True, (5,5,5),(0,0,0))
        image.set_colorkey((0,0,0),RLEACCEL)
        text_rect = image.get_rect()
        text_rect.centerx = 630
        text_rect.centery = 630
        self.display.blit(image,text_rect)
        pygame.display.flip()
        time.sleep(1)
        image = self.font.render("como en el nuestro....",True, (5,5,5),(0,0,0))
        image.set_colorkey((0,0,0),RLEACCEL)
        text_rect.centery = 650
        self.display.blit(image,text_rect)
        pygame.display.flip()
        cont = True 
        while(cont):
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        cont=False
                    if event.key == K_INSERT:
                        cont=False 
                if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                        cont = False
        self.step_2(background,msg_view)
    def step_2(self,background, msg_view):
        #si no se optimiza uniendo las imagenes background y msg_view (e incluso si se hace ) quizas se podria 
        # optimizar solo haciendo blit del msg_view sobre el background sucio
        self.display.blit(background,(0,0))
        self.display.blit(msg_view,(0,0))
        #####Hacer un modulo que haga texto#####
        image = self.font.render("Un joven matemático comienza su travesía, con el propósito",True, (5,5,5),(0,0,0))
        image.set_colorkey((0,0,0),RLEACCEL)
        text_rect = image.get_rect()
        text_rect.centerx = 630
        text_rect.centery = 630
        self.display.blit(image,text_rect)
        pygame.display.flip()
        time.sleep(1)
        image = self.font.render("de restaurar la gloria de la forja de sus antepasados.",True, (5,5,5),(0,0,0))
        image.set_colorkey((0,0,0),RLEACCEL)
        text_rect.centery = 650
        self.display.blit(image,text_rect)
        pygame.display.flip()
        cont = True 
        while(cont):
           for event in pygame.event.get():
               if event.type == KEYDOWN:
                   if event.key == K_SPACE:
                       cont=False
                   if event.key == K_INSERT:
                       cont=False 
               if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                        cont = False
        self.step_3()
    def step_3(self):
        ###### Usar Main Screen para pintar el background en lugar de cargarlo
        # background_path = "resources\state_1.png"
        # background = pygame.image.load(background_path).convert()
        background = Main_screen(0)
        self.display.blit(background.Paint(),(0,0))
        katrine_msg_path = "resources\Characters\katrine_msg.png"
        katrine_msg_view = pygame.image.load(katrine_msg_path).convert()
        katrine_msg_view.set_colorkey((0,0,0),RLEACCEL)
        self.display.blit(katrine_msg_view,(0,0))
        
        image = self.font.render("Viejo calvo: Hola joven, mi nombre es Katrine y fui amigo de tu",True, (5,5,5),(0,0,0))
        image.set_colorkey((0,0,0),RLEACCEL)
        text_rect = image.get_rect()
        text_rect.centerx = 630
        text_rect.centery = 630
        self.display.blit(image,text_rect)
        pygame.display.flip()
        time.sleep(1)
        image = self.font.render("abuelo. Me alegra ver que tienes la idea de trabajar en su forja.",True, (5,5,5),(0,0,0))
        image.set_colorkey((0,0,0),RLEACCEL)
        text_rect.centery = 650
        self.display.blit(image,text_rect)
        pygame.display.flip()
        cont = True
        while(cont):
          for event in pygame.event.get():
               if event.type == KEYDOWN:
                   if event.key == K_SPACE:
                       cont=False
                   if event.key == K_INSERT:
                       cont=False 
               if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                        cont = False
        self.step_4(background,katrine_msg_view)
    def step_4(self,background,katrine_msg_view):
        self.display.blit(background.Paint(),(0,0))
        self.display.blit(katrine_msg_view,(0,0))
        image = self.font.render("Katrine:Te gustaría que te explique las reglas del jue..digo, negocio?",True, (5,5,5),(0,0,0))
        image.set_colorkey((0,0,0),RLEACCEL)
        text_rect = image.get_rect()
        text_rect.centerx = 630
        text_rect.centery = 630
        self.display.blit(image,text_rect)
        pygame.display.flip()
        time.sleep(1)
        #### YES OR NO CLICKABLE MODULE NEEDED ######################
        yes_selectable = self.font.render("Si",True, (5,5,5),(0,0,0))
        yes_selectable.set_colorkey((0,0,0),RLEACCEL)
        yes_rect = yes_selectable.get_rect()
        yes_rect.centerx = 630
        yes_rect.centery = 650
        self.display.blit(yes_selectable,yes_rect)
        no_selectable = self.font.render("No",True, (5,5,5),(0,0,0))
        no_selectable.set_colorkey((0,0,0),RLEACCEL)
        no_rect = no_selectable.get_rect()
        no_rect.centerx = 630
        no_rect.centery = 670
        self.display.blit(no_selectable,no_rect)
        pygame.display.flip()
        cont = True
        while(cont):
          for event in pygame.event.get():
               if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                        if yes_rect.collidepoint(pygame.mouse.get_pos()): 
                            cont=False
                            self.step_5(background,katrine_msg_view)
                        if no_rect.collidepoint(pygame.mouse.get_pos()):
                            cont=False
    def step_5(self,background,katrine_msg_view):
        self.display.blit(background.Paint(),(0,0))
        self.display.blit(katrine_msg_view,(0,0))
        image = self.font.render("Katrine: Vamos a ver que puedes hacer. Forjame algo capaz",True, (5,5,5),(0,0,0))
        image.set_colorkey((0,0,0),RLEACCEL)
        text_rect = image.get_rect()
        text_rect.centerx = 630
        text_rect.centery = 630
        self.display.blit(image,text_rect)
        pygame.display.flip()
        time.sleep(1)
        image = self.font.render("de matar a la maldita pitón que está viviendo en mi jardín.",True, (5,5,5),(0,0,0))
        image.set_colorkey((0,0,0),RLEACCEL)
        text_rect.centery = 650
        self.display.blit(image,text_rect)
        pygame.display.flip()
        cont = True
        while(cont):
          for event in pygame.event.get():
               if event.type == KEYDOWN:
                   if event.key == K_SPACE:
                       cont=False
                   if event.key == K_INSERT:
                       cont=False 
               if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                        cont = False
        self.step_6()
    def step_6(self):
        background = Main_screen(1)
        self.display.blit(background.Paint(),(0,0))
        msg_path = "resources\msg.png"
        msg_view = pygame.image.load(msg_path).convert()
        msg_view.set_colorkey((0,0,0),RLEACCEL)
        self.display.blit(msg_view,(0,0))
        pygame.display.flip()
        image = self.font.render("Click en el mensaje para ver las misiones",True, (5,5,5),(0,0,0))
        image.set_colorkey((0,0,0),RLEACCEL)
        text_rect = image.get_rect()
        text_rect.centerx = 630
        text_rect.centery = 630
        self.display.blit(image,text_rect)
        pygame.display.flip()
        cont = True
        while(cont):
          for event in pygame.event.get():
               if event.type == KEYDOWN:
                   if event.key == K_SPACE:
                       cont=False
                   if event.key == K_INSERT:
                       cont=False 
               if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                         if background.quest_rect.collidepoint(pygame.mouse.get_pos()):
                             cont=False
                             self.step_7()
    def step_7(self): ##FUNCIONAMIENTO DEL QUEST BOARD
        background = Main_screen(1)
        self.display.blit(background.Paint(),(0,0))
        screen = Quest_screen(0)
        butt = screen.wait()
        if butt == "main_screen":
            self.step_6()
        self.step_8()
    def step_8(self):
        forge = Forge_screen() 
        butt = forge.wait()
        if butt == "main_screen":
            pygame.display.get_surface().fill((0,0,0))
            self.step_6()
           
                                
        
        
        
    
        
    
    