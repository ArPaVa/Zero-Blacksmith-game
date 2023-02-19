import pygame
import logic
import sys
from pygame.locals import (QUIT,KEYDOWN,RLEACCEL,K_ESCAPE,K_UP,K_DOWN,K_LALT,K_t,MOUSEBUTTONDOWN)
from pygame_texteditor import TextEditor

def recreate_quests():
    # el reward de cada quest si tendra q definirlo el profespr
    quest0 = logic.Quest(0,"katrine","The tutorial isn't that hard","Bueno joven, esa pitón no debería ser un oponente demasiado difícil, cualquier arma me servirá.",[logic.Python()], 69, 0,logic.intial_code(),8)
    # 0.4606/0.3501/0.4541/0.117/0.6282 sec.   
    quest1 = logic.Quest(1,"katrine","Yo solía ser un aventurero","Yo solía ir de aventuras con tu abuelo, pero un día una     rodilla golpeo mi flecha y me tuve que retirar. Quizás si me haces un buen arma pueda enfrentar a algunos goblins.       Objetivo: Derrotar 3 goblins.", [logic.Goblin(),logic.Goblin(),logic.Goblin()], 150, 1,logic.intial_code(),8)
    # 1.5694/2.1125/1.5045/0.3301/1.5534 sec.
    quest2 = logic.Quest(2,"katerina","GPOP","Encantada de conocerte, mi nombre es Katerina, soy la nieta de Katrine, me pidió que te recordara que al cumplir todas  las misiones de un rango pasarás automáticamente al         siguiente.                                                  Nadie se puede enterar pero necesito tu ayuda, los secuaces de mi novio no me dejarán verlo a no ser que los derrote, su nombre es Kimbling Parkbling. Y es taaaan bonito o3o.            Objetivo: Derrotar 6 goblins.", [logic.Goblin(),logic.Goblin(),logic.Goblin(),logic.Goblin(),logic.Goblin(),logic.Goblin()], 300, 1,logic.intial_code(),8)
    # 3.2648/3.0733/3.0748/0.7097/2.5287 sec
    quest3 = logic.Quest(3,"katrine","La culpa, la maldita culpa","Buenas joven, necesito tu ayuda, los nuevos  amigos de mi ni-eta son muy maleducados. Tendré que enseñarles una lección.   Objetivo: Derrotar 2 goblins y 2 orcos.", [logic.Goblin(),logic.Orc(),logic.Goblin(),logic.Orc()], 400, 2,logic.intial_code(),8)#2qr
    # 2.0095/1.9515/2.0835/2.0007 sec
    quest4 = logic.Quest(4,"arthur","Una misión más normal","O noble artesano, solicito tu ayuda pues debo embarcarme en una aventura de grandes proporciones para recuperar aquello que ha de ser mío, la excalibur , por favor forjame un arma capaz de superar tales pruebas.                             Objetivo: Derrotar 6 goblins y 3 orcos.", [logic.Goblin(),logic.Goblin(),logic.Goblin(),logic.Orc(),logic.Goblin(),logic.Goblin(),logic.Goblin(),logic.Orc(),logic.Orc()], 750, 2,logic.intial_code(),8)#2qr
    # 4.4847/4.4691/5.8434/4.0505 sec
    quest5 = logic.Quest(5,"katerina","Las espinas de una rosa","Bah, soy demasiado cool para hablar contigo, solo fórjame una mejor arma.     Objetivo: Derrotar 1 golem.", [logic.Golem()], 1000, 2,logic.intial_code(),3)#2
    # 0.6462/0.113/0.6882 sec.
    quest6 = logic.Quest(6,"lucy","El pueblo está infestado","Buenas, mi nombre es Lucy. Mi hermano, el pequeño Prince,   ha sido convertido en zombie por sus amigos.                Necesito tu ayuda con un arma que me permita ir a salvarlo.    Él siempre queda atrapado en la marea TTwTT.             Objetivo: Derrotar 7 zombies.", [logic.Zombie(),logic.Zombie(),logic.Zombie(),logic.Zombie(),logic.Zombie(),logic.Zombie(),logic.Zombie()], 2100, 2,logic.intial_code(),8) #3qr
    # 1.0523/3.4584 sec.
    quest7 = logic.Quest(7,"arthur","La fuente de infinito saber","Yo, el gran Arthur he regresado de mi contienda. Gracias a  ti he logrado recuperar mi gran bolígrafo 'Excalibur'.           Ahora requiero tus servicios para una intentar una      incursión al Códice Divino.                                 Objetivo: Derrotar 1 golem, 3 cíclopes y 3 minotauros.", [logic.Golem(),logic.Cyclop(),logic.Cyclop(),logic.Cyclop(),logic.Minotaur(),logic.Minotaur(),logic.Minotaur()], 2888, 3,logic.intial_code(),8) #3qr
    # 3.885/2.8927/0.6932/3.6649  sec.
    quest8 = logic.Quest(8,"prince","Mis pobres ovejas","Hola, soy Prince. Desde que mi hermana atacó a mis amigos me he dedicado a cuidar los animales de la granja.            Pero las ovejas están siendo atacadas en la noche.                       ¿Me podrías ayudar a protegerlas?                  Objetivo: Derrotar 2 goblins, 2 orcos, 2 zombies y      1 golem.", [logic.Goblin(),logic.Goblin(),logic.Orc(),logic.Orc(),logic.Zombie(),logic.Zombie(),logic.Golem()], 1800, 3,logic.intial_code(),8) #3
    # 3.9785/3.5914/3.4974 sec.
    quest9 = logic.Quest(9,"katrine","¡Cuidado con las maldiciones!","Tu abuelo decía que a veces ocurrían cosas impredecibles con sus productos.  ¿Te ha pasado algo así?                    Espero que no caigas presa de las maldiciones imperdonables.      Por cierto, el jefe de la guardia necesita mejorar las            armas de varios miembros. Te lo encargo.              Objetivo: Derrotar 2 orcos, 3 golems y 1 grifo.", [logic.Orc(),logic.Orc(),logic.Golem(),logic.Golem(),logic.Golem(),logic.Griffin()], 3400, 3,logic.intial_code(),8) #3qr
    # 2.9202/3.1108/3.0543 sec
    quest10 = logic.Quest(10,"lucy","Fuera de lugar","Muchas gracias por lo de la otra vez, mi hermano ya no pasa                el día jugando con sus amiguitos.                    Como debes saber, los cíclopes no suelen salir de la montaña, pero he visto algunos rondando el pueblo.          ¿Serías tan amable de hacerme un arma que pueda acabar con esas bestias?                                                Objetivo: Derrotar 4 cíclopes y 1 minotauro.", [logic.Cyclop(),logic.Cyclop(),logic.Cyclop(),logic.Cyclop(),logic.Minotaur()], 1900, 3,logic.intial_code(),8) #3
    # 2.5907/2.5026 sec
    quest11 = logic.Quest(11,"katerina","Entrenamiento en la cascada","Mi abuelo me envió a entrenar mi espíritu en la cascada;pero parece que unos grifos han hecho un nido cerca.Necesito un arma que pueda derribar a criaturas voladoras tan fuertes.          Objetivo: Derrotar 4 grifos.", [logic.Griffin(),logic.Griffin(),logic.Griffin(),logic.Griffin()], 4200, 3,logic.intial_code(),8)
    # 1.9135/1.9705 sec
    quest12 = logic.Quest(12,"katrine","100 años más joven","Tener tanta acción recientemente me ha rejuvenecido.        Ya he descubierto porqué había pitones rondando.            Ha aparecido un Basilisco, el rey de las serpientes.                              ¿Tú sabes parseltonge?                    Bueno, como sea, necesito un arma que penetre su gruesa piel.                   Objetivo: Derrotar 1 basilisco.", [logic.Basilisk()], 2000, 4,logic.intial_code(),8)
    # 0.6001/0.4701/0.5031/0.5251 sec
    quest13 = logic.Quest(13,"prince","Amor letal","No le cuentes a mi hermana, pero he encontrado el amor. Sin embargo ella está atrapada por peligrosas quimeras. Necesito rescatarla, con sus 4 espinas no podrá defenderse.         Por favor, ayudame a salvar a mi rosa.                                      Objetivo: Derrotar 5 quimeras.", [logic.Chimera(),logic.Chimera(),logic.Chimera(),logic.Chimera(),logic.Chimera()], 11111, 4,logic.intial_code(),8)
    # 2.6695/2.5376/2.4786 sec
    quest14 = logic.Quest(14,"arthur","Retirada estratégica","       ¿Sabes qué es lo más importante en el mundo?         Planeo averiguarlo en el Códice Divino cuando logre         conquistarlo. Yo no fui derrotado, es solo que .....        había demasiados enemigos. Por ahora voy a reponer fuerzas y hacer tareas menores. ¡Ah!, lo siento por romper el arma,  necesito otra para defenderme.                               Objetivo: Derrotar 5 zombies y 4 minotauros.", [logic.Zombie(),logic.Zombie(),logic.Zombie(),logic.Zombie(),logic.Zombie(),logic.Minotaur(),logic.Minotaur(),logic.Minotaur(),logic.Minotaur()], 8500, 4, logic.intial_code(),8)
    # 3.4889/4.3826/4.3666 sec
    quest15 = logic.Quest(15,"lucy","Al rescate, otra vez","El viejo Katrine olvidó que hay más de un basilisco -_-' .  Katerina y yo iremos a rescatarlo. Pero necesitaremos       equipamiento que nos ayude con todo eso de la petrificación.                  Lo dejo en tus manos.                       Objetivo: Derrotar 3 basiliscos.", [logic.Basilisk(),logic.Basilisk(),logic.Basilisk()], 6666, 4, logic.intial_code(),8)
    # 4.004/1.4934/1.6194 sec
    quest16 = logic.Quest(16,"arthur","La batalla por el conocimiento","He reclutado a tus clientes habituales para librar la       contienda por la bibliotec..., digo, el Gran Códice. Menos  al pequeño Prince, que dice que está ocupado domesticando una zorra invisible, o algo similar. Noble artesano, espero solo lo mejor de ti, armas que puedan vencer a las hidras del códice, míticas por su regeneración.                           Objetivo: Derrotar 5 Hidras.", [logic.Hydra(),logic.Hydra(),logic.Hydra(),logic.Hydra(),logic.Hydra()], 99999, 4,logic.intial_code(),5)
    # 2.6137 sec
        
    quests = {0: quest0,1:quest1,2:quest2,3:quest3,4:quest4,5:quest5,6:quest6,7:quest7,8:quest8,9:quest9,10:quest10,11:quest11,14:quest14,12:quest12,13:quest13,15:quest15,16:quest16}  
    quests_save = logic.Quests_save(quests)
    quests_save.write_save()
    
