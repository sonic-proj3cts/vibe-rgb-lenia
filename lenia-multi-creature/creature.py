import numpy as np
import pygame

class Creature:
    def __init__(
        self,
        dt,
        radii,
        ring_centers,
        ring_width,
        mu,
        sigma,
        ring_weights=None,
        interaction=None,          # self-field interaction matrix for the creature's own field
        world_interaction=None,    # worldview interaction matrix for how the creature interacts with other creatures' fields
        stamp_strength=1.0,
        stamp_filename=None,
        stamp_scale=1.0,
        cutoff=2.0,                # Cutoff distance for the kernel, limits the effective radius of influence
        growth_mode=0,             # Growth mode to determine how the field evolves (e.g., Gaussian, sigmoid, etc.)
        genetic_code=None,          # Genetic code for mutation and reproduction
        name=""
    ):
        """
        Initialize a creature object with its attributes. These attributes determine how the creature interacts 
        with its field, other creatures, and how it evolves over time.
        
        Parameters:
            dt (float): Time step for the simulation (controls the speed of field growth).
            radii (list): List of radii for each channel (typically RGB), which influence the convolution process.
            ring_centers (list of lists): The center values for the rings in the kernel for each channel.
            ring_width (float): The width of the rings used in the kernel.
            mu (list): Mean values for the Gaussian distribution used in kernel generation for each channel.
            sigma (list): Standard deviation values for the Gaussian distribution for each channel.
            ring_weights (list, optional): Weights for each of the rings in the kernel. Defaults to equal weights.
            interaction (list of lists, optional): Self-field interaction matrix for the creature's own channels. Defaults to identity matrix (no interaction).
            world_interaction (list of lists, optional): Interaction matrix for the creature's worldview (i.e., interaction with other creatures' fields). Defaults to zero interaction.
            stamp_strength (float): The strength of the "stamp" effect applied to the field (default is 1.0).
            stamp_filename (str, optional): Path to the image file for the creature's stamp. This will be used to imprint a pattern on the field.
            cutoff (float): Maximum distance for kernel influence. Anything beyond this distance is not considered in the kernel.
            growth_mode (int): Defines the type of growth function used for the creature's field. Examples might be Gaussian, sigmoidal, or other types.
        """
        
        # Store all the provided parameters as instance variables
        self.dt = dt  # Time step for the simulation
        self.radii = radii  # Radii for each of the channels (RGB)
        self.ring_centers = ring_centers  # The center values of the rings for each channel
        self.ring_width = ring_width  # The width of each ring in the kernel
        self.mu = mu  # The mean values for the Gaussian distributions
        self.sigma = sigma  # The standard deviation for the Gaussian distributions

        # If no ring weights are provided, default to equal weight for all rings
        self.ring_weights = ring_weights if ring_weights is not None else [1.0] * len(ring_centers[0])

        # Self-field interaction matrix: controls how the creature interacts with its own channels
        self.interaction = np.array(interaction, dtype=np.float32) if interaction is not None else np.eye(3)
        
        # Worldview interaction matrix: controls how the creature interacts with other creatures (world field)
        self.world_interaction = np.array(world_interaction, dtype=np.float32) if world_interaction is not None else np.zeros((3, 3))
        
        # Other parameters
        self.stamp_strength = stamp_strength  # The strength of the creature's "stamp" effect
        self.stamp_filename = stamp_filename  # File path to the image used as a stamp
        self.stamp_scale = stamp_scale # The size of the stamp scaled
        self.stamp_field = None  # This will store the processed stamp field once it's loaded
        
        # New attributes related to kernel and growth behavior
        self.cutoff = cutoff  # Defines the cutoff distance for the kernel's effective range
        #print(f"DEBUG: Creature initialized with cutoff = {self.cutoff}")  # Debug print to track cutoff
        
        self.growth_mode = growth_mode  # Defines the growth function to control how the field evolves
        
        # If no genetic code is provided, generate a random one, otherwise copy the parent's genetic code
        if genetic_code is None:
            # Use the current values of self to generate the genetic code
            self.genetic_code = self.create_genetic_code_from_self()
        else:
            self.genetic_code = genetic_code.copy()  # Copy the genetic code from the parent
        
        self.name=name
        
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
            "world_interaction": self.world_interaction # Inherit world interaction from the parent
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
            "interaction": np.random.uniform(0, 1, (3, 3)),  # Random interaction matrix (3x3)
            "world_interaction": np.random.uniform(0, 1, (3, 3))  # Random interaction matrix (3x3)
        }
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
                elif gene == "world_interaction":
                    # Mutate the world_interaction matrix (2D array)
                    self.genetic_code[gene] = self.genetic_code[gene] + np.random.uniform(-0.1, 0.1, self.genetic_code[gene].shape)
                    # Optionally clip the values to keep them within a reasonable range (e.g., 0 to 1)
                    np.clip(self.genetic_code[gene], 0, 1, out=self.genetic_code[gene])

    def reproduce(self, other_creature, genetransfer_rate=0.1, mutation_rate=0.2):
        """
        Reproduce a new creature by combining the genetic codes of two creatures and applying mutation.
        """
        # Combine genes from both parents by averaging their genetic codes
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
            radii=new_genetic_code["radii"],
            ring_centers=new_genetic_code["ring_centers"],
            ring_width=self.ring_width,
            mu=new_genetic_code["mu"],
            sigma=new_genetic_code["sigma"],
            interaction=self.interaction,
            world_interaction=self.world_interaction,
            stamp_strength=self.stamp_strength,
            stamp_filename=self.stamp_filename,
            cutoff=new_genetic_code["cutoff"],
            growth_mode=new_genetic_code["growth_mode"],
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
        Loads and returns the stamp field, which is a grayscale and normalized image used to modify the creature's field.
        
        If the stamp image hasn't been loaded yet, this method will load it from the file, convert it to a grayscale image, 
        normalize the pixel values to the range [0, 1], and store it in `self.stamp_field`.
        
        Returns:
            np.ndarray: The normalized grayscale stamp field.
        """
        
        # If the stamp field has not been loaded yet and a stamp filename is provided
        if self.stamp_field is None and self.stamp_filename is not None:
            # Load the image file using pygame (convert_alpha() is used to handle transparency)
            print(f"Attempting to load stamp image from: {self.stamp_filename}")
            stamp_img = pygame.image.load(self.stamp_filename).convert_alpha()
            
            # Convert the image to a 3D numpy array (RGB), and then calculate the mean across the color channels to make it grayscale
            arr = pygame.surfarray.array3d(stamp_img).astype(np.float32)
            arr = arr.mean(axis=2).T  # Transpose to ensure the correct orientation
            
            # Normalize the array to the range [0, 1] by subtracting the minimum value and dividing by the maximum value
            arr -= arr.min()  # Make sure the minimum value is 0
            arr /= arr.max() + 1e-8  # Normalize the array to [0, 1] to prevent division by zero
            
            # Store the processed stamp field for future use
            self.stamp_field = arr
        
        # Return the stamp field (either newly loaded or previously cached)
        return self.stamp_field
