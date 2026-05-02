# Import necessary libraries
import numpy as np  # numpy for array operations and numerical computing
import pygame  # pygame for handling image loading and graphical components

class Creature:
    """
    A class representing a creature in a simulation, which can grow and interact with its environment.
    The creature's appearance and behavior are determined by various parameters such as radii, growth mode, and interaction matrices.
    """

    def __init__(
        self,
        dt,                    # Time step for the simulation
        radii,                 # List of radii values for each color channel (R, G, B)
        ring_centers,          # List of 3D centers for the rings associated with the creature's kernels
        ring_width,            # The width of the rings (used to control the range of influence)
        mu,                    # List of growth parameters for the creature (typically scaling factors for growth)
        sigma,                 # List of standard deviations for each color channel, controls the spread of the growth
        ring_weights=None,     # Optional: Weights for each of the rings in the kernel
        interaction=None,      # Optional: Interaction matrix for how the creature's channels (R, G, B) influence each other
        stamp_strength=1.0,    # Strength of the "stamp" applied to the environment (e.g., creature’s influence field)
        stamp_scale=1.0,       # Scale of the "stamp" applied to the environment (e.g., creature’s influence field)
        stamp_filename=None,   # Optional: Path to the image used as the stamp (can be an external image)
        cutoff=2.0,            # Optional: Cutoff parameter that limits certain behaviors (e.g., growth or interaction)
        growth_mode=1,         # Growth mode (default value 1), affects how the creature grows over time
        genetic_code=None      # Genetic code for mutation and reproduction
    ):
        # Initialize the creature's properties with the provided parameters
        self.dt = dt  # Time step for simulation, controls the speed of simulation
        self.radii = radii  # Radii values for each channel (R, G, B), affects size of the creature
        self.ring_centers = ring_centers  # List of 3D centers for the rings in the kernels, determines creature's field
        self.ring_width = ring_width  # The width of the kernels' rings, impacts the range of influence of each channel
        self.mu = mu  # Growth parameters, affecting how the creature grows over time
        self.sigma = sigma  # Standard deviations of the growth, affects how quickly it expands or spreads
        self.growth_mode = growth_mode  # Mode for controlling how the creature grows (like sigmoid, linear, etc.)
        self.cutoff = cutoff  # The cutoff parameter that will restrict certain behaviors or interactions

        # If no ring_weights are provided, initialize to a uniform weight (1.0) for each ring
        self.ring_weights = ring_weights if ring_weights is not None else [1.0] * len(ring_centers[0])

        # If no interaction matrix is provided, use an identity matrix (each channel interacts only with itself)
        self.interaction = np.array(interaction, dtype=np.float32) if interaction is not None else np.eye(3)

        # Strength of the stamp field, how strongly it influences the environment
        self.stamp_strength = stamp_strength

        # Scale of the stamp, how big it is
        self.stamp_scale = stamp_scale

        # Filename for the stamp image, which could be used for a texture or field representation of the creature
        self.stamp_filename = stamp_filename

        # Field for the stamp, initialized as None. This will be populated when the stamp is loaded
        self.stamp_field = None
        
        # If no genetic code is provided, generate a random one, otherwise copy the parent's genetic code
        if genetic_code is None:
            # Use the current values of self to generate the genetic code
            self.genetic_code = self.create_genetic_code_from_self()
        else:
            self.genetic_code = genetic_code.copy()  # Copy the genetic code from the parent

    def create_genetic_code_from_self(self):
        """
        Generate genetic code based on the current values of the Creature's parameters.
        This ensures that the offspring's genetic code is initialized with values based on the parent.
        """
        genetic_code = {
            "radii": self.radii,  # Inherit the radii from the parent
            "ring_centers": self.ring_centers,  # Inherit the ring_centers from the parent
            "mu": self.mu,  # Inherit mu from the parent
            "sigma": self.sigma,  # Inherit sigma from the parent
            "growth_mode": self.growth_mode,  # Inherit growth_mode from the parent
            "cutoff": self.cutoff,  # Inherit cutoff from the parent
            "interaction": self.interaction, # Inherit interaction from the parent
        }
        return genetic_code
        
    def generate_genetic_code(self):
        """
        Generate a genetic code that consists of all the parameters that influence the creature's behavior.
        """
        genetic_code = {
            "radii": np.random.uniform(15, 30, 3),  # Random radii for the 3 RGB channels
            "ring_centers": np.random.uniform(0.3, 1.0, (3, 6)),  # Random ring centers for each channel
            "mu": np.random.uniform(0.1, 0.3, 3),  # Random mu for growth behavior
            "sigma": np.random.uniform(0.01, 0.05, 3),  # Random sigma for growth behavior
            "growth_mode": np.random.choice([0, 1]),  # Random growth mode
            "cutoff": np.random.uniform(1.0, 3.0),  # Random cutoff distance
            "interaction": np.random.uniform(0, 1, (3, 3))  # Random interaction matrix (3x3)
        }
        return genetic_code
        return genetic_code

    def mutate(self, mutation_rate=0.1):
        """
        Apply mutation to the creature's genetic code.
        Mutation rate determines how often a gene will be mutated.
        """
        for gene in self.genetic_code:
            if np.random.rand() < mutation_rate:
                # Randomly mutate the gene
                if gene == "radii":
                    self.genetic_code[gene] = np.random.uniform(15, 30, 3)
                elif gene == "ring_centers":
                    self.genetic_code[gene] = np.random.uniform(0.3, 1.0, (3, 6))
                elif gene == "mu":
                    self.genetic_code[gene] = np.random.uniform(0.1, 0.3, 3)
                elif gene == "sigma":
                    self.genetic_code[gene] = np.random.uniform(0.01, 0.05, 3)
                elif gene == "growth_mode":
                    # Ensure growth_mode is always an integer between [0, 1]
                    self.genetic_code[gene] = np.random.choice([0, 1])  # Integer only mutation for growth_mode
                elif gene == "cutoff":
                    self.genetic_code[gene] = np.random.uniform(1.0, 3.0)
                elif gene == "interaction":
                    # Mutate the interaction matrix (2D array)
                    self.genetic_code[gene] = self.genetic_code[gene] + np.random.uniform(-0.1, 0.1, self.genetic_code[gene].shape)
                    # Optionally clip the values to keep them within a reasonable range (e.g., 0 to 1)
                    np.clip(self.genetic_code[gene], 0, 1, out=self.genetic_code[gene])

    def reproduce(self, other_creature, genetransfer_rate=0.1, mutation_rate=0.2):
        """
        Reproduce a new creature by combining the genetic codes of two creatures and applying mutation.
        """
        new_genetic_code = {}

        for gene in self.genetic_code:
            # Get the genes from both parents
            self_gen = self.genetic_code[gene]
            other_gen = other_creature.genetic_code.get(gene, None)
            
            if other_gen is None:
                new_genetic_code[gene] = self_gen  # If the other creature doesn't have the gene, just use self's
                continue

            # Ensure both genes are numpy arrays for element-wise operations
            if isinstance(self_gen, (np.ndarray, list)):
                self_gen = np.array(self_gen, dtype=np.float32)  # Ensure it's a numpy array for element-wise operations
                other_gen = np.array(other_gen, dtype=np.float32)  # Same for the other creature

                # Handle shape mismatch between self_gen and other_gen
                if self_gen.shape != other_gen.shape:
                    print(f"Shape mismatch for gene {gene}: {self_gen.shape} vs {other_gen.shape}")
                    
                    # Handle specific cases like 'ring_centers' (multi-dimensional) separately
                    if gene == "ring_centers":
                        # Interpolate to match shapes (columns) of the smaller array to the larger one
                        if self_gen.shape[1] < other_gen.shape[1]:
                            print(f"Interpolating {gene} from {self_gen.shape[1]} to {other_gen.shape[1]}")
                            # Interpolate each row separately for the 3 color channels
                            new_self_gen = np.array([np.interp(np.linspace(0, 1, other_gen.shape[1]), 
                                                              np.linspace(0, 1, self_gen.shape[1]), row) 
                                                     for row in self_gen])
                            self_gen = new_self_gen
                        elif self_gen.shape[1] > other_gen.shape[1]:
                            print(f"Interpolating {gene} from {self_gen.shape[1]} to {other_gen.shape[1]}")
                            # Interpolate other_gen to match self_gen's shape
                            new_other_gen = np.array([np.interp(np.linspace(0, 1, self_gen.shape[1]), 
                                                               np.linspace(0, 1, other_gen.shape[1]), row) 
                                                      for row in other_gen])
                            other_gen = new_other_gen
                    else:
                        # For 1D genes or non-ring genes, handle the size mismatch by padding or averaging
                        if self_gen.shape[0] < other_gen.shape[0]:
                            # Pad self_gen to match the other_gen's size (pad with zeros or mean values)
                            self_gen = np.pad(self_gen, (0, other_gen.shape[0] - self_gen.shape[0]), mode='constant', constant_values=0)
                        elif self_gen.shape[0] > other_gen.shape[0]:
                            # Pad other_gen to match self_gen's size
                            other_gen = np.pad(other_gen, (0, self_gen.shape[0] - other_gen.shape[0]), mode='constant', constant_values=0)

            # Combine the genes and apply the mutation rate with the sign
            genetransfer_sign = np.random.choice([-1, 1])  # Randomly choose -1 or 1 (negative or positive)
            new_genetic_code[gene] = self_gen + other_gen * genetransfer_rate * genetransfer_sign
                
        # Ensure growth_mode is an integer after averaging or crossover
        if 'growth_mode' in new_genetic_code:
            new_genetic_code["growth_mode"] = int(np.floor(new_genetic_code["growth_mode"] + 0.5))

        # Create a new creature with the combined genetic code
        offspring = Creature(
            dt=self.dt,
            radii=new_genetic_code.get("radii", self.radii),
            ring_centers=new_genetic_code.get("ring_centers", self.ring_centers),
            ring_width=self.ring_width,
            mu=new_genetic_code.get("mu", self.mu),
            sigma=new_genetic_code.get("sigma", self.sigma),
            interaction=self.interaction,
            stamp_strength=self.stamp_strength,
            stamp_filename=self.stamp_filename,
            cutoff=new_genetic_code.get("cutoff", self.cutoff),
            growth_mode=new_genetic_code.get("growth_mode", self.growth_mode),
            genetic_code=new_genetic_code
        )

        # Apply mutation to the offspring's genetic code after combining
        offspring.mutate(mutation_rate)

        return offspring
        
    def print_genetic_code(self, fixed_width=40):
        """
        Print the genetic code with arrays formatted properly (i.e., respecting newlines for 2D arrays).
        This version ensures all printed values are aligned at a fixed x position.
        """
        for gene, value in self.genetic_code.items():
            # Ensure that each gene's name is printed at the same position
            print(f"{gene.ljust(fixed_width)}", end=": ")

            if isinstance(value, np.ndarray):
                if value.ndim == 2:  # Handle 2D arrays (like ring_centers)
                    # Print the 2D array with a fixed-width for each element
                    print("[")

                    # Iterate over each row in the 2D array and print it, formatted
                    for row in value:
                        # Print each row with the elements properly spaced
                        print(f"{' ' * (fixed_width + 2)}" + ', '.join([f"{x:.4f}" for x in row]))

                    print("]")
                else:
                    # Print 1D arrays (like radii, mu, sigma)
                    print(f"{value}")
            else:
                # For regular list or scalar values, just print them
                print(f"{value}")
        
    def get_stamp(self):
        """
        Loads the stamp image from the given filename and processes it into a 2D array.
        The stamp field is normalized (scaled between 0 and 1) to match the environment.
        
        Returns:
            np.ndarray: The processed stamp field (2D array), representing the creature's influence pattern.
        """
        # Check if the stamp field hasn't been loaded already and if a filename is provided
        if self.stamp_field is None and self.stamp_filename is not None:
            # Load the image using Pygame
            stamp_img = pygame.image.load(self.stamp_filename).convert_alpha()  # Load image with alpha channel (transparency)
            
            # Convert the image to a 3D numpy array (RGB channels)
            arr = pygame.surfarray.array3d(stamp_img).astype(np.float32)
            
            # Calculate the mean along the third dimension (RGB) to convert to grayscale intensity
            arr = arr.mean(axis=2).T  # Transpose for compatibility
            
            # Normalize the values in the array (to be between 0 and 1)
            arr -= arr.min()  # Subtract the minimum value to make the smallest value 0
            arr /= arr.max() + 1e-8  # Divide by the maximum value to normalize (adding a small epsilon to prevent division by zero)
            
            # Save the processed stamp field in the creature object
            self.stamp_field = arr
        
        # Return the processed (or already loaded) stamp field
        return self.stamp_field
