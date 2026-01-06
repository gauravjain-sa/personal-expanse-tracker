"""
Base Frame
Base class for all frames with common functionality
"""
import customtkinter as ctk
from typing import Optional
from config import Config


class BaseFrame(ctk.CTkFrame):
    """
    Base frame with common styling and functionality
    All frames should inherit from this class
    """

    def __init__(
        self,
        parent,
        title: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize BaseFrame

        Args:
            parent: Parent widget
            title: Optional frame title
            **kwargs: Additional CTkFrame parameters
        """
        # Set default styling from Config
        default_kwargs = {
            'fg_color': Config.COLORS['surface'],
            'corner_radius': 10,
            'border_width': 0
        }
        default_kwargs.update(kwargs)

        super().__init__(parent, **default_kwargs)

        self.title_text = title

        # Grid configuration for responsive layout
        self.grid_columnconfigure(0, weight=1)

        # Create title if provided
        if self.title_text:
            self._create_title()

    def _create_title(self):
        """Create frame title"""
        title_label = ctk.CTkLabel(
            self,
            text=self.title_text,
            font=Config.get_font('title'),
            text_color=Config.COLORS['text_primary']
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

    def create_label(
        self,
        text: str,
        font_type: str = 'body',
        **kwargs
    ) -> ctk.CTkLabel:
        """
        Create styled label (reusable method)

        Args:
            text: Label text
            font_type: Font type from Config
            **kwargs: Additional CTkLabel parameters

        Returns:
            CTkLabel instance
        """
        default_kwargs = {
            'font': Config.get_font(font_type),
            'text_color': Config.COLORS['text_primary']
        }
        default_kwargs.update(kwargs)

        return ctk.CTkLabel(self, text=text, **default_kwargs)

    def create_entry(
        self,
        placeholder: str = "",
        **kwargs
    ) -> ctk.CTkEntry:
        """
        Create styled entry widget (reusable method)

        Args:
            placeholder: Placeholder text
            **kwargs: Additional CTkEntry parameters

        Returns:
            CTkEntry instance
        """
        default_kwargs = {
            'font': Config.get_font('body'),
            'fg_color': Config.COLORS['surface'],
            'border_color': Config.COLORS['border'],
            'placeholder_text': placeholder
        }
        default_kwargs.update(kwargs)

        return ctk.CTkEntry(self, **default_kwargs)

    def create_button(
        self,
        text: str,
        command=None,
        style: str = 'primary',
        **kwargs
    ) -> ctk.CTkButton:
        """
        Create styled button (reusable method)

        Args:
            text: Button text
            command: Button command
            style: Button style ('primary', 'secondary', 'success', 'danger')
            **kwargs: Additional CTkButton parameters

        Returns:
            CTkButton instance
        """
        # Get color based on style
        color_map = {
            'primary': Config.COLORS['primary'],
            'secondary': Config.COLORS['secondary'],
            'success': Config.COLORS['success'],
            'danger': Config.COLORS['error']
        }
        fg_color = color_map.get(style, Config.COLORS['primary'])

        default_kwargs = {
            'font': Config.get_font('body'),
            'fg_color': fg_color,
            'hover_color': self._darken_color(fg_color),
            'corner_radius': 8,
            'height': 36
        }
        default_kwargs.update(kwargs)

        return ctk.CTkButton(self, text=text, command=command, **default_kwargs)

    def create_combobox(
        self,
        values: list,
        **kwargs
    ) -> ctk.CTkComboBox:
        """
        Create styled combobox (reusable method)

        Args:
            values: List of values
            **kwargs: Additional CTkComboBox parameters

        Returns:
            CTkComboBox instance
        """
        default_kwargs = {
            'font': Config.get_font('body'),
            'fg_color': Config.COLORS['surface'],
            'border_color': Config.COLORS['border'],
            'button_color': Config.COLORS['primary'],
            'dropdown_fg_color': Config.COLORS['surface']
        }
        default_kwargs.update(kwargs)

        return ctk.CTkComboBox(self, values=values, **default_kwargs)

    def show_error(self, message: str):
        """
        Show error message (can be overridden)

        Args:
            message: Error message
        """
        print(f"Error: {message}")

    def show_success(self, message: str):
        """
        Show success message (can be overridden)

        Args:
            message: Success message
        """
        print(f"Success: {message}")

    def _darken_color(self, hex_color: str, factor: float = 0.8) -> str:
        """
        Darken a hex color (for hover effects)

        Args:
            hex_color: Hex color code
            factor: Darkening factor (0.0 to 1.0)

        Returns:
            Darkened hex color
        """
        # Remove '#' if present
        hex_color = hex_color.lstrip('#')

        # Convert to RGB
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

        # Darken
        r, g, b = int(r * factor), int(g * factor), int(b * factor)

        # Convert back to hex
        return f'#{r:02x}{g:02x}{b:02x}'
