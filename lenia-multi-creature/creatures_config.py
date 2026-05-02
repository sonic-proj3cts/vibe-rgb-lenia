# creatures_config.py
from creature import Creature

def create_creatures():
    creature1 = Creature(
        dt=0.080,
        radii=[23, 23, 23],
        ring_centers=[
            [0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
            [0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
            [0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
        ],
        ring_width=0.10,
        mu    = [0.139, 0.117, 0.163],
        sigma = [0.019, 0.013, 0.015],
        growth_mode=1,
        interaction = [
            [0.5, 0.2, 0.3],   # R influenced by R, G, B
            [0.1, 0.5, 0.2],    # G influenced by ...
            [0.3, 0.3, 0.5]    # B influenced by ...
        ],
        world_interaction = [
            [0.00, 0.10, 0.10],   # R influenced by R, G, B
            [0.10, 0.00, 0.10],    # G influenced by ...
            [0.10, 0.10, 0.00]    # B influenced by ...
        ],
        stamp_strength=1.0,
        stamp_filename="./stamps/biorbium.webp",
        name="creature1"
    )

    creature2 = Creature(
        dt=0.080,
        radii=[23, 23, 23],
        ring_centers=[
            [0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
            [0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
            [0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
        ],
        ring_width=0.10,
        mu    = [0.139, 0.117, 0.163],
        sigma = [0.019, 0.013, 0.015],
        growth_mode=1,
        interaction = [
            [0.5, 0.2, 0.3],   # R influenced by R, G, B
            [0.1, 0.5, 0.2],    # G influenced by ...
            [0.3, 0.3, 0.5]    # B influenced by ...
        ],
        world_interaction = [
            [0.00, 0.10, 0.10],   # R influenced by R, G, B
            [0.10, 0.00, 0.10],    # G influenced by ...
            [0.10, 0.10, 0.00]    # B influenced by ...
        ],
        stamp_strength=1.0,
        stamp_filename="./stamps/biorbium2.webp",
        name="creature2"
    )

    creature3 = Creature(
        dt=0.080,
        radii=[23, 23, 23],
        ring_centers=[
            [0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
            [0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
            [0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
        ],
        ring_width=0.10,
        mu    = [0.185, 0.200, 0.215],
        sigma = [0.030, 0.030, 0.030],
        growth_mode=1,
        interaction = [
            [0.5, 0.2, 0.3],   # R influenced by R, G, B
            [0.1, 0.5, 0.2],    # G influenced by ...
            [0.3, 0.3, 0.5]    # B influenced by ...
        ],
        world_interaction = [
            [0.00, 0.10, 0.10],   # R influenced by R, G, B
            [0.10, 0.00, 0.10],    # G influenced by ...
            [0.10, 0.10, 0.00]    # B influenced by ...
        ],
        stamp_strength=1.0,
        stamp_filename="./stamps/biorbium2.webp",
        name="creature3"
    )

    creature4 = Creature(
        dt=0.080,
        radii=[23, 23, 23],
        ring_centers=[
            [0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
            [0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
            [0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
        ],
        ring_width=0.10,
        mu    = [0.139, 0.117, 0.151],
        sigma = [0.011, 0.013, 0.015],
        growth_mode=1,
        interaction = [
            [0.5, 0.2, 0.3],   # R influenced by R, G, B
            [0.1, 0.5, 0.2],    # G influenced by ...
            [0.3, 0.3, 0.5]    # B influenced by ...
        ],
        world_interaction = [     # do not influence self with self
            [0.00, 0.10, 0.10],   # Red channel influenced by R, G, B
            [0.10, 0.00, 0.10],   # Green channel influenced by ...
            [0.10, 0.10, 0.00]    # Blue channel  influenced by ...
        ],
        stamp_strength=1.0,
        stamp_filename="./stamps/orbium5.webp",
        name="creature4"
    )
    creature5 = Creature(
        dt=0.080,
        radii=[23, 23, 23],
        ring_centers=[
            [0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
            [0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
            [0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95],
        ],
        ring_width=0.10,
        mu    = [0.139, 0.117, 0.151],
        sigma = [0.011, 0.013, 0.015],
        growth_mode=1,
        interaction = [
            [0.5, 0.2, 0.3],   # R influenced by R, G, B
            [0.1, 0.5, 0.2],    # G influenced by ...
            [0.3, 0.3, 0.5]    # B influenced by ...
        ],
        world_interaction = [     # do not influence self with self
            [0.00, 0.10, 0.10],   # Red channel influenced by R, G, B
            [0.10, 0.00, 0.10],   # Green channel influenced by ...
            [0.10, 0.10, 0.00]    # Blue channel  influenced by ...
        ],
        stamp_strength=1.0,
        stamp_filename="./stamps/orbium4.webp",
        name="creature5"
    )
    creature6 = Creature(
        dt=0.080,
        radii=[23, 23, 23],
        ring_centers=[
            [0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00],
            [0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00],
            [0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00],
        ],
        ring_width=0.25,
        mu    = [0.139, 0.117, 0.163],
        sigma = [0.019, 0.013, 0.015],
        growth_mode=1,
        interaction = [
            [0.5, 0.3, 0.3],   # R influenced by R, G, B
            [0.2, 0.5, 0.2],   # G influenced by ...
            [0.3, 0.3, 0.5]    # B influenced by ...
        ],
        world_interaction = [
            [0.00, 0.10, 0.10],   # R influenced by R, G, B
            [0.10, 0.00, 0.10],    # G influenced by ...
            [0.10, 0.10, 0.00]    # B influenced by ...
        ],
        stamp_strength=1.0,
        stamp_filename="./stamps/biorbium.webp",
        cutoff=1.0,
        name="creature6"
    )

    creature7 = Creature(
        dt=0.080,
        radii=[25, 25, 25],
        ring_centers=[
              [0.4070, 0.4580, 0.5090, 0.5600, 0.6110, 0.6620, 0.7130, 0.7640, 0.8150, 0.8660, 0.9170, 0.9680, 1.0190],
              [0.4070, 0.4580, 0.5090, 0.5600, 0.6110, 0.6620, 0.7130, 0.7640, 0.8150, 0.8660, 0.9170, 0.9680, 1.0190],
              [0.4070, 0.4580, 0.5090, 0.5600, 0.6110, 0.6620, 0.7130, 0.7640, 0.8150, 0.8660, 0.9170, 0.9680, 1.0190]
        ],
        ring_width=0.15,
        mu    = [0.127, 0.103, 0.166],
        sigma = [0.013, 0.013, 0.015],
        growth_mode=1,  # Experiment with a different growth mode (e.g., 1: sigmoid-like growth)
        interaction=[[0.5, 0.3, 0.3], 
                     [0.3, 0.5, 0.3], 
                     [0.3, 0.3, 0.5]],  # Different interaction values
        world_interaction = [
            [0.00, 0.10, 0.10],   # R influenced by R, G, B
            [0.10, 0.00, 0.10],    # G influenced by ...
            [0.10, 0.10, 0.00]    # B influenced by ...
        ],
        stamp_strength=0.9,  # Slightly higher stamp strength
        stamp_filename="./stamps/orbium2.webp",
        cutoff=1.0,
        name="creature7"
    )
    
    creature8 = Creature(
        dt=0.080,
        radii=[25, 25, 25],
        ring_centers=[ [0.4, 0.5, 0.6], [0.45, 0.55, 0.65], [0.55, 0.65, 0.75] ],  # Slightly different ring_centers
        ring_width=0.15,
        mu    = [0.139, 0.112, 0.163],
        sigma = [0.019, 0.013, 0.015],
        growth_mode=1,  # Experiment with a different growth mode (e.g., 1: sigmoid-like growth)
        interaction=[[0.5, 0.3, 0.3], 
                     [0.3, 0.5, 0.3], 
                     [0.3, 0.3, 0.5]],  # Different interaction values
        world_interaction = [
            [0.00, 0.10, 0.10],   # R influenced by R, G, B
            [0.10, 0.00, 0.10],    # G influenced by ...
            [0.10, 0.10, 0.00]    # B influenced by ...
        ],
        stamp_strength=2.0,  # Slightly higher stamp strength
        stamp_scale=1.5,
        stamp_filename="./stamps/biorbium2.webp",
        cutoff=1.0,
        name="creature8"
    )
    creature9 = Creature(
        dt=0.080,
        radii=[25, 25, 25],
        ring_centers=[ [0.4, 0.5, 0.6], [0.45, 0.55, 0.65], [0.55, 0.65, 0.75] ],  # Slightly different ring_centers
        ring_width=0.15,
        mu=[0.350, 0.355, 0.345],
        sigma=[0.065, 0.055, 0.050],
        growth_mode=1,  # Experiment with a different growth mode (e.g., 1: sigmoid-like growth)
        interaction=[[0.5, 0.3, 0.3], 
                     [0.3, 0.5, 0.3], 
                     [0.3, 0.3, 0.5]],  # Different interaction values
        world_interaction = [
            [0.00, 0.10, 0.10],   # R influenced by R, G, B
            [0.10, 0.00, 0.10],    # G influenced by ...
            [0.10, 0.10, 0.00]    # B influenced by ...
        ],
        stamp_strength=1.0,  # Slightly higher stamp strength
        stamp_filename="./stamps/paraptera_arcus_pedes.webp",
        cutoff=1.0,
        name="creature9"
    )
    creature10 = Creature(
        dt=0.080,
        radii=[25, 25, 25],
        ring_centers=[ [0.4, 0.5, 0.6], [0.45, 0.55, 0.65], [0.55, 0.65, 0.75] ],  # Slightly different ring_centers
        ring_width=0.15,
        mu=[0.377, 0.353, 0.327],
        sigma=[0.050, 0.065, 0.050  ],
        growth_mode=1,  # Experiment with a different growth mode (e.g., 1: sigmoid-like growth)
        interaction=[[0.5, 0.3, 0.3], 
                     [0.3, 0.5, 0.3], 
                     [0.3, 0.3, 0.5]],  # Different interaction values
        world_interaction = [
            [0.00, 0.10, 0.10],   # R influenced by R, G, B
            [0.10, 0.00, 0.10],    # G influenced by ...
            [0.10, 0.10, 0.00]    # B influenced by ...
        ],
        stamp_strength=1.0,  # Slightly higher stamp strength
        stamp_filename="./stamps/paraptera_arcus_pedes2.webp",
        cutoff=1.0,
        name="creature10"
    )
    creature11 = Creature(
        dt=0.080,
        radii=[25, 25, 25],
        ring_centers=[ [0.4, 0.5, 0.6], [0.45, 0.55, 0.65], [0.55, 0.65, 0.75] ],  # Slightly different ring_centers
        ring_width=0.15,
        mu=[0.381, 0.353, 0.327],
        sigma=[0.050, 0.065, 0.050],
        growth_mode=1,  # Experiment with a different growth mode (e.g., 1: sigmoid-like growth)
        interaction=[[0.5, 0.3, 0.3], 
                     [0.3, 0.5, 0.3], 
                     [0.3, 0.3, 0.5]],  # Different interaction values
        world_interaction = [
            [0.00, 0.10, 0.10],   # R influenced by R, G, B
            [0.10, 0.00, 0.10],    # G influenced by ...
            [0.10, 0.10, 0.00]    # B influenced by ...
        ],
        stamp_strength=1.0,  # Slightly higher stamp strength
        stamp_filename="./stamps/googlescutium.webp",
        cutoff=1.0,
        name="creature11"
    )
    creature12 = Creature(
        dt=0.080,
        radii=[25, 25, 25],
        ring_centers=[ [0.4, 0.5, 0.6], [0.45, 0.55, 0.65], [0.55, 0.65, 0.75] ],  # Slightly different ring_centers
        ring_width=0.15,
        mu=[0.267, 0.290, 0.245],
        sigma=[0.030, 0.030, 0.038],
        growth_mode=1,  # Experiment with a different growth mode (e.g., 1: sigmoid-like growth)
        interaction=[[0.5, 0.3, 0.3], 
                     [0.3, 0.5, 0.3], 
                     [0.3, 0.3, 0.5]],  # Different interaction values
        world_interaction = [
            [0.00, 0.10, 0.10],   # R influenced by R, G, B
            [0.10, 0.00, 0.10],    # G influenced by ...
            [0.10, 0.10, 0.00]    # B influenced by ...
        ],
        stamp_strength=1.0,  # Slightly higher stamp strength
        stamp_filename="./stamps/googlescutium2.webp",
        cutoff=1.0,
        name="creature12"
    )

    # Return the list of all creatures
    return [creature1, creature2, creature3, creature4, creature5, creature6, creature7, creature8, creature9, creature10, creature11, creature12]
