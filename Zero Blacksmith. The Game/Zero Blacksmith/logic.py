import pygame
from pygame_texteditor import TextEditor
import pickle
import time
import os
import F0F
from F0F import FunctDetails, Functions, MFUN

from pygame.locals import (RLEACCEL,KEYDOWN,K_INSERT,K_SPACE,MOUSEBUTTONDOWN,K_ESCAPE)

resources_path = "resources"
character_path = os.path.join(resources_path, "Characters")

def pass_level(forge_level:int) -> bool:
    quests = get_quests_for_level(forge_level)
    if len(quests) == 0:
        return False
    for q in quests:
        if not q.completed:
            return False
    return True

def get_quests_for_level(forge_level:int) -> list:
    rquests = Quests_save.read_save().quests
    quests = []
    for q in rquests:
        if rquests[q].rank == forge_level:
            quests.append(rquests[q])
    return quests

def level_up(forge_level:int):
    lvl_text = {
        2: ["¡Felicitaciones! Has mejorado tu forja a rango 2.","Has avanzado en el dominio de las funciones.","NO OLVIDES el ';' ."],
        3: ["¡Felicitaciones! Has mejorado tu forja a rango 3.","Pista: Si una misión tiene muchos enemigos, ","un arma rápida suele ser la mejor opción.",],
        4: ["¡Felicitaciones! Has mejorado tu forja a rango 4.","Recuerda, no existe un arma omnipotente, ","todas tienen algún defecto."],
        5: ["¡¡¡Excelente!!!","Has vencido a todas las funciones que se han puesto en tu camino.","Has trascendido el camino de la forja, y ganado pelo en el proceso.","Puedes intercambiar este recurso tan valioso en otro planos."]
    }
    level_up_path = os.path.join(resources_path,"level_up_"+str(forge_level)+".png")
    level_up_image = pygame.image.load(level_up_path).convert()
    level_up_image.set_colorkey((0,0,0),RLEACCEL)
    level_up_rect = level_up_image.get_rect()
    
    msg = lvl_text[forge_level]
    font = pygame.font.SysFont("Arial",40)
    text_y = 300
    sep = 70
    for i in range(len(msg)):
        text = font.render(msg[i],True, (5,5,5),(0,0,0))
        text.set_colorkey((0,0,0),RLEACCEL)
        text_rect = text.get_rect()
        text_rect.centerx = 600
        text_rect.centery = text_y
        level_up_image.blit(text,text_rect)
        text_y += sep
        font = pygame.font.SysFont("Arial",26)
        sep = 40
     
    pygame.display.get_surface().blit(level_up_image,level_up_rect)
    pygame.display.flip()

def string_to_list(string:str, size):
    if len(string) == 0:
        return [""]
    result = []
    i=0
    while True:
        if i + size >= len(string):
            result.append(string[i:])
            return result
        result.append(string[i:i+size])
        i += size

def intial_code ():
    return "//Forge your best weapon to defeat those functions \n\nForge (f, min, max)\n{\n\n}"

class Save():
    forge_level = 0
    reward = 0
    def read_save():
        file = open("save.bin","rb")
        save = pickle.load(file)
        file.close()
        return save
    def write_save(self):
        file = open("save.bin","wb")
        pickle.dump(self,file)
        file.close()

class Quests_save(Save):
    def __init__(self,quests:dict):
        self.quests = quests
    def read_save():
        file = open("quests.bin","rb")
        save = pickle.load(file)
        file.close()
        return save
    def write_save(self):
        file = open("quests.bin","wb")
        pickle.dump(self,file)
        file.close()  

