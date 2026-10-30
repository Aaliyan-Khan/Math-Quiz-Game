import sys
from PyQt6.QtWidgets import QPushButton, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget
from PyQt6.QtGui import QIcon

# Import the module to avoid circular dependency loops and track variable changes dynamically
import quiz 

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Math App")
        self.setFixedSize(600, 350)  
        self.setWindowIcon(QIcon("maththug.png"))
        
        # Initialize the very first question when the app loads
        quiz.question_generator()
        
        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        
        # --- Top Header Row ---
        header_layout = QHBoxLayout()
        
        self.level_label = QLabel(self)
        self.level_label.setObjectName("level")
        
        self.score_label = QLabel(self)
        self.score_label.setObjectName("score")
        
        self.heart_label = QLabel(self) 
        self.heart_label.setStyleSheet("font-size: 20px;")
        
        header_layout.addWidget(self.level_label)
        header_layout.addStretch()
        header_layout.addWidget(self.score_label)
        header_layout.addStretch()
        header_layout.addWidget(self.heart_label)
        
        main_layout.addLayout(header_layout)
        
        # --- Question Label ---
        self.question_label = QLabel(self)
        self.question_label.setObjectName("question")
        main_layout.addWidget(self.question_label)
        main_layout.addSpacing(10)
        
        # --- Grid for the 4 Answer Choices ---
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        self.btn1 = QPushButton(self)
        self.btn2 = QPushButton(self)
        self.btn3 = QPushButton(self)
        self.btn4 = QPushButton(self)
        
        # Connect buttons directly to the tracking logic
        self.btn1.clicked.connect(self.user_input_updater)
        self.btn2.clicked.connect(self.user_input_updater)
        self.btn3.clicked.connect(self.user_input_updater)
        self.btn4.clicked.connect(self.user_input_updater)
        
        grid_layout.addWidget(self.btn1, 0, 0)
        grid_layout.addWidget(self.btn2, 0, 1) 
        grid_layout.addWidget(self.btn3, 1, 0)  
        grid_layout.addWidget(self.btn4, 1, 1) 
        
        main_layout.addLayout(grid_layout)
        
        # Populate UI elements with the initial problem data
        self.update_ui_elements()

    def update_ui_elements(self):
        """Refreshes all labels and buttons with current state values from quiz.py"""
        # Handle Game Over screen state gracefully
        if quiz.heart <= 0:
            self.question_label.setText(f"Game Over! Final Score: {quiz.score}")
            self.heart_label.setText("🖤🖤🖤")
            self.btn1.setDisabled(True)
            self.btn2.setDisabled(True)
            self.btn3.setDisabled(True)
            self.btn4.setDisabled(True)
            return

        # Regular game layout updates
        self.level_label.setText(f"Level: {quiz.lvl}")
        self.score_label.setText(f"Score: {quiz.score}")
        self.heart_label.setText("❤️" * quiz.heart + "🖤" * (3 - quiz.heart))
        self.question_label.setText(quiz.question)
        
        self.btn1.setText(str(quiz.choices[0]))
        self.btn2.setText(str(quiz.choices[1]))
        self.btn3.setText(str(quiz.choices[2]))
        self.btn4.setText(str(quiz.choices[3]))

    def user_input_updater(self):
        """Determines which button clicked, passes selection to logic system, advances state"""
        sending_btn = self.sender()
        
        if sending_btn == self.btn1:
            quiz.check_answer(quiz.choices[0])
        elif sending_btn == self.btn2:
            quiz.check_answer(quiz.choices[1])
        elif sending_btn == self.btn3:
            quiz.check_answer(quiz.choices[2])
        elif sending_btn == self.btn4:
            quiz.check_answer(quiz.choices[3])
            
        # Move forward by generating the next question phase
        if quiz.heart > 0:
            quiz.question_generator()
            
        # Push the updated problem data into the visual view framework
        self.update_ui_elements()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("style.qss", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Could not find style.qss")

    mathapp = MyApp()
    mathapp.show()
    sys.exit(app.exec())
