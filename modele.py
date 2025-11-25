import random

# ------------------ CLASSES ------------------
prochain_id = 0

def createur_identifiant():
    global prochain_id
    prochain_id += 1
    return "id_"+str(prochain_id)

class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vitesse = -10  # vers le haut
        self.taille_x = 2
        self.taille_y = 10

    def mise_a_jour(self):
        self.y += self.vitesse


class Powerup:
    def __init__(self, x, y, vitesse, id, type):
        self.x = x
        self.y = y
        self.vitesse = 5
        self.taille_x = 10
        self.taille_y = 10
        self.type = ["vie", "shield"]
        self.id = id

    def mise_a_jour(self):
        self.y += self.vitesse


class Vaisseau:
    def __init__(self, x, y, modele):
        self.x = x
        self.y = y
        self.vie = 3
        self.projectiles = []
        self.taille_x = 15
        self.taille_y = 15
        self.modele = modele  

    def deplacer(self, x):
        self.x = x
    def tirer(self):
        match self.modele.niveau :
            case 1:
                nouveau_proj = Projectile(self.x, self.y - 20)
                self.projectiles.append(nouveau_proj)
            case 2:
                nouveau_proj = Projectile(self.x, self.y - 20)
                self.projectiles.append(nouveau_proj)
            case 3:
                nouveau_proj = Projectile(self.x, self.y - 20)
                self.projectiles.append(nouveau_proj)
                nouveau_proj = Projectile(self.x - 20, self.y - 20)
                self.projectiles.append(nouveau_proj)
                nouveau_proj = Projectile(self.x + 20, self.y - 20)
                self.projectiles.append(nouveau_proj)
            case 4:
                self.taille_x = 4
                nouveau_proj = Projectile(self.x - 10, self.y - 20)
                self.projectiles.append(nouveau_proj)
                nouveau_proj = Projectile(self.x + 10, self.y - 20)
                self.projectiles.append(nouveau_proj)
                nouveau_proj = Projectile(self.x - 20, self.y - 20)
                self.projectiles.append(nouveau_proj)
                nouveau_proj = Projectile(self.x + 20, self.y - 20)
                self.projectiles.append(nouveau_proj)
            case 5:
                self.niveau = 5

    def mise_a_jour(self):
        for p in self.projectiles:
            p.mise_a_jour()

        self.projectiles = [
            p for p in self.projectiles
            if p.y > 0
        ]


class OVNI:
    def __init__(self, x, y, vy, id):
        self.x = x
        self.y = y
        self.vy = vy
        self.taille_x = 12
        self.taille_y = 6
        self.id = id 
        self.degat = 1

    def mise_a_jour(self):
        self.y += self.vy


class Asteroide:
    def __init__(self, x, y, vy, id):
        self.x = x
        self.y = y
        self.vy = vy
        self.size = random.randint(10, 50)
        self.taille_x = self.size
        self.taille_y = self.size
        self.degat = 1
        self.id = id

    def mise_a_jour(self):
        self.y += self.vy


# ------------------ MODÈLE ------------------

