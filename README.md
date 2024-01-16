# Progetto_finale
Repository contenente il codice dell'esame di metodi computazionali per la fisica - Enrico Duca -

La richiesta del progetto era quella di sviluppare in Python una simulazione Monte Carlo di un apparato sperimentale per riprodurre degli esperimenti sullo scattering di Rutherford.

Innanzitutto bisogna specificare che ciò che è stato fatto è un'approssimazione dell'esperienza reale, in quanto si sono supposte considerazioni e condizioni per semplificare il tutto.

Come detto precedentemente, il codice fornisce una simulazione approssimata dell'esperimento di Rutherford incentrato soprattutto sul numero possibile di lamine, in modo particolare fino a 3. Alcune parti sono state pensate per una possibile implementazione e modifica, se necessarie, a casi più generali.

Nel codice si definisce inizialmente la classe  "Lamina_metallo" che permette di creare l'oggetto lamina con diversi attributi di input, in ordine:

- la posizione, che deve essere del tipo np.array([x, z]) e, come già detto precedentemente, dato che si tratta di una approssimazione si colloca lungo l'asse z. Un esempio potrebbe essere "posizione = np.array([-2, 1.5])": in questo caso la lamina si dispone simmetricamente all'asse delle ordinate, con l'ascissa che va da -2 a 2 e z = 1.5. E' importante che x in input sia < 0 per una buona interpretazione grafica e logica, in quanto il codice assume per scontato che la lamina intersechi l'asse z.
- il materiale di cui è composta la lamina da passare come stringa (ad esempio materiale = "oro");
- il numero atomico del materiale di cui è composta la lamina;
- la distanza fra due o più lamine: si suppone che le lamine sono distanti di uguale valore (esso va inserito ugualmente nei diversi oggetti).

A questo punto si è definita la classe "esperimento_Rutherford" che, come attributi di ingresso ha:

- l'energia cinetica del fascio di particelle alpha che vengono inviate contro la lamina;
- la distanza del collimatore, il foro collimatore viene posizionato lungo l'asse z ("self.posizione_collimatore = np.array([0, 0, distanza_collimatore])");
- la dimensione del collimatore: si intende il diametro del foro collimatore (si consigliano dimensioni piccole per avere un fascio più collimato, in quanto le particelle alpha vengono poste in maniera randomatica nella circonferenza del foro);
- la posizione dello schermo sensibile, dove con schermo sensibile si intende la mappa di pixel;
- la dimensione dei pixel;
- le lamine di metallo utilizzate per l'esperimento voluto, bisogna richiamare una o più lamine create attraverso la classe precedente, ad esempio: "lamine_metallo = [lamina_metallo1,lamina_metallo2]";
- il numero di particelle alpha del fascio incidente;
- la dimensione dello schermo sensibile di pixel: è importante per una corretta visualizzazione delle particelle scatterate che questo valore sia scelto correttamente.

Chiaramente per la buona riuscita della simulazione il foro collimatore deve essere posizionato prima delle lamine di metallo che, a loro volta, dovranno essere posizonate prima dello schermo sensibile di pixel.


All'interno della seconda classe si sono definiti anche alcuni moduli:

- "simulazione": riproduce il fascio di particelle alpha che sono deviate dagli atomi d'oro della lamina. Le particelle deviano in accordo con ciascun parametro di impatto, conformemente all'angolo definito dalla formula di Rutherford.
L'incognita iniziale, controllata da fenomeni casuali, è il parametro di impatto in quanto va assunto che ci siano più atomi nella lamina in posizioni non perfettamente determinate. 
Tutto ciò è stato realizzato con un iniziale ciclo for che considera il numero di particelle scelto, ed un altro ciclo for indentato al primo per il passaggio attraverso le diverse lamine. 
Ad ogni giro del for che agisce sul numero di particelle si crea un atomo lungo la lunghezza della lamina in un intorno della posizione della particella dell'ordine di 10^-10m (si è assunto l'ordine dell'angstrom); si calcola il parametro di impatto come la differenza fra la posizione di questo atomo creato casualmente e la posizione della particella quando arriva alla lamina. All'interno dei due cicli for vi sono molte possibilità in base all'apparato scelto e al numero di particelle, per risolvere questa moltitudine di casi si sono utilizzate delle condizioni "if". Inoltre nel modulo "simulazione" si mostra anche l'istogramma con tutti gli angoli di deviazione delle particelle alpha (dato che sono valori molto piccoli è necessario zoomare il grafico intorno all'origine), le varie tracce delle particelle e lo schermo di pixel dove è possibile individuare qualitativamente le particelle deviate significamente.

- "visualizza_apparato" che, permette di visualizzare attraverso "subplots": il foro collimatore con annesso raggio, una o più lamine di  metallo ed infine lo schermo sensibile. Tutto ciò viene mostrato nelle posizioni scelte dall'utente negli attributi di input.

Per quanto riguarda lo schermo sensibile se viene scelto con grandi dimensioni non si vedranno i pixel a meno di ingrandimenti "manuali", all'opposto se viene scelto con dimensioni molto ridotte si vedrà solo il fascio concentrato oppure poche delle particelle deviate.
Stesso discorso per le dimensioni dei pixel: pixel troppo piccoli sono di difficile rintracciamento visivo, mentre pixel troppo grandi inglobano troppi dati e non vi è apprezzamento fisico del fenomeno dello scattering.
Si consiglia di fare qualche prova con diversi parametri per prenderci la mano e capire come impostare al meglio la mappa di pixel.

A questo punto vengono consigliati diversi parametri di prova per la visualizzazione di 4 diversi casi:

a) Particella alpha dal decadimento di 222Rn (E = 5.5MeV) che attraversa una lamina d'oro
        
    lamina_metallo1 = Lamina_metallo(posizione = np.array([-2, 1.5]), materiale = "oro", numero_atomico = 79, distanza_fra_lamine = 0)

    prova1 = esperimento_Rutherford(energia = 5.5, distanza_collimatore = 1, dimensioni_collimatore = 0.1,
                                    posizione_schermo_sensibile = 1.7, dimensioni_pixel =0.0025,
                                    lamine_metallo = [lamina_metallo1], n_particelle = 5000, dimensione_schermo = 2)

    prova1.visualizza_apparato()

    prova1.simulazione()

