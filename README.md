# TEMSA (Translittération et étiquetage morphosyntaxique de l'arabe)

Ce script est un outil de Traitement Automatique du Langage (TAL) arabe qui permet d'accomplir les tâches suivantes :

    1.Détection de l'alternance codique 
    2.Translittération automatique en graphie arabe
    3.Segmentation morphologique
    4.Étiquetage morphosyntaxique (POS tagging)
    5.Lemmatisation 
   
Le script est rédigé en Python un langage universel et très populaire pour de nombreuses tâches de TAL.

## Pour commencer

Pour mener à bien votre projet il faut que :

    1.Les données soient sous le format .eaf propre à l'outil de transcription Elan, sinon vous pouvez convertir vos données avec [TEI.CORPO](https://github.com/christopheparisse/teicorpo) (C.Parisse, 2021)
    2. Les données doivent comporter une transcription en Arabizi
    3.Le dictionnaire Lefff (B.Sagot, 2010) soit dans le même répertoire du script, sinon mentionnez le répertoire du fichier dans le script
    4.Les répertoires des fichiers d'entrées et des fichiers de sorties doivent être définis dans le script  

## Pré-requis

Pour exécuter le script il faut installer les librairies suivantes :

    1. [pympi](https://pypi.org/project/pympi-ling/)	(pip install pympi-ling)
    2. [requests](https://pypi.org/project/requests/)	(pip install requests)
    3. [farasa](https://pypi.org/project/farasapy/)	(pip install farasapy)
    4. Vérifie aussi si vous avez les librairies (re, os, http, json)

## Détails du fichier de sortie : 

Le script fournit un fichier de sortie sous le format .eaf comportant les tiers suivantes :

#### A\ tiers générées automatiquement :

    1. spk	transcription initiale en arabizi
    2. spk_trans	translittération en graphie arabe en laissant les tokens français en graphie latine (il ne faut pas se méfier à l’ordre visuel dû au phénomène de bidirectionnalité, l’ordre numérique est juste), une segmentation morphologique a été effectuée sur l'arabe avec des plus (+)
    3. spk_pos	étiquetage morphosyntaxique, les catégories syntaxiques du même token sont séparées par des plus (+)
    4. spk_lemma	comporte les racines des tokens arabe (les résultat n'était pas fiable pour la variété de l'arabe tunisien)

#### B\ tiers vides dédiées à l'évaluation et l'annotation manuelle :

    1. spk_word_based	cette tier est dédiée à une segmentation manuelle au niveau des morphèmes en arabizi, en ajoutant des plus (+)
    2. spk_errors	désigne de potentielles erreurs au niveau de la translittération (en cours de développement)
    3. L'ensemble des tiers qui se terminent par _eval (spk_pos_seg_eval, spk_trans_seg_eval) sont des tiers vides, dédiées la vérification manuelle des données générées automatiquement
    4. L'ensemble des tiers qui se terminent par _seg (spk_pos_seg, spk_trans_seg, spk_word_based_seg), dédiées à la segmentation lexicale en suivant ces étape sur Elan: Acteur-> Tokenizer l’acteur -> choisir la tiers source  (spk_pos, spk_trans) et la tiers d’arrivée (spk_pos_seg, spk_trans_seg, spk_word_based_seg) -> choisir délimiteur token par défaut (espace)

Notez bien que vous pouvez paramettrer le choix des tiers du fichier de sortie, il suffit de mettre en commentaire (#) les tiers dont vous voulez vous passer 

## Ce script était construit avec :

    1.pympi			(M.Lubbers, 2013)
    2.Lefff			(B.Sagot, 2010)
    3.farasa			(A.Abdelali et al., 2016)
    4.Google Outils de saisie	(https://www.google.com/inputtools/)

## Dans la prochaine version :

- [ ] L'ajout d'une tiers traduction en arabe MSA, anglais, Français
- [ ] L'ajout d'une tiers analyse syntaxique en dépendence
- [ ] L'ajout des indications d'event (bruit) dans la tiers translittération (spk_trans)
- [ ] Amélioration des résultat de segmentation, du POS tagging et de la lemmatisation

## Comment citer

@software{khoudri_temsa_2021,
	title = {{TEMSA}: Un script Python pour l'enrichissement des données de l’arabe parlé (translittération et étiquetage morphosyntaxique)},
	rights = {{CC}-{BY}-{NC}-4.0},
	url = {https://github.com/bazinga34/TEMSA.git},
	shorttitle = {{TEMSA}},
	version = {1.0},
	author = {Khoudri, Mustapha},
	date = {2021},
	keywords = {arabe parlé, corpus oral, {POS} tagging, python, {TAL}, translittération}
}

## License

Ce projet est sous licence Creative Commons Attribution Non Commercial 4.0 international [CC-BY-NC-4.0](https://spdx.org/licenses/CC-BY-NC-4.0.html)
