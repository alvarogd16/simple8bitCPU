import pygame

class Screen():
    def __init__(self):
        pygame.init()

        self.width = 1200
        self.height = 900

        self.surface = pygame.display.set_mode((self.width, self.height))

        self.draw_RGB()

        self.running = True

    def initScreen(self):
        while self.running:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
        pygame.quit()

    def draw_RGB(self):
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        for i in range(0, self.height, 100):
            for j in range(0, self.width, 100):
                pygame.draw.rect(self.surface, colors[j%300 // 100], (j, i, 100, 100))
            c = colors.pop(0)
            colors.append(c)


screen = Screen()
screen.initScreen()