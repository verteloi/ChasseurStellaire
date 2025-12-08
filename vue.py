import tkinter as tk

class Vue:
    def __init__(self, controleur, modele):
        self.controleur = controleur
        self.modele = modele
        self.root = tk.Tk()
        self.root.title("Vertical Shooter - MVC")

        self.creer_fenetre_principale()
        self.creer_frame_canevas()
        self.creer_frame_infos()


    # ---------- Création de l'interface ----------
    def creer_fenetre_principale(self):
        self.frame_principale = tk.Frame(self.root)
        self.frame_principale.pack()

    def creer_frame_canevas(self):
        self.canevas = tk.Canvas(self.frame_principale, width=600, height=700, bg="black")
        self.canevas.grid(row=0, column=0)

        # Bindings (la Vue gère le canevas)
        self.canevas.bind("<Motion>", self.deplacer_vaisseau)
        self.canevas.bind("<Button-1>", self.tirer)
        self.canevas.bind("<ButtonRelease-1>", self.release)

    def creer_frame_infos(self):
        self.frame_infos = tk.Frame(self.frame_principale, bg="#222")
        self.frame_infos.grid(row=0, column=1, sticky="n")

        self.label_vie = tk.Label(self.frame_infos, text="Vies : 3", fg="white", bg="#222", font=("Arial", 12))
        self.label_vie.pack(pady=10)

        self.label_niveau = tk.Label(self.frame_infos, text="Niveau : 1", fg="white", bg="#222", font=("Arial", 12))
        self.label_niveau.pack(pady=10)

        self.label_score = tk.Label(self.frame_infos, text="Score : 0", fg="white", bg="#222", font=("Arial", 12))
        self.label_score.pack(pady=10)

    def clear_window(self):
        self.canevas.delete("all")
        self.canevas.config(bg="black")

        self.canevas.create_text(300, 250, text="GAME OVER", font=("Arial", 40, "bold"), fill="red")
        self.canevas.create_text(300, 320, text=f"Score finale : {self.modele.score} ovnis détruits", font=("Arial", 20), fill="white")
        self.btn_rejouer = tk.Button(self.root, text="Réessayer?", font=("Arial", 16), command=self.controleur.rejouer)
        self.canevas.create_window(300, 400, window=self.btn_rejouer)
        self.btn_enregistrerScore = tk.Button(self.root, text="Enregistrer Score", font=("Arial", 16), command=self.controleur.enregistrerScore)
        self.canevas.create_window(300, 450, window=self.btn_enregistrerScore)

    def affichageNiveau(self, niveau):
        self.delay = 2500
        self.texteNiveau = self.canevas.create_text(300, 250, text=f"NIVEAU {niveau}", font=("Arial", 40, "bold"), fill="yellow")

        def effacer_text():
            self.canevas.delete(self.texteNiveau)
        
        self.root.after(self.delay, effacer_text)

    # ---------- Affichage du jeu ----------
    def afficher_jeu(self):
        modele = self.modele
        self.canevas.delete("jeu")

        # --- Vaisseau du joueur ---
        v = modele.vaisseau
        self.canevas.create_rectangle(
            v.x - v.taille_x,
            v.y - 5,
            v.x + v.taille_x,
            v.y + 5,
            fill="grey", tags="jeu"
        )
        self.canevas.create_oval(
            v.x - (v.taille_x // 2),
            v.y - v.taille_y,
            v.x + (v.taille_x // 2),
            v.y - 5,
            fill="lightblue", tags="jeu"
        )
        self.canevas.create_line(
            v.x,
            v.y - v.taille_y,
            v.x,
            v.y - v.taille_y - 5,
            fill="grey",
            width=2, tags="jeu"
        )

        if (v.shield == True):
            self.canevas.create_line(
                v.x - 10,             
                v.y - v.taille_y - 10,    
                v.x + 10,             
                v.y - v.taille_y - 10,    
                fill="deepskyblue",
                width=4, tags="jeu"
        )

        # --- Projectiles ---
        for p in v.projectiles:
            self.canevas.create_rectangle(
                p.x - p.taille_x,
                p.y - p.taille_y,
                p.x + p.taille_x,
                p.y,
                fill="yellow", tags="jeu"
            )

        # --- OVNIs ---
        for o in modele.ovnis:
            self.canevas.create_rectangle(
                o.x - o.taille_x,
                o.y - o.taille_y,
                o.x + o.taille_x,
                o.y + o.taille_y,
                fill=o.couleur, tags="jeu"
            )
            self.canevas.create_line(
                o.x,
                o.y + o.taille_y,
                o.x,
                o.y + o.taille_y + 6,
                fill="grey",
                width=2, tags="jeu"
            )

        # --- Astéroïdes ---
        for a in modele.asteroides:
            self.canevas.create_oval(
                a.x - a.taille_x,
                a.y - a.taille_y,
                a.x + a.taille_x,
                a.y + a.taille_y,
                fill="gray", tags="jeu"
            )

        # --- Powerups ---
        for p in modele.powerups:
            self.canevas.create_oval(
                p.x - p.taille_x,
                p.y - p.taille_y,
                p.x + p.taille_x,
                p.y + p.taille_y,
                fill=p.color, tags="jeu"
            )

            # self.canevas.create_text(
            #     p.x, p.y + 10,                # Coordinates of the text's anchor point
            #         text="+1",    # The string to display
            #         fill="white",        # Text color
            #         font=("Arial", 20),  # Font settings
            # )

        # --- Explosion --
        for e in modele.explosion:
            self.canevas.create_oval(
                e.x - e.taille_x,
                e.y - e.taille_y,
                e.x + e.taille_x,
                e.y + e.taille_y,
                fill="red", tags="jeu"
            )

        # --- Infos ---
        self.label_vie.config(text=f"Vies : {v.vie}")
        self.label_niveau.config(text=f"Niveau : {modele.niveau}")
        self.label_score.config(text=f"Score : {modele.score}")

    def deplacer_vaisseau(self,evt):
        # on pourrait vouloir le déplacer en y aussi
        self.controleur.deplacer_vaisseau(evt.x)

    def tirer(self,evt):
        self.controleur.tirer()

    def rejouer(self):
        self.controleur.rejouer()

    def release(self, evt):
        self.controleur.release()