b) Particella alpha dal decadimento di 214Po (E = 7.7MeV) che attraversa una lamina d'oro

    prova2 = esperimento_Rutherford(energia = 7.7, distanza_collimatore = 1, dimensioni_collimatore = 0.1,
                                    posizione_schermo_sensibile = 1.7, dimensioni_pixel = 0.0025,
                                    lamine_metallo = [lamina_metallo1], n_particelle = 5000, dimensione_schermo = 2)

    prova2.visualizza_apparato()

    prova2.simulazione()


c) Particella alpha dal decadimento di 222Rn (E = 5.5MeV) che attraversa due lamine d'oro poste ad 1cm di distanza

    lamina_metallo2 = Lamina_metallo(posizione = np.array([-2, 2]),materiale = "oro", numero_atomico = 79, distanza_fra_lamine = 1)
    lamina_metallo3 = Lamina_metallo(posizione = np.array([-3, 3]),materiale = "oro", numero_atomico = 79, distanza_fra_lamine = 1)

    prova3 = esperimento_Rutherford(energia = 5.5, distanza_collimatore = 1, dimensioni_collimatore = 0.1,
                                    posizione_schermo_sensibile = 4, dimensioni_pixel = 0.0025,
                                    lamine_metallo = [lamina_metallo2,lamina_metallo3], n_particelle = 5000, dimensione_schermo = 2)

    prova3.visualizza_apparato()

    prova3.simulazione()

d) Particella alpha dal decadimento di 222Rn (E = 5.5MeV) che attraversa tre lamine d'oro poste ad 1mm di distanza

    lamina_metallo4 = Lamina_metallo(posizione = np.array([-2, 2]), materiale = "oro", numero_atomico = 79, distanza_fra_lamine = 0.1)

    lamina_metallo5 = Lamina_metallo(posizione = np.array([-2, 2.1]), materiale = "oro", numero_atomico = 79, distanza_fra_lamine = 0.1)

    lamina_metallo6 = Lamina_metallo(posizione = np.array([-2, 2.2]), materiale = "oro", numero_atomico = 79, distanza_fra_lamine = 0.1)

    prova4 = esperimento_Rutherford(energia = 5.5, distanza_collimatore = 1, dimensioni_collimatore = 0.1,
                                    posizione_schermo_sensibile = 3, dimensioni_pixel = 0.0025,
                                    lamine_metallo = [lamina_metallo4,lamina_metallo5,lamina_metallo6], n_particelle = 5000, dimensione_schermo = 2)

    prova4.visualizza_apparato()

    prova4.simulazione()

Quanto fatto per i punti precedenti può essere ripetuto con un minore numero di particelle, regolando chiaramente anche le dimensioni dello schermo di pixel. Se invece si vuole una migliore analisi statistica si consiglia di aumentare il numero di particelle, facendo attenzione alla rappresentazione delle tracce che potrebbe metterci un po' di tempo per essere eseguita.

Link per la presentazione del progetto: https://www.canva.com/design/DAF3KmVsV78/uarHy-AeX6vse3UOIC6jeQ/view?utm_content=DAF3KmVsV78&utm_campaign=designshare&utm_medium=link&utm_source=editor