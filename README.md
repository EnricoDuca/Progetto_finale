# Progetto_finale
Repository contenente il codice dell'esame di metodi computazionali per la fisica - Enrico Duca -

La richiesta del progetto era quella di sviluppare in python una simulazione Monte Carlo di un apparato sperimentale per riprodurre degli esperimenti sullo scattering di Rutherford.
Innanzitutto bisogna specificare che ciò che è stato fatto è un'approssimazione dell'esperienza reale, in quanto si sono supposte considerazioni e condizioni per semplificare il tutto.

Nel codice si definisce inizialmente la classe  "Lamina_metallo" che permette di creare l'oggetto lamina con diversi attributi di "input", in ordine: 
- la posizione che deve essere del tipo np.array([x, y]) e, come già detto precedentemente, dato che è un'approssimazione bisogna stare attenti a definire una posizione che permette al nucleo (che si trova al centro della lamina) di collocarsi lungo l'asse y ( un esempio potrebbe essere: posizione = np.array([-2,2]));
- il materiale di cui è composta la lamina da passsare come stringa (ad esempio materiale = "oro");
- la larghezza della lamina, che poi andrà a definire la posizione del nucleo;
- il numero atomico del materiale di cui è composta la lamina;
- la distanza fra due o più lamine: se le lamine sono distanti di uguale valore esso va inserito ugualmente nei diversi oggetti.

Abbiamo citato il nucleo che, come già specificato prima, si trova al centro della lamina di metallo. Verrà considerato come parametro di impatto la differenza fra la posizione lungo l'asse x della particella quando si trova all'altezza della lamina e quella del nucleo.

A questo punto si è definita la classe "esperimento_Rutherford", come attributi di ingresso ha:
- l'energia cinetica del fascio di particelle alpha che vengono inviate contro la lamina;
- la distanza del collimatore, il foro collimatore viene posizionato lungo l'asse y: "self.posizione_collimatore = np.array([0, distanza_collimatore])";
- la dimensione del collimatore, dove con dimensione si intende il diametro del foro;
- la posizione dello schermo sensibile, dove con schermo sensibile si intende la mappa di pixel;
- la dimensione dei pixel;
- le lamine di metallo utilizzate per l'esperimento voluto, bisogna richiamare una o più lamine create dalla classe precedente, ad esempio: "lamine_metallo = [lamina_metallo1,lamina_metallo2]";
- il numero di particelle alpha del fascio incidente;
- una condizione sul parametro di impatto (b), tale condizione verrà usata per decidere se una particella che arriva alla stessa altezza del nucleo viene deviata o meno: "if b <=self.condizione_b".

