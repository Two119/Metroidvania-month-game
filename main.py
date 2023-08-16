from assets.scripts.game import *
game = Game()
clock = pygame.time.Clock()
async def main():
    while game.run:
        game.update()
        if not web:
             for event in pygame.event.get():
                    if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        game.run = False
        pygame.display.update()
        await asyncio.sleep(0)
asyncio.run( main() )