class Quest():
    def __init__(self,id:int,npc:str,title:str,description:str,monster_list:list,reward:int,rank:int,code:str,max_time:int):
        self.id = id
        self.npc = npc
        self.title = title
        self.description = description
        self.monster_list = monster_list
        self.completed = False
        self.cashed = False
        self.reward = reward
        self.rank = rank
        self.code = code
        self.max_time = max_time
        self.completeness_message = "En Espera"
        self.sins = 0
        self.error_list = []
    
    def __str__(self) -> str:
        q_str = "Quest " + str(self.id) + " ---- " + self.title +"   " +  self.completeness_message + \
                " ---- rank : "+ str(self.rank) + " --- " + "reward : " + str(self.reward)
        return q_str
    def __repr__(self) -> str:
        return self.__str__()
    
    def Paint(self):
        """ Paint quest title and the quest info"""
        title_font = pygame.font.SysFont("Arial",40)
        font = pygame.font.SysFont("Arial",26)
        quest_image_path = os.path.join(resources_path,"quest_board.png")
        image = pygame.image.load(quest_image_path).convert()
        title = title_font.render(self.title,True, (5,5,5),(0,0,0))
        title.set_colorkey((0,0,0), RLEACCEL)
        title_rect = title.get_rect()
        title_rect.centerx = 640
        title_rect.centery = 150
        image.blit(title,title_rect)
        description = string_to_list(self.description,60) + string_to_list("Recompenza : "+str(self.reward)+".",60) +  string_to_list(self.completeness_message,60)
        if self.sins > 0:
            description = description + ["Contador de mldición : "+ str(self.sins)] 
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
 
    def Quest_complete(self): 
        return self.completed
    
    def check_completeness(self):
        self.error_list = []
        self.completed = False
        # open thread
        st = time.time()
        i = 0
        eq = 0
        # try:
        for monster in self.monster_list:
            monster:Monster
            Forge_eval, had_error, error_list = F0F.compile(self.code, [monster.fun, monster.fun.llim, monster.fun.rlim])
            if had_error:
                self.completeness_message = "El arma tiene muchos problemas."
                self.completed = False
                self.error_list = error_list
                self.sins = 0
                return Forge_eval, had_error, error_list
            elif not monster.check_zero(Forge_eval[0]):
                self.completeness_message = "No todos los enemigos fueron vencidos."
                self.completed = False
                self.sins = 0
                return Forge_eval, had_error, error_list
            eq += Forge_eval[1]
            i+=1
        # except Exception as err:
        #     self.completeness_message = "El arma tiene muchos problemas."
        #     self.completed = False
        #     return None, True, []
        et = time.time()
        #check thread ended
        print( self.__str__(), ' time: ', round(et-st,4))
        if round(et-st,4) > self.max_time:
            self.completeness_message = "El arma es demasiado lenta para vencer."
            self.completed = False
            self.sins = eq
        else:
            self.completeness_message = "¡COMPLETADA!"
            self.completed = True
            self.sins = eq
        
  
class Screen ():    
    name = ""
    #Every screen needs to know how to draw it self
    def Paint(self):
        pass
    def wait(self):
        pass

class Main_screen (Screen):
    name = "main_screen"
    def __init__(self, forge_level:int,current_reward:int,tutorial = False):
        self.forge_level = forge_level
        self.reward = current_reward
        self.is_tutorial = tutorial
        quest_sign_path = os.path.join(resources_path,"quest_sign.png") 
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
            path = os.path.join(resources_path,"state_1.png")
            view = pygame.image.load(path).convert()
            pygame.display.get_surface().blit(view,(0,0))        
        else:
            state_path = "state_" + str(self.forge_level) + ".png"
            path = os.path.join(resources_path,state_path)
            view = pygame.image.load(path).convert()
            quest_sign_path = os.path.join(resources_path,"quest_sign.png")
            quest_sign = pygame.image.load(quest_sign_path).convert()
            quest_sign.set_colorkey((0,0,0),RLEACCEL)
            view.blit(quest_sign,self.quest_rect)
            pygame.display.get_surface().blit(view,(0,0))
        if not self.is_tutorial:
            score_path = os.path.join(resources_path,"score.png")
            score_image = pygame.image.load(score_path).convert()
            score_image.set_colorkey((0,0,0),RLEACCEL)
            
            score_rect = score_image.get_rect()
            score_rect.centerx = 80
            score_rect.centery = 40
            output = ['Pelo:',str(self.reward)]
            
            text_y = 30
            panel_font = pygame.font.SysFont("Arial",24)
            for i in range(len(output)):
                text = panel_font.render(output[i],True, (255,255,255),(0,0,0))
                text.set_colorkey((0,0,0),RLEACCEL)
                text_rect = text.get_rect()
                text_rect.centerx = 80
                text_rect.centery = text_y
                score_image.blit(text,text_rect)
                text_y += 30       

            pygame.display.get_surface().blit(score_image,score_rect)  
        pygame.display.flip() 
        
    def wait(self):
        cont = True
        while(cont):
            self.Paint()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return "quit", None
                if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                        butt , cont = self.OnClick(pygame.mouse.get_pos())
        return butt , None
    
    def OnClick(self,mouse_pos:tuple):
        if self.quest_rect.collidepoint(mouse_pos):
            return "quest_screen",False
        return "",True
                        
