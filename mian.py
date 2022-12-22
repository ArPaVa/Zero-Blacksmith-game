import pygame
import logic
import pickle
from pygame.locals import (QUIT,KEYDOWN,RLEACCEL,K_ESCAPE,K_UP,K_DOWN,K_LALT,K_t,MOUSEBUTTONDOWN)

pygame.init()
# tempsave = logic.Save()
# tempsave.write_save()
save:logic.Save = logic.Save.read_save()


info = pygame.display.Info()
display = pygame.display.set_mode((info.current_w,info.current_h))
screen = logic.Main_screen(save.forge_level)
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_UP and save.forge_level<4:
                save.forge_level+=1
                screen = logic.Main_screen(save.forge_level)
                display.blit(screen.Paint(),(0,0))
            if event.key == K_DOWN and save.forge_level > 0:
                save.forge_level-=1
                screen = logic.Main_screen(save.forge_level)
                display.blit(screen.Paint(),(0,0))
            if event.key == K_t:
                tutorial = logic.Tutorial(display)
        # if event.type == MOUSEBUTTONDOWN:
        #     if pygame.mouse.get_pressed(3)[0]== True:
        #         print (pygame.mouse.get_pos())
                
            
    save.write_save()
    #screen = logic.Main_screen(save.forge_level)
    #display.blit(screen.Paint(),(0,0))
    pygame.display.flip()
    clock.tick(40)
    
                
                
pygame.quit()    