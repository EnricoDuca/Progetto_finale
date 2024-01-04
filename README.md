# Progetto_finale
Repository contenente il codice dell'esame di metodi computazionali per la fisica - Enrico Duca -

La richiesta del progetto era quella di sviluppare in Python una simulazione Monte Carlo di un apparato sperimentale per riprodurre degli esperimenti sullo scattering di Rutherford.

Innanzitutto bisogna specificare che ciò che è stato fatto è un'approssimazione dell'esperienza reale, in quanto si sono supposte considerazioni e condizioni per semplificare il tutto.

Nel codice si definisce inizialmente la classe  "Lamina_metallo" che permette di creare l'oggetto lamina con diversi attributi di input, in ordine: 
- la posizione che deve essere del tipo np.array([x, y]) e, come già detto precedentemente, dato che è un'approssimazione bisogna stare attenti a definire una posizione che permetta al nucleo (che si trova al centro della lamina) di collocarsi lungo l'asse y ( un esempio potrebbe essere: posizione = np.array([-2,2]));
- il materiale di cui è composta la lamina da passsare come stringa (ad esempio materiale = "oro");
- la larghezza della lamina, che poi andrà a definire la posizione del nucleo;
- il numero atomico del materiale di cui è composta la lamina;
- la distanza fra due o più lamine: si suppone che le lamine sono distanti di uguale valore (esso va inserito ugualmente nei diversi oggetti).

Abbiamo citato il nucleo che, come già specificato prima, si trova al centro della lamina di metallo. Verrà considerato come parametro di impatto la differenza fra la posizione lungo l'asse x della particella quando si trova all'altezza della lamina e quella del nucleo.

A questo punto si è definita la classe "esperimento_Rutherford" che, come attributi di ingresso ha:

- l'energia cinetica del fascio di particelle alpha che vengono inviate contro la lamina;
- la distanza del collimatore: il foro collimatore viene posizionato lungo l'asse y ("self.posizione_collimatore = np.array([0, distanza_collimatore])");
- la dimensione del collimatore: si intende il diametro del foro collimatore (si consigliano dimensioni piccole per avere un fascio più collimato, in quanto le particelle alpha vengono poste in maniera randomatica sulla circonferenza del foro);
- la posizione dello schermo sensibile, dove con schermo sensibile si intende la mappa di pixel;
- la dimensione dei pixel;
- le lamine di metallo utilizzate per l'esperimento voluto, bisogna richiamare una o più lamine create dalla classe precedente, ad esempio: "lamine_metallo = [lamina_metallo1,lamina_metallo2]";
- il numero di particelle alpha del fascio incidente;
- una condizione sul parametro di impatto (b), tale condizione verrà usata per decidere se una particella che arriva alla stessa altezza del nucleo viene deviata o meno: "if b <= self.condizione_b";
- la dimensione dello schermo sensibile di pixel: è importante per una corretta visualizzazione delle particelle scatterate che questo valore sia scelto correttamente.

Chiaramente per la buona riuscita della simulazione il foro collimatore deve essere posizionato prima delle lamine di metallo che, a loro volta, dovranno essere posizonate prima dello schermo sensibile di pixel.


All'interno della seconda classe si sono definiti anche alcuni moduli:

- "simulazione": riproduce il fascio di particelle alpha che possono essere deviate dal nucleo dell'atomo d'oro posto al centro della lamina oppure possono passare indisturbate fino allo schermo sensibile. Tutto ciò è stato realizzato con un iniziale ciclo for che considera il numero di particelle scelto ed un altro ciclo for indentato al primo per le diverse lamine. All'interno dei due cicli vi sono molte possibilità in base all'apparato scelto e al numero di particelle, per risolvere questa moltitudine di casi si sono utilizzate delle condizioni "if". Inoltre nel modulo "simulazione" si mostra anche l'istogramma con tutti gli angoli di deviazione delle particelle alpha (dato che sono valori molto piccoli è necessario zoomare il grafico intorno all'origine), le varie tracce delle particelle e lo schermo di pixel e lo schermo di pixel dove è possibile confrontare qualitativamente le particelle deviate con quelle passate indisturbate.

- "visualizza_apparato" che, permette di visualizzare attraverso "subplots": il foro collimatore con annesso raggio, una o più lamine di  metallo con il loro nucleo centrale ed infine lo schermo sensibile. Tutto ciò viene mostrato nelle posizioni scelte dall'utente negli attributi di input.

Dato che la maggior parte delle particelle passa indisturbata, le tracce (sopratutto se viene scelto un elevato numero di particelle) risultano molto concentrate intorno all'origine anche se con qualche particella deviata di parecchio.
Se invece si sceglie una condizione per il parametro di impatto che permetta la deviazione di più particelle e si considera un numero ridotto di particelle allora si possono notare molto meglio le tracce delle particelle alpha e come vengono deviate quando incontrano il nucleo centrale.


