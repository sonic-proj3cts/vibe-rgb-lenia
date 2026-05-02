import pygame
import numpy as np


class CombinedRenderer:
    def __init__(self, combined_field):
        """
        Renderer for the combined Lenia field.
        """
        self.sim = combined_field
        self.size = combined_field.size
        self.creature_index = 0
        self.mu_sigma_index = 0  # 0=R, 1=G, 2=B
        self.show_convolution = False  # Flag to toggle the convolution view
        self.show_dt_difference = False  # Flag to toggle the dt_difference_field view
                
        pygame.init()

        # Resizable window (starts maximized-ish)
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)

        pygame.display.set_caption("Combined Lenia Field")


    def toggle_dt_difference_view(self):
        """
        Toggle the visibility of the dt_difference_field view.
        """
        self.show_dt_difference = not self.show_dt_difference
        print(f"DT Difference view {'enabled' if self.show_dt_difference else 'disabled'}.")

    def toggle_convoluted_view(self):
        """
        Toggle the visibility of the convolved kernel view.
        """
        self.show_convolution = not self.show_convolution
        print(f"Convolution view {'enabled' if self.show_convolution else 'disabled'}.")

    def to_surface(self, img):
        """
        Convert numpy array → pygame Surface if needed.
        """
        if isinstance(img, np.ndarray):
            # Convert the numpy array to an 8-bit range [0, 255]
            img = np.nan_to_num(img * 255, nan=0, posinf=255, neginf=0).astype(np.uint8)

            # Ensure 3 channels (RGB) if it's grayscale
            if img.ndim == 2:
                img = np.stack([img, img, img], axis=-1)

            # Convert the numpy array to a pygame surface
            surf = pygame.surfarray.make_surface(img.swapaxes(0, 1))
            return surf.convert()  # <-- IMPORTANT

        return img.convert_alpha() if img.get_alpha() else img.convert()

    def draw(self):
        import pygame
        import numpy as np

        # -------------------------
        # SELECT CURRENT CREATURE
        # -------------------------
        if len(self.sim.creature_fields) == 0:
            return

        field = self.sim.creature_fields[self.creature_index % len(self.sim.creature_fields)]

        # -------------------------
        # SIMULATION SURFACE
        # -------------------------
        surf = self.to_surface(self.sim.A)

        screen_width, screen_height = self.screen.get_size()

        scale = min(screen_width / self.size, screen_height / self.size)
        new_size = (int(self.size * scale), int(self.size * scale))

        scaled_surf = pygame.transform.smoothscale(surf, new_size)

        x = 0
        y = (screen_height - new_size[1]) // 2

        # ✅ CACHE HERE
        self.sim_rect = pygame.Rect(x, y, new_size[0], new_size[1])
        self.sim_draw_size = new_size

        self.screen.fill((0, 0, 0))
        self.screen.blit(scaled_surf, (x, y))

        pygame.draw.rect(
            self.screen,
            (255, 0, 0),
            pygame.Rect(x, y, new_size[0], new_size[1]),
            3
        )

        # -------------------------
        # UI PANEL
        # -------------------------
        ui_x = new_size[0]
        ui_width = screen_width - new_size[0]

        if ui_width <= 0:
            pygame.display.flip()
            return

        pygame.draw.rect(
            self.screen,
            (0, 255, 0),
            pygame.Rect(ui_x, 0, ui_width, screen_height),
            2
        )

        top_h = screen_height // 3
        bottom_h = screen_height - top_h

        pygame.draw.line(
            self.screen,
            (0, 255, 0),
            (ui_x, top_h),
            (screen_width, top_h),
            2
        )

        # =====================================================
        # 1) STAMP (TOP 1/3)
        # =====================================================
        try:
            stamp = field.creature.get_stamp()

            if not isinstance(stamp, np.ndarray):
                stamp = pygame.surfarray.array3d(stamp).mean(axis=2) / 255.0
                stamp = np.stack([stamp] * 3, axis=-1)

            stamp_surf = self.to_surface(stamp)

            max_w = ui_width - 20
            max_h = top_h - 20

            scale_factor = min(
                max_w / stamp_surf.get_width(),
                max_h / stamp_surf.get_height()
            )

            new_size_stamp = (
                int(stamp_surf.get_width() * scale_factor),
                int(stamp_surf.get_height() * scale_factor)
            )

            stamp_scaled = pygame.transform.smoothscale(stamp_surf, new_size_stamp)

            stamp_x = ui_x + (ui_width - new_size_stamp[0]) // 2
            stamp_y = (top_h - new_size_stamp[1]) // 2

            self.screen.blit(stamp_scaled, (stamp_x, stamp_y))

        except Exception as e:
            print("Error loading stamp:", e)

        # =====================================================
        # 2) KERNELS (RGB)
        # =====================================================
        try:
            kernels = field.kernels

            padding = 10
            available_width = ui_width - 4 * padding
            kernel_width = available_width // 3
            kernel_height = (bottom_h // 2) - 30

            colors = [
                np.array([1.0, 0.0, 0.0]),
                np.array([0.0, 1.0, 0.0]),
                np.array([0.0, 0.0, 1.0])
            ]

            font = pygame.font.SysFont("Arial", 16)

            text_y = top_h + kernel_height + 10
            x_offset = ui_x + 10

            for i, k in enumerate(kernels[:3]):
                img = k.kernel

                img = img - img.min()
                img = img / (img.max() + 1e-8)

                rgb = img[..., None] * colors[i]

                surf_k = self.to_surface(rgb)

                surf_k = pygame.transform.smoothscale(
                    surf_k,
                    (kernel_width, kernel_height)
                )

                k_x = ui_x + padding + i * (kernel_width + padding)
                k_y = top_h + 10

                self.screen.blit(surf_k, (k_x, k_y))

                pygame.draw.rect(
                    self.screen,
                    (0, 255, 0),
                    pygame.Rect(k_x, k_y, kernel_width, kernel_height),
                    1
                )

        except Exception as e:
            print("Error drawing kernels:", e)

        # =====================================================
        # 3) MU / SIGMA TEXT (ONE LINE ROW)
        # =====================================================
        font = pygame.font.SysFont("Arial", 16)

        text_y = top_h + kernel_height + 10

        if len(self.sim.creature_fields) > 0:

            kernels = field.kernels

            x_offset = ui_x + 10

            for i, k in enumerate(kernels[:3]):

                is_selected = (i == self.mu_sigma_index)

                prefix = ">" if is_selected else " "

                txt = f"{prefix} K{i+1}: μ={k.mu:.3f}  σ={k.sigma:.3f}"

                # highlight selected channel slightly
                color = (255, 220, 120) if is_selected else (255, 255, 255)

                label = font.render(txt, True, color)
                self.screen.blit(label, (x_offset, text_y))

                x_offset += label.get_width() + 58

        # =====================================================
        # 4) GROWTH FUNCTION GRAPH (RGB OVERLAY)
        # =====================================================
        try:
            kernels = field.kernels

            font = pygame.font.SysFont("Arial", 14)

            plot_top = text_y + 25
            plot_height = bottom_h - (kernel_height + 70)

            padding = 10
            plot_x = ui_x + padding
            plot_y = plot_top
            plot_width = ui_width - 2 * padding

            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                pygame.Rect(plot_x, plot_y, plot_width, plot_height),
                1
            )

            mid_y = plot_y + plot_height // 2
            pygame.draw.line(
                self.screen,
                (80, 80, 80),
                (plot_x, mid_y),
                (plot_x + plot_width, mid_y),
                1
            )

            colors = [
                (255, 80, 80),
                (80, 255, 80),
                (80, 80, 255)
            ]

            U_vals = np.linspace(0, 1, 200)

            for i, k in enumerate(kernels[:3]):
                pts = []

                for u in U_vals:
                    U = np.full((1, 1), u)
                    g = k.grow(U)[0, 0]

                    px = plot_x + int(u * plot_width)
                    py = plot_y + int((1 - (g + 1) / 2) * plot_height)

                    pts.append((px, py))

                pygame.draw.lines(self.screen, colors[i], False, pts, 2)

            label = font.render("Growth functions (R/G/B)", True, (255, 255, 255))
            self.screen.blit(label, (plot_x + 5, plot_y + 5))

        except Exception as e:
            print("Error drawing growth graph:", e)

        # =====================================================
        # 5) DT DISPLAY (BOTTOM LEFT OF UI)
        # =====================================================
        try:
            font = pygame.font.SysFont("Arial", 18)

            dt_value = getattr(self.sim, "dt", None)

            if dt_value is None and len(self.sim.creature_fields) > 0:
                dt_value = self.sim.creature_fields[self.creature_index].dt  # fallback

            txt = f"dt: {dt_value:.5f}"

            label = font.render(txt, True, (200, 200, 255))

            # bottom-left inside UI panel
            dt_x = ui_x + 10
            dt_y = screen_height - label.get_height() - 10

            self.screen.blit(label, (dt_x, dt_y))

        except Exception as e:
            print("Error drawing dt:", e)

        # -------------------------
        # UI PANEL - CONVOLVED FIELD (Toggleable Overlay)
        # -------------------------
        if self.show_convolution:
            # Get the current creature's field
            field = self.sim.creature_fields[self.creature_index % len(self.sim.creature_fields)]

            # Get the convolved field from the creature field
            convolved_field = field.get_convolved_field()

            # Scale it to fit inside the UI panel (same as other UI items)
            convolved_surf = self.to_surface(convolved_field)

            # Calculate scaling factor and size for convolution
            scale_factor = min(new_size[0] / convolved_surf.get_width(), new_size[1] / convolved_surf.get_height())
            convolved_surf = pygame.transform.smoothscale(convolved_surf, (int(convolved_surf.get_width() * scale_factor), int(convolved_surf.get_height() * scale_factor)))

            # Position it over the simulation field (scaled)
            self.screen.blit(convolved_surf, (x, y))

        # -------------------------
        # UI PANEL - DT DIFFERENCE FIELD (Toggleable Overlay)
        # -------------------------
        if self.show_dt_difference:
            # Get the current creature's field
            field = self.sim.creature_fields[self.creature_index % len(self.sim.creature_fields)]

            # Get the dt_difference_field from the creature field
            dt_diff_field = field.get_dt_difference_field()

            # Convert the dt_diff_field to a surface
            dt_diff_surf = self.to_surface(dt_diff_field)

            # Apply transparency by setting the alpha channel
            dt_diff_surf.set_alpha(256) 

            # Calculate scaling factor and size for dt_difference
            scale_factor = min(new_size[0] / dt_diff_surf.get_width(), new_size[1] / dt_diff_surf.get_height())
            dt_diff_surf = pygame.transform.smoothscale(dt_diff_surf, (int(dt_diff_surf.get_width() * scale_factor), int(dt_diff_surf.get_height() * scale_factor)))

            # Position it over the simulation field (scaled)
            self.screen.blit(dt_diff_surf, (x, y))

        # -------------------------
        # FINAL FLIP
        # -------------------------
        pygame.display.flip()
                    
    def draw_next_creature(self):
        if len(self.sim.creature_fields) == 0:
            return
        self.creature_index = (self.creature_index + 1) % len(self.sim.creature_fields)

    def draw_prev_creature(self):
        if len(self.sim.creature_fields) == 0:
            return
        self.creature_index = (self.creature_index - 1) % len(self.sim.creature_fields)

    def adjust_mu(self, delta):    # changes mu's of current creature
        field = self.sim.creature_fields[self.creature_index % len(self.sim.creature_fields)]
        field.adjust_mu(self.mu_sigma_index, delta)

    def adjust_sigma(self, delta): # changes sigma's of current creature
        field = self.sim.creature_fields[self.creature_index % len(self.sim.creature_fields)]
        field.adjust_sigma(self.mu_sigma_index, delta)        

    def adjust_dt(self, delta):    # changes animation time step of current creature
        field = self.sim.creature_fields[self.creature_index % len(self.sim.creature_fields)]
        field.adjust_dt(delta)

    def  prev_mu_sigma(self):
        self.mu_sigma_index=(self.mu_sigma_index - 1) % 3
        
    def  next_mu_sigma(self):
        self.mu_sigma_index=(self.mu_sigma_index + 1) % 3
        
    def screen_to_sim(self, mouse_pos):
        if not hasattr(self, "sim_rect"):
            return None  # draw() hasn't run yet

        mx, my = mouse_pos

        if not self.sim_rect.collidepoint(mx, my):
            return None

        rel_x = (mx - self.sim_rect.x) / self.sim_rect.width
        rel_y = (my - self.sim_rect.y) / self.sim_rect.height

        sim_x = int(rel_x * self.size)
        sim_y = int(rel_y * self.size)

        return sim_x, sim_y