class Quest_screen (Screen):
    name = "quest_screen"
    
    def __init__(self,forge_level):
        self.forge_level = forge_level
        
        self.quests = get_quests_for_level(self.forge_level)
        self.max_index = len(self.quests)//3
        if len(self.quests)%3 != 0:
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
        return butt , self.selected
            
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
        quest_board_path = os.path.join(resources_path,"quest_board.png")
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
            
            main_screen_buttom_path = os.path.join(resources_path,"buttom.png")
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
                small_back_buttom_path = os.path.join(resources_path,"small_back_buttom.png")
                small_back_buttom = pygame.image.load(small_back_buttom_path).convert()
                small_back_buttom.set_colorkey((0,0,0),RLEACCEL)
                self.small_back_buttom_rect = small_back_buttom.get_rect()
                self.small_back_buttom_rect.centerx = 320
                self.small_back_buttom_rect.centery = 670
                quest_board.blit(small_back_buttom,self.small_back_buttom_rect)
            if self.index != self.max_index:
                small_next_buttom_path = os.path.join(resources_path,"small_next_buttom.png")
                small_next_buttom = pygame.image.load(small_next_buttom_path).convert()
                small_next_buttom.set_colorkey((0,0,0),RLEACCEL)
                self.small_next_buttom_rect = small_next_buttom.get_rect()
                self.small_next_buttom_rect.centerx = 520
                self.small_next_buttom_rect.centery = 670
                quest_board.blit(small_next_buttom,self.small_next_buttom_rect)
            small_buttom_path = os.path.join(resources_path,"small_buttom.png")
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
                npc = quest.npc + "_quest.png"
                quest_path = os.path.join(character_path, npc)
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
            quest_image = self.selected.Paint()
            image_rect = quest_image.get_rect()
            quest_board.blit(quest_image, image_rect)
            
            # paint back button            
            back_buttom_path = os.path.join(resources_path,"back_buttom.png")
            back_buttom_image = pygame.image.load(back_buttom_path).convert()
            back_buttom_image.set_colorkey((0,0,0),RLEACCEL)
            back_buttom_rect = back_buttom_image.get_rect()
            back_buttom_rect.centerx = 700
            back_buttom_rect.centery = 650
            self.detailed_back_rect = back_buttom_rect
            quest_board.blit(back_buttom_image,back_buttom_rect)
            
            if self.selected.completed:
                pygame.display.get_surface().blit(quest_board,(0,0))
                pygame.display.flip()
                self.detailed_forge_rect = None
            else:
                # paint forge button
                forge_buttom_path = os.path.join(resources_path,"forge_buttom.png")
                forge_buttom_image = pygame.image.load(forge_buttom_path).convert()
                forge_buttom_image.set_colorkey((0,0,0),RLEACCEL)
                forge_buttom_rect = forge_buttom_image.get_rect()
                forge_buttom_rect.centerx = 900
                forge_buttom_rect.centery = 650
                self.detailed_forge_rect = forge_buttom_rect
                quest_board.blit(forge_buttom_image,forge_buttom_rect)
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
        if self.detailed_forge_rect != None and self.detailed_forge_rect.collidepoint(mouse_pos):
            return 'forge_screen', False
        return '', True

