import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import e, epsilon_0

class Lamina_metallo:

    def __init__(self, posizione, materiale, larghezza, numero_atomico, distanza_fra_lamine):

        self.posizione = posizione
         
        # Quando si definiscono le coordinate della lamina ("self.posizione") è importante sceglierle in modo tale che il nucleo 
        # sia posizionato lungo l'asse y, in questo modo è allineato con il foro collimatore e quindi con il fascio di particelle.
 
        self.materiale = materiale      

        self.larghezza = larghezza
        
        self.numero_atomico = numero_atomico
        
        self.distanza_fra_lamine = distanza_fra_lamine
        
        self.lunghezza = abs(self.posizione[0]) * 2
        
        self.nucleo = posizione + np.array([self.lunghezza / 2, larghezza / 2]) # Posiziono il nucleo dell'atomo al centro della lamina
        

class esperimento_Rutherford:

    def __init__(self, energia, distanza_collimatore, dimensioni_collimatore, posizione_schermo_sensibile, dimensioni_pixel, lamine_metallo, n_particelle, condizione_b, dimensione_schermo):
        
        self.energia = energia
        
        self.distanza_collimatore = distanza_collimatore
        
        self.dimensioni_collimatore = dimensioni_collimatore
    
        self.posizione_schermo_sensibile = posizione_schermo_sensibile
        
        self.dimensioni_pixel = dimensioni_pixel

        self.lamine_metallo = lamine_metallo # definite tramite la classe "Lamina_metallo"
        
        self.n_particelle = n_particelle

        self.condizione_b = condizione_b

        # Posizione foro di collimazione lungo l'asse y

        self.posizione_collimatore = np.array([0, distanza_collimatore])

        self.raggio_collimatore = dimensioni_collimatore / 2.0 # Raggio del foro collimatore

        self.dimensione_schermo = dimensione_schermo # Dimensione dello schermo sensibile di pixel
        
        self.n_pixel_schermo = int(self.dimensione_schermo / dimensioni_pixel) # Numero di pixel dello schermo sensibile

        # Inizializzazione dello schermo sensibile

        self.schermo = np.zeros((self.n_pixel_schermo, self.n_pixel_schermo))

    def simulazione(self): 
            
            angoli_deflessione = []  # Lista per memorizzare gli angoli di deflessione
            
            # I diversi count terranno conto del numero di particelle deviate durante la simulazione dell'esperimento
            
            count = 0 
            count_successivi = 0
            count_ultima_lamina = 0

            posizioni_scatterate = []
            posizioni_scatterate_successivamente =[]
            posizioni_scatterate_ultima_lamina =[]
            
            tracce_particelle_dopo_prima_lamina = [] 
            tracce_fino_prima_lamina = []
            tracce_dopo_lamine_intermedie = []
            tracce_dopo_ultima_lamina = []

            for i in range(self.n_particelle):
                
                theta = np.random.uniform(0,2*np.pi)
                
                # Fisso un angolo di incidenza molto piccolo, in modo da avere un fascio collimato che non si disperda
                
                angolo_incidenza = np.random.uniform(0,0.025) 

                # Posiziono la particella inizialmente all'interno del foro del collimatore

                direzione_iniziale = np.array([np.sin(angolo_incidenza) * np.cos(theta), np.sin(angolo_incidenza) * np.sin(theta)])
                
                posizione_iniziale = self.posizione_collimatore + self.raggio_collimatore * direzione_iniziale

                '''
                Il motivo per cui viene calcolato il vettore direzione è perché, in termini di coordinate 
                cartesiane, la direzione è rappresentata come un vettore tridimensionale normalizzato. 
                Questo vettore indica la direzione in cui la particella si sta muovendo.
                '''
                
                traccia_particella_fino_prima_lamina = [tuple(posizione_iniziale.copy())]
                
                for indice, lamina in enumerate(self.lamine_metallo):
                    
                    if (indice == 0):

                        direzione = np.array([0,0])
                        
                        b = abs(posizione_iniziale[0] - lamina.nucleo[0]) #cm - parametro di impatto
                        
                        # Con nuova_posizione_iniziale si intende la posizione finale della particella nel percorso dal collimatore fino al nucleo della lamina
                        
                        nuova_posizione_iniziale_y = posizione_iniziale[1] + (lamina.nucleo[1] - self.distanza_collimatore)

                        nuova_posizione_iniziale_x = posizione_iniziale[0]

                        nuova_posizione_iniziale = (nuova_posizione_iniziale_x, nuova_posizione_iniziale_y)
                        

                        traccia_particella_fino_prima_lamina.append(tuple(nuova_posizione_iniziale))

                        traccia_particella_dopo_prima_lamina = [tuple(nuova_posizione_iniziale)]
                        

                        if b <= self.condizione_b : # La particella viene deviata 0.00002

                            # (1.4*10e-10)*2 è il "raggio atomico" dell' oro moltiplicato per 2, che si riferisce alla dimensione approssimativa di un atomo

                            # Angolo calcolato con la formula di Rutherford

                            theta = 2 * np.arctan((lamina.numero_atomico * e**2) / (2 * np.pi * epsilon_0 * self.energia *1.602*10**-13 * b*10**-2)) # in rad
                            
                            # l'energia è stata convertita in Joule mentre b è stata calcolata in metri per rendere l'argomento dell'arcotangente a-dimensionale

                            angoli_deflessione.append(theta*180/np.pi) # angolo in gradi

                            direzione = np.array([np.sin(theta), np.cos(theta)]) 
                            
                            # Se c'è solo una lamina la particella subito dopo la lamina incontra lo schermo di pixel:   
                                                        
                            if len(self.lamine_metallo) == 1: 

                                '''
                                Se la particella arriva da sotto o da sopra rispetto al nucleo avrà una deflessione diversa in segno.
                                Questo perchè per la forza di Coulomb può essere attrattiva, se le cariche delle particelle sono opposte,
                                oppure repulsiva, se le cariche sono le stesse -> questo è il nostro caso.
                                
                                Le particelle alfa sono costituite da due protoni e due neutroni, essenzialmente il nucleo di un atomo
                                di elio. Pertanto, le particelle alfa hanno una carica complessiva positiva di +2.

                                Il nucleo di un atomo di oro è costituito da protoni e neutroni. L'oro ha un numero atomico di 79, 
                                il che significa che ci sono 79 protoni nel suo nucleo, quindi ha una carica positiva di +79.

                                Per questo a volte si somma per la direzione * spostamente mentre altre volte la si sottrae.
                                '''
                                
                                if posizione_iniziale[0] > 0:

                                    posizione_finale = nuova_posizione_iniziale + direzione * (self.posizione_schermo_sensibile - lamina.nucleo[1])

                                else:

                                    posizione_finale_x = (nuova_posizione_iniziale[0] - direzione[0] * (self.posizione_schermo_sensibile - lamina.nucleo[1]))
                                    posizione_finale_y = (nuova_posizione_iniziale[1] + direzione[1] * (self.posizione_schermo_sensibile - lamina.nucleo[1]))
                                    
                                    posizione_finale = (posizione_finale_x, posizione_finale_y)
                            # Se dopo la prima lamina ce ne sono altre:    
                                    
                            else:

                                if posizione_iniziale[0] > 0:
                                    
                                    posizione_finale = nuova_posizione_iniziale + direzione * (lamina.distanza_fra_lamine + lamina.larghezza)
                                
                                else:
                                   
                                    posizione_finale_x = (nuova_posizione_iniziale[0] - direzione[0] * (lamina.distanza_fra_lamine + lamina.larghezza))             
                                    posizione_finale_y = (nuova_posizione_iniziale[1] + direzione[1] * (lamina.distanza_fra_lamine + lamina.larghezza))
                                    
                                    posizione_finale = (posizione_finale_x, posizione_finale_y)
                            
                            count += 1

                            posizioni_scatterate.append(count)
                            
                            traccia_particella_dopo_prima_lamina.append(tuple(posizione_finale)) # Salva la posizione finale nella traccia
                        
                        # La particella passa indisturbata   
                                  
                        else:   
                            
                            x = nuova_posizione_iniziale[0] # la coordinata x rimane immutata

                            if len(self.lamine_metallo) == 1:

                                y = nuova_posizione_iniziale[1] + (self.posizione_schermo_sensibile - lamina.nucleo[1])
                                
                                posizione_finale = (x,y)
                            
                            else:
                            
                                y = nuova_posizione_iniziale[1] + lamina.distanza_fra_lamine + lamina.larghezza
                                
                                posizione_finale = (x, y)
                               
                            traccia_particella_dopo_prima_lamina.append(tuple(posizione_finale))  # Salva la posizione finale nella traccia
                            
                            
                    # Incontra la seconda lamina:
                            

                    if np.logical_and(indice > 0, indice < len(self.lamine_metallo)-1) :
                        
                        b = abs(posizione_finale[0] - lamina.nucleo[0])

                        traccia_dopo_lamine_intermedie = [tuple(posizione_finale)]

                        '''
                        la particella viene deviata valutando il parametro di impatto fra la posizione successiva alla prima lamina
                        e la posizione del nucleo della seconda. Ciò implica che una particella può essere daviata nella prima 
                        lamina e non nella seconda, perchè si è allontanata abbastanza dalla retta passante per i nuclei, oppure
                        può essere deviata anche nella seconda se rispetta la condizione:
                        '''

                        if b <=self.condizione_b :

                            theta = 2 * np.arctan((lamina.numero_atomico * e**2) / (2 * np.pi * epsilon_0 * self.energia *1.602*10**-13 * b*10**-2))
                            
                            # Se la particella viene deviata chiaramente cambia anche la direzione di propagazione:

                            direzione = np.array([ np.sin(theta), np.cos(theta)])
                            
                            if posizione_finale[0] > 0:

                                posizione_finale = posizione_finale + direzione * (lamina.distanza_fra_lamine + lamina.larghezza)
                            
                            else:
                            
                                posizione_finale_x = posizione_finale[0] - direzione[0] * (lamina.distanza_fra_lamine + lamina.larghezza)
                                posizione_finale_y = posizione_finale[1] + direzione[1] * (lamina.distanza_fra_lamine + lamina.larghezza)
                                
                                posizione_finale = (posizione_finale_x, posizione_finale_y)

                            count_successivi += 1

                            posizioni_scatterate_successivamente.append(count_successivi)

                            traccia_dopo_lamine_intermedie.append(tuple(posizione_finale))

                        # La particella passa indisturbata attraverso la seconda lamina
                            
                        else:
                            
                            if np.all(direzione == 0): # Caso in cui la particella non è mai stata deviata e quindi la variabile "direzione" mantiene come valore "direzione = np.array([0,0])"

                                x = posizione_finale[0]
                                y = posizione_finale[1] + (lamina.distanza_fra_lamine + lamina.larghezza)
                            
                            else: # Se la particella ha già subito una deviazione precedentemente deve mantenere la direzione con cui arriva 

                                y = posizione_finale[1] + direzione[1] * (lamina.distanza_fra_lamine + lamina.larghezza)
                                
                                if posizione_finale[0] > 0:
                                
                                    x = posizione_finale[0] + direzione[0] * (lamina.distanza_fra_lamine + lamina.larghezza)    
                                
                                else: 
                                
                                    x = posizione_finale[0] - direzione[0] * (lamina.distanza_fra_lamine + lamina.larghezza)
                                
                            posizione_finale = (x, y)

                            traccia_dopo_lamine_intermedie.append(tuple(posizione_finale))


                    # Ultima lamina, valgono tutte le considerazioni descritte per le precedenti lamine:


                    if np.logical_and(indice == (len(self.lamine_metallo)-1), indice != 0):
                       
                        b = abs(posizione_finale[0] - lamina.nucleo[0])

                        traccia_dopo_ultima_lamina = [tuple(posizione_finale)]
                        
                        if b <= self.condizione_b :

                            theta = 2 * np.arctan((lamina.numero_atomico * e**2) / (2 * np.pi * epsilon_0 * self.energia *1.602*10**-13 * b*10**-2))

                            direzione = np.array([ np.sin(theta), np.cos(theta)]) 
                            
                            if posizione_finale[0] > 0:

                                posizione_finale = posizione_finale + direzione * (self.posizione_schermo_sensibile  - (lamina.nucleo[1]))
                            
                            else:
                            
                                posizione_finale_x = posizione_finale[0] - direzione[0] * (self.posizione_schermo_sensibile  - (lamina.nucleo[1]))
                                posizione_finale_y = posizione_finale[1] + direzione[1] * (self.posizione_schermo_sensibile  - (lamina.nucleo[1]))
                            
                                posizione_finale = (posizione_finale_x, posizione_finale_y)

                            count_ultima_lamina += 1
                            
                            posizioni_scatterate_ultima_lamina.append(count_ultima_lamina)

                            traccia_dopo_ultima_lamina.append(tuple(posizione_finale))
                        
                        else:
    
                            if np.all(direzione == 0):

                                x = posizione_finale[0]
                                y = posizione_finale[1] + self.posizione_schermo_sensibile - lamina.nucleo[1]

                            else:

                                y = posizione_finale[1] + direzione[1] * (self.posizione_schermo_sensibile - lamina.nucleo[1])
                                    
                                if posizione_finale[0] > 0:

                                    x = posizione_finale[0] + direzione[0] * (self.posizione_schermo_sensibile - lamina.nucleo[1])

                                else:

                                    x = posizione_finale[0] - direzione[0] * (self.posizione_schermo_sensibile - lamina.nucleo[1])
                                    
                            posizione_finale = (x, y)

                            traccia_dopo_ultima_lamina.append(tuple(posizione_finale))

                  
                differenza = abs(self.posizione_schermo_sensibile - posizione_finale[1])
                pixel_x = int((posizione_finale[0] + self.dimensione_schermo / 2) / self.dimensioni_pixel)
                pixel_y = int((posizione_finale[1] - self.posizione_schermo_sensibile - differenza + self.dimensione_schermo / 2) / self.dimensioni_pixel)
            
                '''
                "pixel_x" e "pixel_y" calcolano le coordinate del pixel corrispondente alla posizione finale della particella. 
                
                La trasformazione ("posizione_finale[0] + self.dimensione_schermo / 2" e "posizione_finale[1] - self.posizione_schermo_sensibile 
                - differenza") centra le coordinate rispetto all'origine, poi la divisione per self.dimensioni_pixel converte le 
                coordinate continue in coordinate discrete di pixel. 
                
                "differenza" rappresenta la distanza fra lo schermo sensibile e la posizione finale della particella acquisita dalle coordinate y 
                attraverso le varie deviazioni subite, serve solo per centrarla esattamente nel piano di pixel.
                Questo è dato dal fatto che la coordinata y del piano sensibile è uguale e fissa per ogni particella.
                
                La conversione a int è utilizzata per ottenere un indice intero.
                '''
              
                if 0 <= pixel_x < self.n_pixel_schermo and 0 <= pixel_y < self.n_pixel_schermo:
                    self.schermo[pixel_y, pixel_x] += 1

                '''
                La condizione "if 0 <= pixel_x < self.n_pixel_schermo and 0 <= pixel_y < self.n_pixel_schermo" verifica 
                se la posizione finale della particella è effettivamente all'interno del piano sensibile. 
                Se la condizione  è verificata, incrementa il contatore associato al pixel corrispondente nella matrice self.schermo.
                '''

                tracce_particelle_dopo_prima_lamina.append(traccia_particella_dopo_prima_lamina)
                tracce_fino_prima_lamina.append(traccia_particella_fino_prima_lamina)

                # printa il numero di particelle deviate, ovviamente agisce in base a quante lamine sono presenti nell'esperimento: 

                if len(self.lamine_metallo) == 2:
                    tracce_dopo_ultima_lamina.append(traccia_dopo_ultima_lamina)
                if len(self.lamine_metallo)>2:
                    tracce_dopo_lamine_intermedie.append(traccia_dopo_lamine_intermedie)
                    tracce_dopo_ultima_lamina.append(traccia_dopo_ultima_lamina)

            print('Sono state scatterate nella prima lamina: ',len(posizioni_scatterate),' particelle su ',self.n_particelle)
            if (len(self.lamine_metallo) == 2):
                print('Sono state scatterate nella seconda lamina ',len(posizioni_scatterate_ultima_lamina),' particelle su ',self.n_particelle)
            if (len(self.lamine_metallo) > 2):
                print('Sono state scatterate nelle lamine intermedie: ',len(posizioni_scatterate_successivamente),' particelle su ',self.n_particelle)
                print('Sono state scatterate nell\' ultima lamina: ',len(posizioni_scatterate_ultima_lamina),' particelle su ',self.n_particelle)
            

            # istogramma angoli di deflessione


            plt.figure(figsize=(11, 7))
            plt.hist(angoli_deflessione, bins=5000, color='darkred', alpha=0.7)
            plt.title('Distribuzione degli angoli di deflessione')
            plt.xlabel('Angolo di deflessione (gradi)')
            plt.ylabel('Frequenza')
            plt.grid(True)
            plt.show()


            # plot tracce particelle scatterate
            

            plt.figure(figsize=(11, 7))

            for traccia_particella_fino_prima_lamina in tracce_fino_prima_lamina:

                x_traccia = [pos[0] for pos in traccia_particella_fino_prima_lamina]
                y_traccia = [pos[1] for pos in traccia_particella_fino_prima_lamina]
                
                plt.plot(y_traccia, x_traccia, '-')
            
            for traccia_particella_dopo_prima_lamina in tracce_particelle_dopo_prima_lamina:
            
                x_traccia1 = [pos[0] for pos in traccia_particella_dopo_prima_lamina]
                y_traccia1 = [pos[1] for pos in traccia_particella_dopo_prima_lamina]
            
                plt.plot(y_traccia1, x_traccia1, '-')
            
            for traccia_particella_dopo_lamine_intermedie in tracce_dopo_lamine_intermedie:
            
                x_traccia2 = [pos[0] for pos in traccia_particella_dopo_lamine_intermedie]
                y_traccia2 = [pos[1] for pos in traccia_particella_dopo_lamine_intermedie]
            
                plt.plot(y_traccia2, x_traccia2, '-')
            
            for traccia_particella_dopo_ultima_lamina in tracce_dopo_ultima_lamina:
            
                x_traccia3 = [pos[0] for pos in traccia_particella_dopo_ultima_lamina]
                y_traccia3 = [pos[1] for pos in traccia_particella_dopo_ultima_lamina]
            
                plt.plot(y_traccia3, x_traccia3, '-')

            plt.title('Tracce delle particelle nell\'apparato sperimentale')

            plt.xlabel('Posizione Y (cm)')
            plt.ylabel('Posizione X (cm)')

            plt.grid(True)
            plt.show()


            #piano_schermo_sensibile pixel


            plt.figure(figsize= (11,7))
            
            pixel_map = plt.imshow(self.schermo, extent=[-self.dimensione_schermo / 2, self.dimensione_schermo / 2,-self.dimensione_schermo / 2, self.dimensione_schermo / 2], cmap='gray',interpolation='none', vmin=0, vmax=1)
            
            '''
            Il parametro extent viene utilizzato per specificare l'intervallo dei valori sugli assi x e y della mappa di pixel, 
            definisce così l'area della figura che deve essere visualizzata.

            Questo può essere utile per garantire che la mappa di pixel sia correttamente allineata e dimensionata.
            '''

            plt.title(f'Schermo sensibile, fascio con {self.energia} MeV ')
            
            plt.xlabel('Posizione X (cm)')
            plt.ylabel('Posizione Y (cm)')
            
            plt.grid(True, color='white', linestyle='--', linewidth=0.5)

            # barra di colore:

            cbar = plt.colorbar(pixel_map, label='Pixel colpiti')
            
            plt.tight_layout()
            plt.show()


    # Qui si definisce un metodo per visualizzare il proprio esperimento e tutte le sue componenti
            
    def visualizza_apparato(self):

        fig, ax = plt.subplots(figsize=(11, 7))

        # Plotta la posizione del foro di collimazione:

        ax.plot(self.posizione_collimatore[0], self.posizione_collimatore[1], 'ro', label='Foro di collimazione')
        
        # Plotta il cerchio del collimatore

        theta = np.linspace(0, 2*np.pi, 100)

        x_cerchio = self.posizione_collimatore[0] + self.raggio_collimatore * np.cos(theta)
        y_cerchio = self.posizione_collimatore[1] + self.raggio_collimatore * np.sin(theta)

        ax.plot(x_cerchio, y_cerchio, 'r--', label='Cerchio del collimatore')

        # Plotta la posizione delle lamine di metallo

        for lamina in self.lamine_metallo:
        
            x = [lamina.posizione[0], lamina.posizione[0] + lamina.lunghezza, lamina.posizione[0] + lamina.lunghezza, lamina.posizione[0], lamina.posizione[0]]
            y = [lamina.posizione[1], lamina.posizione[1], lamina.posizione[1] + lamina.larghezza, lamina.posizione[1] + lamina.larghezza, lamina.posizione[1]]

            ax.plot(x, y, color='blue', label = f'Lamina di {lamina.materiale}')

            # Plotta il nucleo della lamina

            ax.plot(lamina.nucleo[0], lamina.nucleo[1], 'kx', label=f'Nucleo Lamina {lamina.numero_atomico}')

        # Plotta la posizione dello schermo sensibile

        ax.plot(0, self.posizione_schermo_sensibile, 'g^', label='Schermo sensibile ')
    
        ax.set_xlabel('Posizione X (cm)')
        ax.set_ylabel('Posizione Y (cm)')
        ax.set_title('Apparato sperimentale Rutherford')
        
        ax.legend()
        ax.grid()

        plt.show()

