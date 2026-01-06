"""
Transaction Dialog Base Class
Common functionality for transaction-related dialogs
"""
import customtkinter as ctk
from typing import Optional, Callable
from config import Config


class TransactionDialog(ctk.CTkToplevel):
    """Base class for transaction dialogs with common functionality"""

    def __init__(
        self,
        parent,
        title: str = "Transaction",
        width: int = 600,
        height: int = 700
    ):
        """
        Initialize TransactionDialog

        Args:
            parent: Parent widget
            title: Dialog title
            width: Dialog width
            height: Dialog height
        """
        super().__init__(parent)

        self.result = None
        self._setup_window(title, width, height)

    def _setup_window(self, title: str, width: int, height: int):
        """Setup dialog window properties"""
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)

        # Configure grid first
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Set colors
        self.configure(fg_color=Config.COLORS['background'])

        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Make modal (grab focus) - do this after all setup
        self.transient(self.master)
        self.focus()
        self.grab_set()

    def create_label(
        self,
        parent,
        text: str,
        font_type: str = 'body',
        **kwargs
    ) -> ctk.CTkLabel:
        """
        Create styled label

        Args:
            parent: Parent widget
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

        return ctk.CTkLabel(parent, text=text, **default_kwargs)

    def create_entry(
        self,
        parent,
        placeholder: str = "",
        **kwargs
    ) -> ctk.CTkEntry:
        """
        Create styled entry widget

        Args:
            parent: Parent widget
            placeholder: Placeholder text
            **kwargs: Additional CTkEntry parameters

        Returns:
            CTkEntry instance
        """
        default_kwargs = {
            'font': Config.get_font('body'),
            'fg_color': Config.COLORS['surface'],
            'border_color': Config.COLORS['border'],
            'placeholder_text': placeholder,
            'height': 36
        }
        default_kwargs.update(kwargs)

        return ctk.CTkEntry(parent, **default_kwargs)

    def create_button(
        self,
        parent,
        text: str,
        command=None,
        style: str = 'primary',
        **kwargs
    ) -> ctk.CTkButton:
        """
        Create styled button

        Args:
            parent: Parent widget
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

        return ctk.CTkButton(parent, text=text, command=command, **default_kwargs)

    def create_combobox(
        self,
        parent,
        values: list,
        **kwargs
    ) -> ctk.CTkComboBox:
        """
        Create styled combobox

        Args:
            parent: Parent widget
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
            'dropdown_fg_color': Config.COLORS['surface'],
            'height': 36
        }
        default_kwargs.update(kwargs)

        return ctk.CTkComboBox(parent, values=values, **default_kwargs)

    def create_textbox(
        self,
        parent,
        **kwargs
    ) -> ctk.CTkTextbox:
        """
        Create styled textbox

        Args:
            parent: Parent widget
            **kwargs: Additional CTkTextbox parameters

        Returns:
            CTkTextbox instance
        """
        default_kwargs = {
            'font': Config.get_font('body'),
            'fg_color': Config.COLORS['surface'],
            'border_color': Config.COLORS['border'],
            'wrap': 'word'
        }
        default_kwargs.update(kwargs)

        return ctk.CTkTextbox(parent, **default_kwargs)

    def show_error(self, message: str):
        """
        Show error message

        Args:
            message: Error message
        """
        print(f"Error: {message}")
        # Show messagebox
        try:
            from tkinter import messagebox
            messagebox.showerror("Error", message, parent=self)
        except Exception as e:
            print(f"Could not show error dialog: {e}")

    def show_success(self, message: str):
        """
        Show success message

        Args:
            message: Success message
        """
        print(f"Success: {message}")
        # Show messagebox
        try:
            from tkinter import messagebox
            messagebox.showinfo("Success", message, parent=self)
        except Exception as e:
            print(f"Could not show success dialog: {e}")

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

    def close(self):
        """Close the dialog"""
        self.grab_release()
        self.destroy()
