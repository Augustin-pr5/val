# PROMPT — Bande-annonce « La Princesse de Clèves » en motion design dessiné (HyperFrames)

Tu es motion designer et monteur. Tu vas refaire **entièrement l'image** d'une bande-annonce de 3 min 32 s avec **HyperFrames**, dans un style « collage d'archives + dessin à l'encre qui s'anime », **sur une bande-son déjà terminée** (voix off, musique, bruitages). Tout ce dont tu as besoin est dans ce dossier. Lis ce fichier en entier avant de commencer, puis `timeline.json`.

---

## 0. Le projet en une phrase

Un lycéen (Augustin PERRON) présente *La Princesse de Clèves* (Madame de Lafayette, 1678) et montre que le roman **interroge** « l'amour plus fort que tout » inventé par Chrétien de Troyes dans *Le Chevalier de la charrette* : Lancelot monte dans la charrette par amour, la princesse, elle, a le courage de **rester sur le chemin**. La bande-annonce doit donner envie de lire le livre.

## 1. Contraintes NON négociables (c'est noté par un professeur)

1. **La bande-son est la référence absolue.** Utilise `assets/audio/bande_son_finale_212s.m4a` telle quelle : ne la coupe pas, ne la décale pas, ne la remixe pas. Durée de la vidéo : **212,0 s exactement**, 1920 × 1080, **25 i/s**.
2. Doivent apparaître à l'écran : **titre, auteur, date (1678), contexte historique** (cour d'Henri II, 1558), le **lien avec *Le Chevalier de la charrette*** (Chrétien de Troyes, vers 1180), un **point de vue** (pas un résumé), et **au moins 2 citations** du roman (il y en a 4, voir plus bas : toutes doivent être lisibles à l'écran).
3. **Ne jamais dévoiler la fin** (pas de mort du prince, pas de choix final de la princesse, pas de couvent ni de retraite). La fin de la bande-annonce est une accroche.
4. **Uniquement des médias libres de droits** : ceux de ce dossier. Aucun extrait de film, de série, de clip ou de chanson. N'utilise **aucun** logo ou élément de marque des vidéos de référence (voir § 3).
5. Les textes à l'écran sont **exactement** ceux donnés ici (orthographe, accents, guillemets « » avec espace insécable, espace insécable avant « : ? ! »).
6. Le **générique** final est imposé (§ 7).

## 2. Ce que contient le dossier

```
PROMPT.md                ← ce fichier
timeline.json            ← temps exacts : scènes, phrases de la voix off, textes, temps forts sonores
PLANCHE_TOUTES_LES_IMAGES.jpg ← aperçu de tous les médias avec leur nom
DA/                      ← 2 vidéos de référence de direction artistique + leurs planches
assets/audio/            ← bande_son_finale_212s.m4a (voix + musique + bruitages, DÉFINITIVE)
assets/images_ia/        ← 20 images IA nettoyées (1920×828, sans bandes noires)
assets/images_ia_detourees/ ← 14 PNG détourés (fond transparent) pour le collage
assets/archives/         ← 8 œuvres anciennes (Gallica/BnF, domaine public) : Clouet, Masson, tournoi 1559, enluminure de Lancelot
assets/photos/           ← 4 photos de châteaux (Pexels)
assets/videos/           ← vidéos Pexels (dont versions « encre noire sur blanc ») + 2 animations IA (1920×828)
fonts/                   ← Source Serif 4, IM FELL English, Noto Serif (licence OFL)
reference/               ← l'ancienne version de la bande-annonce (540p) : sert UNIQUEMENT de repère de timing
```

Si tu as besoin d'un détourage en plus, utilise l'outil de suppression de fond de HyperFrames (`/hyperframes-media`).

## 3. Direction artistique

Regarde `DA/DA_1_style_general_collage_gravures_traits_encre.mp4` (style général) et `DA/DA_2_style_citations_livre_mots_surlignes.mp4` (style des citations) avant d'écrire une ligne de code. **On reprend le langage visuel, jamais la marque** : pas de logo, pas d'astérisque, pas du mot « Claude » ni « DistilBook », pas leur orange.

### Palette (stricte)
- Fond papier ivoire `#F5F1E8`, avec un grain de papier très léger (fixe, pas animé).
- Encre `#161412` pour les traits et les textes.
- Gris « pas encore dit » `#B8B2A7`.
- **Un seul accent : rouge cire `#B3261E`** (la passion, le cachet des lettres, le sang du tournoi). Il sert pour le **point rouge** (voir motif), les surlignages et quelques détails. Jamais de grandes surfaces rouges.
- Toutes les images passent en **noir et blanc** (CSS : `grayscale(1) contrast(1.12) brightness(1.04) sepia(.08)`). **Seule exception en couleur : les 3 bougies qui s'éteignent (S10)**, le seul moment sombre du film.

### Typographie
- Grands mots (style DA_1) : **Source Serif 4**, graisse 700 à 900, très gros (140 à 260 px), apparition **mot par mot, en coupe franche**, calée sur la voix.
- Citations, dates, légendes d'archives : **IM FELL English** (fonte du XVIIe siècle), romain et italique.
- Légendes d'archives : petites (28–32 px), italiques, comme des cartels de musée, avec la source (« Gallica / BnF »).
- Texte minimum lisible : 34 px. Rien à moins de 80 px du bord.

### Langage du mouvement
- **Le trait d'encre qui se dessine** (SVG `stroke-dasharray` / `stroke-dashoffset`) : cercles qui entourent un visage, flèches, lignes qui relient les personnages (le triangle Princesse – Nemours – Clèves), spirale (le vertige, le précipice), soulignés, ratures. Traits irréguliers, comme à la plume.
- **Le « boil »** : les traits tremblent légèrement comme un dessin animé fait main (filtre SVG `feTurbulence` + `feDisplacementMap`, graine changée toutes les 2 images = 12,5 i/s). Discret.
- **Collage** : images détourées et archives « posées » sur le papier (fine ombre douce, légère rotation ±1,5°), qui glissent, se superposent, se répondent. Parallaxe lente entre plans.
- **Le point rouge** = motif conducteur. Il naît de la goutte d'encre de la plume (S01), voyage d'une scène à l'autre (il devient le cachet d'une lettre, le cœur de la spirale du précipice, le « ? » de la question, le point final de « Lisez-le. »). Il fait le lien visuel de tout le film.
- **Rythme** : alterner le calme (citations, 4 à 7 s) et le très rapide (montages de 0,3 à 0,7 s sur les temps forts sonores de `timeline.json`).
- **À éviter absolument** (effet « CapCut ») : glitch, décalage RVB, flou de zoom à répétition, tremblements partout, transitions toutes faites, émojis, polices fantaisie, plus d'une couleur d'accent.