def restart_progress():
    tempsave = logic.Save()
    tempsave.write_save()

def cash_quests():
    quest_save:logic.Quests_save = logic.Quests_save.read_save()
    q = quest_save.quests
    change = False
    for id in q:
        if q[id].completed and not q[id].cashed:
            save.reward += (q[id].reward - q[id].sins)
            q[id].cashed = True
            change = True
    if change:
        quest_save.write_save()
        save.write_save()
               
def RunGame():
    save:logic.Save = logic.Save.read_save()
                
    pygame.init()                                                                                                                       
    info = pygame.display.Info()
    display = pygame.display.set_mode((info.current_w,info.current_h))
    clock = pygame.time.Clock()

    screen = logic.Main_screen(save.forge_level,save.reward)
    running = True
    next = "main_screen"
    while running:
        if save.forge_level == 0:
            tutorial_completed = logic.Tutorial(display)
            if tutorial_completed.completed:
                cash_quests()
                save.forge_level+=1
                save.write_save()
                screen = logic.Main_screen(save.forge_level,save.reward)
        
        pygame.display.get_surface().fill((0,0,0))
                
        next , needed = screen.wait()
        save.write_save()
        if next == "main_screen":
            screen = logic.Main_screen(save.forge_level,save.reward)
        elif next == "quest_screen":
            screen = logic.Quest_screen(save.forge_level)
        elif next == "forge_screen":
            screen = logic.Forge_screen(needed)
        elif next == "forge":
            cash_quests()
            pygame.display.get_surface().fill((0,0,0))
            if logic.pass_level(save.forge_level):
                save.forge_level+=1
                save.write_save()
                logic.level_up(save.forge_level)
                wait_clk = True
                while wait_clk:
                    pygame_events = pygame.event.get()
                    for event in pygame_events:
                        if event.type == MOUSEBUTTONDOWN:
                            if pygame.mouse.get_pressed(3)[0]== True:
                                wait_clk = False
                                break        
                if save.forge_level > 4:
                    running = False
                    continue
            screen = logic.Main_screen(save.forge_level,save.reward)
        elif next == "quit":
            running = False

        clock.tick(40)
                
    save.write_save()                
    pygame.quit()    
    

if __name__ == "__main__":
    if sys.argv != None and len(sys.argv) > 1 and sys.argv[1] == 'True':    
        print('restarting')
        restart_progress()
        recreate_quests()   
    try:
        logic.Save.read_save()
        logic.Quests_save.read_save()
    except:
        restart_progress()
        recreate_quests() 
    save:logic.Save = logic.Save.read_save() 
    if save.forge_level < 0 or save.forge_level > 4 :
        print("You are trying to continue the game after finishing it, or corrupted a file.")   
    else:
        RunGame()