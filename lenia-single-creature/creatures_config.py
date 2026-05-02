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
        mu    = [0.128, 0.101, 0.163, 0.152, 0.150],
        sigma = [0.013, 0.013, 0.015, 0.013, 0.013],
        growth_mode=1,
        interaction = [
            [0.5, 0.2, 0.3],   # R influenced by R, G, B
            [0.1, 0.5, 0.2],    # G influenced by ...
            [0.3, 0.3, 0.5]    # B influenced by ...
        ],
        stamp_strength=1.0,
        stamp_filename="./stamps/biorbium.webp"
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
        mu    = [0.128, 0.101, 0.163, 0.152, 0.150],
        sigma = [0.013, 0.013, 0.015, 0.013, 0.013],
        growth_mode=1,
        interaction = [
            [0.5, 0.2, 0.3],   # R influenced by R, G, B
            [0.1, 0.5, 0.2],    # G influenced by ...
            [0.3, 0.3, 0.5]    # B influenced by ...
        ],
        stamp_strength=1.0,
        stamp_filename="./stamps/biorbium2.webp"
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
        stamp_strength=1.0,
        stamp_filename="./stamps/biorbium2.webp"
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
        mu    = [0.143, 0.117, 0.163],
        sigma = [0.013, 0.013, 0.015],
        growth_mode=1,
        interaction = [
            [0.5, 0.2, 0.3],   # R influenced by R, G, B
            [0.1, 0.5, 0.2],    # G influenced by ...
            [0.3, 0.3, 0.5]    # B influenced by ...
        ],
        stamp_strength=1.0,
        stamp_filename="./stamps/biorbium2.webp"
    )

    creature5 = Creature(
        dt=0.080,
        radii=[23, 23, 23],
        ring_centers=[
            [0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00],
            [0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00],
            [0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00],
        ],
        ring_width=0.025,
        mu    = [0.1800, 0.2000, 0.2100],
        sigma = [0.0300, 0.0300, 0.0300],
        growth_mode=0,
        interaction = [
            [0.5, 0.2, 0.3],   # R influenced by R, G, B
            [0.1, 0.5, 0.2],    # G influenced by ...
            [0.3, 0.3, 0.5]    # B influenced by ...
        ],
        stamp_strength=1.0,
        #stamp_filename="creature.webp"
        stamp_filename="./stamps/biorbium2.webp"
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
        mu    = [0.1240, 0.1010, 0.1630],
        sigma = [0.0130, 0.0130, 0.0150],
        growth_mode=1,
        interaction = [
            [0.5, 0.3, 0.3],   # R influenced by R, G, B
            [0.2, 0.5, 0.2],   # G influenced by ...
            [0.3, 0.3, 0.5]    # B influenced by ...
        ],
        stamp_strength=1.0,
        stamp_filename="./stamps/biorbium.webp",
        cutoff=1.0
    )

    creature7 = Creature(
        dt=0.080,
        radii=[25, 25, 25],
        ring_centers=[ [0.4, 0.5, 0.6], [0.45, 0.55, 0.65], [0.55, 0.65, 0.75] ],  # Slightly different ring_centers
        ring_width=0.15,
        mu=[0.225, 0.210, 0.180],
        sigma=[0.025, 0.025, 0.025],
        growth_mode=1,  # Experiment with a different growth mode (e.g., 1: sigmoid-like growth)
        interaction=[[0.5, 0.3, 0.3], 
                     [0.3, 0.5, 0.3], 
                     [0.3, 0.3, 0.5]],  # Different interaction values
        stamp_strength=0.9,  # Slightly higher stamp strength
        stamp_filename="./stamps/orbium2.webp",
        cutoff=1.0
    )
    creature8 = Creature(
        dt=0.080,
        radii=[25, 25, 25],
        ring_centers=[ [0.4, 0.5, 0.6], [0.45, 0.55, 0.65], [0.55, 0.65, 0.75] ],  # Slightly different ring_centers
        ring_width=0.15,
        mu=[0.350, 0.355, 0.345],
        sigma=[0.065, 0.065, 0.065],
        growth_mode=1,  # Experiment with a different growth mode (e.g., 1: sigmoid-like growth)
        interaction=[[0.5, 0.3, 0.3], 
                     [0.3, 0.5, 0.3], 
                     [0.3, 0.3, 0.5]],  # Different interaction values
        stamp_strength=2.0,  # Slightly higher stamp strength
        stamp_scale=1.5,
        stamp_filename="./stamps/biorbium2.webp",
        cutoff=1.0
    )
    creature9 = Creature(
        dt=0.080,
        radii=[25, 25, 25],
        ring_centers=[ [0.4, 0.5, 0.6], [0.45, 0.55, 0.65], [0.55, 0.65, 0.75] ],  # Slightly different ring_centers
        ring_width=0.15,
        mu=[0.350, 0.355, 0.345],
        sigma=[0.065, 0.065, 0.065],
        growth_mode=1,  # Experiment with a different growth mode (e.g., 1: sigmoid-like growth)
        interaction=[[0.5, 0.3, 0.3], 
                     [0.3, 0.5, 0.3], 
                     [0.3, 0.3, 0.5]],  # Different interaction values
        stamp_strength=1.0,  # Slightly higher stamp strength
        stamp_filename="./stamps/paraptera_arcus_pedes.webp",
        cutoff=1.0
    )
    creature10 = Creature(
        dt=0.080,
        radii=[25, 25, 25],
        ring_centers=[ [0.4, 0.5, 0.6], [0.45, 0.55, 0.65], [0.55, 0.65, 0.75] ],  # Slightly different ring_centers
        ring_width=0.15,
        mu=[0.381, 0.353, 0.327],
        sigma=[0.065, 0.065, 0.065],
        growth_mode=1,  # Experiment with a different growth mode (e.g., 1: sigmoid-like growth)
        interaction=[[0.5, 0.3, 0.3], 
                     [0.3, 0.5, 0.3], 
                     [0.3, 0.3, 0.5]],  # Different interaction values
        stamp_strength=1.0,  # Slightly higher stamp strength
        stamp_filename="./stamps/paraptera_arcus_pedes.webp",
        cutoff=1.0
    )
    creature11 = Creature(
        dt=0.080,
        radii=[25, 25, 25],
        ring_centers=[ [0.4, 0.5, 0.6], [0.45, 0.55, 0.65], [0.55, 0.65, 0.75] ],  # Slightly different ring_centers
        ring_width=0.15,
        mu=[0.381, 0.353, 0.327],
        sigma=[0.065, 0.065, 0.065],
        growth_mode=1,  # Experiment with a different growth mode (e.g., 1: sigmoid-like growth)
        interaction=[[0.5, 0.3, 0.3], 
                     [0.3, 0.5, 0.3], 
                     [0.3, 0.3, 0.5]],  # Different interaction values
        stamp_strength=1.0,  # Slightly higher stamp strength
        stamp_filename="./stamps/googlescutium.webp",
        cutoff=1.0
    )
    creature12 = Creature(
        dt=0.080,
        radii=[25, 25, 25],
        ring_centers=[ [0.4, 0.5, 0.6], [0.45, 0.55, 0.65], [0.55, 0.65, 0.75] ],  # Slightly different ring_centers
        ring_width=0.15,
        mu=[0.270, 0.290, 0.245],
        sigma=[0.039, 0.039, 0.039],
        growth_mode=1,  # Experiment with a different growth mode (e.g., 1: sigmoid-like growth)
        interaction=[[0.5, 0.3, 0.3], 
                     [0.3, 0.5, 0.3], 
                     [0.3, 0.3, 0.5]],  # Different interaction values
        stamp_strength=1.0,  # Slightly higher stamp strength
        stamp_filename="./stamps/googlescutium.webp",
        cutoff=1.0
    )

    # Return the list of all creatures
    return [creature1, creature2, creature3, creature4, creature5, creature6, creature7, creature8, creature9, creature10, creature11, creature12]