class Modele:
    def __init__(self, parent, largeur, hauteur):
        self.parent = parent
        self.largeur = 600
        self.hauteur = 700
        self.vaisseau = Vaisseau(self.largeur // 2, self.hauteur - 50, self)
        self.ovnis = []
        self.asteroides = []
        self.powerups = []
        self.score = 0
        self.niveau = 1
        self.compteur = 0
        self.shooting = False


    #Collision ovni/vaisseau
    def collisionOvniVaisseau(self):
        for o in list(self.ovnis):
            if o.x - o.taille_x <= self.vaisseau.x <= o.x + o.taille_x and o.y - o.taille_y <= self.vaisseau.y <= o.y + o.taille_y:
                self.supprimerOvni(o.id)
                self.vaisseau.vie -= o.degat
                if (self.vaisseau.vie == 0):
                    self.parent.rejouer()
                break

    #Collision asteroide/vaisseau
    def collisionAsteroideVaisseau(self):
        for a in list(self.asteroides):
            if a.x - a.taille_x <= self.vaisseau.x <= a.x + a.taille_x and a.y - a.taille_y <= self.vaisseau.y <= a.y + a.taille_y:
                self.supprimerAsteroide(a.id)
                self.vaisseau.vie -= a.degat
                if (self.vaisseau.vie == 0):
                    self.parent.rejouer()
                break

    #Collision powerup/vaisseau
    def collisionPowerupVaisseau(self):
        for p in list(self.powerups):
            if p.x - p.taille_x <= self.vaisseau.x <= p.x + p.taille_x and p.y - p.taille_y <= self.vaisseau.y <= p.y + p.taille_y:
                print("collision")
                self.supprimerPowerup(p.id)
                break

    #Collision tire/ovni:
    def collisionProjectile(self):
        for o in list(self.ovnis):
            for p in list(self.vaisseau.projectiles):
                if o.x - o.taille_x <= p.x <= o.x + o.taille_x and o.y - o.taille_y <= p.y <= o.y + o.taille_y:
                    self.supprimerOvni(o.id)
                    self.vaisseau.projectiles.remove(p)
                    self.score += 1

                    alea_power = random.random()
                    if alea_power < 1:
                        nouveau_power = Powerup(o.x,o.y, 10, createur_identifiant(), "vie")
                        self.powerups.append(nouveau_power)
                    break

    # verifier tous les collisions
    def verifierToutCollisions(self):
        self.collisionOvniVaisseau()
        self.collisionAsteroideVaisseau()
        self.collisionProjectile()
        self.collisionPowerupVaisseau()

    def supprimerOvni(self, id):
        for o in self.ovnis:
            if o.id == id:
                self.ovnis.remove(o)
                break

    def supprimerAsteroide(self, id):
        for a in self.asteroides:
            if a.id == id:
                self.asteroides.remove(a)
                break

    def supprimerPowerup(self, id):
        for p in self.powerups:
            if p.id == id:
                self.powerups.remove(p)
                break


    def deplacer_vaisseau(self,x):
        self.vaisseau.deplacer(x)
    def tirer(self):
        self.vaisseau.tirer()
    def mise_a_jour(self):
        self.vaisseau.mise_a_jour()
        self.verifierToutCollisions()
        self.levelUp()

        if self.niveau >= 2:
            if self.shooting:
                if self.compteur >= 4:   # 7 frames ~ cooldown
                    self.vaisseau.tirer()
                    self.compteur = 0


        # Apparition aléatoire des ennemis
        alea_ovni = random.random()
        if alea_ovni < 0.10:
            nouvel_ovni = OVNI(
                random.randint(0, self.largeur),
                0,
                random.randint(2, 5),
                createur_identifiant()
            )
            self.ovnis.append(nouvel_ovni)

        alea_asteroide = random.random()
        if alea_asteroide < 0.01:
            nouvel_ast = Asteroide(
                random.randint(0, self.largeur),
                0,
                random.randint(3, 6),
                createur_identifiant()
            )
            self.asteroides.append(nouvel_ast)

        # Déplacement des ennemis
        for o in self.ovnis:
            o.mise_a_jour()

        for a in self.asteroides:
            a.mise_a_jour()

        for p in self.powerups:
            p.mise_a_jour()

        # Nettoyage des objets sortis de l'écran
        self.ovnis = [
            o for o in self.ovnis
            if o.y < self.hauteur
        ]

        self.asteroides = [
            a for a in self.asteroides
            if a.y < self.hauteur
        ]

        self.powerups = [
            p for p in self.powerups
            if p.y < self.hauteur
        ]

        self.compteur += 1

    def levelUp(self):
        match self.score :
            case 10:
                self.niveau = 2
            case 25:
                self.niveau = 3
            case 50:
                self.niveau = 4
            case 100:
                self.niveau = 5
