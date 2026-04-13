import customtkinter as ctk
import json
import os

class TaskManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TO-DO List")
        self.geometry("750x350")
        
        # Custom Color Palette
        self.MINT_GREEN = "#76e897"   
        self.DARK_PURPLE = "#130026"  
        self.HOVER_PURPLE = "#290054" 
        self.TEXT_LIGHT = "white"     
        self.TEXT_DARK = "black"      
        
        # Set overall app background
        self.configure(fg_color=self.MINT_GREEN)

        self.data_file = "tasks.json"
        self.tasks = self.load_tasks()

        # --- LEFT COLUMN: CONTROLS ---

        # Title
        ctk.CTkLabel(self, text="TO-DO List", font=ctk.CTkFont(size=28, weight="bold"), 
                     text_color=self.TEXT_DARK).place(x=30, y=30)

        # Entry Box (Updated placeholder text)
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter the task", height=35, width=240,
                                  fg_color=self.DARK_PURPLE, text_color=self.TEXT_LIGHT, 
                                  border_width=0, corner_radius=0)
        self.entry.place(x=30, y=90)
        self.entry.bind("<Return>", lambda event: self.add_task())

        # Add Button
        ctk.CTkButton(self, text="Add", width=60, height=35, 
                      fg_color=self.DARK_PURPLE, text_color=self.TEXT_LIGHT, 
                      hover_color=self.HOVER_PURPLE, corner_radius=0, 
                      font=ctk.CTkFont(size=14), command=self.add_task).place(x=280, y=90)

        # Action Buttons
        ctk.CTkButton(self, text="Check All", width=80, height=30, 
                      fg_color=self.DARK_PURPLE, text_color=self.TEXT_LIGHT, 
                      hover_color=self.HOVER_PURPLE, corner_radius=0, 
                      font=ctk.CTkFont(size=12), command=self.check_all).place(x=30, y=140)

        ctk.CTkButton(self, text="Clear All", width=80, height=30, 
                      fg_color=self.DARK_PURPLE, text_color=self.TEXT_LIGHT, 
                      hover_color=self.HOVER_PURPLE, corner_radius=0, 
                      font=ctk.CTkFont(size=12), command=self.clear_all).place(x=120, y=140)

        ctk.CTkButton(self, text="Remove (Checked)", width=130, height=30, 
                      fg_color=self.DARK_PURPLE, text_color=self.TEXT_LIGHT, 
                      hover_color=self.HOVER_PURPLE, corner_radius=0, 
                      font=ctk.CTkFont(size=12), command=self.remove_done).place(x=210, y=140)


        # --- RIGHT COLUMN: TASK LIST ---

        # Main List Box
        self.list_frame = ctk.CTkScrollableFrame(self, width=350, height=270, 
                                                 corner_radius=0, fg_color=self.DARK_PURPLE, 
                                                 scrollbar_button_color=self.MINT_GREEN,
                                                 scrollbar_button_hover_color="#5ec97d")
        self.list_frame.place(x=370, y=30)

        self.checks = []
        self.populate()

    def load_tasks(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []

    def save_tasks(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f)

    def add_single_checkbox(self, task_text):
        # Reverted to default styling, kept text white for visibility on dark purple
        cb = ctk.CTkCheckBox(self.list_frame, text=task_text, text_color=self.TEXT_LIGHT, 
                             font=ctk.CTkFont(size=16))
        cb.pack(anchor="w", pady=8, padx=8)
        self.checks.append((cb, task_text))

    def populate(self):
        for w in self.list_frame.winfo_children():
            w.destroy()
        self.checks.clear()
        
        for t in self.tasks:
            self.add_single_checkbox(t)

    def add_task(self):
        t = self.entry.get().strip()
        if t and t not in self.tasks:
            self.tasks.append(t)
            self.save_tasks()
            self.add_single_checkbox(t) 
            self.entry.delete(0, 'end')

    def check_all(self):
        for cb, _ in self.checks:
            cb.select()

    def clear_all(self):
        for cb, _ in self.checks:
            cb.deselect()

    def remove_done(self):
        self.tasks = [t for cb, t in self.checks if not cb.get()]
        self.save_tasks()
        self.populate()

if __name__ == "__main__":
    app = TaskManagerApp()
    app.mainloop()