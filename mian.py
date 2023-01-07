import pygame
import logic
import pickle
from pygame.locals import (QUIT,KEYDOWN,RLEACCEL,K_ESCAPE,K_UP,K_DOWN,K_LALT,K_t,MOUSEBUTTONDOWN)
from pygame_texteditor import TextEditor

pygame.init()
tempsave = logic.Save()
tempsave.write_save()
save:logic.Save = logic.Save.read_save()
# quest0 = logic.Quest(0,"katrine","A test","Katrine te ha dado un quest de prueba para que compruebes si el sistema funciona","a_monster_list", 69, 0,logic.intial_code())
# quest1 = logic.Quest(1,"katrine","Another test1","Ahora unos cuantos quest para comprobar la pantalla del quest", "a_monster_list", 1, 1,logic.intial_code())
# quest2 = logic.Quest(2,"katrine","Another test2","Ahora unos cuantos quest para comprobar la pantalla del quest", "a_monster_list", 1, 1,logic.intial_code())
# quest3 = logic.Quest(3,"katrine","Another test3","Ahora unos cuantos quest para comprobar la pantalla del quest", "a_monster_list", 1, 1,logic.intial_code())
# quest4 = logic.Quest(4,"katrine","Another test1","Ahora unos cuantos quest para comprobar la pantalla del quest", "a_monster_list", 1, 2,logic.intial_code())
# quest5 = logic.Quest(5,"katrine","Another test2","Ahora unos cuantos quest para comprobar la pantalla del quest", "a_monster_list", 1, 2,logic.intial_code())
# quest6 = logic.Quest(6,"katrine","Another test3","Ahora unos cuantos quest para comprobar la pantalla del quest", "a_monster_list", 1, 2,logic.intial_code())
# quests = {0: quest0,1:quest1,2:quest2,3:quest3,4:quest4,5:quest5,6:quest6}
# file = open("quests.bin","wb")
# pickle.dump(quests,file) 
# file.close()

info = pygame.display.Info()
display = pygame.display.set_mode((info.current_w,info.current_h))
screen = logic.Main_screen(save.forge_level)
clock = pygame.time.Clock()
running = True
next = "main_screen"
while running:
    if save.forge_level == 0:
        tutorial_completed = logic.Tutorial(display)
        if tutorial_completed:
            save.forge_level+=1
            save.write_save()
            screen = logic.Main_screen(save.forge_level)
    pygame.display.get_surface().fill((0,0,0))
            
    next , needed = screen.wait()
    save.write_save()
    if next == "main_screen":
        screen = logic.Main_screen(save.forge_level)
    elif next == "quest_screen":
        screen = logic.Quest_screen(save.forge_level)
    elif next == "forge_screen":
        screen = logic.Forge_screen(needed)
    elif next == "forge":
        screen = logic.Main_screen(save.forge_level)
    elif next == "quit":
        running = False
        
        
    
    # for event in pygame.event.get():
    #     if event.type == QUIT:
    #         running = False
    #     if event.type == KEYDOWN:
    #         if event.key == K_ESCAPE:
    #             running = False
    #         if event.key == K_UP and save.forge_level<4:
    #             save.forge_level+=1
    #             screen = logic.Main_screen(save.forge_level)
    #             display.blit(screen.Paint(),(0,0))
    #         if event.key == K_DOWN and save.forge_level > 0:
    #             save.forge_level-=1
    #             screen = logic.Main_screen(save.forge_level)
    #             display.blit(screen.Paint(),(0,0))
    #     # if event.type == MOUSEBUTTONDOWN:
    #     #     if pygame.mouse.get_pressed(3)[0]== True:
    #     #         print (pygame.mouse.get_pos())
                  
    save.write_save()
    # #screen = logic.Main_screen(save.forge_level)
    # display.blit(screen.Paint(),(0,0))
    # pygame.display.flip()
    clock.tick(40)
#file = open("quests.bin","wb")
#pickle.dump(quests,file) 
#file.close()             
save.write_save()                
pygame.quit()    