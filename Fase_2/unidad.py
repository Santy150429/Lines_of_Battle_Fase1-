
import math
import pygame

class Unidad:
    def __init__(self, x, y, ancho, alto, color, bando):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.color = color
        self.bando = bando
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
        # barra de vida
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