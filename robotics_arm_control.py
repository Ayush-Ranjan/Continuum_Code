import pygame
import serial
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Arm Control")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.Font(None, 36)

# Initialize serial connection
ser = serial.Serial('COM3', 9600, timeout=1)  # Replace 'COM3' with your Arduino port
time.sleep(2)  # Wait for the connection to establish

# Servo angles
inner_horizontal = 90
outer_horizontal = 90
inner_vertical = 90
outer_vertical = 90



feedback = 1
def send_command(servo, angle):
    
    command = f"{servo}{angle}\n"
    # print(command)
    ser.write(command.encode())
    feedback = ser.readline().decode().strip().split(',')
    if len(feedback) == 4:
        return list(map(int, feedback))
    return 1

def update_display():
    screen.fill(WHITE)
    text = font.render(f"IH: {inner_horizontal} OH: {outer_horizontal}", True, BLACK)
    screen.blit(text, (10, 10))
    text = font.render(f"IV: {inner_vertical} OV: {outer_vertical}", True, BLACK)
    screen.blit(text, (10, 50))
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
    
    if shift_pressed:
        if keys[pygame.K_LEFT]:
            outer_horizontal = max(0, outer_horizontal - 1)
            feedback = send_command('O', outer_horizontal)
        elif keys[pygame.K_RIGHT]:
            outer_horizontal = min(180, outer_horizontal + 1)
            feedback = send_command('O', outer_horizontal)
        elif keys[pygame.K_UP]:
            outer_vertical = min(180, outer_vertical + 1)
            feedback = send_command('W', outer_vertical)
        elif keys[pygame.K_DOWN]:
            outer_vertical = max(0, outer_vertical - 1)
            feedback = send_command('W', outer_vertical)
    else:
        if keys[pygame.K_LEFT]:
            inner_horizontal = max(0, inner_horizontal - 1)
            outer_horizontal = max(0, outer_horizontal - 1)
            feedback = send_command('I', inner_horizontal)
            feedback = send_command('O', outer_horizontal)
        elif keys[pygame.K_RIGHT]:
            inner_horizontal = min(180, inner_horizontal + 1)
            outer_horizontal = min(180, outer_horizontal + 1)
            feedback = send_command('I', inner_horizontal)
            feedback = send_command('O', outer_horizontal)
        elif keys[pygame.K_UP]:
            inner_vertical = min(180, inner_vertical + 1)
            outer_vertical = min(180, outer_vertical + 1)
            feedback = send_command('V', inner_vertical)
            feedback = send_command('W', outer_vertical)
        elif keys[pygame.K_DOWN]:
            inner_vertical = max(0, inner_vertical - 1)
            outer_vertical = max(0, outer_vertical - 1)
            feedback = send_command('V', inner_vertical)
            feedback = send_command('W', outer_vertical)
    
    if feedback:
        inner_horizontal, outer_horizontal, inner_vertical, outer_vertical = feedback
    
    update_display()
    pygame.time.wait(50)  # Add a small delay to control the speed of movement

pygame.quit()
ser.close()