class Forge_screen(Screen):
    name = "forge_screen"
    def __init__(self, quest:Quest):
        self.TX = TextEditor(250,0,1110,775,pygame.display.get_surface())
        self.TX.set_line_numbers(True)
        self.main_screen_buttom_rect = None
        self.reset_buttom_rect = None
        self.forge_buttom_rect = None
        self.quest = quest
        self.first_time = True
        self.error_list = self.quest.error_list
  
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
        return butt , self.quest
        
    def Paint(self,pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed):
        font = pygame.font.SysFont("Arial",26)
        buttom_path = os.path.join(resources_path,"buttom.png")
        buttom_image = pygame.image.load(buttom_path).convert()
        buttom_image.set_colorkey((0,0,0),RLEACCEL)
        
        output_panel_path = os.path.join(resources_path,"output_panel.png")
        output_panel_image = pygame.image.load(output_panel_path).convert()
        output_panel_image.set_colorkey((0,0,0),RLEACCEL)
        output_panel_rect = output_panel_image.get_rect()
        output_panel_rect.centerx = 125
        output_panel_rect.centery = 550
        output = []
        for err in self.error_list:
            output = output + string_to_list(str(err),31)
        text_y = 20
        panel_font = pygame.font.SysFont("Arial",18)
        for i in range(len(output)):
            text = panel_font.render(output[i],True, (5,5,5),(0,0,0))
            text.set_colorkey((0,0,0),RLEACCEL)
            text_rect = text.get_rect()
            text_rect.centerx = 110
            text_rect.centery = text_y
            output_panel_image.blit(text,text_rect)
            text_y += 30       
        pygame.display.get_surface().blit(output_panel_image,output_panel_rect)   
        
        self.main_screen_buttom_rect = buttom_image.get_rect()
        self.main_screen_buttom_rect.centerx = 125
        self.main_screen_buttom_rect.centery = 100
        pygame.display.get_surface().blit(buttom_image,self.main_screen_buttom_rect)
        text = font.render("Menu principal",True, (5,5,5),(0,0,0))
        text.set_colorkey((0,0,0), RLEACCEL)
        text_rect = text.get_rect()
        text_rect.centerx = 125
        text_rect.centery = 100
        pygame.display.get_surface().blit(text,text_rect)
        
        self.reset_buttom_rect = buttom_image.get_rect()
        self.reset_buttom_rect.centerx = 125
        self.reset_buttom_rect.centery = 200
        pygame.display.get_surface().blit(buttom_image,self.reset_buttom_rect)
        text = font.render("Reiniciar",True, (5,5,5),(0,0,0))
        text.set_colorkey((0,0,0), RLEACCEL)
        text_rect = text.get_rect()
        text_rect.centerx = 125
        text_rect.centery = 200
        pygame.display.get_surface().blit(text,text_rect)
        
        self.forge_buttom_rect = buttom_image.get_rect()
        self.forge_buttom_rect.centerx = 125
        self.forge_buttom_rect.centery = 300
        pygame.display.get_surface().blit(buttom_image,self.forge_buttom_rect)
        text = font.render("Forjar!!",True, (5,5,5),(0,0,0))
        text.set_colorkey((0,0,0), RLEACCEL)
        text_rect = text.get_rect()
        text_rect.centerx = 125
        text_rect.centery = 300
        pygame.display.get_surface().blit(text,text_rect)
        
        self.TX.display_editor(pygame_events, pressed_keys, mouse_x, mouse_y, mouse_pressed)
        if self.first_time:
            self.TX.set_text_from_string(self.quest.code)
            self.first_time= False
        # update pygame window 
        pygame.display.flip()

    def OnClick(self,mouse_pos):
        if self.main_screen_buttom_rect != None and self.main_screen_buttom_rect.collidepoint(mouse_pos):
            # save the code and go back to main_screen
            self.error_list = self.quest.error_list
            self.quest.code = self.TX.get_text_as_string()
            quest_save:Quests_save = Quests_save.read_save()
            quest_save.quests[self.quest.id] = self.quest
            quest_save.write_save()
            return "main_screen" , False
        elif self.forge_buttom_rect != None and self.forge_buttom_rect.collidepoint(mouse_pos):
            # paint the loading image, check the code for sintaxis error, if none, pass the code onto the quest
            # to check if it finds every zero in the especified time.
            self.error_list = []
            self.quest.code = self.TX.get_text_as_string()
            
            load_path = os.path.join(resources_path,"load.png")
            load_image = pygame.image.load(load_path).convert()
            load_image.set_colorkey((0,0,0),RLEACCEL) 
            load_rect = load_image.get_rect()
            pygame.display.get_surface().blit(load_image,load_rect)
            pygame.display.flip()
            
            _, had_error, error_list = F0F.compile(self.quest.code,None)
            # remove had error and let the quest manage everything. There, len(error_list) > 0 return "", True
            if had_error:
                self.error_list = error_list
                return "",True
            else:
                self.quest.check_completeness()
                self.error_list = self.quest.error_list
                quest_save:Quests_save = Quests_save.read_save()
                quest_save.quests[self.quest.id] = self.quest
                quest_save.write_save()
                return "forge",False
        elif self.reset_buttom_rect != None and self.reset_buttom_rect.collidepoint(mouse_pos):
            self.error_list = [] # self.quest.error_list
            self.TX.set_text_from_string(intial_code())
        return "", True
        
        
