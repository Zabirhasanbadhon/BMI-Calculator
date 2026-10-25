import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os


BG = "#eef4f7"
CARD = "#ffffff"
PRIMARY = "#245b73"
PRIMARY_DARK = "#17445a"
ACCENT = "#49b9bd"
TEXT = "#263238"
MUTED = "#71808a"
BORDER = "#dce6ea"

FONT = "Segoe UI"


class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("ZaBir | BMI Calculator")
        self.root.geometry("900x650")
        self.root.minsize(780, 580)
        self.root.configure(bg=BG)

        # Keep images alive
        self.images = {}

        self.load_images()
        self.setup_styles()
        self.build_ui()

        self.root.bind("<Return>", lambda event: self.calculate_bmi())
        self.root.bind("<Escape>", lambda event: self.clear_fields())

    # --------------------------------------------------------
    # Images
    # --------------------------------------------------------
    def load_images(self):
        base = os.path.dirname(os.path.abspath(__file__))

        def load(name, size=None):
            path = os.path.join(base, name)
            if not os.path.exists(path):
                return None
            try:
                img = Image.open(path).convert("RGBA")
                if size:
                    img.thumbnail(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception:
                return None

        self.images["icon"] = load("icon.png", (82, 82))
        self.images["top"] = load("top.png", (496, 80))
        self.images["man"] = load("man.png", (55, 210))
        self.images["scale"] = load("scale.png", (45, 220))
        self.images["box"] = load("box.png", (150, 140))

    # --------------------------------------------------------
    # Styles
    # --------------------------------------------------------
    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Modern.TEntry",
            fieldbackground="#f8fafb",
            background="#f8fafb",
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            padding=12,
            relief="flat",
            font=(FONT, 12)
        )

        style.configure(
            "Modern.TCombobox",
            fieldbackground="#f8fafb",
            background="#f8fafb",
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            padding=10,
            font=(FONT, 11)
        )

        style.configure(
            "Primary.TButton",
            font=(FONT, 11, "bold"),
            foreground="white",
            background=PRIMARY,
            borderwidth=0,
            padding=(22, 12)
        )
        style.map(
            "Primary.TButton",
            background=[("active", PRIMARY_DARK), ("pressed", PRIMARY_DARK)]
        )

        style.configure(
            "Clear.TButton",
            font=(FONT, 10, "bold"),
            foreground=PRIMARY,
            background="#e7f1f4",
            borderwidth=0,
            padding=(18, 12)
        )
        style.map(
            "Clear.TButton",
            background=[("active", "#d6e8ed"), ("pressed", "#d6e8ed")]
        )

    # --------------------------------------------------------
    # Helpers
    # --------------------------------------------------------
    def rounded_frame(self, parent, bg=CARD, padx=20, pady=20):
        frame = tk.Frame(
            parent,
            bg=bg,
            highlightbackground=BORDER,
            highlightthickness=1,
            bd=0
        )
        frame.pack_propagate(False)
        return frame

    def label(self, parent, text, size=11, weight="normal", color=TEXT, **kwargs):
        return tk.Label(
            parent,
            text=text,
            font=(FONT, size, weight),
            fg=color,
            bg=parent.cget("bg"),
            **kwargs
        )

    # --------------------------------------------------------
    # Main UI
    # --------------------------------------------------------
    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=PRIMARY, height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        header_left = tk.Frame(header, bg=PRIMARY)
        header_left.pack(side="left", padx=28, pady=12)

        if self.images.get("icon"):
            tk.Label(
                header_left,
                image=self.images["icon"],
                bg=PRIMARY
            ).pack(side="left", padx=(0, 14))

        title_box = tk.Frame(header_left, bg=PRIMARY)
        title_box.pack(side="left")

        tk.Label(
            title_box,
            text="ZaBir HaSan",
            font=(FONT, 23, "bold"),
            fg="white",
            bg=PRIMARY
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text="Check your Body Mass Index in seconds",
            font=(FONT, 10),
            fg="#d9eef1",
            bg=PRIMARY
        ).pack(anchor="w", pady=(2, 0))

        # Decorative image on header
        if self.images.get("top"):
            tk.Label(
                header,
                image=self.images["top"],
                bg=PRIMARY
            ).pack(side="right", padx=18)

        # Content
        content = tk.Frame(self.root, bg=BG)
        content.pack(fill="both", expand=True, padx=24, pady=22)

        # Left input card
        input_card = tk.Frame(
            content,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        input_card.pack(side="left", fill="both", expand=True, padx=(0, 12))

        # Right result card
        result_card = tk.Frame(
            content,
            bg=PRIMARY,
            highlightbackground=PRIMARY,
            highlightthickness=1
        )
        result_card.pack(side="right", fill="both", expand=True, padx=(12, 0))

        self.build_input_card(input_card)
        self.build_result_card(result_card)

        # Footer
        footer = tk.Frame(self.root, bg=BG, height=34)
        footer.pack(fill="x")
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="BMI categories follow commonly used adult BMI ranges.",
            font=(FONT, 9),
            fg=MUTED,
            bg=BG
        ).pack(side="left", padx=28)

        tk.Label(
            footer,
            text="Enter = Calculate   •   Esc = Clear",
            font=(FONT, 9, "bold"),
            fg=MUTED,
            bg=BG
        ).pack(side="right", padx=28)

    def build_input_card(self, card):
        top = tk.Frame(card, bg=CARD)
        top.pack(fill="x", padx=28, pady=(26, 12))

        tk.Label(
            top,
            text="Your Information",
            font=(FONT, 18, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w")

        tk.Label(
            top,
            text="Enter your details below to calculate your BMI.",
            font=(FONT, 10),
            fg=MUTED,
            bg=CARD
        ).pack(anchor="w", pady=(4, 0))

        form = tk.Frame(card, bg=CARD)
        form.pack(fill="x", padx=28, pady=10)

        # Gender
        tk.Label(
            form, text="Gender", font=(FONT, 10, "bold"),
            fg=TEXT, bg=CARD
        ).grid(row=0, column=0, sticky="w", pady=(6, 7))

        self.gender = tk.StringVar(value="Male")
        gender_frame = tk.Frame(form, bg=CARD)
        gender_frame.grid(row=1, column=0, sticky="ew", pady=(0, 14))

        for value in ("Male", "Female"):
            rb = tk.Radiobutton(
                gender_frame,
                text=value,
                value=value,
                variable=self.gender,
                font=(FONT, 10),
                fg=TEXT,
                bg=CARD,
                activebackground=CARD,
                activeforeground=PRIMARY,
                selectcolor="#e7f1f4",
                padx=8
            )
            rb.pack(side="left", padx=(0, 12))

        # Weight
        tk.Label(
            form, text="Weight (kg)", font=(FONT, 10, "bold"),
            fg=TEXT, bg=CARD
        ).grid(row=2, column=0, sticky="w", pady=(5, 7))

        weight_box = tk.Frame(
            form, bg="#f8fafb",
            highlightbackground=BORDER, highlightthickness=1
        )
        weight_box.grid(row=3, column=0, sticky="ew", pady=(0, 14))

        self.weight_var = tk.StringVar()
        self.weight_entry = tk.Entry(
            weight_box,
            textvariable=self.weight_var,
            font=(FONT, 12),
            bg="#f8fafb",
            fg=TEXT,
            insertbackground=PRIMARY,
            relief="flat",
            bd=0
        )
        self.weight_entry.pack(side="left", fill="x", expand=True, padx=12, pady=10)

        tk.Label(
            weight_box, text="kg", font=(FONT, 10, "bold"),
            fg=PRIMARY, bg="#f8fafb"
        ).pack(side="right", padx=12)

        # Height
        tk.Label(
            form, text="Height (cm)", font=(FONT, 10, "bold"),
            fg=TEXT, bg=CARD
        ).grid(row=4, column=0, sticky="w", pady=(5, 7))

        height_box = tk.Frame(
            form, bg="#f8fafb",
            highlightbackground=BORDER, highlightthickness=1
        )
        height_box.grid(row=5, column=0, sticky="ew", pady=(0, 18))

        self.height_var = tk.StringVar()
        self.height_entry = tk.Entry(
            height_box,
            textvariable=self.height_var,
            font=(FONT, 12),
            bg="#f8fafb",
            fg=TEXT,
            insertbackground=PRIMARY,
            relief="flat",
            bd=0
        )
        self.height_entry.pack(side="left", fill="x", expand=True, padx=12, pady=10)

        tk.Label(
            height_box, text="cm", font=(FONT, 10, "bold"),
            fg=PRIMARY, bg="#f8fafb"
        ).pack(side="right", padx=12)

        # Buttons
        buttons = tk.Frame(form, bg=CARD)
        buttons.grid(row=6, column=0, sticky="ew", pady=(2, 0))

        ttk.Button(
            buttons,
            text="Calculate BMI",
            style="Primary.TButton",
            command=self.calculate_bmi
        ).pack(side="left", fill="x", expand=True, padx=(0, 6))

        ttk.Button(
            buttons,
            text="Clear",
            style="Clear.TButton",
            command=self.clear_fields
        ).pack(side="right", padx=(6, 0))

        # Tip / image
        tip = tk.Frame(card, bg="#f2f8fa")
        tip.pack(fill="x", padx=28, pady=(12, 24))

        if self.images.get("man"):
            tk.Label(tip, image=self.images["man"], bg="#f2f8fa").pack(
                side="left", padx=(12, 8), pady=10
            )

        tk.Label(
            tip,
            text="Tip\nUse your height and weight in the units shown above.",
            justify="left",
            font=(FONT, 9),
            fg=PRIMARY_DARK,
            bg="#f2f8fa"
        ).pack(side="left", pady=12)

    def build_result_card(self, card):
        # Header
        tk.Label(
            card,
            text="YOUR BMI RESULT",
            font=(FONT, 11, "bold"),
            fg="#cfecef",
            bg=PRIMARY
        ).pack(pady=(26, 4))

        self.status_label = tk.Label(
            card,
            text="Ready",
            font=(FONT, 11, "bold"),
            fg="white",
            bg=PRIMARY
        )
        self.status_label.pack()

        # BMI number
        self.bmi_value = tk.Label(
            card,
            text="--",
            font=(FONT, 58, "bold"),
            fg="white",
            bg=PRIMARY
        )
        self.bmi_value.pack(pady=(10, 0))

        tk.Label(
            card,
            text="BMI",
            font=(FONT, 11, "bold"),
            fg="#cfecef",
            bg=PRIMARY
        ).pack()

        # Category
        self.category_label = tk.Label(
            card,
            text="Enter your information",
            font=(FONT, 17, "bold"),
            fg="white",
            bg=PRIMARY
        )
        self.category_label.pack(pady=(20, 5))

        self.message_label = tk.Label(
            card,
            text="Your result will appear here.",
            font=(FONT, 9),
            fg="#d9eef1",
            bg=PRIMARY,
            wraplength=300,
            justify="center"
        )
        self.message_label.pack(padx=25)

        # Scale image
        if self.images.get("scale"):
            tk.Label(
                card,
                image=self.images["scale"],
                bg=PRIMARY
            ).pack(side="bottom", pady=(5, 16))

        # Bottom status bar
        self.range_label = tk.Label(
            card,
            text="Underweight  < 18.5   |   Normal  18.5–24.9   |   Overweight  25–29.9   |   Obese  ≥ 30",
            font=(FONT, 8),
            fg="#d9eef1",
            bg=PRIMARY,
            wraplength=330,
            justify="center"
        )
        self.range_label.pack(side="bottom", pady=(0, 4))

    # --------------------------------------------------------
    # BMI calculation
    # --------------------------------------------------------
    def calculate_bmi(self):
        weight_text = self.weight_var.get().strip().replace(",", ".")
        height_text = self.height_var.get().strip().replace(",", ".")

        if not weight_text or not height_text:
            messagebox.showwarning(
                "Missing Information",
                "Please enter both your weight and height."
            )
            return

        try:
            weight = float(weight_text)
            height_cm = float(height_text)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numbers for weight and height."
            )
            return

        if weight <= 0 or height_cm <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Weight and height must be greater than zero."
            )
            return

        if weight > 500 or height_cm > 300:
            messagebox.showerror(
                "Unusual Value",
                "Please check your weight and height values."
            )
            return

        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)

        if bmi < 18.5:
            category = "Underweight"
            message = "Your BMI is below the commonly used healthy range."
        elif bmi < 25:
            category = "Normal Weight"
            message = "Your BMI is within the commonly used healthy range."
        elif bmi < 30:
            category = "Overweight"
            message = "Your BMI is above the commonly used healthy range."
        else:
            category = "Obesity"
            message = "Your BMI is in the obesity range."

        self.bmi_value.config(text=f"{bmi:.1f}")
        self.category_label.config(text=category)
        self.message_label.config(text=message)
        self.status_label.config(text=f"{self.gender.get()} • {weight:g} kg • {height_cm:g} cm")

    # --------------------------------------------------------
    # Clear
    # --------------------------------------------------------
    def clear_fields(self):
        self.weight_var.set("")
        self.height_var.set("")
        self.gender.set("Male")
        self.bmi_value.config(text="--")
        self.category_label.config(text="Enter your information")
        self.message_label.config(text="Your result will appear here.")
        self.status_label.config(text="Ready")
        self.weight_entry.focus_set()


def main():
    root = tk.Tk()

    # Windows taskbar / title icon
    try:
        icon_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "icon.png"
        )
        if os.path.exists(icon_path):
            icon = ImageTk.PhotoImage(Image.open(icon_path).convert("RGBA"))
            root.iconphoto(True, icon)
            root._app_icon = icon
    except Exception:
        pass

    BMICalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
