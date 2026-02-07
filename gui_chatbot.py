import customtkinter as ctk
import tkinter as tk
import requests
import threading
from datetime import datetime
from tkinter import Canvas


COLORS = {
    "bg": "#020617",               # Deepest Midnight Blue
    "chat_bg": "#0f172a",          # Dark Slate Blue
    "gradient_start": "#0f172a",   # Dark Slate
    "gradient_mid": "#0e7490",     # Deep Teal
    "gradient_end": "#06b6d4",     # Electric Cyan
    "input_bg": "#1e293b",         # Slate Grey
    "user_msg": "#0891b2",         # Cyan/Teal
    "bot_msg": "#334155",          # Cool Grey
    "text": "#f8fafc",             # Bright White
    "subtext": "#94a3b8",          # Muted Blue-Grey
    "accent": "#22d3ee",           # Bright Electric Blue (Button)
    "glow": "#38bdf8",             # Light Blue Glow
    "border": "#1e293b",           # Subtle Border
    "green": "#10b981",            # Online Status
    "red": "#ef4444"               # Offline Status
}

FONT_MAIN = ("Segoe UI", 14)
FONT_MSG = ("Segoe UI", 13)
FONT_HEADER = ("Segoe UI", 20, "bold")
API_URL = "http://127.0.0.1:5000/chat"

# Set Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# ================== GRADIENT BACKGROUND ENGINE ==================
class GradientFrame(ctk.CTkFrame):
    """Animated gradient background"""
    def __init__(self, master, colors, orientation="vertical", **kwargs):
        super().__init__(master, **kwargs)
        self.colors = colors
        self.orientation = orientation
        self.canvas = Canvas(self, highlightthickness=0, bg=colors[0])
        self.canvas.pack(fill="both", expand=True)
        self.bind("<Configure>", self._draw_gradient)
        
    def _draw_gradient(self, event=None):
        width = self.winfo_width()
        height = self.winfo_height()
        if width < 2 or height < 2:
            return
            
        self.canvas.delete("gradient")
        
        if self.orientation == "horizontal":
            steps = max(width, 100)
            for i in range(steps):
                ratio = i / steps
                color = self._interpolate_color(ratio)
                x = int(i * width / steps)
                self.canvas.create_rectangle(
                    x, 0, x + width // steps + 1, height,
                    outline=color, fill=color, tags="gradient"
                )
        else:  # vertical
            steps = max(height, 100)
            for i in range(steps):
                ratio = i / steps
                color = self._interpolate_color(ratio)
                y = int(i * height / steps)
                self.canvas.create_rectangle(
                    0, y, width, y + height // steps + 1,
                    outline=color, fill=color, tags="gradient"
                )
    
    def _interpolate_color(self, ratio):
        """Interpolate between gradient colors"""
        num_colors = len(self.colors)
        if ratio >= 1:
            return self.colors[-1]
        
        segment = ratio * (num_colors - 1)
        idx = int(segment)
        local_ratio = segment - idx
        
        if idx >= num_colors - 1:
            return self.colors[-1]
            
        color1 = self.colors[idx]
        color2 = self.colors[idx + 1]
        
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)
        
        r = int(r1 + (r2 - r1) * local_ratio)
        g = int(g1 + (g2 - g1) * local_ratio)
        b = int(b1 + (b2 - b1) * local_ratio)
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    @staticmethod
    def _hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# ================== CUSTOM CHAT BUBBLE ==================
