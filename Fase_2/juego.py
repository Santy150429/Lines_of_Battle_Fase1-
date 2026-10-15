
import os
import pygame
from unidad import Unidad

def crear_ejercitos(bando, x, color, cantidad, direccion):
    ejercito = []
    for i in range(cantidad):
        fila = i % 5
        columna = i // 5
        ejercito.append(Unidad(x + columna * 100 * direccion, 80 + fila * 90, 80, 40, color, bando))
    return ejercito

pygame.init()
pantalla = pygame.display.set_mode((1000, 600))

unidades = crear_ejercitos("azul", 100, (40, 80, 200), 10, 1) + crear_ejercitos("rojo", 800, (200, 50, 50), 10, -1)

carpeta = os.path.dirname(os.path.abspath(__file__))
fondo = pygame.image.load(os.path.join(carpeta, "Mapas", "mapa1.jpg"))
fondo = pygame.transform.scale(fondo, (1000, 600))

fase = "ordenes"
DURACION_RESOLUCION = 180
contador = 0
ganador = ""

fuente = pygame.font.Font(None, 36)
fuente_grande = pygame.font.Font(None, 80)

reloj = pygame.time.Clock()
corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        if event.type == pygame.MOUSEBUTTONDOWN and fase == "ordenes":
            if event.button == 1:
                for unidad in unidades:
                    unidad.seleccionada = unidad.contiene(event.pos)
            if event.button == 3:
                for unidad in unidades:
                    if unidad.seleccionada:
                        unidad.destino = event.pos
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if fase == "ordenes":
                fase = "resolucion"
                contador = 0

    if fase == "resolucion":
        for unidad in unidades:
            unidad.mover()
        for atacante in unidades:
            for objetivo in unidades:
                if atacante.bando != objetivo.bando and atacante.a_alcance(objetivo):
                    objetivo.vida = max(0, objetivo.vida - atacante.ataque)
        vivas = []
        for unidad in unidades:
            if unidad.vida > 0:
                vivas.append(unidad)
        unidades = vivas
        contador += 1
        if contador >= DURACION_RESOLUCION:
            fase = "ordenes"
            contador = 0
        azules = 0
        rojos = 0
        for unidad in unidades:
            if unidad.bando == "azul":
                azules += 1
            else:
                rojos += 1
        if azules == 0 or rojos == 0:
            fase = "fin"
            if azules == 0 and rojos == 0:
                ganador = "Empate"
            elif azules == 0:
                ganador = "Ganan los rojos"
            else:
                ganador = "Ganan los azules"

    pantalla.blit(fondo, (0, 0))
    for unidad in unidades:
        unidad.dibujar(pantalla)
    texto = fuente.render("Fase: " + fase, True, (255, 255, 255))
    pantalla.blit(texto, (20, 20))
    if fase == "fin":
        texto_fin = fuente_grande.render(ganador, True, (255, 255, 255))
        rect_fin = texto_fin.get_rect(center=(500, 300))
        pantalla.blit(texto_fin, rect_fin)
    pygame.display.update()

    reloj.tick(60)

pygame.quit()