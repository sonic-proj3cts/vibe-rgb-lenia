import numpy as np
from kernel import Kernel
from scipy.ndimage import rotate
from scipy.ndimage import zoom

class LeniaCreatureField:
    def __init__(self, creature, size=200, kernel_size=50):
        """
        Initializes the field for a single creature.
        
        Parameters:
            creature (Creature): The creature whose field we are simulating.
            size (int): The size of the field (default is 400x400).
            kernel_size (int): The size of the kernel used in the field (default is 90).
        """
        self.size = size  # Set the size of the field
        self.dt = creature.dt  # Time step for simulation (from creature)
        self.creature = creature  # Store the reference to the creature object
        self.kernels = []  # List to store kernel objects
        self.kernel_size = kernel_size  # IMPORTANT: used in rebuild
        
        # Initialize an empty RGB field for the creature (field for each channel)
        self.A = np.zeros((size, size, 3), dtype=np.float32)

        # Build kernels for the RGB channels (one kernel for each color channel)
        for i in range(3):  # Loop for 3 channels (R, G, B)
            k = Kernel(
                world_size=size,
                kernel_size=kernel_size,
                radius=creature.radii[i],  # Creature's radius for each color channel
                ring_centers=creature.ring_centers[i],  # Ring centers for each channel
                ring_width=creature.ring_width,  # Width of each ring
                ring_weights=creature.ring_weights,  # Weights for each ring
                mu=creature.mu[i],  # Mean for Gaussian growth for the channel
                sigma=creature.sigma[i],  # Standard deviation for Gaussian growth for the channel
                stamp_strength=creature.stamp_strength,  # Strength for stamping
                cutoff=creature.cutoff,  # Cutoff for kernel behavior
                growth_mode=creature.growth_mode  # Growth mode to be used for kernel
            )
            k.creature = creature  # Associate this kernel with the creature
            self.kernels.append(k)  # Add kernel to the list of kernels
            
            
        self.G = np.zeros_like(self.A) # Create the object and initialize once here instead of every step()
        self.convolved_field = np.zeros((size, size, 3), dtype=np.float32)  # Store the convolved field
        self.dt_difference_field = np.zeros((size, size, 3), dtype=np.float32)  # Store the convolved field

    def _rebuild_kernel(self, i):
        """
        Rebuild only ONE kernel (RGB channel).
        """
        self.kernels[i] = Kernel(
            world_size=self.size,
            kernel_size=self.kernel_size,
            radius=self.creature.radii[i],
            ring_centers=self.creature.ring_centers[i],
            ring_width=self.creature.ring_width,
            ring_weights=self.creature.ring_weights,
            mu=self.creature.mu[i],
            sigma=self.creature.sigma[i],
            stamp_strength=self.creature.stamp_strength,
            cutoff=self.creature.cutoff,
            growth_mode=self.creature.growth_mode
        )
        self.kernels[i].creature = self.creature

    def adjust_mu(self, mu_index, delta):
        """
        Adjust ONLY one mu value and rebuild only affected kernel.
        """
        self.creature.mu[mu_index % 3] += delta
        self._rebuild_kernel(mu_index % 3)  # 3 kernels per Field RGB

    def adjust_sigma(self, sigma_index, delta):
        """
        Adjust ONLY one sigma value and rebuild only affected kernel.
        """
        self.creature.sigma[sigma_index % 3] += delta
        self._rebuild_kernel(sigma_index % 3)  # 3 kernels per Field RGB

    def adjust_dt(self, delta):
        """
        Adjust simulation timestep (global, no kernel rebuild needed).
        """
        self.dt += delta
        self.creature.dt = self.dt
        
    def step(self,world_field=None):
        """
        Perform a simulation step for the creature field.
        This involves convolving the field with each kernel and updating the field.
        """

        # Ensure buffer shapes are valid
        if self.G.shape != self.A.shape: 
            self.G = np.zeros_like(self.A)

        if self.convolved_field.shape != self.A.shape:
            self.convolved_field = np.zeros_like(self.A)

        if self.dt_difference_field.shape != self.A.shape:
            self.dt_difference_field = np.zeros_like(self.A)
            
        # Initialize the growth array for the field (G will store growth values)
        G = self.G ; G.fill(0)        
        
        # Cleare the convolved field (used only for visualization later)
        self.convolved_field.fill(0)

        # Loop over all kernels (one for each channel) and apply the growth
        for i, k in enumerate(self.kernels):
            U = k.convolve(
                self.A,
                interaction_row=k.creature.interaction[i],
                world_field=world_field,
                world_interaction_row=k.creature.world_interaction[i]
            )  # Convolve field with kernel
            G[..., i] = k.grow(U)  # Apply growth based on the convolution result
            
            # Store the convolved field for visualization later
            self.convolved_field[...,i] = U
            
        # Store the timestep difference field for visualization later
        self.dt_difference_field[:] = self.dt * G

        # Update the field A with growth values scaled by dt (time step)
        self.A = np.clip(self.A + self.dt_difference_field, 0, 1)  # Keep values in range [0, 1]

        #print(f"Updated field A: min={self.A.min()} max={self.A.max()}")  # Debug A values

    def get_convolved_field(self):
        """
        Return the convolved field.
        """
        return self.convolved_field

    def get_dt_difference_field(self):
        """
        Return the dt difference field.
        """
        return self.dt_difference_field

    def reset_field(self):
        self.A = np.zeros((self.size, self.size, 3), dtype=np.float32)

    def stamp(self, x=None, y=None, scale=1.0, strength=None, stamp_field=None):
        if stamp_field is None:
            stamp_field = self.creature.get_stamp()
        stamp_field = np.asarray(stamp_field, dtype=float)

        if strength is None:
            strength = self.creature.stamp_strength

        # Apply scaling
        if scale != 1.0:
            stamp_field = zoom(stamp_field, scale, order=1)

        # Ensure integer shape
        h, w = stamp_field.shape
        h, w = int(np.round(h)), int(np.round(w))
        stamp_field = stamp_field[:h, :w]

        # Random position if not provided
        if x is None:
            x = int(np.random.randint(0, max(1, self.size - w)))
        else:
            x = int(x)

        if y is None:
            y = int(np.random.randint(0, max(1, self.size - h)))
        else:
            y = int(y)

        # Clip x and y to fit within field
        x_start = max(0, x)
        y_start = max(0, y)
        x_end = min(x + w, self.size)
        y_end = min(y + h, self.size)

        # Compute stamp slice that fits
        stamp_x_start = max(0, -x)  # if x < 0
        stamp_y_start = max(0, -y)  # if y < 0
        stamp_x_end = stamp_x_start + (x_end - x_start)
        stamp_y_end = stamp_y_start + (y_end - y_start)

        # Ensure valid shapes
        if (x_end <= x_start) or (y_end <= y_start):
            return  # stamp is completely outside the field, skip

        patch_cropped = stamp_field[stamp_y_start:stamp_y_end, stamp_x_start:stamp_x_end]

        # Apply the stamp safely
        self.A[y_start:y_end, x_start:x_end, :] += patch_cropped[:, :, None] * strength
        self.A = np.clip(self.A, 0, 1)

    def stamp_transform(self, x=None, y=None, strength=1.0, rotation_deg=None, scale=1.0):
        stamp_field = np.asarray(self.creature.get_stamp(), dtype=float)

        # Apply scaling
        if scale != 1.0:
            stamp_field = zoom(stamp_field, scale, order=1)

        # Apply rotation
        rot = np.random.uniform(0, 360) if rotation_deg is None else rotation_deg
        stamp_field = rotate(stamp_field, rot, reshape=True, order=1, mode='nearest')

        # Ensure integer shape after rotation
        h, w = stamp_field.shape
        h, w = int(np.round(h)), int(np.round(w))
        stamp_field = stamp_field[:h, :w]

        # Apply the stamp
        self.stamp(stamp_field=stamp_field, x=x, y=y, scale=1.0, strength=strength)

