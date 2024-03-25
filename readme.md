## Abstract

Elektroencefalografia jest najpopularniejszą metodą obrazowania stosowaną w dziedzinie rozwiązan mózg-komputer ktorej rozwoj pozwolil na


Praca prezentuje proces opracowania oraz ewaluacji modelu pozwalającego na wykrywanie stopnia skupienia człowieka za pomocą elektroencefalografii (EEG). W tym celu przygotowano dedykowane oprogramowanie pozwalające na nagrywanie sygnału EEG podczas wykonywania prezentowanych zadań matematycznych. Następnie przeprowadzono kampanię badawczą na próbce ochotników, analizując zebrane dane oraz testująć wydajność lasów losowych oraz głębokich, konwolucyjnych i rekurencyjnych sieci neuronowych.

This paper presents the process of creating and evaluating a machine learning model aimed at detecting attention states using electroencephalography (EEG). Dedicated software was developed to record EEG signals during mental arithmetic tasks. Following a data collection campaign, statistical analysis was conducted. The performance of random forests, as well as dense, convolutional, and recurrent neural networks (RNNs), was evaluated.

## Dyskusja

Pomimo statystycznie istotnej różnicy pomiedzy sygnałami odczytywanymi w czasie skupienia i w stanie spoczynku zastosowane modele uczenia maszynowego nie wykazaly zdolnosci do wykrycia tej zaleznosci na na oddzielonej populacji kontrolnej. Wyniki te mimo zastosowania architektur \cite{} i metod trenowania modeli \cite{} zgodnych o potwierdzonej skutecznosci i zgodnych z najnowszymi osiągnięciami w dziedzinie uczenia maszynowego sugerują niewystarczającą wielkość zbioru badawczego (hipoteza niepoprawngo wykonania pomiarów odrzucona została z względu na wykrywalna statystycznie roznice pomiedzy badanymi stanami), niespodziewanie wysokie wariacje wprowadzone przez zbadane zmienne zakłócające wydają się wspierać te wnioski. Jednoczesnie badania zaprezentowane przez \cite{} przy zachowaniu podobnej ilosci uczestnikow osiagaja stanowczo lepsze rezultaty efekt ktory spowodowany mogl byc wykorzystaniem urządzeń pomiarowych przeznaczonych do uzytku medycznego, a przez to osiągnięcie wyższego efektywnego stosunku sygnału do szumu. W celu jednoznaczenego zweryfikowania tezy badawczej wymagane jest zebranie większej ilości danych przez przeprowadzenie dodatkowej kampanii badawczej.


## Wyniki

W celu opracowania algorytmu wykrywania stanu skupienia przetestowano szereg różnego rodzaju algorytmów \footnote{Zebrany zbiór danych oraz implementacje modeli znaleźć można pod adresem \url{https://github.com/mateuszkojro/bachelors-thesis/}} między innymi lasy losowe, proste sieci neuronowe – \autoref{fig:simple-nn}, konwolucyjne sieci neuronowe - \autoref{fig:conv-nn} oraz specjalistyczne sieci do klasyfikacji szeregów czasowych – architektura MLSTM-FCN \cite{karim_multivariate_2019} przedstawiona na rysunku \ref{fig:mlstm} i metod przygotowania danych wejściowych – wejścia w postaci różnej długośći czasowych wycinków zmierzonych napięc lub transformaty wyników transformaty Fouriera.

Sprawnośc modeli oceniana była za pomocą zestawu danych walidacyjnych przygotowanych poprzez wykluczenie pomiarów wykonanych na trzech osobach z zbioru uzywanego do trenowania. Do oceny jakośći wykorzystana zostala standardowa dla problemów klasyfikacji binarnej miara F1 (obliczana za pomocą wzoru \ref{eq:calculation-f1}).

W celu dobrania odpowiednich metod przygotowania danych oraz wartości hiperparametrów modeli przeprowadzono eksperymenty mające na celu ich ustalenie. Wpływ rozmiaru okna czasowego na uczenie modelu sprawdzony został poprzez trenowanie lasu losowego na tym samym zbiorze danych z różnym rozmiarem okna czasowego jako wejścia do modelu (\autoref{fig:window-size}). Natomiast głębokość lasu losowego dostosowana została przez jej sukcesywne zwiększanie aż do osiągnięcia stabilizacji (\autoref{fig:rf-num-nodes}). Wartosci f1 najlepszych modeli przedstawiono w tabelii \ref{} jednoznacznie pokazując brak zdolnośći predykcyjnej algorytmów.