class Tutorial():
    def __init__(self,display:pygame.Surface):
        self.display = display
        self.font = pygame.font.SysFont("Arial",26)
        self.step_1()
    
    def step_1(self):
        
        background_path = os.path.join(resources_path,"tutorial_screen.jpg")
        background = pygame.image.load(background_path).convert()
        self.display.blit(background,(0,0))
        
        msg_path = os.path.join(resources_path,"msg.png")
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
        time.sleep(1)
        cont = True 
        while(cont):
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                        cont = False
                        
        self.step_2(background,msg_view)
        
    def step_2(self,background, msg_view):        
        self.display.blit(background,(0,0))
        self.display.blit(msg_view,(0,0))
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
        time.sleep(1)
        cont = True 
        while(cont):
           for event in pygame.event.get():
               if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                        cont = False
                        
        self.step_3()
        
    def step_3(self):
        background = Main_screen(0,0,True)
        background.Paint()
        katrine_msg_path = os.path.join(character_path, "katrine_msg.png")
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
        time.sleep(1)
        cont = True
        while(cont):
          for event in pygame.event.get():
               if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                        cont = False
        
        self.step_4(background,katrine_msg_view)
        
    def step_4(self,background,katrine_msg_view):        
        background.Paint()
        self.display.blit(katrine_msg_view,(0,0))
        image = self.font.render("Katrine:Te gustaría que te explique las reglas del jue..digo, negocio?",True, (5,5,5),(0,0,0))
        image.set_colorkey((0,0,0),RLEACCEL)
        text_rect = image.get_rect()
        text_rect.centerx = 630
        text_rect.centery = 630
        self.display.blit(image,text_rect)
        pygame.display.flip()
        time.sleep(1)
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
        time.sleep(1)
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
                            self.step_11()
    
    def step_5(self,background,katrine_msg_view):        
        background.Paint()
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
        time.sleep(1)
        cont = True
        while(cont):
          for event in pygame.event.get():
               if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                        cont = False
        self.step_6()
        
    def step_6(self):        
        background = Main_screen(1,0,True)
        background.Paint()
        msg_path = os.path.join(resources_path,"msg.png")
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
        time.sleep(1)
        cont = True
        while(cont):
          for event in pygame.event.get():
               if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                         if background.quest_rect.collidepoint(pygame.mouse.get_pos()):
                             cont=False
                             self.step_7()
        
    def step_7(self):        
        background = Main_screen(1,0,True)
        background.Paint()
        screen = Quest_screen(0)
        butt, quest = screen.wait()
        if butt == "main_screen":
            self.step_6()
        else:
            self.step_8(quest)
    
    def step_8(self, quest):        
        forge = Forge_screen(quest) 
        butt , quest = forge.wait()
        if butt == "main_screen":
            pygame.display.get_surface().fill((0,0,0))
            self.step_6()
        if butt == "forge":
            self.step_9(quest)
    
    def step_9(self,quest:Quest):        
        checker = quest.Quest_complete()
        if checker:
            self.step_10()
        else:
            pygame.display.get_surface().fill((0,0,0))
            background = Main_screen(0,0,True)
            background.Paint()
            katrine_msg_path = os.path.join(character_path,"katrine_msg.png")
            katrine_msg_view = pygame.image.load(katrine_msg_path).convert()
            katrine_msg_view.set_colorkey((0,0,0),RLEACCEL)
            self.display.blit(katrine_msg_view,(0,0))
            
            image = self.font.render("Katrine: Es una pena pero no lo has conseguido, vuelve a intentarlo",True, (5,5,5),(0,0,0))
            image.set_colorkey((0,0,0),RLEACCEL)
            text_rect = image.get_rect()
            text_rect.centerx = 630
            text_rect.centery = 630
            self.display.blit(image,text_rect)
            pygame.display.flip()
            time.sleep(1)
            cont = True
            while(cont):
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed(3)[0] == True:
                                cont=False
            self.step_6()  
                  
    def step_10(self):        
        pygame.display.get_surface().fill((0,0,0))
        background = Main_screen(0,0,True)
        background.Paint()
        katrine_msg_path = os.path.join(character_path,"katrine_msg.png")
        katrine_msg_view = pygame.image.load(katrine_msg_path).convert()
        katrine_msg_view.set_colorkey((0,0,0),RLEACCEL)
        self.display.blit(katrine_msg_view,(0,0))
        
        image = self.font.render("Katrine: Un excelente trabajo! Ya estás listo para seguir por ti mismo",True, (5,5,5),(0,0,0))
        image.set_colorkey((0,0,0),RLEACCEL)
        text_rect = image.get_rect()
        text_rect.centerx = 630
        text_rect.centery = 630
        self.display.blit(image,text_rect)
        pygame.display.flip()
        time.sleep(1)
        cont = True
        while(cont):
          for event in pygame.event.get():
               if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                        cont = False
        self.completed = True       
    
    def step_11(self):        
        pygame.display.get_surface().fill((0,0,0))
        background = Main_screen(0,0)
        background.Paint()
        katrine_msg_path = os.path.join(character_path,"katrine_msg.png")
        katrine_msg_view = pygame.image.load(katrine_msg_path).convert()
        katrine_msg_view.set_colorkey((0,0,0),RLEACCEL)
        self.display.blit(katrine_msg_view,(0,0))
        
        image = self.font.render("Katrine: Ja , Ja el ímpetu de la juventud ...",True, (5,5,5),(0,0,0))
        image.set_colorkey((0,0,0),RLEACCEL)
        text_rect = image.get_rect()
        text_rect.centerx = 630
        text_rect.centery = 630
        self.display.blit(image,text_rect)
        pygame.display.flip()
        time.sleep(1)
        image = self.font.render("Bueno, saldré de tu camino. Buena suerte joven",True, (5,5,5),(0,0,0))
        image.set_colorkey((0,0,0),RLEACCEL)
        text_rect = image.get_rect()
        text_rect.centerx = 630
        text_rect.centery = 650
        self.display.blit(image,text_rect)
        pygame.display.flip()
        cont = True
        while(cont):
          for event in pygame.event.get():
               if event.type == MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed(3)[0]== True:
                        cont = False
                        
        self.completed = True      
        
        