### Les citations (style DA_2)
Chaque citation apparaît **imprimée sur une page de livre ancien** (papier, IM FELL justifié, lettrine pour l'incipit) filmée en **3D** : perspective (`rotateX` 20–35°), lent glissement de caméra, **profondeur de champ** (bords de la page floutés). Les mots passent du gris `#B8B2A7` à l'encre **au moment exact où ils sont dits** (karaoké mot à mot, d'après la transcription). Les mots clés reçoivent un **surlignage au marqueur rouge** (35 % d'opacité, bords irréguliers, balayage de gauche à droite en 0,3 s). L'attribution s'écrit en italique sous la citation. Entrées et sorties : tourne-page ou balayage d'encre.

Pour entourer la citation de vrai texte du roman sur la page, tu peux récupérer le passage exact sur Wikisource (*La Princesse de Clèves*, domaine public) ; ce texte autour reste flou. **N'invente jamais de faux texte** : si tu n'as pas accès au passage, affiche la citation seule sur la page.

| # | Scène | Citation (exacte) | Attribution | Surligner |
|---|---|---|---|---|
| 1 | S02 | « La magnificence et la galanterie n'ont jamais paru en France avec tant d'éclat que dans les dernières années du règne de Henri second. » | Madame de Lafayette, *La Princesse de Clèves*, 1678 — première phrase du roman | magnificence, galanterie |
| 2 | S04 | « Si vous jugez sur les apparences en ce lieu-ci, vous serez souvent trompée : ce qui paraît n'est presque jamais la vérité. » | Madame de Chartres à sa fille | apparences, vérité |
| 3 | S08 | « Vous êtes sur le bord du précipice. » | Madame de Chartres, mourante | précipice |
| 4 | S10 | « Je vais vous faire un aveu que l'on n'a jamais fait à son mari. » | La princesse de Clèves | aveu, jamais |

## 4. Découpage scène par scène

Les temps exacts sont dans `timeline.json`. Les idées ci-dessous sont des intentions : garde le sens, améliore la forme si tu as mieux. **Les coupes fortes tombent sur les temps forts sonores.**

- **S00 · 0,0–2,6 · Ouverture éclair.** Quatre images en noir et blanc (bal, aveu, jardin, mère mourante), dans des cadres posés sur le papier, claquent sur les impacts (0,43 / 0,85 / 1,28), chacune avec un cercle d'encre qui se referme d'un coup. À 1,8 s, un grand trait d'encre balaie tout → papier vide jusqu'à 2,6.
- **S01 · 2,6–10,0 · « 1678 ».** La plume (`ia_plume_encrier.png`) trace « 1678 » à l'encre (IM FELL, écrit en direct). Une goutte tombe et devient **le point rouge**. Puis « Un roman paraît. Sans nom d'auteur. » mot par mot (Source Serif, gros).
- **S02 · 10,0–19,6 · Citation 1, l'incipit.** La page du livre (lettrine « L ») en 3D, karaoké sur la voix (10,84 → 17,98). Autour, en collage : la photo de Chenonceau en noir et blanc avec sa légende, puis la peinture du *Bal à la cour des Valois* avec sa légende. Fin : la caméra recule et le bal s'anime (`ia_video_bal_danse_1920x828.mp4`, en noir et blanc, dans un cadre ovale gravé).
- **S03 · 19,6–36,0 · La cour.** Les trois portraits de Clouet épinglés sur le papier (coupes à 19,6 / 23,6 / 25,0) avec leurs légendes ; des traits d'encre les relient comme un arbre généalogique. Gros mots : « 1558. » puis « fêtes. bals. tournois. » sur la voix ; sur « tournois » (26,25) les **chevaux en silhouette** (`pexels_chevaux_silhouettes_ralenti_NB.mp4`) galopent en travers. « rumeurs, secrets » : des points noirs dérivent comme une constellation (`pexels_etincelles_points_noirs_sur_blanc.mp4`), reliés par des traits. « en un regard » (≈ 33 s) : un cercle d'encre se referme sur un œil.
- **S04 · 36,0–45,6 · Citation 2, la mère.** Page de livre + `ia_mere_conseil.png` à côté. Sur « ce qui paraît » (41,54), l'image de la princesse se dédouble en miroir (une copie inversée et pâlie) : l'apparence et la vérité.
- **S05 · 45,6–62,6 · Elle.** Portrait détouré de la princesse, son nom écrit à la plume : *Mademoiselle de Chartres*. Gros mot « la vertu. » (≈ 52 s). La gravure de Masson (rencontre) avec sa légende. Le prince de Clèves entre (53,6). « Lui l'aime à la folie » : depuis Clèves part une **spirale rouge** ; « Elle, elle l'estime » : depuis elle, une **ligne droite** calme. Sur « Ce n'est pas la même chose » : AIMER ≠ ESTIMER (le ≠ se dessine). C'est un moment de point de vue : sois clair.
- **S06 · 61,6–84,6 · La rencontre.** Le bal (vidéo IA en noir et blanc). **Coupure nette à 67,6** : papier vide, « Le duc de Nemours. » apparaît mot par mot, le point final est le point rouge ; silence jusqu'à 70,6. À 70,6, Nemours détouré claque avec un cercle d'encre. « Toute la cour les regarde » : des dizaines de petits yeux / cercles d'encre autour d'eux. « Eux ne voient qu'eux » : un trait relie Nemours et la princesse, le reste devient gris. « il vole son portrait » (79,3) : `ia_vol_du_portrait.png`, le point rouge part avec la miniature. « Et elle se tait » : un doigt d'encre / un trait qui ferme une bouche, ou simplement le silence et le blanc.
- **S07 · 84,6–109,0 · Le lien avec Lancelot (scène clé du barème).** Changement de monde à 84,6 : la page devient un parchemin médiéval. L'enluminure de *Lancelot et Guenièvre* (avec légende) et la charrette (`ia_lancelot_charrette_nb.jpg`). Écrire à la plume : « Chrétien de Troyes, *Le Chevalier de la charrette*, vers 1180 ». Sur « plus fort que l'honneur / que le roi / que la raison » : trois gros mots qui claquent sur les impacts (≈ 96,0 / 97,3 / 98,6), chacun **barré d'un trait rouge** (l'amour gagne). « Madame de Lafayette pose une autre question » (100,16) : la femme qui écrit (`pexels_femme_ecrit_plume.mp4` en noir et blanc), sa plume trace un grand « ? ». **104,0–108,7 : carton** « Et si l'amour plus fort que tout / était un danger ? », le « ? » en rouge, la fumée d'encre noire monte derrière (`pexels_fumee_encre_noire_sur_blanc.mp4`).
- **S08 · 109,0–116,2 · Citation 3, le précipice.** Idée : la citation est imprimée **au bord de la page**, la caméra bascule par-dessus le bord, et derrière : le vide (ou une spirale d'encre avec le point rouge au centre). `ia_mere_mourante.jpg` en petit, en noir et blanc.
- **S09 · 116,2–126,6 · La montée (rapide).** Un nom = une image = une coupe sur chaque impact : « Les tournois. » (gravure du tournoi de 1559 + `ia_joute.png`, légende) · « Les lettres perdues. » (le **cachet de cire rouge** `element_cachet_de_cire_rouge.png`, seule tache rouge) · « Les rumeurs. » (l'éventail `ia_chuchotement_eventail.png` + ondes d'encre) · « Chaque regard est un piège. » (un œil pris dans une toile de traits) · « Elle fuit la cour. Elle fuit Paris. » (le carrosse `ia_carrosse_fuite.png` file, une ligne de route se dessine) · « Elle se fuit elle-même. » (la princesse se sépare de son propre double).
- **S10 · 126,6–138,6 · Citation 4, l'aveu.** Page de livre + `ia_aveu_couple.png`. Karaoké sur la voix de la princesse (128,48 → 132,48). **134,0 : coupe franche sur les 3 bougies en couleur** (le seul plan sombre du film) : le clip `pexels_bougies_extinction.mp4` placé pour que l'extinction tombe à **135,05** (voir `timeline.json`). 136,0 : retour au papier, le jardin la nuit (`ia_video_jardin_nuit_1920x828.mp4`, noir et blanc).
- **S11 · 136,0–147,2 · Dans l'ombre.** « Elle ignore que quelqu'un, dans l'ombre, entend tout. » : une silhouette d'encre noire se dessine au bord du cadre, des ondes relient le pavillon à cette ombre. Puis la gravure de Masson *L'aveu* avec sa légende.
- **S12 · 147,2–158,0 · L'accroche.** Écran partagé : à gauche, la charrette de Lancelot, une flèche d'encre monte dedans (« Lancelot est monté dans la charrette », 148,64). À droite, le chemin dans la brume (`pexels_chemin_brume.mp4`, noir et blanc). **Sur « Elle, » (151,88)** : coupe sur `ia_princesse_chemin.png`, le chemin se dessine en un long trait d'encre devant elle. « Mais jusqu'où ? » (≈ 156) : le trait file hors champ et finit sur le point rouge.
- **S13 · 158,0–164,0 · Trois mots.** « Le devoir. » / « La passion. » / « Le repos. » plein écran, un mot par impact (158 / 160 / 162), chacun avec son signe d'encre : une verticale droite, une spirale rouge, une horizontale (un horizon).
- **S14 · 164,0–167,0 · Montage éclair.** 8 images détourées, une toutes les 0,3 s sur les impacts, chacune entourée d'un cercle qui claque. 166,4–167,0 : papier vide.
- **S15 · 167,0–177,5 · Titre.** « LA PRINCESSE DE CLÈVES » (Source Serif 900, très grand) se dessine ou s'imprime lettre à lettre ; « Madame de Lafayette · 1678 » en IM FELL italique. Sur « regarder à l'intérieur d'un cœur » (≈ 173–175), la caméra plonge dans le point rouge → blanc.
- **S16 · 177,5–182,5.** « Son choix, » / « personne ne l'a vu venir. » mot par mot.
- **S17 · 182,5–186,5.** « Lisez-le. » très grand ; le point final est le point rouge. Derrière, très pâle, des pages qui tournent (`pexels_pages_livre.mp4` en noir et blanc, opacité 15 %).
- **S18 · 186,5–212,0 · Générique** (§ 7), défilement lent ou cartons successifs, sur papier, avec les points noirs qui dérivent.

## 5. Textes à l'écran (exacts)

- 1678
- Un roman paraît. Sans nom d'auteur.
- 1558.
- La cour du roi Henri II.
- Des fêtes. Des bals. Des tournois.
- Mademoiselle de Chartres
- la vertu.
- AIMER ≠ ESTIMER
- Le duc de Nemours.
- Chrétien de Troyes, *Le Chevalier de la charrette*, vers 1180
- plus fort que l'honneur · plus fort que le roi · plus fort que la raison
- Et si l'amour plus fort que tout était un danger ?
- Les tournois. · Les lettres perdues. · Les rumeurs. · Chaque regard est un piège.
- Le devoir. · La passion. · Le repos.
- LA PRINCESSE DE CLÈVES · Madame de Lafayette · 1678
- Son choix, personne ne l'a vu venir.
- Lisez-le.
- Les 4 citations du § 3 et les légendes d'archives de `timeline.json`.

## 6. Méthode de travail (dans cet ordre)

1. **Installe les compétences HyperFrames** si ce n'est pas fait : `npx skills add heygen-com/hyperframes`, puis utilise `/hyperframes` (composition), `/hyperframes-cli` (init, lint, preview, render) et `/hyperframes-media` (transcription, détourage).
2. **Transcris la bande-son mot à mot** avec `/hyperframes-media` et enregistre `words.json` (texte + début/fin de chaque mot). Vérifie que les temps collent à `timeline.json` (écart < 0,2 s). Tout le karaoké et les apparitions de mots se calent sur `words.json`.
3. **Prototype d'abord deux scènes seulement : S02 (citation 1) et S07 (Lancelot).** Rends 6 images fixes (11 s, 15 s, 88 s, 96 s, 98,6 s, 106 s) et un aperçu vidéo de ces deux scènes. **Arrête-toi et montre-les-moi** avant de faire le reste.
4. Une fois validé, construis toutes les scènes, **une sous-composition par scène** (S00…S18), pour pouvoir corriger une scène sans tout casser.
5. Lance le lint, puis l'aperçu complet. Vérifie :
   - la synchro mot à mot ;
   - la lisibilité de chaque texte ;
   - la palette (aucune image en couleur sauf les bougies) ;
   - les temps forts sonores ;
   - l'absence de spoiler ;
   - la durée de **212,0 s**.
6. **Rends** en MP4 H.264, 1920×1080, 25 i/s, audio AAC 192 kbit/s, en deux versions :
   - `PrincesseCleves_BA_dessinee_1080p_HQ.mp4` ;
   - `PrincesseCleves_BA_dessinee_1080p_leger.mp4`, de moins de 100 Mo, pour École Directe.
7. Contrôle final : ouvre la vidéo rendue et extrais une image toutes les 10 s dans une planche. Vérifie que l'audio de la vidéo est **identique** à `bande_son_finale_212s.m4a`, sans décalage.

## 7. Générique (texte exact, dans cet ordre)

LA PRINCESSE DE CLÈVES
Bande-annonce

RÉALISATION
Augustin PERRON

D'APRÈS LE ROMAN DE
Madame de Lafayette (1678)

IMAGES
Générées par intelligence artificielle
Archives : Gallica / BnF (œuvres du domaine public)
Vidéos et photos : Pexels (libres de droits)

VOIX OFF, MUSIQUE ET BRUITAGES
Générés par intelligence artificielle

LOGICIELS UTILISÉS
ElevenLabs · HyperFrames · Claude Code

100 % LIBRE DE DROITS

Merci d'avoir regardé

## 8. Sources des médias (pour la fiche à rendre)

- **Archives (Gallica / BnF, domaine public)** :
  - portraits d'Henri II, de Catherine de Médicis et de Marie Stuart par François Clouet (et atelier) ;
  - *Bal à la cour des Valois* (1582) ;
  - *Le tournoi de 1559* de Tortorel et Perrissin ;
  - gravures de Masson pour l'édition Quantin (1878) ;
  - *Lancelot et Guenièvre* (BnF, ms. fr. 118, vers 1405).
- **Pexels** (licence Pexels, sans attribution obligatoire) :
  - vidéos n° 11997585 (chevaux), 12025939 (fumée), 12847647 (étincelles), 8677058 (bougies), 6752415 (femme qui écrit), 6479697 (chemin) et 5283827 (pages) ;
  - photo n° 19136597 (Chenonceau), ainsi que les photos de Chantilly, Villandry et du jardin de Chenonceau fournies par Augustin.
- **Images, animations, voix, musique et bruitages** : générés avec ElevenLabs.