class ChatBubble(ctk.CTkFrame):
    def __init__(self, master, text, sender="bot", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.sender = sender
        is_user = sender == "user"

        # Container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=6)
        
        # Timestamp
        time_str = datetime.now().strftime("%I:%M %p")
        
        # Bubble with glow effect
        bubble_color = COLORS["user_msg"] if is_user else COLORS["bot_msg"]
        border_color = COLORS["glow"] if is_user else COLORS["border"]
        
        self.bubble = ctk.CTkFrame(
            container, 
            fg_color=bubble_color, 
            corner_radius=20,
            border_width=2 if is_user else 1,
            border_color=border_color
        )
        self.bubble.pack(side="right" if is_user else "left", padx=5)

        # Message Text
        self.label = ctk.CTkLabel(
            self.bubble, 
            text=text, 
            text_color=COLORS["text"], 
            font=FONT_MSG, 
            wraplength=350, 
            justify="left"
        )
        self.label.pack(padx=18, pady=(12, 5))

        # Time Label
        self.time = ctk.CTkLabel(
            self.bubble, 
            text=time_str, 
            text_color=COLORS["subtext"], 
            font=("Segoe UI", 9)
        )
        self.time.pack(padx=18, pady=(0, 10), anchor="e")


# ================== MAIN APP ==================
class ModernChatbot(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Clothing Brand Chatbot")
        self.geometry("500x750")
        self.resizable(False, False)
        self.configure(fg_color=COLORS["bg"])

        # Layout
        self.create_header()
        self.create_chat_area()
        self.create_input_area()

        # Check server status
        self.check_server_status()

    def create_header(self):
        """Gradient header with modern design"""
        header = GradientFrame(
            self, 
            colors=[COLORS["gradient_start"], COLORS["gradient_mid"], COLORS["gradient_end"]],
            orientation="horizontal",
            height=90
        )
        header.pack(fill="x", pady=(0, 0))
        header.pack_propagate(False)
        
        # Content on top of gradient
        content = ctk.CTkFrame(header.canvas, fg_color="transparent")
        header.canvas.create_window(250, 45, window=content)
        
        # Avatar with glow
        avatar_frame = ctk.CTkFrame(
            content, 
            width=60, 
            height=60,
            fg_color=COLORS["bg"],
            corner_radius=30,
            border_width=2,
            border_color=COLORS["glow"]
        )
        avatar_frame.pack(side="left", padx=15)
        avatar_frame.pack_propagate(False)
        
        avatar = ctk.CTkLabel(
            avatar_frame, 
            text="👔",  # Changed icon to clothing
            font=("Arial", 28)
        )
        avatar.pack(expand=True)

        # Title & Status
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.pack(side="left", padx=10)

        # UPDATED TITLE HERE
        title = ctk.CTkLabel(
            info_frame, 
            text="Clothing Brand Chatbot", 
            font=FONT_HEADER, 
            text_color=COLORS["text"]
        )
        title.pack(anchor="w")

        self.status = ctk.CTkLabel(
            info_frame, 
            text="● Connecting...", 
            font=("Segoe UI", 10), 
            text_color=COLORS["subtext"]
        )
        self.status.pack(anchor="w")

    def create_chat_area(self):
        """Chat area with custom styling"""
        chat_container = ctk.CTkFrame(self, fg_color=COLORS["chat_bg"], corner_radius=0)
        chat_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        self.scroll_frame = ctk.CTkScrollableFrame(
            chat_container, 
            fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["glow"]
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=10)
        
        self.messages_inner = []

    def create_input_area(self):
        """Futuristic input with gradient button"""
        input_frame = ctk.CTkFrame(self, height=100, fg_color=COLORS["bg"])
        input_frame.pack(fill="x", padx=15, pady=15)
        input_frame.pack_propagate(False)
        
        # Input container with border glow
        input_container = ctk.CTkFrame(
            input_frame,
            fg_color=COLORS["input_bg"],
            corner_radius=28,
            border_width=2,
            border_color=COLORS["border"]
        )
        input_container.pack(fill="both", expand=True)

        self.entry = ctk.CTkEntry(
            input_container, 
            placeholder_text="Type your message...",
            height=50,
            border_width=0,
            fg_color="transparent",
            text_color=COLORS["text"],
            font=FONT_MAIN,
            placeholder_text_color=COLORS["subtext"]
        )
        self.entry.pack(side="left", fill="both", expand=True, padx=20, pady=15)
        self.entry.bind("<Return>", self.start_send_process)

        self.send_btn = ctk.CTkButton(
            input_container, 
            text="➤", 
            width=55, 
            height=55,
            fg_color=COLORS["accent"],
            hover_color=COLORS["glow"],
            font=("Arial", 22, "bold"),
            corner_radius=28,
            text_color="#000000",
            command=self.start_send_process
        )
        self.send_btn.pack(side="right", padx=10)

    def check_server_status(self):
        """Check Flask server status"""
        def check():
            try:
                response = requests.get("http://127.0.0.1:5000/", timeout=2)
                if response.status_code == 200:
                    self.after(0, lambda: self.status.configure(
                        text="● Online",
                        text_color=COLORS["green"]
                    ))
                    # Add welcome message
                    self.after(500, lambda: self.receive_message(
                        "Welcome to our Clothing Brand! 👔\n\nAsk me about:\n• New Arrivals\n• Size Guides\n• Return Policy\n\nHow can I help you style up today?"
                    ))
                else:
                    self.show_offline_status()
            except:
                self.show_offline_status()
        
        threading.Thread(target=check, daemon=True).start()
    
    def show_offline_status(self):
        self.status.configure(
            text="● Server Offline",
            text_color=COLORS["red"]
        )
        self.after(500, lambda: self.receive_message(
            "⚠️ System Message\n\nThe server is currently offline.\nPlease start the Flask backend."
        ))

    def start_send_process(self, event=None):
        msg = self.entry.get().strip()
        if not msg: 
            return

        # Clear & disable entry
        self.entry.delete(0, "end")
        self.entry.configure(state="disabled")
        self.send_btn.configure(state="disabled")

        # Add user message
        self.add_bubble(msg, "user")

        # Fetch response in thread
        threading.Thread(target=self.fetch_response, args=(msg,), daemon=True).start()

    def fetch_response(self, msg):
        """Get response from Flask API"""
        try:
            response = requests.post(API_URL, json={"message": msg}, timeout=10)
            reply = response.json().get("reply", "I didn't understand that.")
        except requests.exceptions.ConnectionError:
            reply = "🚫 Connection Error: Is the server running?"
        except requests.exceptions.Timeout:
            reply = "⏱️ Timeout: Server took too long."
        except Exception as e:
            reply = f"⚠️ Error: {str(e)}"

        # Update UI
        self.after(0, lambda: self.receive_message(reply))

    def receive_message(self, text):
        """Re-enable input and show bot response"""
        self.entry.configure(state="normal")
        self.send_btn.configure(state="normal")
        self.typing_simulation(text)

    def typing_simulation(self, text, index=0, current_bubble=None):
        """Typewriter effect for bot messages"""
        if index == 0:
            current_bubble = ChatBubble(self.scroll_frame, text="", sender="bot")
            current_bubble.pack(fill="x", pady=5)
            self.messages_inner.append(current_bubble)
            self.scroll_to_bottom()
        
        if index < len(text):
            current_text = text[:index+1]
            current_bubble.label.configure(text=current_text + " ▌")
            speed = 8 if len(text) > 100 else 20
            self.after(speed, lambda: self.typing_simulation(text, index+1, current_bubble))
        else:
            current_bubble.label.configure(text=text)
            self.scroll_to_bottom()

    def add_bubble(self, text, sender):
        """Add message bubble to chat"""
        bubble = ChatBubble(self.scroll_frame, text=text, sender=sender)
        bubble.pack(fill="x", pady=5)
        self.messages_inner.append(bubble)
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        """Auto-scroll to latest message"""
        self.scroll_frame.update_idletasks()
        self.scroll_frame._parent_canvas.yview_moveto(1.0)

if __name__ == "__main__":
    app = ModernChatbot()
    app.mainloop()