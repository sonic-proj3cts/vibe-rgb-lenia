import numpy as np
import pygame


class Renderer:
    def __init__(self, sim):
        self.sim = sim

        self.graph_h = 120
        self.show_integration_field = False
        self.show_growth_field = False
        self.show_change_field = False
        self.show_convolution_field = False
        
        pygame.init()
        info = pygame.display.Info()

        self.screen = pygame.display.set_mode(
            (info.current_w, info.current_h),
            pygame.RESIZABLE
        )

        self.graph_surface = pygame.Surface((self.sim.size, self.graph_h))
        self.font = pygame.font.SysFont("consolas", 18)

    # -----------------------
    # FIELD
    # -----------------------
    def render_field(self):
        field = np.nan_to_num(self.sim.A * 255, nan=0, posinf=255, neginf=0)
        field = field.astype(np.uint8)
        return pygame.surfarray.make_surface(field.swapaxes(0, 1))

    # -----------------------
    # KERNELS
    # -----------------------
    def render_kernels(self):
        imgs = []
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

        for i, k in enumerate(self.sim.kernels):
            arr = k.kernel

            arr = (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)
            arr = np.power(arr, 0.4)

            color = colors[i % 3]
            img = np.zeros((arr.shape[0], arr.shape[1], 3))

            for c in range(3):
                img[..., c] = arr * (color[c] / 255)

            imgs.append((img * 255).astype(np.uint8))

        return imgs

    # -----------------------
    # GRAPH
    # -----------------------
    def render_graph(self):
        self.graph_surface.fill((10, 10, 10))

        u = np.linspace(0, 1, 200)
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

        for i, k in enumerate(self.sim.kernels):
            g = k.grow(u)
            g = (g - g.min()) / (g.max() - g.min() + 1e-8)
            g = self.graph_h - g * self.graph_h

            for j in range(len(u) - 1):
                x1 = int(j * self.sim.size / len(u))
                x2 = int((j + 1) * self.sim.size / len(u))
                y1 = int(g[j])
                y2 = int(g[j + 1])

                pygame.draw.line(
                    self.graph_surface,
                    colors[i % 3],
                    (x1, y1),
                    (x2, y2),
                    2
                )

    # -----------------------
    # DRAW MAIN
    # -----------------------

    def draw(self):
        # -----------------------
        # UPDATE LAYOUT FIRST
        # -----------------------
        self.update_layout()

        self.screen.fill((0, 0, 0))

        win_w, win_h = pygame.display.get_window_size()

        # -----------------------
        # GRAPH UPDATE
        # -----------------------
        self.render_graph()

        # -----------------------
        # SIMULATION SURFACE
        # -----------------------
        sim_surface = pygame.Surface((self.sim.size, self.sim.size))
        sim_surface.fill((0, 0, 0))

        # base field
        field = self.render_field()
        sim_surface.blit(field, (0, 0))

        # -----------------------
        # OVERLAY SELECTION
        # -----------------------
        data = None

        if self.show_change_field:
            data = self.sim.change_field

        elif self.show_convolution_field:
            data = self.sim.convolution_field

        elif self.show_integration_field:
            data = self.sim.dA_integration

        elif self.show_growth_field:
            data = self.sim.dA_dt_field

        # -----------------------
        # OVERLAY RENDER
        # -----------------------
        if data is not None:
            d = np.nan_to_num(data)

            if d.ndim == 2:
                d = np.stack([d, d, d], axis=-1)

            d_min, d_max = d.min(), d.max()
            if d_max - d_min > 1e-8:
                d = (d - d_min) / (d_max - d_min)
            else:
                d = np.zeros_like(d)

            d = (d * 255).astype(np.uint8)

            overlay = pygame.surfarray.make_surface(d.swapaxes(0, 1))
            sim_surface.blit(overlay, (0, 0))

        # -----------------------
        # SCALE TO LEFT PANEL
        # -----------------------
        sim_scaled = pygame.transform.smoothscale(
            sim_surface,
            (self.left_rect.width, self.left_rect.height)
        )

        self.screen.blit(sim_scaled, self.left_rect.topleft)

        # -----------------------
        # RIGHT PANEL
        # -----------------------
        self.draw_side_panel(self.right_rect)

        # -----------------------
        # DEBUG BORDERS
        # -----------------------
        pygame.draw.rect(self.screen, (255, 0, 0), self.left_rect, 2, border_radius=6)
        pygame.draw.rect(self.screen, (0, 255, 0), self.right_rect, 2, border_radius=6)

        # -----------------------
        # RIGHT SPLIT DEBUG
        # -----------------------
        stamp_h = self.right_rect.height // 3
        rest_h = self.right_rect.height - stamp_h

        top_rect = pygame.Rect(
            self.right_rect.x,
            self.right_rect.y,
            self.right_rect.width,
            stamp_h
        )

        bottom_rect = pygame.Rect(
            self.right_rect.x,
            self.right_rect.y + stamp_h,
            self.right_rect.width,
            rest_h
        )

        pygame.draw.rect(self.screen, (0, 255, 0), top_rect, 2)
        pygame.draw.rect(self.screen, (0, 255, 0), bottom_rect, 2)

        pygame.display.flip()

    # -----------------------
    # SIDE PANEL
    # -----------------------
    def draw_side_panel(self, rect):
        panel = pygame.Surface((rect.width, rect.height))
        panel.fill((0, 0, 0))

        padding = 20

        # =========================
        # SPLIT LAYOUT
        # =========================
        stamp_h = rect.height // 3
        rest_h = rect.height - stamp_h

        stamp_rect = pygame.Rect(0, 0, rect.width, stamp_h)
        rest_rect = pygame.Rect(0, stamp_h, rect.width, rest_h)

        # =========================
        # STAMP AREA (TOP 1/3)
        # =========================
        creature = self.sim.kernels[0].creature

        stamp_surface = None
        stamp_text = "No stamp"

        if hasattr(creature, "stamp_filename") and creature.stamp_filename is not None:
            stamp_text = f"Stamp: {creature.stamp_filename}"
            stamp = creature.get_stamp()

            if stamp is not None:
                stamp = np.nan_to_num(stamp)

                if stamp.ndim == 2:
                    stamp = np.stack([stamp] * 3, axis=-1)

                maxv = stamp.max()
                if maxv <= 1.0:
                    stamp = np.clip(stamp, 0, 1)
                    stamp = (stamp * 255).astype(np.uint8)
                else:
                    stamp = np.clip(stamp, 0, 255).astype(np.uint8)

                stamp_surface = pygame.surfarray.make_surface(stamp.swapaxes(0, 1))

        if stamp_surface is not None:
            max_w = rect.width - 2 * padding
            max_h = stamp_h - 2 * padding

            sw, sh = stamp_surface.get_size()
            scale = min(max_w / sw, max_h / sh)

            new_size = (int(sw * scale), int(sh * scale))
            stamp_surface = pygame.transform.smoothscale(stamp_surface, new_size)

            x = padding + (max_w - new_size[0]) // 2
            y = stamp_rect.y + (stamp_h - new_size[1]) // 2

            panel.blit(stamp_surface, (x, y))

        # =========================
        # REST AREA (BOTTOM 2/3)
        # =========================
        y = rest_rect.y + padding

        # ---- Kernels (EVEN SPACING) ----
        kernels = self.render_kernels()

        available_w = rect.width - 2 * padding
        n = len(kernels)

        gap = 10
        total_gap = gap * (n - 1)
        kernel_w = (available_w - total_gap) // n

        x = padding
        max_h = 0

        for k_img in kernels:
            surf = pygame.surfarray.make_surface(k_img.swapaxes(0, 1))

            scale = kernel_w / surf.get_width()
            h = int(surf.get_height() * scale)

            surf = pygame.transform.smoothscale(surf, (kernel_w, h))
            panel.blit(surf, (x, y))

            # green outline per kernel
            pygame.draw.rect(
                panel,
                (0, 255, 0),
                pygame.Rect(x, y, kernel_w, h),
                2
            )

            x += kernel_w + gap
            max_h = max(max_h, h)

        y += max_h + 20

        # =========================
        # HUD
        # =========================
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]

        row_width = rect.width - 2 * padding
        col_w = row_width // len(self.sim.kernels)

        for i, k in enumerate(self.sim.kernels):
            x0 = padding + i * col_w

            selected = ">" if i == self.sim.selected_kernel else " "
            mu_text = self.font.render(f"{selected} μ:{k.mu:.4f}", True, colors[i % 3])
            sigma_text = self.font.render(f"σ:{k.sigma:.4f}", True, colors[i % 3])

            panel.blit(mu_text, (x0, y))
            panel.blit(sigma_text, (x0 + mu_text.get_width() + 10, y))

        y += 30


        # ---- Graph (fill remaining vertical space, reserve DT space) ----
        graph_w = rect.width - 2 * padding

        dt_height = self.font.get_height()   # reserve space for dt

        remaining_h = rest_rect.bottom - y - padding - dt_height
        remaining_h = max(50, remaining_h)

        graph = pygame.transform.smoothscale(
            self.graph_surface,
            (graph_w, remaining_h)
        )

        panel.blit(graph, (padding, y))
        y += remaining_h + 20

        # =========================
        # DT TEXT (BOTTOM + BACKGROUND)
        # =========================
        dt_text = self.font.render(f"dt = {self.sim.dt:.5f}", True, (255, 255, 255))

        dt_x = padding
        dt_y = rect.height - dt_text.get_height() - 10

        # black background behind text (with padding)
        bg_pad_x = 8
        bg_pad_y = 4

        bg_rect = pygame.Rect(
            dt_x - bg_pad_x,
            dt_y - bg_pad_y,
            dt_text.get_width() + bg_pad_x * 2,
            dt_text.get_height() + bg_pad_y * 2
        )

        pygame.draw.rect(panel, (0, 0, 0), bg_rect)

        panel.blit(dt_text, (dt_x, dt_y))

        # =========================
        # BLIT PANEL
        # =========================
        self.screen.blit(panel, rect.topleft)

    def screen_to_sim(self, mx, my):
        """
        Convert screen coordinates → simulation coordinates (Lenia grid space)
        using the current left_rect (simulation viewport).
        """

        # Safety: layout must exist
        if not hasattr(self, "left_rect"):
            return None

        # Check if click is inside simulation area
        if not self.left_rect.collidepoint(mx, my):
            return None

        # Convert to local coordinates inside simulation panel
        local_x = mx - self.left_rect.x
        local_y = my - self.left_rect.y

        # Scale screen → simulation grid
        scale_x = self.sim.size / self.left_rect.width
        scale_y = self.sim.size / self.left_rect.height

        sim_x = int(local_x * scale_x)
        sim_y = int(local_y * scale_y)

        # Clamp to valid range
        sim_x = max(0, min(self.sim.size - 1, sim_x))
        sim_y = max(0, min(self.sim.size - 1, sim_y))

        return sim_x, sim_y

    def update_layout(self):
        """
        Computes and stores screen layout rectangles.
        This must be called every frame before using screen transforms.
        """
        win_w, win_h = pygame.display.get_window_size()

        # LEFT: simulation view
        self.left_rect = pygame.Rect(
            0, 0,
            win_w // 2,
            win_h
        )

        # RIGHT: UI panel
        self.right_rect = pygame.Rect(
            win_w // 2, 0,
            win_w // 2,
            win_h
        )
