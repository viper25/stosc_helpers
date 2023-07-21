import customtkinter

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.values = values
        self.title = title
        self.checkboxes = []

        self.title = customtkinter.CTkLabel(self, text=self.title, fg_color="gray60", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

        self.button = customtkinter.CTkButton(self, text="Generate")
        self.button.grid(row=len(values)+2, column=0, padx=10, pady=10, sticky="nsew")

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

class MyTabView(customtkinter.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Generate Members")
        self.add("Create Sub Invoices")
        self.add("Create Harvest Invoices")
        self.add("Compare Xero and CRM")

        self.checkbox_frame_1 = MyFrame(master=self.tab("Generate Members"), title="Options", values=["All Members", "Inactive Members"])
        self.checkbox_frame_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("STOSC")

        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=20, pady=20)


app = App()
app.mainloop()