class Monster():
    def __init__(self):
        self.fun_det = FunctDetails(None,None)
        self.fun:MFUN = self.fun_det.get_funct()
        
    def check_zero(self,point):
        try:
            point = tuple(point)
        except:
            point = tuple([point])
        return FunctDetails.check_zero(self.fun, point)
    
    def graph(self,point,name) -> str:
        return FunctDetails.graph(self.fun, point,name)

class Python(Monster):    
    def __init__(self):
        self.fun_det = FunctDetails([Functions.snk1,Functions.snk2],[0.5,0.5])
        self.fun:MFUN = self.fun_det.get_funct()  
        
class Goblin(Monster): 
    def __init__(self):
        self.fun_det = FunctDetails([Functions.pol1,Functions.pol2,Functions.pol4,Functions.pol5,Functions.pol6],
                                    None)
        self.fun:MFUN = self.fun_det.get_funct()                              

class Orc(Monster):
    def __init__(self):
        self.fun_det = FunctDetails([Functions.pol3,Functions.pol7,Functions.pol8],
                                    None)
        self.fun:MFUN = self.fun_det.get_funct()   

class Golem(Monster):
    def __init__(self):
        self.fun_det = FunctDetails([Functions.trig2,Functions.trig4,Functions.trig6,Functions.trig9],
                                    None)
        self.fun:MFUN = self.fun_det.get_funct() 

class Zombie(Monster):
    def __init__(self):
        self.fun_det = FunctDetails([Functions.trig1,Functions.trig3,Functions.trig5,Functions.trig8], #Functions.trig7,
                                    None)
        self.fun:MFUN = self.fun_det.get_funct() 

class Cyclop(Monster):
    def __init__(self):
        self.fun_det = FunctDetails([Functions.exp2,Functions.exp3,Functions.exp4,Functions.exp6],
                                    None)
        self.fun:MFUN = self.fun_det.get_funct() 

class Minotaur(Monster):
    def __init__(self):
        self.fun_det = FunctDetails([Functions.exp1,Functions.exp5,Functions.exp7,Functions.exp8],
                                    None)
        self.fun:MFUN = self.fun_det.get_funct()   

class Griffin(Monster):
    def __init__(self):
        self.fun_det = FunctDetails([Functions.trex1,Functions.trex2,Functions.trex3,Functions.trex4],
                                    None)
        self.fun:MFUN = self.fun_det.get_funct() 
           
class Basilisk(Monster):
    def __init__(self):
        self.fun_det = FunctDetails([Functions.log1,Functions.log2,Functions.log3],
                                    None)
        self.fun:MFUN = self.fun_det.get_funct() 
           
class Chimera(Monster):
    def __init__(self):
        self.fun_det = FunctDetails([Functions.inv1,Functions.inv2,Functions.inv3],None)
        self.fun:MFUN = self.fun_det.get_funct() 
         
class Hydra(Monster):
    def __init__(self):
        self.fun_det = FunctDetails([Functions.other1,Functions.other2,Functions.other3,Functions.other4], #,Functions.other5
                                    None)
        self.fun:MFUN = self.fun_det.get_funct() 
        
