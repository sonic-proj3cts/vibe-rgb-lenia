import numpy as np  # Importing numpy for numerical array operations
from kernel import Kernel  # Import the Kernel class from the kernel module
from scipy.ndimage import rotate, zoom


# -----------------------
# Lenia Simulation
# -----------------------
class Lenia:
    def __init__(self, creature, population, size=300, kernel_size=50, dt=0.1):
        # Initialize simulation parameters
        self.size = size                # Size of the simulation field (square)
        self.kernel_size = kernel_size  # Kernel size used in convolution
        self.dt = creature.dt           # Time step from the creature object
        self.population = population
        self.kernels = []               # List to store kernels for different creatures
        self.creature = creature

        # Initialize the scalar field (A) as a 3D array to hold RGB channels
        self.A = np.zeros((self.size, self.size, 3))  # Initialize the field to all zeros (black)

        self._build_kernels(creature)   # Build the kernels based on the creature's parameters
        
        # The currently selected kernel (0, 1, 2 for different types)
        self.selected_kernel = 0
        self.stamp_field = creature.stamp_field

        # -----------------------
        # Diagnostics / stored fields
        # -----------------------
        self.dA_dt_field = np.zeros((size, size, 3), dtype=np.float32)        # F(A) = dA/dt
        self.dA_integration = np.zeros((size, size, 3), dtype=np.float32)     # dt * dA/dt
        self.change_field = np.zeros((size, size, 3), dtype=np.float32)       # A(t+dt) - A(t)
        self.convolution_field = np.zeros((size, size), dtype=np.float32)
    # -----------------------
    # Cycle selected kernel
    # -----------------------
    def next_kernel(self):
        # Move to the next kernel (cycling through the list of kernels)
        self.selected_kernel = (self.selected_kernel + 1) % len(self.kernels)

    def prev_kernel(self):
        # Move to the previous kernel (cycling in reverse through the list)
        self.selected_kernel = (self.selected_kernel - 1) % len(self.kernels)

    # -------------------------------
    # Field initialization functions
    # -------------------------------
    
    #def reset_stamp(self):
    #    # Reset the field (A) to all zeros, and apply random "stamp" to each channel (RGB)
    #    self.A = np.zeros((self.size, self.size, 3))  # Reset for RGB channels
    #    for _ in range(self.population):
    #        x = np.random.randint(0, self.size)  # Random x-coordinate
    #        y = np.random.randint(0, self.size)  # Random y-coordinate
    #        for c in range(3):  # Apply stamp to each channel (R, G, B)
    #            self.stamp(self.stamp_field, x, y, self.creature.stamp_scale, channel=c)

    def reset_stamp(self, x=None, y=None, strength_scale=1.0, rotation_deg=None, scale=1.0):
        """
        Reset the field using a single stamp applied to all RGB channels at the same position.
        Optional x, y coordinates allow placing the stamp at a specific location.
        """
        # Clear field
        self.A = np.zeros((self.size, self.size, 3), dtype=np.float32)

        # Get 2D stamp
        stamp_field = self.creature.get_stamp()  # guaranteed 2D

        # Apply scaling
        if scale != 1.0:
            stamp_field = zoom(stamp_field, scale, order=1)

        # Apply rotation
        rot = np.random.uniform(0, 360) if rotation_deg is None else rotation_deg
        stamp_field = rotate(stamp_field, rot, reshape=True, order=1, mode='nearest')

        # Pick random position if not provided
        h, w = stamp_field.shape
        if x is None:
            x = np.random.randint(0, max(1, self.size - w))
        if y is None:
            y = np.random.randint(0, max(1, self.size - h))

        # Apply stamp using the class method (handles boundaries)
        self.stamp(stamp_field=stamp_field, x=int(x), y=int(y), scale=strength_scale, channel=None)

    def reset_blob(self):
        """
        Reset the field to a random blob for all RGB channels.
        Ensures self.A is always shape (size, size, 3)
        """
        n_blobs = 5  # Number of blobs to generate
        radius = 40  # Blob radius

        A = np.zeros((self.size, self.size))  # Initialize a 2D field (grayscale)

        for _ in range(n_blobs):
            # Randomly select the center of each blob
            cx = np.random.randint(radius, self.size - radius)
            cy = np.random.randint(radius, self.size - radius)

            # Generate a 2D meshgrid to compute distances
            y, x = np.ogrid[:self.size, :self.size]
            dist = np.sqrt((x - cx)**2 + (y - cy)**2)  # Calculate distance from the center

            # Create a Gaussian envelope based on the distance
            envelope = np.exp(-(dist**2) / (2 * radius**2))
            # Add random noise scaled by the envelope
            noise = (np.random.rand(self.size, self.size)*2 - 1) * envelope
            A += envelope + 0.8 * noise  # Add the envelope and noise to the field

        # Normalize the field so that values range from 0 to 1
        A -= A.min()  # Subtract the minimum value to make the range start from 0
        A /= (A.max() + 1e-8)  # Normalize the field to [0, 1]

        # Make it RGB by stacking the grayscale array in all three channels
        self.A = np.stack([A, A, A], axis=-1)  # Convert the field to RGB format

    def reset_noise(self):
        """
        Reset the field to random noise for all RGB channels.
        """
        noise = np.random.rand(self.size, self.size)  # Generate random noise
        self.A = np.stack([noise, noise, noise], axis=-1)  # Stack the noise into RGB channels

    def reset_void(self):
        """
        Reset the field to random noise for all RGB channels.
        """
        self.A = np.zeros((self.size, self.size, 3))  # clear all channels

    # -----------------------
    # Kernels
    # -----------------------
    
    def create_kernel(self, size, radius, channel=0):
        # Create a kernel with a given size and radius for a specific channel
        y, x = np.ogrid[-size//2:size//2, -size//2:size//2]  # Create a grid
        dist = np.sqrt(x**2 + y**2)  # Calculate the distance from the center

        r = dist / radius  # Normalize distance by the radius

        # Get the parameters for the kernel (from creature)
        ring_centers = self.ring_centers[channel]  # Get ring centers for the specific channel
        ring_width = self.ring_width  # Ring width (controls the width of the rings)
        ring_weights = self.ring_weights  # Weights for each ring

        k = np.zeros_like(r)  # Initialize the kernel to all zeros

        # Add Gaussian rings based on the ring centers and weights
        for c, w in zip(ring_centers, ring_weights):
            k += w * np.exp(-((r - c)**2) / (2 * ring_width**2))

        # Set values beyond a certain cutoff to zero
        k[r > 2.0] = 0
        k /= k.sum() + 1e-8  # Normalize the kernel to avoid division by zero

        return k

    def _build_kernels(self, creature):
        # Create kernels for the creature using its parameters
        for i in range(3):  # Assume there are 3 kernels (one for each RGB channel)
            k = Kernel(
                world_size=self.size,
                kernel_size=self.kernel_size,
                radius=creature.radii[i],
                ring_centers=creature.ring_centers[i],
                ring_width=creature.ring_width,
                ring_weights=creature.ring_weights,
                mu=creature.mu[i],
                sigma=creature.sigma[i],
                growth_mode=creature.growth_mode,  # <- pass growth_mode here
                stamp_strength=creature.stamp_strength,
                cutoff=creature.cutoff  # <- pass the cutoff here
            )
            k.creature = creature  # Optional, to link the kernel back to the creature
            self.kernels.append(k)

    # -----------------------
    # Dynamics
    # -----------------------
    def combine_channels(self):
        # Combine the RGB channels into one 2D view (e.g., average of channels)
        combined_view = np.mean(self.A, axis=-1)
        return combined_view

    def convolve(self):
        # Convolve the combined view with each kernel
        combined_view = self.combine_channels()
        return [k.convolve(combined_view) for k in self.kernels]

    def grow(self, U_list):
        # Apply the growth function to each kernel's output
        G = np.zeros_like(self.A)

        for i, k in enumerate(self.kernels):
            G[..., i] = k.grow(U_list[i])

        return G
    
    def step(self):
        """
        Perform one simulation step (Euler integration) of the Lenia dynamics.

        Pipeline:
        U = convolution(A(t))
        G = growth(U)
        G = F(A(t))
        U = convolution(A(t)) -> F(A(t)) = growth(U) = G = dA/dt -> integration -> A(t+dt)
        """
        
        # Store previous state for true difference computation
        A_prev = self.A.copy()

        # Store the averrage convolution
        self.convolution_field = np.zeros_like(self.convolution_field)

        A = self.A
        G = np.zeros_like(A)

        # -----------------------
        # Kernel dynamics
        # -----------------------
        for i, k in enumerate(self.kernels):

            # interaction weights (cross-channel coupling)
            interaction_row = k.creature.interaction[i]

            # -----------------------
            # Convolution step
            # U = K(A)
            # where K is the kernel operator applied to field A(t)
            # -----------------------
            U = k.convolve(A, interaction_row=interaction_row)
            self.convolution_field += U
            
            # -----------------------
            # Growth function
            # F(A) = growth(U) = growth(K(A))
            # G = F(A) = dA/dt (local growth rate field)
            # -----------------------
            G[..., i] = k.grow(U)

        # -----------------------
        # Store derivatives (diagnostics)
        # -----------------------

        # averrage Convolution over all kernels
        self.convolution_field /= len(self.kernels)

        # dA/dt (continuous-time growth rate)
        self.dA_dt_field = G

        # Euler update increment: ΔA ≈ dt * (dA/dt)
        self.dA_integration = self.dt * G

        # -----------------------
        # State update
        # -----------------------

        # Integrate forward in time
        self.A = np.clip(A + self.dA_integration, 0, 1)

        # True discrete change in state
        self.change_field = self.A - A_prev

        # Optional: symmetry-breaking noise (disabled by default)
        # self.A += 0.001 * np.random.randn(*self.A.shape)
        # self.A = np.clip(self.A, 0, 1)

    # -----------------------
    # Stamp into field
    # -----------------------

    def stamp(self, stamp_field=None, x=None, y=None, scale=1.0, channel=None, strength=None):
        # Apply a "stamp" (image or pattern) onto the field

        # Load the stamp field if not provided
        if stamp_field is None:
            stamp_field = self.kernels[0].creature.get_stamp()  # lazy load stamp

        # Use the creature's stamp strength if not provided
        if strength is None:
            strength = self.kernels[0].creature.stamp_strength

        # Scale and apply strength to the stamp
        patch = np.asarray(stamp_field * scale * strength)
   
        h, w = patch.shape  # Get the height and width of the stamp

        # Randomly select the position on the field if not provided
        if x is None:
            x = np.random.randint(0, self.size/2)
        if y is None:
            y = np.random.randint(0, self.size/2)

        # Clamp the stamp position to stay within the bounds of the field
        x_end = min(x + w, self.size)
        y_end = min(y + h, self.size)

        x = min(x, self.size - 1)
        y = min(y, self.size - 1)

        # Slice the patch to fit within the target region
        patch = patch[:(y_end - y), :(x_end - x)]

        # Apply the patch to the appropriate channel(s)
        if channel is not None:
            self.A[y:y_end, x:x_end, channel] += patch
        else:
            self.A[y:y_end, x:x_end, :] += patch[:, :, None]

        # Ensure the field values stay within the [0, 1] range
        self.A = np.clip(self.A, 0, 1)

    # -----------------------
    # controls
    # -----------------------
    def adjust_mu(self, d):
        # Adjust the 'mu' (mean) parameter of the selected kernel
        k = self.kernels[self.selected_kernel]
        k.mu = np.clip(k.mu + d, 0.01, 0.99)

    def adjust_sigma(self, d):
        # Adjust the 'sigma' (standard deviation) parameter of the selected kernel
        k = self.kernels[self.selected_kernel]
        k.sigma = np.clip(k.sigma + d, 0.001, 0.1)
        
    def adjust_dt(self, d):
        # Adjust the time step (dt) of the simulation
        self.dt = np.clip(self.dt + d, 0.001, 1.0)
