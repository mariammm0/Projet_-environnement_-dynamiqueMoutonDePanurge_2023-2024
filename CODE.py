```py
import numpy as np
import matplotlib.pyplot as plt
import random 

class Mouton:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.influence = random.random() #valeur entre 0 et 1

    def leader (self,moutons):
        # Trouver le leader parmi les autres moutons
        leader = None
        max_influence = -1  # Initialisation avec une valeur très basse

        for mouton in moutons:
            if mouton.influence > max_influence:
                max_influence = mouton.influence
                leader = mouton
        
        return leader
    
                
    def update(self, dt, environnement,nb, moutons):
        
        # 'leader_mouton' contient le mouton avec la plus grande influence
        leader_mouton = self.leader(moutons)        
                
       #on definit de facon random comment le leader va se déplacer par rapport aux moutons
        leader_mouton.vx = random.uniform(-nb,nb)
        leader_mouton.vy = random.uniform(-nb,nb)
       
    	# REGLE DE SUIVI DU LEADER 
        
        # Définir la distance entre chaque mouton et le leader
        dx = leader_mouton.x - self.x
        dy = leader_mouton.y - self.y
        distance_leader = np.sqrt(dx**2 + dy**2)
        
        # Si la distance entre le mouton et le leader est supérieure à 10
        if distance_leader > 3:
            # Ajuster la vitesse du mouton pour suivre le leader
            #modifier vx et vy permet de définir la direction pour suivre le leader
            self.vx += 0.1 * dx/distance_leader
            self.vy += 0.1 * dy/distance_leader
        else:
            # Sinon, arrêter le mouton
            self.vx = 0
            self.vy = 0
            # et aussi le leader
            leader_mouton.vx=0
            leader_mouton.vy=0
      
        # Règle d'évitement des obstacles
        for obstacle in environnement.obstacles:
            dx = obstacle.x - self.x
            dy = obstacle.y - self.y
            distance_obstacle = np.sqrt(dx**2 + dy**2)
            if distance_obstacle < 5:
              self.vx -= 0.1 * dx / distance_obstacle
              self.vy -= 0.1 * dy / distance_obstacle
       
        
        # Règle d'évitement des murs pour les moutons et le leader
        x_min, x_max, y_min, y_max = environnement.murs()

        # Vérifier si la nouvelle position dépasse les limites de l'environnement
        #pour les moutons
        new_x = self.x + self.vx * dt
        new_y = self.y + self.vy * dt

        if new_x <= x_min:
            self.vx = 0  # Arrêter le mouvement horizontal vers la gauche
            new_x = x_min
        elif new_x >= x_max:
            self.vx = 0  # Arrêter le mouvement horizontal vers la droite
            new_x = x_max

        if new_y <= y_min:
            self.vy = 0  # Arrêter le mouvement vertical vers le bas
            new_y = y_min
        elif new_y >= y_max:
            self.vy = 0  # Arrêter le mouvement vertical vers le haut
            new_y = y_max

        # Mettre à jour la position
        self.x = new_x
        self.y = new_y        
       

        # Mise à jour de la position pour le leader
        new_leader_x = leader_mouton.x + leader_mouton.vx * dt
        new_leader_y = leader_mouton.y + leader_mouton.vy * dt

        if new_leader_x <= x_min:
            leader_mouton.vx = 0
            new_leader_x = x_min
        elif new_leader_x >= x_max:
            leader_mouton.vx = 0
            new_leader_x = x_max

        if new_leader_y <= y_min:
            leader_mouton.vy = 0
            new_leader_y = y_min
        elif new_leader_y >= y_max:
            leader_mouton.vy = 0
            new_leader_y = y_max

        leader_mouton.x = new_leader_x
        leader_mouton.y = new_leader_y        
        

    def draw(self, is_leader=False):
        if is_leader:
            plt.plot(self.x, self.y, 'go')  # Dessiner en vert pour le leader
        else:
            plt.plot(self.x, self.y, 'bo')  # Dessiner en bleu pour les autres moutons
            


class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y



class Environnement:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.obstacles = []

    
    def ajouter_obstacles_aleatoires(self, nb_obstacles):
        # Ajouter des obstacles aléatoires à l'environnement
        for _ in range(nb_obstacles):
            self.obstacles.append(Obstacle(np.random.uniform(0, self.largeur), np.random.uniform(0, self.hauteur)))

    def murs(self):
        x_min = 1
        x_max = self.largeur-1
        y_min = 1
        y_max = self.hauteur-1
        return x_min, x_max, y_min, y_max
    
        
        
        
    def draw(self):
       for obstacle in self.obstacles: 
           plt.plot(obstacle.x, obstacle.y, 'ko')  # Dessiner les obstacles en rouge


# Initialisation

nb_moutons = 10
largeur_environnement = 100
hauteur_environnement = 100
nb=0.1

environnement = Environnement(largeur_environnement, hauteur_environnement)
moutons = [Mouton(np.random.uniform(0, largeur_environnement), np.random.uniform(0, hauteur_environnement)) for i in range(nb_moutons)]

# Ajout d'obstacles aléatoires à l'environnement
nb_obstacles = 7  # Nombre d'obstacles à ajouter
environnement.ajouter_obstacles_aleatoires(nb_obstacles)

# Simulation
for t in range(50):
    leader = None
    for mouton in moutons:
        mouton.update(t, environnement,nb, moutons)
        if mouton == mouton.leader(moutons):
            leader = mouton
    
            leader.update(t, environnement,nb, moutons)



    # Visualisation
    plt.clf() # efface la figure actuelle.
    plt.xlim([0, largeur_environnement])
    plt.ylim([0, hauteur_environnement])
    
    for mouton in moutons:
        mouton.draw(is_leader=(mouton == leader))
    for obstacle in environnement.obstacles:
        plt.plot(obstacle.x, obstacle.y, 'ro')
        
    plt.pause(0.5)

plt.show()

#POUR LES COURBES

# x = Nombre d'obstacles y = Temps de suivi des moutons

# Initialisation
nb_moutons = 10
largeur_environnement = 50
hauteur_environnement = 50
nb=0.1

moutons = [Mouton(np.random.uniform(0, largeur_environnement), np.random.uniform(0, hauteur_environnement)) for i in range(nb_moutons)]


def temps_suivi(environnement, moutons, limite_iterations):
    for t in range(limite_iterations):
        leader = None
        for mouton in moutons:
            mouton.update(t, environnement,nb, moutons)
            if mouton == mouton.leader(moutons):
                leader = mouton
                leader.update(t, environnement,nb, moutons)
        
        # vérifier si tous les moutons ont arretés de bouger
        tous_arretes = all(mouton.vx == 0 and mouton.vy == 0 for mouton in moutons)  #La fonction 'all' est une fonction Python qui prend une séquence en argument et renvoie True si tous les éléments de cette séquence sont évalués comme True, sinon elle renvoie False.
        if tous_arretes:
            return t + 1  # Ajouter 1 pour inclure l'itération actuelle
        
    # Si la limite maximale d'itérations est atteinte
    return limite_iterations

    
nb_obstacles = [60,50,40,30,20,10,0]  # Nombre d'obstacles à tester

temps_suivi_moyen = []

for nb_obs in range (0,len(nb_obstacles)):
    environnement = Environnement(largeur_environnement, hauteur_environnement)
    environnement.ajouter_obstacles_aleatoires(nb_obstacles[nb_obs])
    temps_suivi_total = 0
    
    # Exécutez plusieurs fois la simulation pour obtenir une moyenne
    for _ in range(30):  # Exécutez la simulation 30 fois
        temps_suivi_total += temps_suivi(environnement, moutons,50)
    
    # Calculez la moyenne du temps de suivi pour ce nombre d'obstacles
    temps_suivi_moyen.append(int(temps_suivi_total / 30)) # Divisez par le nombre de simulations (30)
    nb_obs+=1

# Tracer la courbe
plt.plot(nb_obstacles, temps_suivi_moyen)
plt.xlabel('Nombre d\'obstacles')
plt.ylabel('Moyenne du temps de suivi des moutons')
plt.title('Temps de suivi des moutons en fonction du nombre d\'obstacles')
plt.ylim(0, 55)  # D√©finir les limites de l'axe y
plt.show()



  
# x = Taille de l'environement  y = Temps de suivi des moutons  

# Initialisation
nb_moutons = 10
largeur_environnement = 50
hauteur_environnement = 50
nb_obstacles=7
nb=0.1
limite_iterations = 50

moutons = [Mouton(np.random.uniform(0, largeur_environnement), np.random.uniform(0, hauteur_environnement)) for i in range(nb_moutons)]


def temps_suivi(environnement, moutons, limite_iterations):
    for t in range(limite_iterations):
        leader = None
        for mouton in moutons:
            mouton.update(t, environnement, nb, moutons)
            if mouton == mouton.leader(moutons):
                leader = mouton
                leader.update(t, environnement, nb, moutons)
        
        # Vérifier si tous les moutons ont arrêté de bouger
        tous_arretes = all(mouton.vx == 0 and mouton.vy == 0 for mouton in moutons)
        if tous_arretes:
            return t + 1  # Ajouter 1 pour inclure l'itération actuelle
        
    # Si la limite maximale d'itérations est atteinte
    return limite_iterations


def simuler_temps_suivi(tailles_environnement):
    temps_suivi_moyen = []
    for taille in tailles_environnement:
        # Calculer le temps de suivi moyen pour chaque taille d'environnement
        temps_suivi_total = 0
        for _ in range(30):  # Exécuter la simulation 30 fois
            environnement = Environnement(taille, taille)
            environnement.ajouter_obstacles_aleatoires(nb_obstacles)
            moutons = [Mouton(np.random.uniform(0, taille), np.random.uniform(0, taille)) for _ in range(nb_moutons)]
            temps_suivi_total += temps_suivi(environnement, moutons, limite_iterations)
        temps_suivi_moyen.append(temps_suivi_total / 30)  # Calculer la moyenne du temps de suivi
    return temps_suivi_moyen


# Liste des tailles d'environnement à tester
tailles_environnement = [10, 20, 30, 40, 50]

# Appel de la fonction pour obtenir les données à tracer
temps_suivi_moyen = simuler_temps_suivi(tailles_environnement)

# Tracer la courbe
plt.plot(tailles_environnement, temps_suivi_moyen)
plt.xlabel('Taille de l\'environnement')
plt.ylabel('Moyenne du temps de suivi des moutons')
plt.title('Temps de suivi des moutons en fonction de la taille de l\'environnement')
plt.show()



# x = Direction aléatoire de leader  y = Temps de suivi des moutons

# Initialisation
nb_moutons = 10
largeur_environnement = 50
hauteur_environnement = 50
nb_obstacles=7
nb=0.1
limite_iterations = 50


moutons = [Mouton(np.random.uniform(0, largeur_environnement), np.random.uniform(0, hauteur_environnement)) for i in range(nb_moutons)]

        

def temps_suivi(environnement, moutons, limite_iterations):
    for t in range(limite_iterations):
        leader = None
        for mouton in moutons:
            mouton.update(t, environnement, nb, moutons)
            if mouton == mouton.leader(moutons):
                leader = mouton
                leader.update(t, environnement, nb, moutons)
        
        # Vérifier si tous les moutons ont arrêté de bouger
        tous_arretes = all(mouton.vx == 0 and mouton.vy == 0 for mouton in moutons)
        if tous_arretes:
            return t + 1  # Ajouter 1 pour inclure l'itération actuelle
        
    # Si la limite maximale d'itérations est atteinte
    return limite_iterations




def simuler_temps_suivi(nb_liste):
    temps_suivi_moyen = []
    for nb in nb_liste:
        # Réinitialiser les moutons avec de nouvelles positions aléatoires
        moutons = [Mouton(np.random.uniform(0, largeur_environnement), np.random.uniform(0, hauteur_environnement)) for _ in range(nb_moutons)]
        # Exécuter la simulation et calculer le temps de suivi moyen
        temps_suivi_total = 0
        for _ in range(50):  # Exécuter la simulation 50 fois
            environnement = Environnement(largeur_environnement, hauteur_environnement)
            environnement.ajouter_obstacles_aleatoires(nb_obstacles)
            temps_suivi_total += temps_suivi(environnement, moutons, limite_iterations)
        temps_suivi_moyen.append(temps_suivi_total / 50)  # Calculer la moyenne du temps de suivi
    return temps_suivi_moyen



# Liste des directions aléatoires du leader à tester
liste_nb = [0.1,0.5,1, 5]

# Appel de la fonction pour obtenir les données à tracer
temps_suivi_moyen = simuler_temps_suivi(liste_nb)

# Tracer la courbe
plt.plot(liste_nb, temps_suivi_moyen)
plt.xlabel('Direction aléatoire du leader')
plt.ylabel('Moyenne du temps de suivi des moutons')
plt.title('Temps de suivi des moutons en fonction de la direction aléatoire du leader')


```
