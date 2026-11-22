# Outils de préparation (hors rendu)

Lancés une fois depuis la racine du projet, ils régénèrent ce qui n'est pas dans les zips d'origine.

| Script | Rôle |
|---|---|
| `prep_nb.sh <projet>` | Crée `assets/nb/` : toutes les images et vidéos en noir et blanc avec la formule du prompt (`grayscale(1) contrast(1.12) brightness(1.04) sepia(.08)`), calculée une fois pour toutes (les bougies restent en couleur). |
| `textures.py <projet>/assets/textures` | Papier ivoire `#F5F1E8` à grain fixe + parchemin (S07). |
| `mms_align.py <projet> <travail> <sortie.json>` | **Alignement forcé** du texte exact de `timeline.json` sur l'audio (modèle CTC MMS de Meta, ONNX `onnx-community/mms-300m-1130-forced-aligner-ONNX`, onnxruntime). |
| `refine_starts.py <projet> <entrée.json> <sortie.json>` | Recule chaque début de mot jusqu'à l'attaque réelle (énergie large bande, ≤ 0,15 s) : le modèle CTC marque une lettre au milieu de son son. Donne `words.json`. |
| `align2.py`, `build_words.py` | Ancienne méthode (Whisper DTW), gardée pour mémoire : dérivait de 0,1–0,3 s dans les longues phrases. |
| `spectro.py <projet> <début> <fin> <sortie.png>` | Spectrogramme + repères de mots, pour vérifier le calage à l'œil. |

`assets/lib/words.js` est généré depuis `words.json` (mêmes données, chargées par les scènes).
La fumée dense de S07 : `ffmpeg -i assets/nb/pexels_fumee_encre_noire_sur_blanc.mp4 -vf "lutyuv=y='clip(16+219*pow(clip((val-16)/(233-16)\,0\,1)\,5)\,16\,235)':u=128:v=128" -c:v libx264 -crf 15 -an assets/nb/pexels_fumee_encre_dense.mp4`
