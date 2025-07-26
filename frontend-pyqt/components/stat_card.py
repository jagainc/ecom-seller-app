from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize

class StatCard(QFrame):
    """
    A reusable PyQt widget to display a single statistical metric.
    It shows a title, a value, a description, and an optional icon.
    """
    def __init__(self, title, value, description="", icon_path=None):
        """
        Initializes the StatCard.

        Args:
            title (str): The title of the statistic (e.g., "Total Sales").
            value (str): The current value of the statistic (e.g., "$12,345.67").
            description (str, optional): A brief description or sub-text. Defaults to "".
            icon_path (str, optional): Path to an icon image file. Defaults to None.
        """
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setFixedSize(280, 160) # Increased fixed size to accommodate larger icons and padding
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 10px;
                padding: 15px;
            }
            QFrame:hover {
                border: 1px solid #BBDEFB; /* Light blue on hover */
                /* box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); */ /* Removed box-shadow */
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        # Top section with title and icon
        title_icon_layout = QHBoxLayout()
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Inter", 14, QFont.Weight.DemiBold))
        self.title_label.setStyleSheet("color: #555;")
        title_icon_layout.addWidget(self.title_label)

        if icon_path:
            self.icon_label = QLabel()
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                # Set a fixed size for the icon label
                icon_size = 40  # You can adjust this value as needed
                self.icon_label.setFixedSize(icon_size, icon_size)
                # Center the pixmap in the label and scale it to fit while keeping aspect ratio
                self.icon_label.setPixmap(
                    pixmap.scaled(
                        icon_size, icon_size,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )
                self.icon_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                title_icon_layout.addWidget(self.icon_label)
            else:
                print(f"Warning: Could not load icon from {icon_path}") # Debugging for icon loading
        
        title_icon_layout.addStretch(1) # Push icon to the right if present

        main_layout.addLayout(title_icon_layout)

        # Value label
        self.value_label = QLabel(value)
        self.value_label.setFont(QFont("Inter", 28, QFont.Weight.Bold))
        self.value_label.setStyleSheet("color: #333; margin-top: 5px; margin-bottom: 5px;")
        main_layout.addWidget(self.value_label)

        # Description label
        self.description_label = QLabel(description)
        self.description_label.setFont(QFont("Inter", 10))
        self.description_label.setStyleSheet("color: #888;")
        main_layout.addWidget(self.description_label)

        main_layout.addStretch(1) # Push content to the top

    def update_value(self, new_value):
        """
        Updates the displayed value of the StatCard.

        Args:
            new_value (str): The new value to display.
        """
        self.value_label.setText(new_value)

