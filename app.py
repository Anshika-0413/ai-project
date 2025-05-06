from tkinter import *
from tkinter import scrolledtext, font
from chat import get_response, bot_name
import webbrowser
import re

# Modern Color Scheme
BG_COLOR = "#1a1a2e"
TEXT_COLOR = "#e6e6e6"
USER_COLOR = "#4cc9f0"
BOT_COLOR = "#f72585"
LINK_COLOR = "#4895ef"
ENTRY_BG = "#16213e"

class ChatApplication:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        
    def run(self):
        self.window.mainloop()
        
    def _setup_main_window(self):
        self.window.title(f"{bot_name} - Thapar Institute")
        self.window.resizable(width=True, height=True)
        self.window.geometry("900x650")
        self.window.configure(bg=BG_COLOR)
        
        # Header with logo
        head_frame = Frame(self.window, bg=BG_COLOR)
        head_frame.pack(fill=X, padx=10, pady=10)
        
        Label(head_frame, text=bot_name, bg=BG_COLOR, fg=BOT_COLOR, 
             font=("Helvetica", 16, "bold")).pack(side=LEFT)
        
        Label(head_frame, text="Ask about admissions, courses, campus life...", 
             bg=BG_COLOR, fg=TEXT_COLOR, font=("Helvetica", 12)).pack(side=RIGHT)
        
        # Chat display
        self.text_widget = scrolledtext.ScrolledText(
            self.window, bg=BG_COLOR, fg=TEXT_COLOR,
            font=("Helvetica", 12), padx=15, pady=10, wrap=WORD,
            insertbackground=TEXT_COLOR, selectbackground="#3a3a4e"
        )
        self.text_widget.pack(expand=True, fill=BOTH, padx=10, pady=(0,10))
        self.text_widget.configure(state=DISABLED)
        
        # Configure tags
        self.text_widget.tag_config('user', foreground=USER_COLOR, 
                                  font=("Helvetica", 12, "bold"))
        self.text_widget.tag_config('bot', foreground=BOT_COLOR, 
                                  font=("Helvetica", 12, "bold"))
        self.text_widget.tag_config('link', foreground=LINK_COLOR, underline=1)
        
        # Bottom frame
        bottom_frame = Frame(self.window, bg=BG_COLOR)
        bottom_frame.pack(fill=X, padx=10, pady=(0,10))
        
        self.msg_entry = Entry(
            bottom_frame, bg=ENTRY_BG, fg=TEXT_COLOR, font=("Helvetica", 12),
            insertbackground=TEXT_COLOR, relief=FLAT, highlightthickness=1,
            highlightbackground="#4a4a5e", highlightcolor=LINK_COLOR
        )
        self.msg_entry.pack(side=LEFT, fill=X, expand=True, ipady=5)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter)
        
        # Send button
        send_button = Button(
            bottom_frame, text="Send", font=("Helvetica", 12, "bold"), bg=BOT_COLOR,
            fg="#f72585", activebackground="#d1145a", activeforeground=TEXT_COLOR,
            relief=FLAT, command=lambda: self._on_enter(None)
        )
        send_button.pack(side=RIGHT, padx=(10,0))
        
        # Welcome message
        self._insert_message(
            "Hello! I'm your Thapar Institute assistant. "
            "You can ask me about:\n- Admissions\n- Courses\n- Scholarships\n- Campus life\n- Placements", 
            bot_name
        )
        
    def _on_enter(self, event):
        msg = self.msg_entry.get().strip()
        if msg:
            self._insert_message(msg, "You")
        
    def _insert_message(self, msg, sender):
        self.msg_entry.delete(0, END)
        
        # Insert sender's message
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, f"{sender}: ", sender)
        self.text_widget.insert(END, f"{msg}\n\n")
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)
        
        # Get and format response
        if sender == "You":
            response = get_response(msg)
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, f"{bot_name}: ", 'bot')
            
            # Handle links
            parts = re.split(r'(https?://\S+)', response)
            for part in parts:
                if part.startswith('http'):
                    self.text_widget.insert(END, part, 'link')
                    self.text_widget.tag_bind('link', '<Button-1>', 
                                            lambda e, url=part: webbrowser.open(url))
                else:
                    self.text_widget.insert(END, part)
            
            self.text_widget.insert(END, "\n\n")
            self.text_widget.configure(state=DISABLED)
            self.text_widget.see(END)

if __name__ == "__main__":
    app = ChatApplication()
    app.run()