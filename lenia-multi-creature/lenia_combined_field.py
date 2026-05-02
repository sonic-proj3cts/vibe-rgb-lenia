import numpy as np
from lenia_creature_field import LeniaCreatureField

class LeniaCombinedField:
    def __init__(self, creatures, size=200, kernel_size=50):
        """
        Initialize the combined simulation containing multiple creatures.

        Parameters:
            creatures (list): List of Creature objects.
            size (int): Size of the simulation grid (size x size).
            kernel_size (int): Size of convolution kernels.
        """
        self.size = size  # Size of the simulation grid
        self.creatures = creatures  # Store all creatures

        # Combined field (used for rendering): sum of all creature fields
        self.A = np.zeros((size, size, 3), dtype=np.float32)
        
        # Create a separate field simulation for each creature
        self.creature_fields = [
            LeniaCreatureField(c, size=size, kernel_size=kernel_size)
            for c in creatures
        ]

    def step(self):
        """
        Advance the simulation by one time step.
        This involves stepping each creature's field and recombining them.
        """
        # Step each creature field individually
        for field in self.creature_fields:
            field.step(self.A)  # Calls the step function of each creature's field
                                # passes combined world view to step of creature field
                                # for evaluation with world interaction matrix
        
        # Recompute the combined field from all creature fields
        self._recompute_combined()

    def _recompute_combined(self):
        """
        Rebuild the combined field from all creature fields.
        """
        self.A.fill(0)  # IMPORTANT: don't replace the array!
        
        # Sum the A fields of each creature and recombine them
        for field in self.creature_fields:
            self.A += field.A

        # Clamp to ensure values are within [0, 1]
        np.clip(self.A, 0, 1, out=self.A)

    def stamp_field(self, index, x=None, y=None, scale=1.0, strength=None, rotation_deg=None):
        """
        Apply a stamp to a single creature field using an index.
        This is the core stamping logic used by stamp_all.
        """
        # Get the field corresponding to the index
        field = self.creature_fields[index]
        field.stamp_transform(x=x, y=y, strength=strength, rotation_deg=rotation_deg, scale=scale)

    def stamp_all(self, x=None, y=None, scale=1.0, strength=None):
        """
        Apply a stamp to every creature field using a shared helper.
        """
        for index in range(len(self.creature_fields)):
            self.stamp_field(index, x=x, y=y, scale=scale, strength=strength)

        self._recompute_combined()

    def reset_stamp(self, index, x=None, y=None, scale=1.0, strength=None, rotation_deg=None):
        """
        Apply a stamp to a single creature field using an index.
        This is the core stamping logic used by stamp_all.
        """
        field = self.creature_fields[index]
        field.reset_field()
        field.stamp_transform(x=x, y=y, strength=strength, rotation_deg=rotation_deg, scale=scale)

    def reset_blob(self):
        """
        Reset each creature's field to a random blob for all RGB channels and recombine the fields.
        Ensures each field gets its own random blob pattern.
        """
        n_blobs = 5  # Number of blobs to generate
        radius = 40  # Blob radius

        # Iterate over each field
        for field in self.creature_fields:
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
                noise = (np.random.rand(self.size, self.size) * 2 - 1) * envelope
                A += envelope + 0.8 * noise  # Add the envelope and noise to the field

            # Normalize the field so that values range from 0 to 1
            A -= A.min()  # Subtract the minimum value to make the range start from 0
            A /= (A.max() + 1e-8)  # Normalize the field to [0, 1]

            # Make it RGB by stacking the grayscale array in all three channels
            field.A = np.stack([A, A, A], axis=-1)  # Convert the field to RGB format

        # Recompute the combined field after resetting each field
        self._recompute_combined()

    def reset_noise(self, strength=0.3):
        """
        Reset each creature's field to random noise for all RGB channels and recombine the fields.
        The noise is the same for all creatures and is scaled by the strength parameter.
        """
        # Generate random noise once
        noise = np.random.rand(self.size, self.size)  # Generate random noise

        # Set each creature's field to the same noise, scaled by strength
        for field in self.creature_fields:
            field.A += np.stack([noise, noise, noise], axis=-1) * strength  # Apply the noise to RGB channels

        # Recompute the combined field after resetting
        self._recompute_combined()
    
    def reset_void(self):
        """
        Reset all creature fields to zero and recombine the fields.
        This effectively "empties" the field, setting all values to zero.
        """
        # Set each creature's field to zero
        for field in self.creature_fields:
            field.A.fill(0) # Set the field to all zeros

        # Recompute the combined field after resetting
        self._recompute_combined()