# Particella alpha dal decadimento di 222Rn (E = 5.5MeV) che attraversa una lamina d'oro
        
lamina_metallo1 = Lamina_metallo(posizione = np.array([-2, 2]), materiale = "oro", larghezza = 0.2, numero_atomico = 79, distanza_fra_lamine = 0)

prova1 = esperimento_Rutherford(energia = 5.5, distanza_collimatore = 1, dimensioni_collimatore = 0.005,
                                posizione_schermo_sensibile = 5,  dimensioni_pixel = 0.00025,
                                lamine_metallo = [lamina_metallo1], n_particelle = 20000, condizione_b = 0.00000001, dimensione_schermo = 0.05)
prova1.visualizza_apparato()
prova1.simulazione()


# Particella alpha dal decadimento di 214Po (E = 7.7MeV) che attraversa una lamina d'oro

prova2 = esperimento_Rutherford(energia = 7.7, distanza_collimatore = 1, dimensioni_collimatore = 0.005,
                                posizione_schermo_sensibile = 5, dimensioni_pixel = 0.00025,
                                lamine_metallo = [lamina_metallo1], n_particelle = 20000, condizione_b = 0.00000001, dimensione_schermo = 0.05)

prova2.visualizza_apparato()

prova2.simulazione()


# Particella alpha dal decadimento di 222Rn (E = 5.5MeV) che attraversa due lamine d'oro poste ad 1cm di distanza

