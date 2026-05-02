import pygame
import numpy as np
from numpy.fft import fft2, ifft2, ifftshift
import random

from creature import Creature
from lenia_combined_field import LeniaCombinedField
from combined_renderer import CombinedRenderer
from creatures_config import create_creatures


def breed(parrent1, parrent2, genetransfer_rate=0.05, mutation_rate=0.5):
    print(f"\n\n{parrent2.name} genetic code:")
    parrent2.print_genetic_code()

    print(f"\n\n{parrent1.name} genetic code:")
    parrent1.print_genetic_code()

    offspring = parrent1.reproduce(parrent2, genetransfer_rate, mutation_rate)

    print(f"\n\noffspring = breed({parrent1.name},{parrent2.name})")
    offspring.print_genetic_code()

    return offspring


def init_lenia(creatures, population=1, genetransfer_rate=0.05, mutation_rate=0.5, do_breed=False):
    global sim, renderer

    selected_creatures = []

    for _ in range(population):
        parrent1 = random.choice(creatures)

        if do_breed:
            parrent2 = random.choice(creatures)
            selected_creature = breed(parrent1, parrent2, genetransfer_rate, mutation_rate)
            selected_creatures.append(selected_creature)
        else:
            selected_creatures.append(parrent1)

    sim = LeniaCombinedField(selected_creatures)
    renderer = CombinedRenderer(sim)

    sim.stamp_all()

    return sim, renderer


# -----------------------
# MAIN
# -----------------------
def main():

    creatures = create_creatures()

    genetransfer_rate = 0.0#5
    mutation_rate = 0.0#5
    population = 2
    do_breed = True

    sim, renderer = init_lenia(
        creatures,
        population,
        genetransfer_rate,
        mutation_rate,
        do_breed
    )

    clock = pygame.time.Clock()
    running = True

    STEP = 0.001  # tuning speed

    # -----------------------
    # MAIN LOOP
    # -----------------------
    while running:

        # -----------------------
        # EVENTS (one-shot actions)
        # -----------------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    sim.reset_blob()

                elif event.key == pygame.K_w:
                    sim.reset_noise()

                elif event.key == pygame.K_t:
                    sim.reset_void()

                elif event.key == pygame.K_q:
                    running = False

                elif event.key == pygame.K_e:
                    #sim.stamp_all() # stamp each creature to it's field
                    #sim.stamp_field(renderer.creature_index) # stamp selected creature to it's field
                    sim.reset_stamp(renderer.creature_index,1.0, np.random.uniform(0, 360), 1.0)

                elif event.key == pygame.K_n:
                    renderer.draw_prev_creature()

                elif event.key == pygame.K_m:
                    renderer.draw_next_creature()

                elif event.key == pygame.K_i:
                    sim, renderer = init_lenia(
                        creatures,
                        population,
                        genetransfer_rate,
                        mutation_rate,
                        do_breed
                    )

                elif event.key == pygame.K_j:
                    renderer.prev_mu_sigma()

                elif event.key == pygame.K_k:
                    renderer.next_mu_sigma()
              
                elif event.key == pygame.K_c:  # Toggle the view for the convolved field
                    renderer.toggle_convoluted_view()

                elif event.key == pygame.K_d:  # Toggle the view for the convolved field
                    renderer.toggle_dt_difference_view()

        # -----------------------
        # CONTINUOUS INPUT (HOLD KEYS)
        # -----------------------
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            renderer.adjust_mu(-STEP)

        if keys[pygame.K_RIGHT]:
            renderer.adjust_mu(+STEP)

        if keys[pygame.K_DOWN]:
            renderer.adjust_sigma(-STEP)

        if keys[pygame.K_UP]:
            renderer.adjust_sigma(+STEP)
        
        if keys[pygame.K_PLUS]:
            renderer.adjust_dt(+STEP)
        
        if keys[pygame.K_MINUS]:
            renderer.adjust_dt(-STEP)

        # -----------------------
        # MOUSE STAMPING
        # -----------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            sim_pos = renderer.screen_to_sim(pos)

            if sim_pos is not None:
                sx, sy = sim_pos
                print("Clicked in sim at:", sx, sy)
                sim.stamp_field(renderer.creature_index, 
                                x=sx, 
                                y=sy, 
                                scale=1.0, 
                                strength=1.0, 
                                rotation_deg=np.random.uniform(0, 360))

        # -----------------------
        # SIM STEP + RENDER
        # -----------------------
        sim.step()
        renderer.draw()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
