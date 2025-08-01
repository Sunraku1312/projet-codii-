import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 550
GRAPH_FIGSIZE = (5, 2.5)
GRAPH_DPI = 100
BUTTON_FONT = ("Helvetica", 14)
LABEL_FONT = ("Helvetica", 18)
INFO_LABEL_FONT = ("Helvetica", 12)

class Asset:
    def __init__(self, name, price, special=False):
        self.name = name
        self.price = price
        self.history = [price]
        self.stocks = 0
        self.down_count = 0
        self.special = special

    def update_price(self):

        variation = random.uniform(-15, 15)
        if random.random() < 0.1:
            variation -= 30

        if self.special:
            if random.random() < 0.55:
                variation = random.uniform(5, 20)
            else:
                variation = random.uniform(-10, 5)

        if self.down_count >= 3:
            variation = max(0, variation + random.uniform(5, 15))
            self.down_count = 0 

        self.price = max(1.0, self.price + variation)

        self.history.append(self.price)
        if variation < 0:
            self.down_count += 1
        else:
            self.down_count = 0

class Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

class HomePage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="🏠 Accueil", font=LABEL_FONT, bg='#2c3e50', fg="white").pack(pady=20)
        ttk.Button(self, text="Mon Portefeuille", command=lambda: controller.show_frame("PortfolioPage")).pack(pady=5)
        ttk.Button(self, text="Portefeuille Ennemi", command=lambda: controller.show_frame("EnemyPage")).pack(pady=5)
        ttk.Button(self, text="Boîte Mail", command=lambda: controller.show_frame("MailPage")).pack(pady=5)

class PortfolioPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        tk.Label(self, text="💼 Mon Portefeuille", font=LABEL_FONT, bg='#34495e', fg="white").pack(pady=10)

        self.asset_var = tk.StringVar()
        self.asset_menu = ttk.OptionMenu(self, self.asset_var, "")
        self.asset_menu.pack(pady=5)

        self.info_label = tk.Label(self, text="", font=INFO_LABEL_FONT, bg='#34495e', fg="white")
        self.info_label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        ttk.Button(self, text="Acheter", command=self.acheter).pack()
        ttk.Button(self, text="Vendre", command=self.vendre).pack()
        ttk.Button(self, text="Débloquer Nouveaux Marchés (500€)", command=self.unlock_assets).pack(pady=5)
        ttk.Button(self, text="Retour", command=lambda: controller.show_frame("HomePage")).pack(pady=10)

        self.message_label = tk.Label(self, text="", fg="blue", bg='#34495e')
        self.message_label.pack()

        self.fig = Figure(figsize=GRAPH_FIGSIZE, dpi=GRAPH_DPI)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack()

    def update_assets_menu(self):
        menu = self.asset_menu["menu"]
        menu.delete(0, "end")
        for name in self.controller.assets:
            menu.add_command(label=name, command=lambda value=name: self.asset_var.set(value))
        self.asset_var.set(list(self.controller.assets.keys())[0])

    def update_display(self):
        name = self.asset_var.get()
        asset = self.controller.assets[name]
        text = f"💰 Cash: {self.controller.cash:.2f} €\n📦 {name}: {asset.stocks} actions à {asset.price:.2f} €"
        self.info_label.config(text=text)
        self.update_graph(asset)

    def update_graph(self, asset):
        self.ax.clear()
        self.ax.plot(asset.history, marker='o', color='green')
        self.ax.set_title(f"Prix - {asset.name}")
        self.canvas.draw()

    def acheter(self):
        try:
            qte = int(self.entry.get())
            asset = self.controller.assets[self.asset_var.get()]
            cost = qte * asset.price
            if cost > self.controller.cash:
                self.message_label.config(text="❌ Pas assez d'argent", fg="red")
            else:
                self.controller.cash -= cost
                asset.stocks += qte
                self.message_label.config(text=f"Acheté {qte} actions de {asset.name}", fg="green")
            self.update_display()
        except:
            self.message_label.config(text="Entrez un nombre valide", fg="red")

    def vendre(self):
        try:
            qte = int(self.entry.get())
            asset = self.controller.assets[self.asset_var.get()]
            if qte > asset.stocks:
                self.message_label.config(text="❌ Pas assez d'actions", fg="red")
            else:
                asset.stocks -= qte
                self.controller.cash += qte * asset.price
                self.message_label.config(text=f"Vendu {qte} actions de {asset.name}", fg="green")
            self.update_display()
        except:
            self.message_label.config(text="Entrez un nombre valide", fg="red")

    def unlock_assets(self):
        if self.controller.cash < 500:
            self.message_label.config(text="❌ Pas assez d'argent", fg="red")
            return
        self.controller.cash -= 500
        self.controller.unlock_assets()
        self.update_assets_menu()
        self.update_display()
        self.message_label.config(text="🎉 Nouveaux marchés débloqués !", fg="green")

    def next_turn(self):
        self.controller.turn += 1
        for asset in self.controller.assets.values():
            asset.update_price()
        self.controller.enemy_turn()
        self.controller.check_messages()
        self.update_display()

class EnemyPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self, text="🧠 Portefeuille Ennemi", font=LABEL_FONT, bg='#34495e', fg="white")
        self.label.pack(pady=10)

        self.stats = tk.Label(self, text="", font=INFO_LABEL_FONT, bg='#34495e', fg="white")
        self.stats.pack(pady=10)

        ttk.Button(self, text="Retour", command=lambda: controller.show_frame("HomePage")).pack()

    def update_enemy_info(self, cash, total):
        self.stats.config(text=f"💰 Cash Ennemi: {cash:.2f} €\n📈 Valeur totale: {total:.2f} €")

class MailPage(Page):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="📬 Boîte Mail", font=LABEL_FONT, bg='#34495e', fg="white").pack(pady=10)
        self.textbox = tk.Text(self, width=60, height=15, state="disabled")
        self.textbox.pack()
        ttk.Button(self, text="Retour", command=lambda: controller.show_frame("HomePage")).pack()

class BourseGameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("💸 Jeu de Bourse VS Ennemi")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(bg='#2c3e50')

        self.cash = 1000.0

        self.assets = {"Sunraku Studio": Asset("Sunraku Studio", 100.0, special=True)}
        self.unlocked = ["Sunraku Studio"]
        self.turn = 0

        self.enemy_cash = 1000.0
        self.enemy_assets = {"Sunraku Studio": Asset("Sunraku Studio", 100.0)}

        container = tk.Frame(self, bg='#2c3e50')
        container.pack(fill="both", expand=True)

        self.frames = {}
        for PageClass in (HomePage, PortfolioPage, EnemyPage, MailPage):
            name = PageClass.__name__
            frame = PageClass(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")
        self.frames["PortfolioPage"].update_assets_menu()
        self.frames["PortfolioPage"].update_display()

        self.auto_update_market()

    def show_frame(self, name):
        self.frames[name].tkraise()
        if name == "EnemyPage":
            total = sum(a.price * a.stocks for a in self.enemy_assets.values())
            self.frames["EnemyPage"].update_enemy_info(self.enemy_cash, total)

    def unlock_assets(self):
        for name, price in [("Bitcoin", 30000), ("VSCode Inc.", 200)]:
            if name not in self.assets:
                self.assets[name] = Asset(name, price)
                self.enemy_assets[name] = Asset(name, price)

    def receive_mail(self, sender, content):
        self.textbox.config(state="normal")
        now = datetime.now().strftime("%H:%M")
        self.textbox.insert("end", f"[{now}] {sender} : {content}\n")
        self.textbox.config(state="disabled")
        self.textbox.see("end")


    def auto_update_market(self):
        for asset in self.assets.values():
            asset.update_price()
        self.enemy_turn()
        self.frames["PortfolioPage"].update_display()
        self.frames["EnemyPage"].update_enemy_info(self.enemy_cash, sum(a.stocks * a.price for a in self.enemy_assets.values()))
        self.after(3000, self.auto_update_market)

    def enemy_turn(self):
        for name, asset in self.enemy_assets.items():
            asset.update_price()
            if asset.price < 110 and self.enemy_cash >= asset.price:
                qte = int(self.enemy_cash // asset.price)
                asset.stocks += qte
                self.enemy_cash -= qte * asset.price
            elif asset.price > 115 and asset.stocks > 0:
                self.enemy_cash += asset.stocks * asset.price
                asset.stocks = 0

    def check_messages(self):
        total_player = sum(a.stocks * a.price for a in self.assets.values()) + self.cash
        total_enemy = sum(a.stocks * a.price for a in self.enemy_assets.values()) + self.enemy_cash
        mail = self.frames["MailPage"]

        if self.turn % 5 == 0:
            if total_enemy > total_player + 500:
                mail.receive_mail("Rival", "💰 J’espère que tu t’en sors bien... Moi je suis en lune de miel avec mes profits 😎")
            elif total_player > total_enemy + 500:
                mail.receive_mail("Rival", "😭 Mec... si t’as 50€ pour manger... j’te rembourse promis.")
            else:
                mail.receive_mail("Rival", "On est au coude à coude... mais j’ai un plan secret héhé.")

app = BourseGameApp()
app.mainloop()