lamina_metallo2 = Lamina_metallo(posizione = np.array([-1.8, 1.8]),materiale = "oro",  larghezza = 0.2, numero_atomico = 79, distanza_fra_lamine = 1)
lamina_metallo3 = Lamina_metallo(posizione = np.array([-3, 3]),materiale = "oro",  larghezza = 0.2, numero_atomico = 79, distanza_fra_lamine = 1)

prova3 = esperimento_Rutherford(energia = 5.5, distanza_collimatore = 1, dimensioni_collimatore = 0.005,
                                posizione_schermo_sensibile = 5, dimensioni_pixel = 0.00025,
                                lamine_metallo = [lamina_metallo2,lamina_metallo3], n_particelle = 20000, condizione_b = 0.00001, dimensione_schermo = 0.1)
prova3.visualizza_apparato()

prova3.simulazione()

# Particella alpha dal decadimento di 222Rn (E = 5.5MeV) che attraversa tre lamine d'oro poste ad 1mm di distanza

lamina_metallo4 = Lamina_metallo(posizione = np.array([-2, 2]), materiale = "oro", larghezza = 0.2, numero_atomico = 79, distanza_fra_lamine = 0.1)

lamina_metallo5 = Lamina_metallo(posizione = np.array([-2.3, 2.3]), materiale = "oro", larghezza = 0.2, numero_atomico = 79, distanza_fra_lamine = 0.1)

lamina_metallo6 = Lamina_metallo(posizione = np.array([-2.6, 2.6]), materiale = "oro", larghezza = 0.2, numero_atomico = 79, distanza_fra_lamine = 0.1)

prova4 = esperimento_Rutherford(energia = 5.5, distanza_collimatore = 1, dimensioni_collimatore = 0.005,
                                posizione_schermo_sensibile = 5, dimensioni_pixel = 0.00025,
                                lamine_metallo = [lamina_metallo4,lamina_metallo5,lamina_metallo6], n_particelle = 20000, condizione_b = 0.00001, dimensione_schermo = 0.1)

prova4.visualizza_apparato()

prova4.simulazione()