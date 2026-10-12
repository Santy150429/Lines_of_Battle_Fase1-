
import math
import pygame

pygame.init()
pantalla = pygame.display.set_mode((1000, 600))

class Unidad:
    def __init__(self, x, y, ancho, alto, color, bando):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.color = color
        self.bando = bando
        self.ataque = 0.3
        self.velocidad = 2
        self.seleccionada = False
        self.destino = None
        self.vida = 100
        self.vida_maxima = 100
        self.alcance = 150
        self.ataque = 0.3

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, (self.x, self.y, self.ancho, self.alto))
        if self.seleccionada:
            pygame.draw.rect(pantalla, (255, 255, 0), (self.x, self.y, self.ancho, self.alto), 3)
        if self.destino is not None:
            pygame.draw.circle(pantalla, (255, 0, 0), self.destino, 5)

        ancho_vida = int(self.ancho * self.vida / self.vida_maxima)
        pygame.draw.rect(pantalla, (120, 0, 0), (self.x, self.y - 10, self.ancho, 5))
        pygame.draw.rect(pantalla, (0, 200, 0), (self.x, self.y - 10, ancho_vida, 5))

    def mover(self):
        if self.destino is None:
            return

        dx = self.destino[0] - self.x
        dy = self.destino[1] - self.y

        if abs(dx) <= self.velocidad:
            self.x = self.destino[0]
        elif dx > 0:
            self.x += self.velocidad
        else:
            self.x -= self.velocidad

        if abs(dy) <= self.velocidad:
            self.y = self.destino[1]
        elif dy > 0:
            self.y += self.velocidad
        else:
            self.y -= self.velocidad

        if self.x == self.destino[0] and self.y == self.destino[1]:
            self.destino = None

    def contiene(self, punto):
        rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        return rect.collidepoint(punto)

    def a_alcance(self, otra):
        dx = otra.x - self.x
        dy = otra.y - self.y
        return math.hypot(dx, dy) <= self.alcance

azul = Unidad(100, 250, 80, 40, (40, 80, 200), "azul")
rojo = Unidad(800, 250, 80, 40, (200, 50, 50), "rojo")
unidades = [azul, rojo]

fase = "ordenes"
DURACION_RESOLUCION = 180
contador = 0

fuente = pygame.font.Font(None, 36)

reloj = pygame.time.Clock()
corriendo = True
while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for unidad in unidades:
                    unidad.seleccionada = unidad.contiene(event.pos)
            if event.button == 3:
                for unidad in unidades:
                    if unidad.seleccionada:
                        unidad.destino = event.pos
            if event.button == 3:
                 for unidad in unidades:
                     if unidad.seleccionada:
                         unidad.destino = event.pos
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if fase == "ordenes":
                fase = "resolucion"
                contador = 0
            else:
                fase = "ordenes"

    if fase == "resolucion":
        for unidad in unidades:
            unidad.mover()
        for atacante in unidades:
            for objetivo in unidades:
                if atacante.bando != objetivo.bando and atacante.a_alcance(objetivo):
                    objetivo.vida = max (0, objetivo.vida - atacante.ataque)
        contador += 1
        if contador >= DURACION_RESOLUCION:
            fase = "ordenes"
            contador = 0

    pantalla.fill((80, 150, 80))
    for unidad in unidades:
        unidad.dibujar(pantalla)
    texto = fuente.render("Fase: " + fase, True, (255, 255, 255))
    pantalla.blit(texto, (20, 20))
    pygame.display.update()

    reloj.tick(60)

pygame.quit()