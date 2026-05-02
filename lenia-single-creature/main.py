import pygame
from creature import Creature
from creatures_config import create_creatures
from lenia import Lenia
from renderer import Renderer
import numpy as np
import random  # Import the random module for random selection

def breed(parrent1, parrent2, genetransfer_rate=0.05, mutation_rate=0.5):
    # Breed offspring and add them to the world
    print("\n\nparrent2 genetic code:")
    parrent2.print_genetic_code()
    print("\n\nparrent1 genetic code:")
    parrent1.print_genetic_code()
    offspring = parrent1.reproduce(parrent2, genetransfer_rate, mutation_rate)
    print("\n\nOffspring genetic code:")
    offspring.print_genetic_code()
    return offspring

def init_lenia(creatures, population=1, genetransfer_rate=0.05, mutation_rate=0.5):
    global sim, renderer  # Declare sim and renderer as global to modify them
    parrent1 = random.choice(creatures)
    parrent2 = random.choice(creatures)
    selected_creature = breed(parrent1, parrent2, genetransfer_rate, mutation_rate)
    # Reinitialize the simulation with the new creature
    sim = Lenia(creature=selected_creature, population=population)
    renderer = Renderer(sim)  # Recreate renderer to show the new creature
    sim.reset_stamp()  # Reset stamp for the new creature
    return sim, renderer  # Return the updated sim and renderer

# -----------------------
# Main
# -----------------------
def main():

    # Create creatures using the function from creatures_config.py
    creatures = create_creatures()

    # Randomly select a creature from the list
    selected_creature = random.choice(creatures)  # Randomly select a creature

    genetransfer_rate = 0.02
    mutation_rate = 0.1
    population = 1

    # Ensure init_lenia is called before the main loop begins
    sim, renderer = init_lenia(creatures, population, genetransfer_rate, mutation_rate)

    clock = pygame.time.Clock()
    running = True

    while running:
        # Event handling (single press)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_f:
                    renderer.show_change_field = not renderer.show_change_field
                    renderer.show_convolution_field = False
                    renderer.show_integration_field = False
                    renderer.show_growth_field = False
                elif event.key == pygame.K_g:
                    renderer.show_growth_field = not renderer.show_growth_field
                    renderer.show_change_field = False
                    renderer.show_convolution_field = False
                    renderer.show_integration_field = False
                elif event.key == pygame.K_h:
                    renderer.show_integration_field = not renderer.show_integration_field
                    renderer.show_convolution_field = False
                    renderer.show_growth_field = False
                    renderer.show_change_field = False
                elif event.key == pygame.K_j:
                    renderer.show_convolution_field = not renderer.show_convolution_field
                    renderer.show_change_field = False
                    renderer.show_integration_field = False
                    renderer.show_growth_field = False
                elif event.key == pygame.K_r:
                    sim.reset_blob()
                elif event.key == pygame.K_w:
                    sim.reset_noise()
                elif event.key == pygame.K_e:
                    sim.reset_stamp(1.0, np.random.uniform(0, 360), 1.0)
                elif event.key == pygame.K_t:
                    sim.reset_void()
                elif event.key == pygame.K_i:
                    # When "i" is pressed, spawn a new random breed creature
                    sim, renderer = init_lenia(creatures, population, genetransfer_rate, mutation_rate)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    sx , sy = event.pos
                    sim_pos = renderer.screen_to_sim(sx,sy)

                    if sim_pos is not None:
                        sx, sy = sim_pos
                        print("Clicked in sim at:", sx, sy)
                        #sim.stamp(sim.stamp_field, x=sx, y=sy, scale=1.0, strength=None)
                        sim.reset_stamp(x=sx, y=sy, strength_scale=1.0, rotation_deg=np.random.uniform(0, 360), scale=1.0)

        # -----------------------------
        # Continuous key handling
        # -----------------------------
        keys = pygame.key.get_pressed()

        # cycle selected kernel (M/N)
        if keys[pygame.K_m]:
            sim.next_kernel()  # next kernel
        if keys[pygame.K_n]:
            sim.prev_kernel()  # previous kernel

        # adjust mu/sigma of the selected kernel
        if keys[pygame.K_LEFT]:
            sim.adjust_mu(-0.001)
        if keys[pygame.K_RIGHT]:
            sim.adjust_mu(+0.001)
        if keys[pygame.K_UP]:
            sim.adjust_sigma(+0.001)
        if keys[pygame.K_DOWN]:
            sim.adjust_sigma(-0.001)

        # adjust dt
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:  # handle + on numpad or shift+=
            sim.adjust_dt(+0.001)
        if keys[pygame.K_MINUS]:
            sim.adjust_dt(-0.001)

        # Ensure sim and renderer are properly initialized before calling methods
        if sim and renderer:
            sim.step()
            renderer.draw()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
