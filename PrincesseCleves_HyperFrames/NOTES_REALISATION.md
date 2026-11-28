# Notes de réalisation

## Structure
- `index.html` : film complet (1920×1080, 212,0 s, 25 i/s), bande-son définitive, papier ivoire, filtre « boil ».
- `compositions/s00.html` … `s18.html` : une sous-composition par scène (temps dans `index.html`).
- `assets/lib/ink.js` : traits d'encre, karaoké, surlignage, écriture à la plume, page de livre 3D.
- `assets/lib/ink.css` : styles communs (collage, cartels, page de livre).
- `words.json` (+ `assets/lib/words.js`) : temps de chaque mot de la voix off.
- `outils/` : scripts de préparation (noir et blanc, textures, alignement des mots), voir `outils/LISEZ-MOI.md`.

## Calage sur la voix
- Alignement forcé du texte exact (modèle CTC MMS de Meta), puis recul de chaque début de mot jusqu'à l'attaque réelle.
- Le karaoké noircit chaque mot 0,05 s avant son début ; les mots « en coupe franche » apparaissent 0,05 s avant.
- Quatre phrases s'écartent de `timeline.json` de plus de 0,2 s ; l'audio (et tous les moteurs) donnent :
  « Ce n'est pas la même chose » 59,41 s · « Un soir de bal… » 62,31 s · « Plus tard, il vole son portrait » 78,45 s · « Mais jusqu'où ? » 155,41 s.

## Choix à connaître
- Apostrophes typographiques (’) à l'écran.
- Légendes d'archives en IM FELL italique 34 px (le prompt demande 28–32 px et un minimum lisible de 34 px).
- Incipit sans guillemets (lettrine « L ») ; les trois autres citations sont entre « » avec espaces insécables.
- S02 : « magnificence » et « galanterie » surlignés en rouge, « Henri second » souligné à l'encre.
- Texte flou autour des citations : vrai texte du roman, édition Lepetit 1820 (Wikisource, domaine public) ; la phrase citée est exactement celle du prompt.
- Noir et blanc : la formule du prompt (`grayscale(1) contrast(1.12) brightness(1.04) sepia(.08)`) est appliquée une fois pour toutes aux fichiers (`assets/nb/`). Exceptions en couleur : les bougies (S10) et le cachet de cire rouge (S09).
- S01 : la main qui écrit « 1678 » (`ia_main_plume.png`) et l'encrier posé à côté (`element_encrier.png`).
- S11 : la silhouette « dans l'ombre » est `silhouette_ombre_homme.png`, collée au bord haut de l'écran, à moitié cachée derrière l'image du jardin ; des ondes d'encre vont de la fenêtre du pavillon vers elle.
- Bords coupés net des personnages : jamais au milieu du papier. Soit collés au bord de l'écran (S10, S14), soit fondus sur 15 % (classes cumulables `fondu-h`, `fondu-b`, `fondu-g`, `fondu-d` dans `ink.css`), soit dans un médaillon ovale tracé à l'encre (S06).
- S07 → XVIIe siècle (≈ 99,5 s) : un grand trait d'encre couvre tout l'écran, les deux mondes s'échangent dessous, jamais superposés.
- S08 : la citation du précipice est composée en 84 px sur deux lignes, au bord bas de la page, juste avant la bascule.

## Rythme « bande-annonce »
- Grands mots tous entre 140 et 300 px (Source Serif 700–900). « Des fêtes. / Des bals. / Des tournois. » s'enchaînent en trois coupes franches sur la voix.
- Aucun plan figé : lentes poussées de caméra (2 à 6 %) sur S01, S03, S05, S06, S12, S13, S16, rapprochement sur la gravure de *L'aveu* (S11), marges de 80 px respectées.
- S06 : le bal en plein cadre (61,9 → 67,6), puis coupure nette sur le papier vide sur l'impact de 67,6 s.
- S13 : chaque mot claque sur son impact (158 / 160 / 162).
- S15 : après la plongée dans le point rouge, le point bat comme un cœur sur les pulsations de basse de la bande-son (175,45 · 175,85 · 176,27 · 176,70 · 177,10 s), avec des ondes d'encre.

## Rendu
```
node .claude/skills/hyperframes/scripts/plugin-cli.mjs render --fps 25 --quality delivery -o PrincesseCleves_BA_dessinee_1080p_HQ.mp4
```
Version légère (< 100 Mo), réencodée depuis la HQ en deux passes, piste audio copiée telle quelle :
```
ffmpeg -y -i PrincesseCleves_BA_dessinee_1080p_HQ.mp4 -c:v libx264 -preset slow -b:v 3000k -pass 1 -an -f null /dev/null
ffmpeg -i PrincesseCleves_BA_dessinee_1080p_HQ.mp4 -c:v libx264 -preset slow -b:v 3000k -pass 2 -pix_fmt yuv420p -r 25 -c:a copy -movflags +faststart PrincesseCleves_BA_dessinee_1080p_leger.mp4
```
