#Nomenclature

Nomenclature est un programme ayant pour but d'effectuer la conversion entre les formules brutes - topologiques et nomenclaturée d'une molécule de chimie organique. 

[TOC]

## License

Copyright (C) 2015 BOUVIN Valentin, HONNORATY Vincent, LEVY-FALK Hugo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Utilisation

### Formule topologique

La saisie de la formule topologique s'effectue au moyen d'un affichage en arbre. Un alinéa symbolise une "filiation", c'est à dire une liaison.

Chaque atome possède une barre d'outils de la sorte :

[Suppression de l'atome] [Type de liaison à créer] [Nature de l'atome à créer] [Lancement de la création de l'atome enfant]

Il n'est pas utile d'ajouter manuellement les hydrogènes car le programme comblera automatiquement les "trous" par des hydrogène.

Il y a à disposition une barre d'outils sur la droite permettant d'ajouter automatiquement des hydrogènes, d'enlever automatiquement les hydrogènes, d'effacer la molécule courrante, d'exporter la formule topologique courrante (nécessite d'avoir lancé la convertion au préalable) et de convertir l'arbre vers la formule topologique, brute et nomenclaturée.

**Note à propos de la suppression d'un atome dans une molécule :** la suppression d'un atome entraîne la suppression de la totalité de ses enfants, sans retour en arrière possible.

Il est possible de modifier un atome créé précédemment au moyen d'un clique droit sur ce dernier.

### Formule brute
*À venir*

### Formule nomenclaturée
La saisie du nom de la formule doit s'effectuer en mettant un "-" entre chaque partie du nom, c'est à dire entre les numéros qui définissent les positions des diférents éléments, puis entre les fonctions, chaîne principale ou branches. La position de la fonction doit également être noté 1 le cas échéant.

Quelques exemples de noms:
- 2-4-diethyl-pentan
- 1-2-4-trimethyl-octan-3-amine
- 1-methyl-5-ethyl-pentan-1-ol