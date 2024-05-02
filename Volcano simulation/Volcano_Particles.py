import sys
import math
import random
import pygame as pg

pg.init()  # Initialize pygame
    
# Define color table
BLACK = (0, 0, 0)
LT_GRAY = (180, 180, 180)
GRAY = (120, 120, 120)
DK_GRAY = (80, 80, 80)

class Particle(pg.sprite.Sprite):
    """Builds ejecta particles for volcano simulation."""

    gases_colors = {'SO2': LT_GRAY, 'CO2': GRAY, 'H2S': DK_GRAY}
    
    VENT_LOCATION_XY = (320, 300)  # Mouth of volcano
    IO_SURFACE_Y = 310  # Y location of Io surface
    GRAVITY = 0.5  # Pixels per frame   
    VELOCITY_SO2 = 8  # pixels-per-frame
    
    # Scalars (SO2 atomic weight/particle atomic weight) used for velocity
    vel_scalar = {'SO2': 1, 'CO2': 1.45, 'H2S': 1.9}   
      
    def __init__(self, screen, background):
        super().__init__()
        self.screen = screen
        self.background = background
        self.image = pg.Surface((4, 4))
        self.rect = self.image.get_rect()
        self.gas = random.choice(list(Particle.gases_colors.keys()))
        self.color = Particle.gases_colors[self.gas]
        self.vel = Particle.VELOCITY_SO2 * Particle.vel_scalar[self.gas]      
        self.x, self.y = Particle.VENT_LOCATION_XY
        self.vector()

    def vector(self):
        """Calculate particle vector at launch."""
        orient = random.uniform(60, 120)  # 90 is vertical
        radians = math.radians(orient)
        self.dx = self.vel * math.cos(radians)
        self.dy = -self.vel * math.sin(radians)  # Negative as y increases down
        
    def update(self):
        """Apply gravity, draw path, and handle boundary conditions."""
        self.dy += Particle.GRAVITY
        pg.draw.circle(self.background, self.color, (int(self.x), self.y), 1)
        screen.blit(background, (0, 0))
        
        self.x += self.dx
        self.y += self.dy
        screen.blit(background, (0, 0))
        
        if self.x < 0 or self.x > self.screen.get_width():
            self.kill()
        if self.y < 0 or self.y > Particle.IO_SURFACE_Y:
            self.kill()

def main():
    """Set-up and run game screen and loop."""
    screen = pg.display.set_mode((639, 360))
    pg.display.set_caption('IO Volcano Simulator')
    background = pg.image.load('tvashtar_plume.gif')

    # Set-up color-coded legenf
    legend_font = pg.font.SysFont('None', 24)
    co2_label = legend_font.render('--- CO2', True, GRAY, BLACK)
    so2_label = legend_font.render('--- SO2/S2', True, LT_GRAY, BLACK)
    h2s_label = legend_font.render('--- H2S', True, DK_GRAY, BLACK)

    particles = pg.sprite.Group()
    
    clock = pg.time.Clock()

    while True:
        clock.tick(20)
        particles.add(Particle(screen, background))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        screen.blit(background, (0, 0))
        screen.blit(h2s_label, (40, 40))
        screen.blit(co2_label, (40, 60))
        screen.blit(so2_label, (40, 80))
        
        particles.update()
        particles.draw(screen)

        pg.display.flip()

if __name__ == "__main__":
    main()