Per quanto riguarda lo schermo sensibile se viene scelto con grandi dimensioni non si vedranno i pixel a meno di ingrandimenti "manuali", all'opposto se viene scelto con dimensioni molto ridotte si vedrà solo il fascio che passa indisturbato oppure poche delle particelle deviate.
Stesso discorso per le dimensioni dei pixel: pixel troppo piccoli sono di difficile rintracciamento visivo, mentre pixel troppo grandi inglobano troppi dati e non vi è apprezzamento fisico del fenomeno dello scattering.
Si consiglia di fare qualche prova con diversi parametri per prenderci la mano e capire come impostare al meglio la mappa di pixel.

Se si vuole confrontare cosa succede quando si aggiungono più lamine bisogna osservare lo schermo di pixel: quando abbiamo più di una lamina i dati intorno all'origine (centro dello schermo) sono più sparpagliati e quindi maggiormente riconoscibili, questo appunto perchè una particella che viene "scatterata" più volte si troverà in una posizione finale maggiore di una deviata solamente una volta.

A questo punto vengono consigliati diversi parametri di prova per la visualizzazione di 4 diversi casi:

a) Particella alpha dal decadimento di 222Rn (E = 5.5MeV) che attraversa una lamina d'oro

    lamina_metallo = Lamina_metallo(posizione = np.array([-2, 2]), materiale = "oro", larghezza = 0.2, numero_atomico = 79, distanza_fra_lamine = 0)

    prova1 = esperimento_Rutherford(energia = 5.5, distanza_collimatore = 1, dimensioni_collimatore = 0.005,
                                    posizione_schermo_sensibile = 5,  dimensioni_pixel = 0.00025,
                                    lamine_metallo = [lamina_metallo], n_particelle = 20000, condizione_b = 0.00000001, dimensione_schermo = 0.05)
    prova1.visualizza_apparato()
    prova1.simulazione()

b) Particella alpha dal decadimento di 214Po (E = 7.7MeV) che attraversa una lamina d'oro

    Uguale al caso di prima però inserire nell'attributo energia 7.7 al posto di 5.5

c) Particella alpha dal decadimento di 222Rn (E = 5.5MeV) che attraversa due lamine d'oro poste ad 1cm di distanza

    lamina_metallo2 = Lamina_metallo(posizione = np.array([-1.8, 1.8]),materiale = "oro",  larghezza = 0.2, numero_atomico = 79, distanza_fra_lamine = 1)
    lamina_metallo3 = Lamina_metallo(posizione = np.array([-3, 3]),materiale = "oro",  larghezza = 0.2, numero_atomico = 79, distanza_fra_lamine = 1)

    prova3 = esperimento_Rutherford(energia = 5.5, distanza_collimatore = 1, dimensioni_collimatore = 0.005,
                                    posizione_schermo_sensibile = 5, dimensioni_pixel = 0.00025,
                                    lamine_metallo = [lamina_metallo2,lamina_metallo3], n_particelle = 20000, condizione_b = 0.00001, dimensione_schermo = 0.1)
    prova3.visualizza_apparato()
    prova3.simulazione()

d) Particella alpha dal decadimento di 222Rn (E = 5.5MeV) che attraversa tre lamine d'oro poste ad 1mm di distanza

    lamina_metallo4 = Lamina_metallo(posizione = np.array([-2, 2]), materiale = "oro", larghezza = 0.2, numero_atomico = 79, distanza_fra_lamine = 0.1)
    lamina_metallo5 = Lamina_metallo(posizione = np.array([-2.3, 2.3]), materiale = "oro", larghezza = 0.2, numero_atomico = 79, distanza_fra_lamine = 0.1)
    lamina_metallo6 = Lamina_metallo(posizione = np.array([-2.6, 2.6]), materiale = "oro", larghezza = 0.2, numero_atomico = 79, distanza_fra_lamine = 0.1)

    Successivamente è uguale al punto c) solo che "lamine_metallo = [lamina_metallo4,lamina_metallo5,lamina_metallo6]"


Quanto fatto per i punti precedenti può essere ripetuto con un minore numero di particelle soprattutto per i punti c) e d), regolando chiaramente anche le dimensioni dello schermo di pixel e l'attributo "condizione_b" (perchè inviando meno particelle è meno probabile che esse vengano scatterate con valori sulla condizione di b molto piccoli).

Da notare che i valori sopra scelti per l'attributo "condizione_b" nei punti a) e b) sono quelli che meglio approssimano la distribuzione attesa per 20000 particelle, ovvero l'ordine delle decine di particelle vengono scatterate.
Per i punti c) e d) si è abbassato questo valore in quanto non veniva scatterata nessuna particella nelle lamine successive in quanto si erano già allontanate sufficientemente da non rispettare più la condizione di scattering.