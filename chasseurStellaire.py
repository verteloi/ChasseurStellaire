from modele import Modele
from vue import Vue

class Controleur:
    def __init__(self):
        self.modele = Modele(self,600,800)
        self.vue = Vue(self, self.modele)
        self.niveau_courant = 0
        self.boucle_jeu()
        self.vue.root.mainloop()

    def boucle_jeu(self):
        if self.modele.vaisseau.vie <= 0:
            self.gameOver()
            return  
        else:
            self.modele.mise_a_jour()
            self.vue.afficher_jeu()
            self.vue.root.after(30, self.boucle_jeu)
            nouveau_niveau = self.modele.levelUp()
            if self.niveau_courant != nouveau_niveau:
                self.niveauActuel()
                self.niveau_courant = nouveau_niveau

    def niveauActuel(self):
        niveauActuel = self.modele.levelUp()
        self.vue.affichageNiveau(niveauActuel)

    # Méthodes appelées par la Vue (via bindings)
    def deplacer_vaisseau(self, x):
        self.modele.deplacer_vaisseau(x)

    def tirer(self):
        self.modele.tirer()
        self.modele.shooting = True

    def release(self):
        self.modele.shooting = False

    def rejouer(self):
        self.vue.canevas.delete("all")
        self.modele = Modele(self,600,800)
        self.vue.modele = self.modele
        self.boucle_jeu()

    def gameOver(self):
        self.vue.clear_window()

    def enregistrerScore(self):
        try:
            with open("scores.txt", "a", encoding="utf-8") as f:
                f.write(f"Score : {self.modele.score}\n")
            print("Score enregistré avec succès !")

            if hasattr(self.vue, "btn_enregistrerScore"):
                self.vue.btn_enregistrerScore.destroy()
                
        except Exception as e:
            print("Erreur lors de l'enregistrement du score :", e)

if __name__ == "__main__":
    c = Controleur()