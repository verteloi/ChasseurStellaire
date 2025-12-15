import random

# ------------------ CLASSES ------------------
prochain_id = 0

def createur_identifiant():
    global prochain_id
    prochain_id += 1
    return "id_"+str(prochain_id)

class Projectile:
    def __init__(self, x, y, vx = 0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vitesse = -10  # vers le haut
        self.taille_x = 2
        self.taille_y = 10

    def mise_a_jour(self):
        self.y += self.vitesse
        self.x += self.vx

class Powerup:
    def __init__(self, x, y, vitesse, id):
        self.x = x
        self.y = y
        self.vitesse = 5
        self.taille_x = 10
        self.taille_y = 10
        self.type = type
        self.id = id
        self.powerupRandom()
        self.setColor()

    def mise_a_jour(self):
        self.y += self.vitesse

    def powerupRandom(self):
        self.randomNumber = random.randint(1, 3)
        match self.randomNumber :
            case 1:
                self.type = "vie"
            case 2:
                self.type = "shield"
            case 3:
                self.type = "exp"

    def setColor(self):
        match self.type :
            case "vie":
                self.color = "firebrick"
            case "shield":
                self.color = "deepskyblue" 
            case "exp":
                self.color = "forestgreen"

class Vaisseau:
    def __init__(self, x, y, modele):
        self.x = x
        self.y = y
        self.vie = 3
        self.projectiles = []
        self.taille_x = 15
        self.taille_y = 15
        self.modele = modele  
        self.shield = False

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
                centre = Projectile(self.x, self.y - 20)                      
                gauche = Projectile(self.x - 20, self.y - 20, vx=-3)           
                droite = Projectile(self.x + 20, self.y - 20, vx=3)           
                self.projectiles.extend([centre, gauche, droite])
            case 4:
                tir1 = Projectile(self.x - 20, self.y - 20)
                tir2 = Projectile(self.x - 7, self.y - 20)
                tir3 = Projectile(self.x + 7, self.y - 20)
                tir4 = Projectile(self.x + 20, self.y - 20)

                self.projectiles.extend([tir1, tir2, tir3, tir4])

            case 5:
                # Center
                centre = Projectile(self.x, self.y - 20)
                # Inner diagonals (mild angle)
                inner_left = Projectile(self.x - 15, self.y - 20, vx=-2)
                inner_right = Projectile(self.x + 15, self.y - 20, vx=2)
                # Outer diagonals (stronger angle)
                outer_left = Projectile(self.x - 30, self.y - 20, vx=-4)
                outer_right = Projectile(self.x + 30, self.y - 20, vx=4)
                self.projectiles.extend([
                    centre,
                    inner_left, inner_right,
                    outer_left, outer_right
                ])

    def mise_a_jour(self):
        for p in self.projectiles:
            p.mise_a_jour()

        self.projectiles = [
            p for p in self.projectiles
            if p.y > 0
        ]

class MINE:
    def __init__(self,x,y,vy,vie):
        self.x = x
        self.y = y
        self.vy = vy
        self.taille_x = 10
        self.taille_y = 10
        self.vie = vie
        self.degat = 1

    def mise_a_jour(self):
        self.y += self.vy



class OVNI:
    def __init__(self, x, y, vy, id, vie):
        self.x = x
        self.y = y
        self.vy = vy
        self.taille_x = 12
        self.taille_y = 6
        self.id = id 
        self.vie = vie
        self.degat = 1
        self.couleur_ovni()

    def couleur_ovni(self):
        match self.vie :
            case 1:
                self.couleur = "firebrick"
            case 2:
                self.couleur = "coral1"
            case 3:
                self.couleur = "darkorange"
            case 4:
                self.couleur = "chocolate1"
            case 5:
                self.couleur = "yellow"

    def mise_a_jour(self):
        self.y += self.vy
        self.couleur_ovni()

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

class Explosion:
    def __init__(self ,x, y,contact):
        self.x = x
        self.y = y
        self.taille_x = 10
        self.taille_y = 10
        self.tik = 2.5
        self.opacity = 1
        self.status = 1
        self.contact = contact



    def mise_a_jour(self):
        tailleMmax = 30 if self.contact == 1 else 50
        print(tailleMmax)
        if (self.taille_y <= tailleMmax and self.status == 1):
            self.taille_x += self.tik
            self.taille_y += self.tik
            if(self.taille_x >= tailleMmax):
                self.status = 2

        if(self.status == 2):
            self.taille_x -= self.tik
            self.taille_y -= self.tik
        if(self.taille_x <= 0 and self.taille_y <= 0 and self.status == 2):
            self.taille_x = 0
            self.taille_y = 0
            return 3


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
        self.explosion = []
        self.mine = []


    #Collision ovni/vaisseau
    def collisionOvniVaisseau(self):
        for o in list(self.ovnis):
            if o.x - o.taille_x <= self.vaisseau.x <= o.x + o.taille_x and o.y - o.taille_y <= self.vaisseau.y <= o.y + o.taille_y:
                self.supprimerOvni(o.id)
                if (self.vaisseau.shield == True):
                    self.vaisseau.shield = False
                else:
                    self.vaisseau.vie -= o.degat
                if (self.vaisseau.vie == 0):
                    self.parent.gameOver()
                break

    #Collision asteroide/vaisseau
    def collisionAsteroideVaisseau(self):
        for a in list(self.asteroides):
            if a.x - a.taille_x <= self.vaisseau.x <= a.x + a.taille_x and a.y - a.taille_y <= self.vaisseau.y <= a.y + a.taille_y:
                self.supprimerAsteroide(a.id)
                if (self.vaisseau.shield == True):
                    self.vaisseau.shield = False
                else:
                    self.vaisseau.vie -= a.degat
                if (self.vaisseau.vie == 0):
                    self.parent.gameOver()
                break

    #Collision powerup/vaisseau
    def collisionPowerupVaisseau(self):
        for p in list(self.powerups):
            if p.x - p.taille_x <= self.vaisseau.x <= p.x + p.taille_x and p.y - p.taille_y <= self.vaisseau.y <= p.y + p.taille_y:
                match p.type :
                    case "vie":
                        self.vaisseau.vie += 1
                    case "shield":
                        self.vaisseau.shield = True
                    case "exp":
                        self.score += 1

                self.supprimerPowerup(p.id)
                break

    #Collision tire/ovni:
    def collisionProjectile(self):
        for o in list(self.ovnis):
            for p in list(self.vaisseau.projectiles):
                if o.x - o.taille_x <= p.x <= o.x + o.taille_x and o.y - o.taille_y <= p.y <= o.y + o.taille_y:
                    o.vie -= 1
                    self.vaisseau.projectiles.remove(p)
                    if (o.vie == 0):
                        self.supprimerOvni(o.id)
                        self.score += 1
                        alea_power = random.random()
                        if alea_power < 0.1:
                            nouveau_power = Powerup(o.x,o.y, 10, createur_identifiant())
                            self.powerups.append(nouveau_power)
                        break
    
    def collisionProjectileAstroide(self):
        for a in list(self.asteroides):
            for p in list(self.vaisseau.projectiles):
                if a.x - a.taille_x <= p.x <= a.x + a.taille_x and a.y - a.taille_y <= p.y <= a.y + a.taille_y:
                    self.vaisseau.projectiles.remove(p)
                    break

    def collisionMineAsteroide(self):
        for a in list(self.asteroides):
            for m in list(self.mine):
                if(a.x - a.taille_x <= m.x <= a.x + a.taille_x and a.y - a.taille_y <= m.y <= a.y + a.taille_y):
                    self.mine.remove(m)
                    nouvelle_explosion = Explosion(m.x,m.y,2)
                    self.explosion.append(nouvelle_explosion)
                    break

    def collisionMineOvnis(self):
        for o in list(self.ovnis):
            for m in list(self.mine):
                if(o.x - o.taille_x <= m.x <= o.x + o.taille_x and o.y - o.taille_y <= m.y <= o.y + o.taille_y):
                    self.mine.remove(m)
                    self.ovnis.remove(o)
                    nouvelle_explosion = Explosion(m.x,m.y,2)
                    self.explosion.append(nouvelle_explosion)
                    break

    def collisionMineProjectile(self):
         for m in list(self.mine):
            for p in list(self.vaisseau.projectiles):
                if m.x - m.taille_x <= p.x <= m.x + m.taille_x and m.y - m.taille_y <= p.y <= m.y + m.taille_y:
                    self.mine.remove(m)
                    self.vaisseau.projectiles.remove(p)
                    nouvelle_explosion = Explosion(m.x,m.y,2)
                    self.explosion.append(nouvelle_explosion)
                    break

    def collisionMineVaisseau(self):
        for m in list(self.mine):
            if (m.x - m.taille_x <= self.vaisseau.x <= m.x + m.taille_x and m.y - m.taille_y <= self.vaisseau.y <= m.y + m.taille_y):
                self.vaisseau.vie -= 1
                self.mine.remove(m)
                nouvelle_explosion = Explosion(m.x,m.y,2)
                self.explosion.append(nouvelle_explosion)
                break
    
    def collsisionExplosionOvni(self):
        for e in list(self.explosion):
            for o in list(self.ovnis):
                if(e.x - e.taille_x <= o.x <= e.x + e.taille_x and e.y - e.taille_y <= o.y <= e.y + e.taille_y):
                    o.vie -= 1
                    if (o.vie == 0):
                        self.supprimerOvni(o.id)

    def collisionExplosionMine(self):
        for e in list (self.explosion):
            for m in list(self.ovnis):
                if(e.x - e.taille_x <= m.x <= e.x + e.taille_x and e.y - e.taille_y <= m.y <= e.y + e.taille_y):
                    self.mine.remove()
    

                
                
    
    def mise_a_jour_explosions(self):
        for e in list(self.explosion):
            doit_supprimer = e.mise_a_jour()
            if doit_supprimer:
                self.explosion.remove(e)

    # verifier tous les collisions
    def verifierToutCollisions(self):
        self.collisionOvniVaisseau()
        self.collisionAsteroideVaisseau()
        self.collisionProjectile()
        self.collisionProjectileAstroide()
        self.collisionPowerupVaisseau()
        self.collisionMineAsteroide()
        self.collisionMineOvnis()
        self.collisionMineProjectile()
        self.collisionMineVaisseau()
        self.collsisionExplosionOvni()
        self.collisionExplosionMine()
        self.mise_a_jour_explosions()
        
    def supprimerOvni(self, id):
        for o in self.ovnis:
            if o.id == id:
                self.ovnis.remove(o)
                nouvelle_explosion = Explosion(o.x,o.y,1)
                self.explosion.append(nouvelle_explosion)
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
        if alea_ovni < 0.04 * self.niveau:
            nouvel_ovni = OVNI(
                random.randint(0, self.largeur),
                0,
                random.randint(2, 5),
                createur_identifiant(),
                self.niveau
            )
            self.ovnis.append(nouvel_ovni)

        alea_asteroide = random.random()
        if alea_asteroide < 0.015 * self.niveau:
            nouvel_ast = Asteroide(
                random.randint(0, self.largeur),
                0,
                random.randint(3, 6),
                createur_identifiant()
            )
            self.asteroides.append(nouvel_ast)

        alea_mine = random.random()
        if alea_mine < 0.025 * self.niveau:
            nouvel_mine = MINE(
                random.randint(0, self.largeur),
                0,
                random.randint(3,6),
                createur_identifiant()
            )
            self.mine.append(nouvel_mine)


        # Déplacement des ennemis
        for o in self.ovnis:
            o.mise_a_jour()

        for a in self.asteroides:
            a.mise_a_jour()

        for p in self.powerups:
            p.mise_a_jour()
        for m in self.mine:
            m.mise_a_jour()

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

        self.mine = [
            m for m in self.mine
            if m.y < self.hauteur
        ]
        
        self.compteur += 1

    def levelUp(self):
        match self.score :
            case 15:
                self.niveau = 2
            case 50:
                self.niveau = 3
            case 100:
                self.niveau = 4
            case 150:
                self.niveau = 5
        return self.niveau
