"""
Main Application Window
Entry point for the UI application
"""
import customtkinter as ctk
from typing import Optional
import sys

from config import Config
from database import initialize_database
from services import AccountService, CategoryService, TransactionService, ReportService, ExportService
from .frames.dashboard_frame import DashboardFrame
from .frames.transactions_frame import TransactionsFrame
from .frames.accounts_frame import AccountsFrame
from .frames.categories_frame import CategoriesFrame
from .frames.management_frame import ManagementFrame


class ExpenseTrackerApp(ctk.CTk):
    """Main application window"""

    def __init__(self):
        """Initialize application"""
        super().__init__()

        # Window configuration
        self.title(f"{Config.APP_NAME} - {Config.VERSION}")
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")

        # Set appearance mode and color theme
        ctk.set_appearance_mode(Config.APPEARANCE_MODE)
        ctk.set_default_color_theme("blue")

        # Initialize database
        if not self._initialize_database():
            print("Failed to initialize database. Exiting...")
            sys.exit(1)

        # Initialize services (shared across frames)
        self.account_service = AccountService()
        self.category_service = CategoryService()
        self.transaction_service = TransactionService()
        self.report_service = ReportService()
        self.export_service = ExportService()

        # Current frame reference
        self.current_frame: Optional[ctk.CTkFrame] = None

        # Create UI
        self._create_layout()
        self._show_dashboard()

    def _initialize_database(self) -> bool:
        """
        Initialize database

        Returns:
            True if successful, False otherwise
        """
        try:
            return initialize_database(force_recreate=False, seed_data=True)
        except Exception as e:
            print(f"Database initialization error: {e}")
            return False

    def _create_layout(self):
        """Create main application layout"""
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create sidebar
        self._create_sidebar()

        # Create main content area
        self.content_frame = ctk.CTkFrame(
            self,
            fg_color=Config.COLORS['background']
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    def _create_sidebar(self):
        """Create navigation sidebar"""
        # Sidebar frame
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            fg_color=Config.COLORS['surface'],
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)  # Push buttons to top

        # App title
        title_label = ctk.CTkLabel(
            self.sidebar,
            text=Config.APP_NAME,
            font=Config.get_font('title'),
            text_color=Config.COLORS['primary']
        )
        title_label.grid(row=0, column=0, padx=20, pady=(30, 40))

        # Navigation buttons
        self.nav_buttons = {}

        nav_items = [
            ("Dashboard", "📊", self._show_dashboard),
            ("Transactions", "💳", self._show_transactions),
            ("Accounts", "🏦", self._show_accounts),
            ("Categories", "📂", self._show_categories),
            ("Management", "⚙️", self._show_management),
        ]

        for idx, (name, icon, command) in enumerate(nav_items, start=1):
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"{icon}  {name}",
                font=Config.get_font('body'),
                fg_color="transparent",
                text_color=Config.COLORS['text_secondary'],
                hover_color=Config.COLORS['border'],
                anchor="w",
                height=40,
                command=command
            )
            btn.grid(row=idx, column=0, padx=10, pady=5, sticky="ew")
            self.nav_buttons[name] = btn

        # Version label at bottom
        version_label = ctk.CTkLabel(
            self.sidebar,
            text=f"v{Config.VERSION}",
            font=Config.get_font('small'),
            text_color=Config.COLORS['text_secondary']
        )
        version_label.grid(row=7, column=0, padx=20, pady=(0, 20))

    def _highlight_nav_button(self, button_name: str):
        """
        Highlight active navigation button

        Args:
            button_name: Name of button to highlight
        """
        for name, btn in self.nav_buttons.items():
            if name == button_name:
                btn.configure(
                    fg_color=Config.COLORS['primary'],
                    text_color="white"
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=Config.COLORS['text_secondary']
                )

    def _switch_frame(self, new_frame: ctk.CTkFrame):
        """
        Switch to new frame

        Args:
            new_frame: Frame to display
        """
        # Destroy current frame
        if self.current_frame:
            self.current_frame.destroy()

        # Display new frame
        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def _show_dashboard(self):
        """Show dashboard frame"""
        self._highlight_nav_button("Dashboard")
        frame = DashboardFrame(
            self.content_frame,
            self.report_service,
            self.transaction_service
        )
        self._switch_frame(frame)

    def _show_transactions(self):
        """Show transactions frame"""
        self._highlight_nav_button("Transactions")
        frame = TransactionsFrame(
            self.content_frame,
            self.transaction_service,
            self.account_service,
            self.category_service,
            self.export_service
        )
        self._switch_frame(frame)

    def _show_accounts(self):
        """Show accounts frame"""
        self._highlight_nav_button("Accounts")
        frame = AccountsFrame(
            self.content_frame,
            self.account_service
        )
        self._switch_frame(frame)

    def _show_categories(self):
        """Show categories frame"""
        self._highlight_nav_button("Categories")
        frame = CategoriesFrame(
            self.content_frame,
            self.category_service
        )
        self._switch_frame(frame)

    def _show_management(self):
        """Show management frame"""
        self._highlight_nav_button("Management")
        frame = ManagementFrame(
            self.content_frame,
            self.transaction_service,
            self.account_service,
            self.category_service
        )
        self._switch_frame(frame)

    def run(self):
        """Start the application"""
        self.mainloop()


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.run()
