import pygame
import sys
import time

SCREEN_SCALE = 10
SCREEN_WIDTH = 24
SCREEN_HEIGHT = 24
SEGMENT_HEIGHT = 100
FPS = 60

ROM = [0] * 256
REG = [0] * 16
FLAGS = {"Z": 0, "C": 0}
PC = 0
HALT = False

screen_buf = [[0] * SCREEN_WIDTH for _ in range(SCREEN_HEIGHT)]
segment_value = 0

def fakeprint(*args): pass

def decode(instr1, instr2):
    opcode = (instr1 & 0xF0) >> 4
    op = (instr1 & 0x0F) << 8 | instr2
    return opcode, op

def set_flag(val):
    FLAGS["Z"] = int(val == 0)
    FLAGS["C"] = int(val > 255 or val < 0)

def run_instruction():
    global PC, HALT, segment_value
    instr1 = ROM[PC % len(ROM)]
    instr2 = ROM[(PC + 1) % len(ROM)]
    opcode, operands = decode(instr1, instr2)
    PC = (PC + 2) % len(ROM)

    print("PC:", PC, "     Instruction:", hex((instr1 << 8) + instr2))

    if opcode == 0x0:
        return
    elif opcode == 0x1:
        HALT = True
    elif opcode == 0x2:
        a, b, c = (operands >> 8) & 0xF, (operands >> 4) & 0xF, operands & 0xF
        REG[c] = (REG[a] + REG[b]) & 0xFF
        set_flag(REG[c])
    elif opcode == 0x3:
        a, b, c = (operands >> 8) & 0xF, (operands >> 4) & 0xF, operands & 0xF
        REG[c] = (REG[a] - REG[b]) & 0xFF
        set_flag(REG[c])
    elif opcode == 0x4:
        a, b, c = (operands >> 8) & 0xF, (operands >> 4) & 0xF, operands & 0xF
        REG[c] = REG[a] & REG[b]
        set_flag(REG[c])
    elif opcode == 0x5:
        a, b, c = (operands >> 8) & 0xF, (operands >> 4) & 0xF, operands & 0xF
        REG[c] = REG[a] | REG[b]
        set_flag(REG[c])
    elif opcode == 0x6:
        a, b, c = (operands >> 8) & 0xF, (operands >> 4) & 0xF, operands & 0xF
        REG[c] = REG[a] ^ REG[b]
        set_flag(REG[c])
    elif opcode == 0x7:
        a, b, c = (operands >> 8) & 0xF, (operands >> 4) & 0xF, operands & 0xF
        REG[c] = ~(REG[a] | REG[b]) & 0xFF
        set_flag(REG[c])
    elif opcode == 0x8:
        addr = operands & 0xFF
        PC = addr
    elif opcode == 0x9:
        a, _, c = (operands >> 8) & 0xF, (operands >> 4) & 0xF, operands & 0xF
        REG[c] = REG[a] >> 1
        set_flag(REG[c])
    elif opcode == 0xA:
        a, _, c = (operands >> 8) & 0xF, (operands >> 4) & 0xF, operands & 0xF
        REG[c] = (REG[a] << 1) & 0xFF
        set_flag(REG[c])
    elif opcode == 0xB:
        reg = (operands >> 8) & 0xF
        imm = operands & 0xFF
        REG[reg] = imm
        print("Set register", reg, "to value", imm)
    elif opcode == 0xC:
        reg = (operands >> 8) & 0xF
        imm = operands & 0xFF
        REG[reg] = (REG[reg] + imm) & 0xFF
        set_flag(REG[reg])
        print(f"ADI: REG[{reg}] += {imm} → {REG[reg]}")
    elif opcode == 0xD:
        addr = operands & 0xFF
        if FLAGS["Z"]:
            PC = addr
    elif opcode == 0xE:
        x = REG[(operands >> 4) & 0xF] % SCREEN_WIDTH
        y = REG[operands & 0xF] % SCREEN_HEIGHT
        screen_buf[y][x] ^= 1
    elif opcode == 0xF:
        segment_value = REG[(operands >> 8) & 0xF] & 0xFF
        print("New segment:", segment_value)

def draw_segment(screen, value, font):
    text = font.render(f"{value:03}", True, (0, 255, 0))
    screen.blit(text, (10, SCREEN_HEIGHT * SCREEN_SCALE + 10))

def draw_screen(screen):
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    pxarray = pygame.PixelArray(surf)
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            pxarray[x, SCREEN_HEIGHT - 1 - y] = 0xFFFFFF if screen_buf[y][x] else 0x000000
    del pxarray
    scaled = pygame.transform.scale(surf, (SCREEN_WIDTH * SCREEN_SCALE, SCREEN_HEIGHT * SCREEN_SCALE))
    screen.blit(scaled, (0, 0))

def update_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        REG[15] = 1
    elif keys[pygame.K_LEFT]:
        REG[15] = 2
    elif keys[pygame.K_UP]:
        REG[15] = 3
    elif keys[pygame.K_RIGHT]:
        REG[15] = 4
    else:
        REG[15] = 0

def main(hz=1000.0, debug=False):
    global cycle_count,start,stop,backupprint
    global print
    if not debug:
        backupprint = print
        print = fakeprint

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH * SCREEN_SCALE, SCREEN_HEIGHT * SCREEN_SCALE + SEGMENT_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("RBC v3")
    font = pygame.font.SysFont("Courier", 48, bold=True)

    cycle_time = 1.0 / hz
    cycle_count = 0
    last_cycle = time.time()
    start = time.time()
    stop = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end()

        update_input()
        now = time.time()
        cycles_to_run = int((now - last_cycle) / cycle_time)

        for _ in range(cycles_to_run):
            if HALT:
                if not stop:
                    stop = time.time()
            else:
                run_instruction()
                cycle_count += 1
            last_cycle += cycle_time

        screen.fill((0, 0, 0))
        draw_screen(screen)
        draw_segment(screen, segment_value, font)
        pygame.display.flip()
        clock.tick(FPS)

def end():
    global stop,start,backupprint,cycle_count
    if not stop:
        stop = time.time()
    backupprint(f"{cycle_count} cycles exécutés en {stop-start} secondes, moyenne {cycle_count / (stop-start)} cycles par seconde")
    pygame.quit()
    sys.exit()