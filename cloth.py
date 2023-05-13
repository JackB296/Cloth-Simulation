import pygame
import math
import sys

class Particle:
  def __init__(self, x, y, mass):
    self.x = x
    self.y = y
    self.prevx = x
    self.prevy = y
    self.mass = mass
    self.isPinned = False

class Stick:
    def __init__(self, p1, p2, length, maxLength):
        self.p1 = p1
        self.p2 = p2
        self.length = length

def getDistance(p1, p2): 
    """
    Get distance between two points using Eucladian Distance Formula
    """
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    return math.sqrt(dx * dx + dy * dy)


def getLength(v): 
    """
    Get length of a vector
    """
    return math.sqrt(v.x * v.x + v.y * v.y)


def getDifference(p1, p2):
    return pygame.math.Vector2(p1.x - p2.x,p1.y - p2.y)

def intersect(p1, p2, p3, p4):
    def orientation(p, q, r):
        # Calculate the orientation of three points (p, q, r)
        # Return 0 if they are colinear, 1 if clockwise, and 2 if counterclockwise
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # Colinear
        elif val > 0:
            return 1  # Clockwise
        else:
            return 2  # Counterclockwise

    def on_segment(p, q, r):
        # Check if point q lies on the line segment between p and r
        if (
            q[0] <= max(p[0], r[0])
            and q[0] >= min(p[0], r[0])
            and q[1] <= max(p[1], r[1])
            and q[1] >= min(p[1], r[1])
        ):
            return True
        return False

    # Get the orientations of the four points
    o1 = orientation(p1, p2, p3)
    o2 = orientation(p1, p2, p4)
    o3 = orientation(p3, p4, p1)
    o4 = orientation(p3, p4, p2)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special cases
    if (
        o1 == 0 and on_segment(p1, p3, p2)
        or o2 == 0 and on_segment(p1, p4, p2)
        or o3 == 0 and on_segment(p3, p1, p4)
        or o4 == 0 and on_segment(p3, p2, p4)
    ):
        return True

    return False

class Cloth:
    def __init__(self, clothWidth, clothHeight, clothSpacing, screen_height, screen_width):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clothSpacing = clothSpacing
        self.clothWidth = int(clothWidth / clothSpacing)
        self.clothHeight = int(clothHeight / clothSpacing)
        self.gravity = pygame.math.Vector2(0.0, 981.0)
        self.drag = 0.01
        self.elasticity = 3
        self.particles = []
        self.sticks = []
        self.deltaTime = 0.01
        self.lastUpdateTime = pygame.time.get_ticks()

    def setup(self):
        for i in range(self.clothWidth):
            for j in range(self.clothHeight):
                x = i * self.clothSpacing
                y = j * self.clothSpacing
                mass = 10000  # Adjust the mass as needed
                particle = Particle(x, y, mass)
                self.particles.append(particle)

                if i > 0:
                    prevParticle = self.particles[(i - 1) * self.clothHeight + j]
                    stick = Stick(particle, prevParticle, getDistance(particle, prevParticle), 50)
                    self.sticks.append(stick)

                if j > 0:
                    prevParticle = self.particles[i * self.clothHeight + (j - 1)]
                    stick = Stick(particle, prevParticle, getDistance(particle, prevParticle), 50)
                    self.sticks.append(stick)

                if j == 0 and i % 2 == 0:
                    self.particles[-1].mass = math.inf
                    self.particles[-1].isPinned = True

    def update(self, mouse_position, prev_mouse_position):
        self.currentTime = pygame.time.get_ticks()
        self.deltaTime = (self.currentTime - self.lastUpdateTime) / 1000.0
        self.lastUpdateTime = self.currentTime


        for particle in self.particles.copy():

            if particle.isPinned: 
                particle.x = particle.prevx
                particle.y = particle.prevy
                continue

            prevPosition = pygame.math.Vector2(particle.x, particle.y)

            # Update the position using Verlet integration
            particle.x += (particle.x - particle.prevx) * (1.0 - self.drag)
            particle.y += (particle.y - particle.prevy) * (1.0 - self.drag) + self.gravity.y * (self.deltaTime ** 2)

            # Update the previous position
            particle.prevx = prevPosition.x
            particle.prevy = prevPosition.y

            if particle.y >= self.screen_height:
                particle.y = self.screen_height
            if particle.x >= self.screen_width:
                particle.x = self.screen_width
            if particle.y < 0:
                particle.y = 0
            if particle.x < 0:
                particle.x = 0
        for _ in range(5):
            for stick in self.sticks.copy():
                diff = getDifference(stick.p1, stick.p2)
                diffFactor = (stick.length - getLength(diff)) / getLength(diff) * 0.5
                offset = pygame.math.Vector2(diff.x * diffFactor, diff.y * diffFactor)
                stick.p1.x += offset[0]
                stick.p1.y += offset[1]
                stick.p2.x -= offset[0]
                stick.p2.y -= offset[1]

                if intersect(mouse_position, prev_mouse_position, (stick.p1.x, stick.p1.y), (stick.p2.x, stick.p2.y)):
                    self.sticks.remove(stick)
        

    def render(self, screen):
        for i in range(len(self.particles)):
            pygame.draw.circle(screen, (255, 255, 255), (self.particles[i].x, self.particles[i].y), 5)


        for i in range(len(self.sticks)):
            pygame.draw.line(screen, (255,255,255), (self.sticks[i].p1.x, self.sticks[i].p1.y), (self.sticks[i].p2.x, self.sticks[i].p2.y))


def main():
    pygame.init()

    # Set up the display
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Cloth Sim")

    clock = pygame.time.Clock()

    #80 works
    #35 works
    cloth = Cloth(800, 600, 25, screen_height, screen_width)

    cloth.setup()

    mouse_down = False
    mouse_position = (0, 0)
    prev_mouse_position = (0, 0)

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_down = True
                    prev_mouse_position = mouse_position
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    mouse_down = False

        # Game logic
        if mouse_down:
            mouse_position = pygame.mouse.get_pos()

        cloth.update(mouse_position, prev_mouse_position)

        # Drawing code
        screen.fill((0, 0, 0))

        # Add your drawing code here
        cloth.render(screen)

        #display FPS
        fps = round(clock.get_fps(), 2)
        font = pygame.font.SysFont(None, 24)
        fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        if mouse_down:
            mouse_text = font.render(f"Mouse Position: {mouse_position}", True, (255, 255, 255))
            screen.blit(mouse_text, (10, 40))

        pygame.display.flip()
        clock.tick(60)  # Limit the frame rate to 60 FPS

if __name__ == "__main__":
    main()
