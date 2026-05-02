import numpy as np
from numpy.fft import fft2, ifft2, ifftshift

# -----------------------
# Kernel 
# -----------------------
class Kernel:
    def __init__(self, world_size, kernel_size, radius,
                 ring_centers, ring_width, ring_weights,
                 mu, sigma, growth_mode=0, cutoff=2.0,
                 stamp_strength=1.0):
        """
        Initialize the kernel which defines how each ring affects the field
        based on the provided parameters. The kernel uses a convolution process 
        to influence the field over time.
        
        Parameters:
            world_size (int): The size of the world field (height and width).
            kernel_size (int): The size of the kernel filter (odd number).
            radius (float): The effective radius of influence for the kernel.
            ring_centers (list): List of ring centers defining different radius bands.
            ring_width (float): The width of each ring.
            ring_weights (list): List of weights for each ring.
            mu (float): Mean value for the growth function.
            sigma (float): Standard deviation for the growth function.
            growth_mode (int): Defines the growth behavior (e.g., Gaussian, Sigmoidal).
            cutoff (float): Maximum distance for the kernel to influence, beyond which it has no effect.
            stamp_strength (float): Strength of the kernel's effect when applied to the field.
        """
        
        # Store the parameters
        self.world_size = world_size
        self.kernel_size = kernel_size
        self.radius = radius
        self.cutoff = cutoff
        self.ring_centers = ring_centers
        self.ring_width = ring_width
        self.ring_weights = ring_weights
        self.mu = mu
        self.sigma = sigma
        self.growth_mode = growth_mode
        self.stamp_strength = stamp_strength  # Store stamp strength for use in the convolution

        # Create the kernel and its Fourier transform
        self.kernel = self._create_kernel()
        self.K_fft = self._build_fft()

    def _create_kernel(self):
        """
        Creates a 2D kernel that determines how each ring affects the field based on 
        the provided parameters like ring centers, widths, and weights. The kernel is 
        Gaussian-based and has a cutoff distance beyond which it has no effect.

        Returns:
            np.ndarray: The generated kernel as a 2D array.
        """
        size = self.kernel_size  # Size of the kernel (filter)
        
        # Generate a grid of coordinates relative to the kernel's center
        y, x = np.ogrid[-size//2:size//2, -size//2:size//2]
        
        # Calculate the Euclidean distance from the kernel's center for each point
        dist = np.sqrt(x**2 + y**2)
        
        # Normalize the distance by dividing by the kernel radius
        r = dist / self.radius

        # Initialize an empty kernel array
        k = np.zeros_like(r)

        # Build the kernel by adding Gaussian functions centered at each ring center
        for c, w in zip(self.ring_centers, self.ring_weights):
            k += w * np.exp(-((r - c) ** 2) / (2 * self.ring_width ** 2))  # Apply Gaussian weighting

        # Apply cutoff: Set values beyond the specified distance (cutoff) to zero
        k[r > self.cutoff] = 0
        
        # Normalize the kernel such that its sum equals 1 (avoids kernel amplification)
        k /= k.sum() + 1e-8  # Small value added to prevent division by zero
        return k
        
    def _build_fft(self):
        """
        Builds the Fourier transform of the kernel. This allows for efficient 
        convolution in the frequency domain using FFT (Fast Fourier Transform).
        
        Returns:
            np.ndarray: The kernel's Fourier transform.
        """
        K = np.zeros((self.world_size, self.world_size))  # Create a zero-padded field for the kernel
        
        # Find the center of the world field (used to place the kernel at the center)
        cx = cy = self.world_size // 2
        ks = self.kernel_size // 2  # Half size of the kernel

        # Place the kernel in the center of the world field
        K[cx-ks:cx+ks, cy-ks:cy+ks] = self.kernel
        
        # Apply FFT shift to center the kernel, then take the Fourier transform
        return fft2(ifftshift(K))

    def convolve(self, field, interaction_row=None, world_field=None, world_interaction_row=None):
        """
        Perform the convolution operation between the kernel and the given field.
        This operation is performed in the frequency domain using FFT for efficiency.
        
        Parameters:
            field (np.ndarray): The own creature's field (height, width, 3 channels).
            interaction_row (np.ndarray): Weights for the creature's own field interaction.
            world_field (np.ndarray, optional): The full combined field (if provided).
            world_interaction_row (np.ndarray, optional): Weights for the worldview interaction.
        
        Returns:
            np.ndarray: The convolved field after applying the kernel's influence.
        """
        # Start by calculating the own-field contribution (the creature's own field)
        mixed = np.zeros_like(field[..., 0], dtype=np.float32)
        for c in range(3):
            mixed += interaction_row[c] * field[..., c]  # Apply the interaction weights for each color channel

        # If a world field and worldview interaction are provided, add the world’s contribution
        if world_field is not None and world_interaction_row is not None:
            for c in range(3):
                mixed += world_interaction_row[c] * world_field[..., c]

        # Perform the convolution in the frequency domain using FFT
        return np.real(ifft2(fft2(mixed) * self.K_fft))  # Return the inverse FFT of the product

    def grow(self, U, max_val=1.0):
        """
        Grow the field based on the input values and the selected growth mode.
        The growth is controlled by the kernel's growth mode, which determines the function
        used to modify the field values.
        
        Parameters:
            U (np.ndarray): The input field values to grow.
            max_val (float): The maximum growth value (used to remap the output to a desired range).
        
        Returns:
            np.ndarray: The grown field values after applying the growth function.
        """
        # Different growth modes apply different mathematical functions to modify the field
        if self.growth_mode == 0:
            # Gaussian growth mode: Applies a Gaussian distribution
            base = np.exp(-((U - self.mu) ** 2) / (2 * self.sigma ** 2)) * 2 - 1
        elif self.growth_mode == 1:
            # Sigmoidal growth mode: Sharp sigmoidal function
            base = 2 / (1 + ((U - self.mu) / self.sigma) ** 4) - 1
        elif self.growth_mode == 2:
            # Tanh growth mode: Applies the hyperbolic tangent function
            base = np.tanh((U - self.mu) / self.sigma)
        elif self.growth_mode == 3:
            # Inverted Gaussian growth mode: Inverse of the Gaussian
            base = 1 - 2 * np.exp(-((U - self.mu) ** 2) / (2 * self.sigma ** 2))

        # Rescale the growth result from [-1, 1] to [0, max_val] for appropriate range of field values
        return -1 + (base + 1) * (max_val + 1) / 2  # Rescale to the range [0, max_val]
