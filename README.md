# Progetto_finale
Repository contenente il codice dell'esame di metodi computazionali per la fisica - Enrico Duca -

La richiesta del progetto era quella di sviluppare in Python una simulazione Monte Carlo di un apparato sperimentale per riprodurre degli esperimenti sullo scattering di Rutherford.

Innanzitutto bisogna specificare che ciò che è stato fatto è un'approssimazione dell'esperienza reale, in quanto si sono supposte considerazioni e condizioni per semplificare il tutto.

Come detto precedentemente, il codice fornisce una simulazione approssimata dell'esperimento di Rutherford incentrato soprattutto sul numero possibile di lamine, in modo particolare fino a 3. Alcune parti sono state pensate per una possibile implementazione e modifica, se necessarie, a casi più generali.

Nel codice si definisce inizialmente la classe  "Lamina_metallo" che permette di creare l'oggetto lamina con diversi attributi di input, in ordine:

- la posizione, che deve essere del tipo np.array([x, y]) e, come già detto precedentemente, dato che si tratta di una approssimazione si colloca lungo l'asse y. Un esempio potrebbe essere "posizione = np.array([-2, 1.5])": in questo caso la lamina si dispone simmetricamente all'asse delle ordinate, con l'ascissa che va da -2 a 2 e y = 1.5. E' importante che x in input sia < 0 per una buona interpretazione grafica e logica, in quanto il codice assume per scontato che la lamina intersechi l'asse y.
- il materiale di cui è composta la lamina da passare come stringa (ad esempio materiale = "oro");
- il numero atomico del materiale di cui è composta la lamina;
- la distanza fra due o più lamine: si suppone che le lamine sono distanti di uguale valore (esso va inserito ugualmente nei diversi oggetti).

A questo punto si è definita la classe "esperimento_Rutherford" che, come attributi di ingresso ha:

- l'energia cinetica del fascio di particelle alpha che vengono inviate contro la lamina;
- la distanza del collimatore, il foro collimatore viene posizionato lungo l'asse y ("self.posizione_collimatore = np.array([0, distanza_collimatore])");
- la dimensione del collimatore: si intende il diametro del foro collimatore (si consigliano dimensioni piccole per avere un fascio più collimato, in quanto le particelle alpha vengono poste in maniera randomatica sulla circonferenza del foro);
- la posizione dello schermo sensibile, dove con schermo sensibile si intende la mappa di pixel;
- la dimensione dei pixel;
- le lamine di metallo utilizzate per l'esperimento voluto, bisogna richiamare una o più lamine create attraverso la classe precedente, ad esempio: "lamine_metallo = [lamina_metallo1,lamina_metallo2]";
- il numero di particelle alpha del fascio incidente;
- la dimensione dello schermo sensibile di pixel: è importante per una corretta visualizzazione delle particelle scatterate che questo valore sia scelto correttamente.

Chiaramente per la buona riuscita della simulazione il foro collimatore deve essere posizionato prima delle lamine di metallo che, a loro volta, dovranno essere posizonate prima dello schermo sensibile di pixel.


All'interno della seconda classe si sono definiti anche alcuni moduli:

- "simulazione": riproduce il fascio di particelle alpha che sono deviate dagli atomi d'oro della lamina. Le particelle deviano in accordo con ciascun parametro di impatto, conformemente all'angolo definito dalla formula di Rutherford.
L'incognita iniziale, controllata da fenomeni casuali, è il parametro di impatto in quanto va assunto che ci siano più atomi nella lamina in posizioni non perfettamente determinate. Tutto ciò è stato realizzato con un iniziale ciclo for che considera il numero di particelle scelto, ed un altro ciclo for indentato al primo per il passaggio attraverso le diverse lamine. Ad ogni giro del for che agisce sul numero di particelle si crea un atomo lungo la lunghezza della lamina e, si calcola il parametro di impatto come la differenza fra la posizione di questo atomo creato casualmente e la posizione della particella quando arriva alla lamina. All'interno dei due cicli for vi sono molte possibilità in base all'apparato scelto e al numero di particelle, per risolvere questa moltitudine di casi si sono utilizzate delle condizioni "if". Inoltre nel modulo "simulazione" si mostra anche l'istogramma con tutti gli angoli di deviazione delle particelle alpha (dato che sono valori molto piccoli è necessario zoomare il grafico intorno all'origine), le varie tracce delle particelle e lo schermo di pixel dove è possibile individuare qualitativamente le particelle deviate significamente.

- "visualizza_apparato" che, permette di visualizzare attraverso "subplots": il foro collimatore con annesso raggio, una o più lamine di  metallo ed infine lo schermo sensibile. Tutto ciò viene mostrato nelle posizioni scelte dall'utente negli attributi di input.

Per quanto riguarda lo schermo sensibile se viene scelto con grandi dimensioni non si vedranno i pixel a meno di ingrandimenti "manuali", all'opposto se viene scelto con dimensioni molto ridotte si vedrà solo il fascio concentrato oppure poche delle particelle deviate.
Stesso discorso per le dimensioni dei pixel: pixel troppo piccoli sono di difficile rintracciamento visivo, mentre pixel troppo grandi inglobano troppi dati e non vi è apprezzamento fisico del fenomeno dello scattering.
Si consiglia di fare qualche prova con diversi parametri per prenderci la mano e capire come impostare al meglio la mappa di pixel.

A questo punto vengono consigliati diversi parametri di prova per la visualizzazione di 4 diversi casi:

a) Particella alpha dal decadimento di 222Rn (E = 5.5MeV) che attraversa una lamina d'oro

    lamina_metallo1 = Lamina_metallo(posizione = np.array([-2, 1.5]), materiale = "oro", numero_atomico = 79, distanza_fra_lamine = 0)

    prova1 = esperimento_Rutherford(energia = 5.5, distanza_collimatore = 1, dimensioni_collimatore = 0.000000005,
                                    posizione_schermo_sensibile = 3,  dimensioni_pixel = 10e-13,
                                    lamine_metallo = [lamina_metallo1], n_particelle = 20000, dimensione_schermo = 0.000000004)
    
    prova1.visualizza_apparato()
    prova1.simulazione()

