% Aya Chetto (2194547)
% Camille Ménard (2214742)

include "globals.mzn";

%-----------------------------------------------------------------------------%
% Données
%-----------------------------------------------------------------------------%

% Nombre d'acteurs et de rôles
int: n;
% Couleurs des costumes
enum costumes; 
% Costume démandé pour un rôle i (première dimension) par un acteur j (seconde dimension)
array[1..n,1..n] of costumes: choix_costume;

%-----------------------------------------------------------------------------%
% Variables de décisions
%-----------------------------------------------------------------------------%

% Variables de décision pour assigner un acteur à un rôle
array [1..n] of var 1..n: assignation_role;
array [1..n] of var costumes: assignation_costume;


%-----------------------------------------------------------------------------%
% Partie étudiant
%-----------------------------------------------------------------------------%
% Chaque rôle doit être attribué à un seul acteur (permutation)
constraint all_different(assignation_role);


% Détermination du costume selon l'acteur et le rôle choisi
constraint forall(a in 1..n)(
assignation_costume[a] = choix_costume[assignation_role[a], a]
);

% Pas de costumes identiques entre acteurs
constraint all_different(assignation_costume);

% Contrainte d’adjacence : deux acteurs voisins ne doivent pas avoir des rôles adjacents
constraint forall(i in 1..n-1)(
abs(assignation_role[i] - assignation_role[i+1]) != 1
);

solve satisfy;
%-----------------------------------------------------------------------------%

output	
  ["L'acteur " ++ format(i) ++ 
   " prendra le rôle " ++ format(fix(assignation_role[i])) ++ 
   " (costume " ++ format(assignation_costume[i]) ++ ")" ++"\n" 
  | i in 1..n];