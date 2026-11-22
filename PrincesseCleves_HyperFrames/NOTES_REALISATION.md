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
- S11 : la silhouette « dans l'ombre » est le détourage de Nemours rempli d'encre (`assets/nb/silhouette_nemours.png`).

## Rendu
```
node .claude/skills/hyperframes/scripts/plugin-cli.mjs render --fps 25 --quality delivery -o PrincesseCleves_BA_dessinee_1080p_HQ.mp4
```
