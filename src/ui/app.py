"""
Main Pygame application for Juego 21.
Integrates Model, Perception-Action Agent, and visual UI components.
"""
import sys
import pygame
from typing import Optional, List

from ..model.game import Game21
from ..model.agent import PerceptionActionAgent
from .constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    WINDOW_TITLE,
    COLOR_BG,
    COLOR_PANEL,
    COLOR_PANEL_BORDER,
    COLOR_HEADER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_ACCENT,
    COLOR_SUCCESS,
    COLOR_SUCCESS_BG,
    COLOR_WARNING,
    COLOR_DANGER,
    COLOR_INFO,
    COLOR_BTN_PRIMARY,
    COLOR_BTN_PRIMARY_HOVER,
    COLOR_BTN_SUCCESS,
    COLOR_BTN_SUCCESS_HOVER,
    COLOR_BTN_WARNING,
    COLOR_BTN_WARNING_HOVER,
    COLOR_BTN_SECONDARY,
    COLOR_BTN_SECONDARY_HOVER,
)
from .die_view import DieView
from .button import Button
from .particles import ParticleSystem


class Game21App:
    """Complete desktop GUI application for Juego 21."""

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.is_running = True

        # Game engine & agent
        self.game = Game21()
        self.agent = PerceptionActionAgent()

        # Visual subcomponents
        self.die_view1 = DieView(self.game.die1, center_x=340, center_y=300, size=150)
        self.die_view2 = DieView(self.game.die2, center_x=620, center_y=300, size=150)
        self.particles = ParticleSystem()

        # Fonts
        self._init_fonts()

        # Controls & Auto-play state
        self.auto_play = False
        self.auto_play_last_tick = 0
        self.auto_play_delay_ms = 700

        # Build UI buttons
        self.buttons: List[Button] = []
        self._create_buttons()

    def _init_fonts(self) -> None:
        """Initialize typography with robust system fallbacks."""
        font_names = ["segoeui", "arial", "helvetica", "sans-serif"]
        self.font_title = pygame.font.SysFont(font_names, 28, bold=True)
        self.font_header = pygame.font.SysFont(font_names, 20, bold=True)
        self.font_body = pygame.font.SysFont(font_names, 16)
        self.font_body_bold = pygame.font.SysFont(font_names, 16, bold=True)
        self.font_small = pygame.font.SysFont(font_names, 13)
        self.font_badge = pygame.font.SysFont(font_names, 12, bold=True)
        self.font_dice_q = pygame.font.SysFont(font_names, 64, bold=True)
        self.font_stats_num = pygame.font.SysFont(font_names, 36, bold=True)

    def _create_buttons(self) -> None:
        """Construct interactive UI buttons with layout coordinates."""
        btn_y1 = 440
        btn_y2 = 505
        btn_w = 170
        btn_h = 48

        # Row 1: Dice rolling actions
        self.btn_roll_both = Button(
            rect=pygame.Rect(115, btn_y1, btn_w, btn_h),
            text="Roll Both",
            shortcut="[Space]",
            color_normal=COLOR_BTN_PRIMARY,
            color_hover=COLOR_BTN_PRIMARY_HOVER,
            on_click=self.action_roll_both,
        )

        self.btn_roll_die1 = Button(
            rect=pygame.Rect(300, btn_y1, btn_w, btn_h),
            text="Roll Die 1",
            shortcut="[1]",
            color_normal=COLOR_BTN_SECONDARY,
            color_hover=COLOR_BTN_SECONDARY_HOVER,
            on_click=lambda: self.action_roll_die(1),
        )

        self.btn_roll_die2 = Button(
            rect=pygame.Rect(485, btn_y1, btn_w, btn_h),
            text="Roll Die 2",
            shortcut="[2]",
            color_normal=COLOR_BTN_SECONDARY,
            color_hover=COLOR_BTN_SECONDARY_HOVER,
            on_click=lambda: self.action_roll_die(2),
        )

        self.btn_agent_step = Button(
            rect=pygame.Rect(670, btn_y1, 185, btn_h),
            text="AI Step",
            shortcut="[A]",
            color_normal=(108, 92, 231),
            color_hover=(124, 110, 240),
            on_click=self.action_agent_step,
        )

        # Row 2: Fixing dice & utilities
        self.btn_fix_die1 = Button(
            rect=pygame.Rect(115, btn_y2, btn_w, btn_h),
            text="Fix Die 1",
            color_normal=COLOR_BTN_WARNING,
            color_hover=COLOR_BTN_WARNING_HOVER,
            on_click=lambda: self.action_fix_die(1),
        )

        self.btn_fix_die2 = Button(
            rect=pygame.Rect(300, btn_y2, btn_w, btn_h),
            text="Fix Die 2",
            color_normal=COLOR_BTN_WARNING,
            color_hover=COLOR_BTN_WARNING_HOVER,
            on_click=lambda: self.action_fix_die(2),
        )

        self.btn_auto_play = Button(
            rect=pygame.Rect(485, btn_y2, btn_w, btn_h),
            text="Auto-Play",
            shortcut="[P]",
            color_normal=(44, 62, 80),
            color_hover=(52, 73, 94),
            on_click=self.toggle_auto_play,
        )

        self.btn_new_game = Button(
            rect=pygame.Rect(670, btn_y2, 185, btn_h),
            text="New Game",
            shortcut="[R]",
            color_normal=COLOR_BTN_SUCCESS,
            color_hover=COLOR_BTN_SUCCESS_HOVER,
            on_click=self.action_new_game,
        )

        self.buttons = [
            self.btn_roll_both,
            self.btn_roll_die1,
            self.btn_roll_die2,
            self.btn_agent_step,
            self.btn_fix_die1,
            self.btn_fix_die2,
            self.btn_auto_play,
            self.btn_new_game,
        ]

    # --- Actions ---

    def action_roll_both(self) -> None:
        if not self.game.can_roll_both():
            return
        self.die_view1.start_roll_animation()
        self.die_view2.start_roll_animation()
        self.game.roll_both()
        self._check_victory()

    def action_roll_die(self, die_id: int) -> None:
        if not self.game.can_roll_die(die_id):
            return
        if die_id == 1:
            self.die_view1.start_roll_animation()
        else:
            self.die_view2.start_roll_animation()
        self.game.roll_die(die_id)
        self._check_victory()

    def action_fix_die(self, die_id: int) -> None:
        if not self.game.can_fix_die(die_id):
            return
        self.game.fix_die(die_id)
        self._check_victory()

    def action_agent_step(self) -> None:
        if self.game.game_over:
            return
        action, _ = PerceptionActionAgent.decide_action(self.game)
        if action == "ROLL_BOTH":
            self.die_view1.start_roll_animation()
            self.die_view2.start_roll_animation()
        elif action == "ROLL_DIE_1":
            self.die_view1.start_roll_animation()
        elif action == "ROLL_DIE_2":
            self.die_view2.start_roll_animation()
        PerceptionActionAgent.step(self.game)
        self._check_victory()

    def toggle_auto_play(self) -> None:
        self.auto_play = not self.auto_play
        if self.auto_play and self.game.game_over:
            self.action_new_game()
            self.auto_play = True
        self.btn_auto_play.text = "Pause Auto" if self.auto_play else "Auto-Play"
        self.btn_auto_play.color_normal = (230, 126, 34) if self.auto_play else (44, 62, 80)

    def action_new_game(self) -> None:
        self.game.reset()
        self.particles.clear()
        self.auto_play = False
        self.btn_auto_play.text = "Auto-Play"
        self.btn_auto_play.color_normal = (44, 62, 80)

    def _check_victory(self) -> None:
        if self.game.is_goal_reached() or self.game.game_over:
            self.particles.burst(WINDOW_WIDTH // 2, 280, count=90)
            if self.auto_play:
                self.auto_play = False
                self.btn_auto_play.text = "Auto-Play"
                self.btn_auto_play.color_normal = (44, 62, 80)

    def _update_button_states(self) -> None:
        """Enable or disable buttons according to game state restrictions."""
        if self.game.game_over:
            for btn in self.buttons:
                if btn != self.btn_new_game:
                    btn.is_enabled = False
            self.btn_new_game.is_enabled = True
            return

        self.btn_roll_both.is_enabled = self.game.can_roll_both()
        self.btn_roll_die1.is_enabled = self.game.can_roll_die(1) and (
            self.game.die2.is_fixed or self.game.die1.value is not None
        )
        self.btn_roll_die2.is_enabled = self.game.can_roll_die(2) and (
            self.game.die1.is_fixed or self.game.die2.value is not None
        )
        self.btn_fix_die1.is_enabled = self.game.can_fix_die(1)
        self.btn_fix_die2.is_enabled = self.game.can_fix_die(2)
        self.btn_agent_step.is_enabled = not self.game.game_over
        self.btn_auto_play.is_enabled = True
        self.btn_new_game.is_enabled = True

    # --- Main Loop & Event Handling ---

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                return

            # Button events
            for btn in self.buttons:
                btn.handle_event(event)

            # Die direct click events (click to fix)
            if self.die_view1.handle_event(event):
                self.action_fix_die(1)
            if self.die_view2.handle_event(event):
                self.action_fix_die(2)

            # Keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game.can_roll_both():
                        self.action_roll_both()
                    elif self.game.can_roll_die(1) and self.game.die2.is_fixed:
                        self.action_roll_die(1)
                    elif self.game.can_roll_die(2) and self.game.die1.is_fixed:
                        self.action_roll_die(2)
                elif event.key == pygame.K_1:
                    if self.game.can_fix_die(1):
                        self.action_fix_die(1)
                    elif self.game.can_roll_die(1):
                        self.action_roll_die(1)
                elif event.key == pygame.K_2:
                    if self.game.can_fix_die(2):
                        self.action_fix_die(2)
                    elif self.game.can_roll_die(2):
                        self.action_roll_die(2)
                elif event.key == pygame.K_a:
                    self.action_agent_step()
                elif event.key == pygame.K_p:
                    self.toggle_auto_play()
                elif event.key == pygame.K_r:
                    self.action_new_game()
                elif event.key == pygame.K_ESCAPE:
                    self.is_running = False

    def update(self) -> None:
        self.die_view1.update()
        self.die_view2.update()
        self.particles.update()
        self._update_button_states()

        # Handle auto-play agent progression with timed pacing
        if self.auto_play and not self.game.game_over:
            now = pygame.time.get_ticks()
            if (
                now - self.auto_play_last_tick >= self.auto_play_delay_ms
                and not self.die_view1.is_animating
                and not self.die_view2.is_animating
            ):
                self.action_agent_step()
                self.auto_play_last_tick = now

    def draw(self) -> None:
        self.screen.fill(COLOR_BG)

        self._draw_header()
        self._draw_status_cards()
        self._draw_advisor_panel()
        self._draw_dice_area()
        self._draw_controls()
        self._draw_victory_overlay()
        self._draw_footer()

        # Draw particles on top
        self.particles.draw(self.screen)

        pygame.display.flip()

    # --- Drawing Subroutines ---

    def _draw_header(self) -> None:
        """Top navigation bar."""
        header_rect = pygame.Rect(0, 0, WINDOW_WIDTH, 68)
        pygame.draw.rect(self.screen, COLOR_HEADER, header_rect)
        pygame.draw.line(self.screen, COLOR_PANEL_BORDER, (0, 68), (WINDOW_WIDTH, 68), 1)

        # Title
        title_surf = self.font_title.render("JUEGO 21", True, COLOR_TEXT_PRIMARY)
        self.screen.blit(title_surf, (28, 12))

        # Subtitle
        sub_text = "Target Goal: (2, 1) or (1, 2)  •  Performance Criterion: Minimize total rolls"
        sub_surf = self.font_small.render(sub_text, True, COLOR_TEXT_MUTED)
        self.screen.blit(sub_surf, (28, 44))

        # Target badge in top right
        target_badge = pygame.Rect(WINDOW_WIDTH - 210, 16, 182, 36)
        pygame.draw.rect(self.screen, (30, 42, 65), target_badge, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_TEXT_ACCENT, target_badge, width=1, border_radius=8)
        target_lbl = self.font_body_bold.render("TARGET: (2, 1) / (1, 2)", True, COLOR_TEXT_ACCENT)
        self.screen.blit(target_lbl, target_lbl.get_rect(center=target_badge.center))

    def _draw_status_cards(self) -> None:
        """Stats cards: Rolls/Cost Counter and Current Game State."""
        # Card 1: Roll / Turn Counter (Cost)
        card1_rect = pygame.Rect(28, 82, 220, 80)
        pygame.draw.rect(self.screen, COLOR_PANEL, card1_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, card1_rect, width=1, border_radius=10)

        lbl1 = self.font_small.render("TOTAL ROLLS (COST = 1)", True, COLOR_TEXT_MUTED)
        self.screen.blit(lbl1, (42, 92))

        val1 = self.font_stats_num.render(str(self.game.roll_count), True, COLOR_TEXT_PRIMARY)
        self.screen.blit(val1, (42, 114))

        # Card 2: Current Game State
        card2_rect = pygame.Rect(260, 82, 380, 80)
        pygame.draw.rect(self.screen, COLOR_PANEL, card2_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, card2_rect, width=1, border_radius=10)

        lbl2 = self.font_small.render("CURRENT STATE", True, COLOR_TEXT_MUTED)
        self.screen.blit(lbl2, (274, 92))

        if self.game.game_over:
            state_text = "GOAL ACHIEVED (VICTORY)"
            state_color = COLOR_SUCCESS
        elif self.game.roll_count == 0:
            state_text = "INITIAL (Unrolled Dice)"
            state_color = COLOR_INFO
        elif self.game.die1.is_fixed or self.game.die2.is_fixed:
            state_text = "IN PROGRESS (1 Die Fixed)"
            state_color = COLOR_WARNING
        else:
            state_text = "IN PROGRESS (Neither Fixed)"
            state_color = COLOR_TEXT_PRIMARY

        val2 = self.font_header.render(state_text, True, state_color)
        self.screen.blit(val2, (274, 118))

        # Card 3: Valid Actions Count
        card3_rect = pygame.Rect(652, 82, 280, 80)
        pygame.draw.rect(self.screen, COLOR_PANEL, card3_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, card3_rect, width=1, border_radius=10)

        lbl3 = self.font_small.render("VALID ACTIONS", True, COLOR_TEXT_MUTED)
        self.screen.blit(lbl3, (666, 92))

        actions = self.game.get_available_actions()
        action_names = ", ".join(a.replace("ROLL_", "R:").replace("FIX_", "F:") for a in actions) if actions else "None (Game Over)"
        val3 = self.font_body_bold.render(action_names, True, COLOR_TEXT_PRIMARY if actions else COLOR_SUCCESS)
        self.screen.blit(val3, (666, 120))

    def _draw_advisor_panel(self) -> None:
        """Perception -> Action Rule Advisor Card."""
        rec_action, rec_reason = PerceptionActionAgent.decide_action(self.game)

        panel_rect = pygame.Rect(28, 172, 904, 46)
        pygame.draw.rect(self.screen, (24, 30, 48), panel_rect, border_radius=8)
        pygame.draw.rect(self.screen, (52, 73, 94), panel_rect, width=1, border_radius=8)

        # AI Badge
        badge_rect = pygame.Rect(40, 180, 100, 28)
        pygame.draw.rect(self.screen, (108, 92, 231), badge_rect, border_radius=6)
        ai_badge = self.font_badge.render("AI ADVISOR", True, (255, 255, 255))
        self.screen.blit(ai_badge, ai_badge.get_rect(center=badge_rect.center))

        # Recommendation text
        rec_text = f"Recommended Action: [{rec_action}] — {rec_reason}"
        rec_surf = self.font_body.render(rec_text, True, (220, 225, 240))
        self.screen.blit(rec_surf, (155, 184))

    def _draw_dice_area(self) -> None:
        """Center stage rendering for Die 1 and Die 2."""
        # Stage backdrop panel
        stage_rect = pygame.Rect(28, 228, 904, 192)
        pygame.draw.rect(self.screen, COLOR_PANEL, stage_rect, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, stage_rect, width=1, border_radius=12)

        # Draw dice
        self.die_view1.draw(self.screen, self.font_dice_q, self.font_body_bold, self.font_badge)
        self.die_view2.draw(self.screen, self.font_dice_q, self.font_body_bold, self.font_badge)

        # Draw comparison or status badge between dice
        vs_rect = pygame.Rect(WINDOW_WIDTH // 2 - 25, 285, 50, 30)
        pygame.draw.rect(self.screen, (38, 46, 68), vs_rect, border_radius=6)
        vs_lbl = self.font_body_bold.render("&", True, COLOR_TEXT_MUTED)
        self.screen.blit(vs_lbl, vs_lbl.get_rect(center=vs_rect.center))

    def _draw_controls(self) -> None:
        """Render action buttons."""
        for btn in self.buttons:
            btn.draw(self.screen, self.font_body_bold, self.font_small)

    def _draw_victory_overlay(self) -> None:
        """Prominent victory banner when target (2,1) or (1,2) is achieved."""
        if not self.game.is_goal_reached():
            return

        banner_rect = pygame.Rect(180, 568, 600, 78)
        pygame.draw.rect(self.screen, COLOR_SUCCESS_BG, banner_rect, border_radius=10)
        pygame.draw.rect(self.screen, COLOR_SUCCESS, banner_rect, width=2, border_radius=10)

        v_title = f"VICTORY! TARGET COMBINATION ({self.game.die1.value}, {self.game.die2.value}) ACHIEVED!"
        v_surf = self.font_header.render(v_title, True, COLOR_SUCCESS)
        self.screen.blit(v_surf, v_surf.get_rect(center=(WINDOW_WIDTH // 2, 592)))

        v_sub = f"Completed in {self.game.roll_count} roll{'s' if self.game.roll_count != 1 else ''}! Press [R] or click 'New Game' to play again."
        v_sub_surf = self.font_small.render(v_sub, True, (220, 245, 230))
        self.screen.blit(v_sub_surf, v_sub_surf.get_rect(center=(WINDOW_WIDTH // 2, 624)))

    def _draw_footer(self) -> None:
        """Bottom status bar narration."""
        if not self.game.is_goal_reached():
            footer_rect = pygame.Rect(0, WINDOW_HEIGHT - 38, WINDOW_WIDTH, 38)
            pygame.draw.rect(self.screen, COLOR_HEADER, footer_rect)
            pygame.draw.line(self.screen, COLOR_PANEL_BORDER, (0, WINDOW_HEIGHT - 38), (WINDOW_WIDTH, WINDOW_HEIGHT - 38), 1)

            status_text = f"Status: {self.game.status_message}"
            status_surf = self.font_small.render(status_text, True, COLOR_TEXT_PRIMARY)
            self.screen.blit(status_surf, (28, WINDOW_HEIGHT - 26))

    def run(self) -> None:
        """Main application loop."""
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
