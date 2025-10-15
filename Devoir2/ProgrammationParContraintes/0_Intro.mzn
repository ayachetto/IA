% NOM_ETUDIANT_1 (MATRICULE_1)
% NOM_ETUDIANT_2 (MATRICULE_2)

include "globals.mzn";

%-----------------------------------------------------------------------------%
% Variables de décisions
%-----------------------------------------------------------------------------%

% Nombre devant satisfaire les critères
var 1000..9999: nombre;

% Décomposition du nombre en un ensemble de chiffres
array[1..4] of var 1..9: chiffres;

%-----------------------------------------------------------------------------%
% Objectif
%-----------------------------------------------------------------------------%

% Variable à minimiser
var int: p = chiffres[2] * chiffres[3] * chiffres[4];

%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%

constraint nombre = 
    1000*chiffres[1] + 100*chiffres[2] + 10*chiffres[3] + chiffres[4];

% Chiffres distincts
constraint alldifferent(chiffres);

% Contraintes du problème
constraint chiffres[4] mod 2 = 0;            % nombre pair
constraint chiffres[1] > chiffres[2];        % millier > centaine
constraint chiffres[3] < chiffres[4];        % dizaine < unité
constraint chiffres[2] > chiffres[4];        % centaine > unité
constraint sum(chiffres) > 15;               % somme > 15

solve minimize p;

%-----------------------------------------------------------------------------%

output [
  show(nombre)
];

