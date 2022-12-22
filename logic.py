import pygame
import pickle
import time

from pygame.locals import (RLEACCEL,KEYDOWN,K_INSERT,K_SPACE,MOUSEBUTTONDOWN)
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
        
class Screen ():
    
    name = ""
    #Every screen needs to know how to draw it self
    def Paint():
        pass
class Main_screen (Screen):
    name = "main screen"
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
    name = "quest screen"
    #init tiene que aceptar en su constructor un logic.Save , del cual va a tomar las misiones pendientes para pintarlas
    def __init__(self) -> None:
        super().__init__()
    def Paint():
        quest_board_path = "resources\quest_board.png"
        quest_board = pygame.image.load(quest_board_path).convert()
        quest_board.set_colorkey((0,0,0),RLEACCEL)
        return quest_board
class Tutorial():
    
    def __init__(self,display:pygame.Surface):
        self.ended = False
        self.step = 0
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
    def step_7(self):
        background = Main_screen(1)
        self.display.blit(background.Paint(),(0,0))
        msg_path = "resources\msg.png"
        msg_view = pygame.image.load(msg_path).convert()
        msg_view.set_colorkey((0,0,0),RLEACCEL)
        self.display.blit(msg_view,(0,0))
        pygame.display.flip()
        image = self.font.render("Worked",True, (5,5,5),(0,0,0))
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
        
                                
        
        
        
    
        
    
    