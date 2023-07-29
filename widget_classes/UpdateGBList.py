import logging
import tkinter
import tkinter as tk

import customtkinter

from scripts import update_gb_eligibility
from widget_classes.LogsDisplay import TkinterTextHandler


class UpdateGBList(customtkinter.CTkFrame):
    # Create an instance variable to hold the logger
    logger5 = None

    def __init__(self, master, title):
        super().__init__(master)
        self.title = title

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray90", corner_radius=3)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        # Checkbox
        self.update_db_flag = tkinter.BooleanVar(value=False)
        self.export_to_txt_flag = tkinter.BooleanVar(value=False)
        self.checkbox_update_db = customtkinter.CTkCheckBox(self,
                                                            text="Update CRM DB",
                                                            variable=self.update_db_flag,
                                                            onvalue=True,
                                                            offvalue=False
                                                            )
        self.checkbox_export_txt = customtkinter.CTkCheckBox(self,
                                                             text="Export to text",
                                                             variable=self.export_to_txt_flag,
                                                             onvalue=True,
                                                             offvalue=False
                                                             )
        self.checkbox_update_db.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.checkbox_export_txt.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew")

        # Submit Button
        self.button = customtkinter.CTkButton(self, text="Update GB List", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # Log Widget
        text_log_widget = tk.Text(self, wrap='word', state='disabled', width=50, height=10, bg="black", fg="white")
        text_log_widget.grid(row=4, column=0, padx=5, pady=5)

        # Create and set the TkinterTextHandler for the root logger
        text_handler = TkinterTextHandler(text_log_widget)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
        text_handler.setFormatter(formatter)
        logging.getLogger().addHandler(text_handler)
        logging.getLogger().setLevel(logging.INFO)
        logging.debug("Initialized logging...")

    def button_callback(self):
        print(f"Update DB Flag: {self.update_db_flag.get()}")

        logging.debug("Debug message")
        logging.info("Info message")
        logging.warning("Warning message")
        logging.error("Error message")
        logging.critical("Critical message")

        eligibility_lists = update_gb_eligibility.process_eligible_GB_members(save_file="eligible_members.csv",
                                                                              update_db_flag=self.update_db_flag.get(),
                                                                              export_to_txt_flag=self.export_to_txt_flag.get()
                                                                              )

        print(f"\n⛔ Members who became ineligible: {eligibility_lists[0]}")
        print(f"✅ Members who became eligible: {eligibility_lists[1]}")
        print("DONE")


# Main method
if __name__ == '__main__':
    class TestApp(customtkinter.CTk):
        def __init__(self):
            super().__init__()
            self.geometry("400x200")
            self.grid_rowconfigure(0, weight=1)  # configure grid system
            self.grid_columnconfigure(0, weight=1)

            self.my_frame = UpdateGBList(master=self, title="TESTING")
            self.my_frame.grid(row=0, column=0, padx=20, pady=20)


    app = TestApp()
    app.mainloop()
