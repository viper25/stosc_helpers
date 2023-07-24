import customtkinter

from scripts import generate_xero_contacts


class GenerateMembersFrame(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.title = title
        self.radio_buttons = []

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray60", corner_radius=3)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        radio_button_active = customtkinter.CTkRadioButton(self, text="Active")
        radio_button_inactive = customtkinter.CTkRadioButton(self, text="In Active")
        radio_button_active.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        radio_button_inactive.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.radio_buttons.append(radio_button_active)
        self.radio_buttons.append(radio_button_inactive)

        self.button = customtkinter.CTkButton(self, text="Generate", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    def button_callback(self):
        status = generate_xero_contacts.generate_xero_contact_list()
        print(status)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.radio_buttons:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

# Main method
if __name__ == '__main__':
    class TestApp(customtkinter.CTk):
        def __init__(self):
            super().__init__()
            self.geometry("400x200")
            self.grid_rowconfigure(0, weight=1)  # configure grid system
            self.grid_columnconfigure(0, weight=1)

            self.my_frame = GenerateMembersFrame(master=self, title="TESTING")
            self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


    app = TestApp()
    app.mainloop()
