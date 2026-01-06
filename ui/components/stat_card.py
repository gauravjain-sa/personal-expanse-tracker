"""
Stat Card
Card widget for displaying statistics on dashboard
"""
import customtkinter as ctk
from typing import Optional
from config import Config


class StatCard(ctk.CTkFrame):
    """Stat card for dashboard metrics"""

    def __init__(
        self,
        parent,
        title: str,
        value: str,
        subtitle: Optional[str] = None,
        color: str = None,
        **kwargs
    ):
        """
        Initialize StatCard

        Args:
            parent: Parent widget
            title: Stat title
            value: Stat value (formatted)
            subtitle: Optional subtitle text
            color: Optional custom color
            **kwargs: Additional CTkFrame parameters
        """
        # Default styling
        default_kwargs = {
            'fg_color': Config.COLORS['surface'],
            'corner_radius': 12,
            'border_width': 1,
            'border_color': Config.COLORS['border']
        }
        default_kwargs.update(kwargs)

        super().__init__(parent, **default_kwargs)

        self.title_text = title
        self.value_text = value
        self.subtitle_text = subtitle
        self.accent_color = color or Config.COLORS['primary']

        self._create_layout()

    def _create_layout(self):
        """Create stat card layout"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)

        # Title label
        title_label = ctk.CTkLabel(
            self,
            text=self.title_text,
            font=Config.get_font('body'),
            text_color=Config.COLORS['text_secondary']
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        # Value label (prominent)
        value_label = ctk.CTkLabel(
            self,
            text=self.value_text,
            font=Config.get_font('heading'),
            text_color=self.accent_color
        )
        value_label.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="w")

        # Subtitle (if provided)
        if self.subtitle_text:
            subtitle_label = ctk.CTkLabel(
                self,
                text=self.subtitle_text,
                font=Config.get_font('small'),
                text_color=Config.COLORS['text_secondary']
            )
            subtitle_label.grid(row=2, column=0, padx=20, pady=(5, 20), sticky="w")
        else:
            # Add padding
            self.grid_rowconfigure(2, minsize=20)

    def update_value(self, new_value: str, new_subtitle: Optional[str] = None):
        """
        Update stat value and optional subtitle

        Args:
            new_value: New value text
            new_subtitle: New subtitle text (optional)
        """
        self.value_text = new_value
        if new_subtitle is not None:
            self.subtitle_text = new_subtitle

        # Recreate layout with new values
        for widget in self.winfo_children():
            widget.destroy()

        self._create_layout()
