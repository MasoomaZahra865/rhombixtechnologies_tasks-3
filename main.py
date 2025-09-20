import pygame
import random
import time

# Step 2: Initialize Pygame
pygame.init()

# Step 3: Set up constants and game variables
WIDTH, HEIGHT = 600, 600  # Size of the window
GRID_SIZE = 4  # Grid is 4x4, i.e., 16 cards in total
CARD_SIZE = 100  # Each card will be 100x100 pixels
TIME_LIMIT = 60  # Game time limit in seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)

# Fonts
font = pygame.font.SysFont('Arial', 30)

# Step 4: Create a class to represent each card
class Card:
    def __init__(self, value, x, y):
        self.value = value  # The number or image on the card
        self.x = x  # X coordinate on the grid
        self.y = y  # Y coordinate on the grid
        self.width = CARD_SIZE
        self.height = CARD_SIZE
        self.is_flipped = False  # Track whether the card is flipped
        self.is_matched = False  # Track whether the card has been matched

    def draw(self, screen):
        if self.is_flipped or self.is_matched:
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
            text = font.render(str(self.value), True, BLACK)
            screen.blit(text, (self.x + self.width // 4, self.y + self.height // 4))
        else:
            pygame.draw.rect(screen, GRAY, (self.x, self.y, self.width, self.height))

    def check_collision(self, pos):
        """ Check if a click is inside the card's rectangle """
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False

# Step 5: Generate shuffled pairs of cards
def generate_cards():
    values = list(range(1, (GRID_SIZE * GRID_SIZE) // 2 + 1)) * 2  # Generate pairs of numbers
    random.shuffle(values)

    cards = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * (CARD_SIZE + 10) + 50  # Space between cards
            y = row * (CARD_SIZE + 10) + 50
            value = values.pop()
            cards.append(Card(value, x, y))

    return cards

# Step 6: Main Game Loop
def game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Memory Puzzle Game")
    
    cards = generate_cards()  # Create and shuffle cards
    flipped_cards = []  # To track flipped cards
    matched_pairs = 0  # To track the number of matched pairs
    start_time = time.time()  # To track game time

    clock = pygame.time.Clock()  # Used for controlling the game speed
    running = True

    # Game Loop
    while running:
        screen.fill(BLACK)
        
        # Display the time remaining
        elapsed_time = int(time.time() - start_time)
        time_remaining = max(TIME_LIMIT - elapsed_time, 0)
        timer_text = font.render(f"Time Left: {time_remaining}s", True, WHITE)
        screen.blit(timer_text, (WIDTH - 200, 20))

        # Draw all cards
        for card in cards:
            card.draw(screen)

        # Check for game over (time is up or all cards matched)
        if time_remaining == 0 or matched_pairs == GRID_SIZE * GRID_SIZE // 2:
            if matched_pairs == GRID_SIZE * GRID_SIZE // 2:
                end_text = font.render("You Win!", True, WHITE)
            else:
                end_text = font.render("Time's Up! Game Over!", True, WHITE)
            screen.blit(end_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds before exiting
            running = False
            break

        # Event handling (user clicks)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse position
                mouse_pos = pygame.mouse.get_pos()

                # Flip the clicked card
                for card in cards:
                    if card.check_collision(mouse_pos) and not card.is_flipped and not card.is_matched:
                        card.is_flipped = True
                        flipped_cards.append(card)
                        
                        # Check for matching pair
                        if len(flipped_cards) == 2:
                            if flipped_cards[0].value == flipped_cards[1].value:
                                # Cards matched
                                flipped_cards[0].is_matched = True
                                flipped_cards[1].is_matched = True
                                matched_pairs += 1
                            else:
                                # Cards do not match, flip them back
                                pygame.time.wait(500)  # Wait for half a second to show the flipped cards
                                flipped_cards[0].is_flipped = False
                                flipped_cards[1].is_flipped = False

                            flipped_cards.clear()  # Clear flipped cards list

        pygame.display.flip()  # Update the display
        clock.tick(30)  # Limit the game to 30 frames per second

    pygame.quit()

# Step 7: Start the game
if __name__ == "__main__":
    game()
