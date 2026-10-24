import asyncio
import random
import sys
import pygame


CELL_SIZE = 30  
COLS, ROWS = 10, 20  
WIDTH = COLS * CELL_SIZE + 200  
HEIGHT = ROWS * CELL_SIZE  

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Тетрис на Python")
clock = pygame.time.Clock()


BLACK = (10, 10, 15)
GREY = (40, 40, 50)
WHITE = (255, 255, 255)


SHAPES = {
    "I": [[(0, -1), (0, 0), (0, 1), (0, 2)], (0, 255, 255)],
    "O": [[(0, 0), (1, 0), (0, 1), (1, 1)], (255, 255, 0)],
    "T": [[(-1, 0), (0, 0), (1, 0), (0, 1)], (128, 0, 128)],
    "S": [[(0, 0), (1, 0), (-1, 1), (0, 1)], (0, 255, 0)],
    "Z": [[(-1, 0), (0, 0), (0, 1), (1, 1)], (255, 0, 0)],
    "J": [[(-1, -1), (-1, 0), (0, 0), (1, 0)], (0, 0, 255)],
    "L": [[(1, -1), (-1, 0), (0, 0), (1, 0)], (255, 165, 0)],
}


-
class Block:
  """Одиночный кубик на сетке."""

  def __init__(self, x, y, color):
    self.x = x
    self.y = y
    self.color = color

  def draw(self, surface):
    rect = pygame.Rect(
        self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1
    )
    pygame.draw.rect(surface, self.color, rect)


class Figure:
  """Фигура Тетриса, состоящая из 4 блоков."""

  def __init__(self, x, y):
    name = random.choice(list(SHAPES.keys()))
    offsets, self.color = SHAPES[name]
    self.name = name
  
    self.blocks = [Block(x + dx, y + dy, self.color) for dx, dy in offsets]

  def move(self, dx, dy):
    """Сдвиг фигуры на dx, dy ячеек."""
    for block in self.blocks:
      block.x += dx
      block.y += dy

  def rotate(self, grid):
    """Поворот фигуры на 90 градусов (кроме O-фигуры)."""
    if self.name == "O":
      return

   
    cx, cy = self.blocks[1].x, self.blocks[1].y

  
    old_positions = [(b.x, b.y) for b in self.blocks]

    for block in self.blocks:
      rx = block.x - cx
      ry = block.y - cy
    
      block.x = cx - ry
      block.y = cy + rx

  
    if not self.is_valid(grid):
      for i, block in enumerate(self.blocks):
        block.x, block.y = old_positions[i]

  def is_valid(self, grid):
    """Проверка: находится ли фигура в границах поля и не врезалась ли в другие блоки."""
    for block in self.blocks:
      if block.x < 0 or block.x >= COLS or block.y >= ROWS:
        return False
   
      if block.y >= 0 and grid[block.y][block.x] is not None:
        return False
    return True

  def draw(self, surface):
    for block in self.blocks:
      block.draw(surface)



async def main():
 

  
  grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

  
  FALL_EVENT = pygame.USEREVENT + 1
  pygame.time.set_timer(FALL_EVENT, 400)


  current_figure = Figure(COLS // 2, 1)
  score = 0
  game_over = False

  running = True
  while running:
    clock.tick(60)

    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

      if game_over:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
          
          grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
          current_figure = Figure(COLS // 2, 1)
          score = 0
          game_over = False
        continue

      
      if event.type == FALL_EVENT:
        current_figure.move(0, 1)
        if not current_figure.is_valid(grid):
          current_figure.move(0, -1) 

        
          for block in current_figure.blocks:
            if block.y >= 0:
              grid[block.y][block.x] = block.color

          
          new_grid = [row for row in grid if any(cell is None for cell in row)]
          removed_lines = ROWS - len(new_grid)
          if removed_lines > 0:
            score += removed_lines * 100
            
            for _ in range(removed_lines):
              new_grid.insert(0, [None for _ in range(COLS)])
            grid = new_grid

        
          current_figure = Figure(COLS // 2, 1)

          
          if not current_figure.is_valid(grid):
            game_over = True

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
            
        if event.key == pygame.K_a:
          current_figure.move(-1, 0)
          if not current_figure.is_valid(grid):
            current_figure.move(1, 0)
        elif event.key == pygame.K_d:
          current_figure.move(1, 0)
          if not current_figure.is_valid(grid):
            current_figure.move(-1, 0)
        elif event.key == pygame.K_s:
          current_figure.move(0, 1)
          if not current_figure.is_valid(grid):
            current_figure.move(0, -1)
        elif event.key == pygame.K_w:
          current_figure.rotate(grid)
        elif event.key == pygame.K_RIGHT: 
            while current_figure.is_valid(grid):
                current_figure.move(1, 0)
            current_figure.move(-1, 0)
        elif event.key == pygame.K_LEFT:
            while current_figure.is_valid(grid):
                current_figure.move(-1, 0)
            current_figure.move(1, 0)

  
    screen.fill(BLACK)

    
    for r in range(ROWS):
      for c in range(COLS):
        rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREY, rect, 1)

  
    for r in range(ROWS):
      for c in range(COLS):
        color = grid[r][c]
        if color:
          rect = pygame.Rect(
              c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1
          )
          pygame.draw.rect(screen, color, rect)

    
    if not game_over:
      current_figure.draw(screen)

 
    font = pygame.font.SysFont("Arial", 24)
    score_text = font.render(f"Счёт: {score}", True, WHITE)
    screen.blit(score_text, (COLS * CELL_SIZE + 20, 50))

    controls_text1 = font.render("A и D: Движение", True, WHITE)
    controls_text2 = font.render("W: Поворот", True, WHITE) 
    controls_text3 = font.render("Стрелки: Телепорт", True, WHITE)
    screen.blit(controls_text1, (COLS * CELL_SIZE + 10, 200))
    screen.blit(controls_text2, (COLS * CELL_SIZE + 10, 230))
    screen.blit(controls_text3, (COLS * CELL_SIZE + 10, 260))

    if game_over:
      go_font = pygame.font.SysFont("Arial", 40, bold=True)
      go_text = go_font.render("GAME OVER", True, (255, 0, 0))
      restart_text = font.render("Пробел для старта", True, WHITE)
      screen.blit(go_text, (COLS * CELL_SIZE // 4, HEIGHT // 2 - 50))
      screen.blit(restart_text, (COLS * CELL_SIZE // 4, HEIGHT // 2 + 10))

    pygame.display.flip()
    await asyncio.sleep(0)  



asyncio.run(main())

