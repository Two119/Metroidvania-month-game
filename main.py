from assets.scripts.game import *
game = Game()
clock = pygame.time.Clock()
async def main():
    while game.run:
        game.update()
        if not web:
             for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game.run = False
        pygame.display.update()
        await asyncio.sleep(0)
asyncio.run( main() )
