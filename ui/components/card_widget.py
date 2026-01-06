"""
Card Widget
Reusable card-style container for grouping related content
"""
import customtkinter as ctk
from typing import Optional
from config import Config


class CardWidget(ctk.CTkFrame):
    """Card-style container widget for modern UI"""

    def __init__(
        self,
        parent,
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize CardWidget

        Args:
            parent: Parent widget
            title: Optional card title
            **kwargs: Additional CTkFrame parameters
        """
        # Default card styling
        default_kwargs = {
            'fg_color': Config.COLORS['surface'],
            'corner_radius': 12,
            'border_width': 1,
            'border_color': Config.COLORS['border']
        }
        default_kwargs.update(kwargs)

        super().__init__(parent, **default_kwargs)

        # Configure grid
        self.grid_columnconfigure(0, weight=1)

        # Current row for dynamic content
        self.current_row = 0

        # Create title if provided
        if title:
            self.create_card_title(title)

    def create_card_title(self, title: str):
        """
        Create card title

        Args:
            title: Title text
        """
        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=Config.get_font('subtitle'),
            text_color=Config.COLORS['text_primary']
        )
        title_label.grid(
            row=self.current_row,
            column=0,
            padx=20,
            pady=(20, 10),
            sticky="w"
        )
        self.current_row += 1

    def add_content(self, widget):
        """
        Add content widget to card

        Args:
            widget: Widget to add
        """
        widget.grid(
            row=self.current_row,
            column=0,
            padx=20,
            pady=10,
            sticky="ew"
        )
        self.current_row += 1

    def add_separator(self):
        """Add horizontal separator line"""
        separator = ctk.CTkFrame(
            self,
            height=1,
            fg_color=Config.COLORS['border']
        )
        separator.grid(
            row=self.current_row,
            column=0,
            padx=20,
            pady=10,
            sticky="ew"
        )
        self.current_row += 1