b) Particella alpha dal decadimento di 214Po (E = 7.7MeV) che attraversa una lamina d'oro

    Uguale al caso di prima però inserire nell'attributo "energia" il valore di 7.7 al posto di 5.5

c) Particella alpha dal decadimento di 222Rn (E = 5.5MeV) che attraversa due lamine d'oro poste ad 1cm di distanza

    lamina_metallo2 = Lamina_metallo(posizione = np.array([-2, 2]),materiale = "oro", numero_atomico = 79, distanza_fra_lamine = 1)
    lamina_metallo3 = Lamina_metallo(posizione = np.array([-3, 3]),materiale = "oro", numero_atomico = 79, distanza_fra_lamine = 1)

    prova3 = esperimento_Rutherford(energia = 5.5, distanza_collimatore = 1, dimensioni_collimatore = 0.000000005,
                                    posizione_schermo_sensibile = 5, dimensioni_pixel = 10e-13,
                                    lamine_metallo = [lamina_metallo2,lamina_metallo3], n_particelle = 20000, 
                                    dimensione_schermo = 0.000000004)

    prova3.visualizza_apparato()
    prova3.simulazione()

d) Particella alpha dal decadimento di 222Rn (E = 5.5MeV) che attraversa tre lamine d'oro poste ad 1mm di distanza

    lamina_metallo4 =Lamina_metallo(posizione = np.array([-2, 2]), materiale = "oro", numero_atomico = 79, distanza_fra_lamine = 0.1)
    lamina_metallo5 =Lamina_metallo(posizione = np.array([-2, 2.1]), materiale = "oro", numero_atomico = 79,distanza_fra_lamine = 0.1)
    lamina_metallo6 =Lamina_metallo(posizione = np.array([-2, 2.2]), materiale = "oro", numero_atomico = 79,distanza_fra_lamine = 0.1)

    prova4 = esperimento_Rutherford(energia = 5.5, distanza_collimatore = 1, dimensioni_collimatore = 0.000000005,
                                posizione_schermo_sensibile = 3, dimensioni_pixel = 10e-13,
                                lamine_metallo = [lamina_metallo4,lamina_metallo5,lamina_metallo6], n_particelle = 20000, dimensione_schermo = 0.000000004)
    prova4.visualizza_apparato()
    prova4.simulazione()

Quanto fatto per i punti precedenti può essere ripetuto con un minore numero di particelle, regolando chiaramente anche le dimensioni dello schermo di pixel.

Si noti che nella visualizzazione della mappa dei pixel molte particelle rimangono all'interno della circonferenza di partenza (foro collimatore) perchè vengono deviate di poco, altre invece vengono scatterate di più e si trovano in posizioni differenti.

Quando ci sono più lamine può avvenire un caso particolare: la particella, dopo essere stata scatterata dalla prima lamina, incontra un atomo della lamina successiva e può essere respinta o verso l'alto (verso sinistra se si pensa a come si visualizza l'esperimento in "visualizza_apparato()) o verso il basso (verso destra se si pensa a come si visualizza l'esperimento in "visualizza_apparato()). Infatti se l'atomo si trova in una posizione inferiore rispetto alla particella allora quest'ultima viene respinta verso il basso mentre se è la particella ad essere in una posizione più piccola rispetto all'atomo allora sarà deviata verso l'alto.

Questo perchè per la forza di Coulomb può essere attrattiva, se le cariche delle particelle sono opposte, oppure repulsiva, se le cariche sono le stesse -> questo è il nostro caso.
Le particelle alfa sono costituite da due protoni e due neutroni, essenzialmente il nucleo di un atomo di elio. Pertanto, le particelle alfa hanno una carica complessiva positiva di +2.
Il nucleo di un atomo di oro è costituito da protoni e neutroni. L'oro ha un numero atomico di 79, il che significa che ci sono 79 protoni nel suo nucleo, quindi ha una carica positiva di +79.


Per questo motivo in "prova3" e "prova4" si possono notare alcune particelle che sono state deviate dalla lamina precedente e, una volta incontrata la lamina successiva, avere una specie di moto in linea retta; in realtà se si ingrandisce "manualmente" il grafico delle tracce si può osservare che non sono linee rette ma hanno una piccolissima pendenza (vero anche per il caso con una sola lamina, in quanto l'angolo di deviazione è minimo).