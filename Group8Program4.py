import sys
import pandas as pd
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

class CarPredictionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Car Type Prediction")
        self.setGeometry(0, 0, 1600, 900)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout()  # สร้างเลย์เอาต์หลัก

        # สร้างเลย์เอาต์สำหรับกล่องข้อความ
        text_box_layout = QVBoxLayout()

        # กล่องข้อความ "Wheel"
        self.wheel_textbox = QLineEdit()
        text_box_layout.addWidget(QLabel("Wheel"))
        text_box_layout.addWidget(self.wheel_textbox)

        # กล่องข้อความ "Chassis"
        self.chassis_textbox = QLineEdit()
        text_box_layout.addWidget(QLabel("Chassis"))
        text_box_layout.addWidget(self.chassis_textbox)

        # กล่องข้อความ "Pax"
        self.pax_textbox = QLineEdit()
        text_box_layout.addWidget(QLabel("Pax"))
        text_box_layout.addWidget(self.pax_textbox)

        # กล่องข้อความ "Type"
        self.type_textbox = QLineEdit()
        text_box_layout.addWidget(QLabel("Type"))
        text_box_layout.addWidget(self.type_textbox)
        
        self.info_label = QLabel()
        text_box_layout.addWidget(self.info_label)

        # กล่องข้อความอยู่ในเลย์เอาต์สำหรับปุ่ม
        button_layout = QVBoxLayout()

        self.central_widget.setLayout(main_layout)

        self.show_data_button = QPushButton("Show Data")
        self.show_data_button.clicked.connect(self.show_data)
        button_layout.addWidget(self.show_data_button)

        self.add_data_button = QPushButton("Add Data")
        self.add_data_button.clicked.connect(self.add_data)
        button_layout.addWidget(self.add_data_button)

        self.edit_data_button = QPushButton("Edit Data")
        self.edit_data_button.clicked.connect(self.edit_data)
        button_layout.addWidget(self.edit_data_button)

        self.search_data_button = QPushButton("Search Data")
        self.search_data_button.clicked.connect(self.search_data)
        button_layout.addWidget(self.search_data_button)

        self.delete_data_button = QPushButton("Delete Data")
        self.delete_data_button.clicked.connect(self.delete_data)
        button_layout.addWidget(self.delete_data_button)

        self.test_button = QPushButton("Test")
        self.test_button.clicked.connect(self.test)
        button_layout.addWidget(self.test_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        button_layout.addWidget(self.exit_button)

        # สร้างตารางแสดงข้อมูล
        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addLayout(text_box_layout)  # เพิ่มเลย์เอาต์กล่องข้อความ
        main_layout.addLayout(button_layout)  # เพิ่มเลย์เอาต์ปุ่ม
        main_layout.addWidget(self.table)

        self.data = None
        self.search_result = None
        self.load_data()

    def load_data(self):
        try:
            self.data = pd.read_excel("car_data.xlsx")
            # self.info_label.setText("Data loaded successfully.")
        except Exception as e:
            self.info_label.setText(f"Error loading data: {str(e)}")
            
    def load_selected_data(self, row_idx):
        if 0 <= row_idx < self.data.shape[0]:
            selected_row_data = self.data.iloc[row_idx]
            self.wheel_textbox.setText(str(selected_row_data['Wheel']))
            self.chassis_textbox.setText(str(selected_row_data['Chassis']))
            self.pax_textbox.setText(str(selected_row_data['Pax']))
            self.type_textbox.setText(selected_row_data['Type'])
            
    def show_data(self):
        self.search_result = None
        self.clear_table()
        self.load_data()
        self.display_data()

    def display_data(self):
        data_to_display = self.search_result if self.search_result is not None else self.data

        if data_to_display is not None:
            self.table.setRowCount(data_to_display.shape[0])
            self.table.setColumnCount(data_to_display.shape[1] + 1)  
            self.table.setHorizontalHeaderLabels(data_to_display.columns.tolist() + ['Select'])

            self.radio_buttons = []

            for row_idx, row_data in data_to_display.iterrows():
                for col_idx, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(row_idx, col_idx, item)

                radio_button = QRadioButton()
                layout = QHBoxLayout()
                layout.addWidget(radio_button)
                layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                widget = QWidget()
                widget.setLayout(layout)
                self.table.setCellWidget(row_idx, data_to_display.shape[1], widget)
                self.radio_buttons.append(radio_button)

                radio_button.toggled.connect(lambda checked, idx=row_idx: self.load_selected_data(idx))

    def add_data(self):
        if self.data is not None:
            wheel_text = self.wheel_textbox.text()
            chassis_text = self.chassis_textbox.text()
            pax_text = self.pax_textbox.text()
            car_type = self.type_textbox.text()

            if not (wheel_text.isdigit() and chassis_text.isdigit() and pax_text.isdigit()):
                self.info_label.setText("Please enter valid numeric values for Wheel, Chassis, and Pax.")
                return

            if not car_type:
                self.info_label.setText("Please enter a valid value for Type.")
                return

            wheel = int(wheel_text)
            chassis = int(chassis_text)
            pax = int(pax_text)

            try:
                new_data = pd.DataFrame({'Wheel': [wheel], 'Chassis': [chassis], 'Pax': [pax], 'Type': [car_type]})
                self.data = pd.concat([self.data, new_data], ignore_index=True)
                self.data.to_excel("car_data.xlsx", index=False)
                # self.info_label.setText("Data added successfully.")
                self.display_data()
            except Exception as e:
                self.info_label.setText(f"Error adding data: {str(e)}")
        else:
            self.info_label.setText("No data loaded.")


    def edit_data(self):
        if self.data is not None:
            wheel = self.wheel_textbox.text()
            chassis = self.chassis_textbox.text()
            pax = self.pax_textbox.text()
            car_type = self.type_textbox.text()

            if not (wheel.isdigit() and chassis.isdigit() and pax.isdigit()):
                self.info_label.setText("Please enter valid numeric values for Wheel, Chassis, and Pax.")
                return

            wheel = int(wheel)
            chassis = int(chassis)
            pax = int(pax)

            try:
                selected_row_idx = None
                for idx, radio_button in enumerate(self.radio_buttons):
                    if radio_button.isChecked():
                        selected_row_idx = idx
                        break

                if selected_row_idx is not None:
                    self.data.at[selected_row_idx, 'Wheel'] = wheel
                    self.data.at[selected_row_idx, 'Chassis'] = chassis
                    self.data.at[selected_row_idx, 'Pax'] = pax
                    self.data.at[selected_row_idx, 'Type'] = car_type

                    self.data.to_excel("car_data.xlsx", index=False)
                    self.info_label.setText("Data edited successfully.")
                    self.display_data()
                else:
                    self.info_label.setText("No row selected for editing.")
            except Exception as e:
                self.info_label.setText(f"Error editing data: {str(e)}")
        else:
            self.info_label.setText("No data loaded.")
    
    def search_data(self):
        if self.data is not None:
            search_wheel = self.wheel_textbox.text()
            search_chassis = self.chassis_textbox.text()
            search_pax = self.pax_textbox.text()
            search_type = self.type_textbox.text()
            
            try:
                if search_wheel and not search_wheel.isdigit():
                    self.info_label.setText("Please enter a valid numeric value for Wheel.")
                    return

                if search_chassis and not search_chassis.isdigit():
                    self.info_label.setText("Please enter a valid numeric value for Chassis.")
                    return

                if search_pax and not search_pax.isdigit():
                    self.info_label.setText("Please enter a valid numeric value for Pax.")
                    return

                search_wheel = int(search_wheel) if search_wheel else None
                search_chassis = int(search_chassis) if search_chassis else None
                search_pax = int(search_pax) if search_pax else None

                wheel_condition = (self.data['Wheel'] == search_wheel) if search_wheel is not None else True
                chassis_condition = (self.data['Chassis'] == search_chassis) if search_chassis is not None else True
                pax_condition = (self.data['Pax'] == search_pax) if search_pax is not None else True
                type_condition = (self.data['Type'] == search_type) if search_type else True

                search_condition = wheel_condition & chassis_condition & pax_condition & type_condition

                self.search_result = self.data[search_condition].reset_index(drop=True)

                if not self.search_result.empty:
                    self.display_data()  # Use the modified display_data function to display results
                    self.info_label.setText("Search result found and displayed.")
                else:
                    self.info_label.setText("No matching data found.")
            except Exception as e:
                self.info_label.setText(f"Error Search data")
        else:
            self.info_label.setText("No data loaded.")

    def delete_data(self):
        if self.data is not None:
            selected_row_idx = None
            for idx, radio_button in enumerate(self.radio_buttons):
                if radio_button.isChecked():
                    selected_row_idx = idx
                    break

            if selected_row_idx is None:
                self.info_label.setText("No row selected for deletion.")
                return

            try:
                self.data = self.data.drop(selected_row_idx, axis=0).reset_index(drop=True)
                self.data.to_excel("car_data.xlsx", index=False)
                self.info_label.setText("Selected row deleted successfully.")
                self.display_data()
            except Exception as e:
                self.info_label.setText(f"Error deleting data: {str(e)}")
        else:
            self.info_label.setText("No data loaded.")

    def test(self):
        features = self.data[['Wheel', 'Chassis', 'Pax']]
        target = self.data['Type']
        x_train, x_test, y_train, y_test = train_test_split(features, target, random_state=0)
        model = KNeighborsClassifier(n_neighbors=5)
        model.fit(x_train, y_train)
        wheel_text = self.wheel_textbox.text()
        chassis_text = self.chassis_textbox.text()
        pax_text = self.pax_textbox.text()

        if not wheel_text or not chassis_text or not pax_text:
            self.info_label.setText("Please enter values for Wheel, Chassis, and Pax.")
            return

        try:
            wheel_value = float(wheel_text)
            chassis_value = float(chassis_text)
            pax_value = float(pax_text)
        except ValueError:
            self.info_label.setText("Invalid input. Please enter valid numeric values.")
            return

        prediction = model.predict([[wheel_value, chassis_value, pax_value]])

        accuracy = '{:.2f}'.format(model.score(x_test, y_test))
        self.info_label.setText(f"Predicted: Wheel: {wheel_value}, Chassis: {chassis_value}, Pax: {pax_value}, Type: {prediction[0]}, Accuracy: {accuracy}")

    def clear_table(self):
        self.table.clearContents()
        self.table.setRowCount(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CarPredictionApp()
    window.show()
    sys.exit(app.exec())
