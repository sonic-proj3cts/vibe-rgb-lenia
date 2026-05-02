import numpy as np  # Importing numpy for numerical array operations
from numpy.fft import fft2, ifft2, ifftshift  # Importing FFT functions for fast Fourier transforms

# -----------------------
# Kernel Class 
# -----------------------
class Kernel:
    """
    The Kernel class represents a convolutional kernel that is used to process and modify fields (e.g., creatures, environments).
    It defines how the kernel is created, its properties, and how it interacts with a field via convolution and growth.
    """
    def __init__(self, world_size, kernel_size, radius,
                 ring_centers, ring_width, ring_weights,
                 mu, sigma, growth_mode=0, cutoff=2.0,
                 stamp_strength=1.0):
        """
        Initializes the Kernel object with various parameters that define its behavior.
        
        Parameters:
            - world_size: Size of the world (height and width of the grid the kernel operates on)
            - kernel_size: Size of the kernel (affects the convolutional filter size)
            - radius: The radius used for determining distances in the kernel
            - ring_centers: List of the centers of the rings that make up the kernel
            - ring_width: Width of the rings (affects how spread out the rings are)
            - ring_weights: Weights associated with each ring (determines their influence)
            - mu: Growth parameter (central value for growth calculation)
            - sigma: Growth parameter (standard deviation for growth calculation)
            - growth_mode: Determines the growth function behavior (0 for Gaussian, 1 for a sharp sigmoidal growth, etc.)
            - cutoff: Distance cutoff beyond which kernel values become zero
            - stamp_strength: Strength of the "stamp" (effect) that the kernel applies to the environment
        """
        # Store parameters
        self.world_size = world_size
        self.kernel_size = kernel_size
        self.radius = radius
        self.cutoff = cutoff
        self.ring_centers = ring_centers
        self.ring_width = ring_width
        self.ring_weights = ring_weights

        self.mu = mu
        self.sigma = sigma
        self.growth_mode = growth_mode  # Store the growth mode to later determine the growth function
        self.stamp_strength = stamp_strength

        # Create the kernel (a 2D filter) based on the provided parameters
        self.kernel = self._create_kernel()
        
        # Build the FFT (Fast Fourier Transform) of the kernel, which allows for efficient convolution
        self.K_fft = self._build_fft()

    def _create_kernel(self):
        """
        Creates a 2D kernel based on the specified ring centers, widths, and weights.
        The kernel defines the behavior of how each ring affects the field.
        
        Returns:
            np.ndarray: The generated kernel as a 2D array.
        """
        size = self.kernel_size  # Size of the kernel (filter)
        
        # Create a grid of coordinates relative to the kernel center (x and y)
        y, x = np.ogrid[-size//2:size//2, -size//2:size//2]
        
        # Compute the distance from the center for each point in the grid
        dist = np.sqrt(x**2 + y**2)
        
        # Normalize the distance by the radius
        r = dist / self.radius

        # Initialize the kernel to zero
        k = np.zeros_like(r)

        # Loop through each ring center and weight, and build the kernel by applying a Gaussian function
        for c, w in zip(self.ring_centers, self.ring_weights):
            k += w * np.exp(-((r - c) ** 2) / (2 * self.ring_width ** 2))  # Apply the Gaussian function

        # Set kernel values to zero beyond the cutoff distance
        k[r > self.cutoff] = 0
        
        # Normalize the kernel values so that the sum of all values equals 1
        k /= k.sum() + 1e-8  # Add a small value to prevent division by zero
        return k

    def _build_fft(self):
        """
        Builds the Fast Fourier Transform (FFT) of the kernel, which is used to perform efficient convolutions.
        
        Returns:
            np.ndarray: The FFT of the kernel, ready for convolution in the frequency domain.
        """
        # Create a zero array of size (world_size, world_size)
        K = np.zeros((self.world_size, self.world_size))
        
        # Find the center of the world size (for placing the kernel in the center)
        cx = cy = self.world_size // 2
        ks = self.kernel_size // 2  # Half the kernel size
        
        # Place the kernel in the center of the larger K array
        K[cx-ks:cx+ks, cy-ks:cy+ks] = self.kernel
        
        # Compute the FFT of the kernel and return it
        return fft2(ifftshift(K))  # Shift the kernel for proper FFT alignment

    def convolve(self, field, interaction_row=None):
        """
        Convolve the kernel with the provided field to produce an output.
        
        Parameters:
            field: The input field (H, W, 3) which has three channels (e.g., RGB channels)
            interaction_row: Optional parameter to mix channels according to specific weights
            
        Returns:
            np.ndarray: The result of applying the kernel (in the frequency domain) to the field.
        """
        # Assert that the field has the correct dimensions (H, W, 3)
        #assert field.ndim == 3 and field.shape[2] == 3, f"Expected (H,W,3), got {field.shape}"

        # If the field has only two dimensions, add a third dimension (for RGB channels)
        #if field.ndim == 2:
        #    field = field[..., None]

        H, W, C = field.shape  # Height, width, and number of channels in the field

        # Initialize an empty array to store the mixed channels
        mixed = np.zeros((H, W), dtype=np.float32)

        # If an interaction row is provided, mix the channels accordingly
        for c in range(3):
            mixed += interaction_row[c] * field[..., c]  # Multiply the field by the interaction weights

        # Perform convolution in the frequency domain using FFT
        return np.real(ifft2(fft2(mixed) * self.K_fft))  # Use inverse FFT to return the convolved result

    def grow(self, U, max_val=1.0):
        """
        Grow the kernel's output based on the field values and the growth mode.
        
        Parameters:
            U: The input field values (to grow)
            max_val: The maximum value for the growth (used to remap the output to a desired range)
            
        Returns:
            np.ndarray: The grown field values based on the selected growth mode.
        """
        # Different growth modes define how the kernel's output will grow
        if self.growth_mode == 0:
            # Gaussian growth
            base = np.exp(-((U - self.mu)**2) / (2 * self.sigma**2)) * 2 - 1
        elif self.growth_mode == 1:
            # Sharp sigmoidal growth
            base = 2 / (1 + ((U - self.mu)/self.sigma)**4) - 1
        elif self.growth_mode == 2:
            # Tanh growth
            base = np.tanh((U - self.mu) / self.sigma)
        elif self.growth_mode == 3:
            # Inverted Gaussian growth
            base = 1 - 2*np.exp(-((U - self.mu)**2)/(2*self.sigma**2))

        # Remap the growth result from [-1,1] to [-1,max_val]
        return -1 + (base + 1) * (max_val + 1) / 2  # Rescale to [0, max_val]
