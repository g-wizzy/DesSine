# Compilateurs - Documentation _DesSine_
###### Pierre Bürki, Loïck Jeanneret

## Table des matières
[TOC]

## Concept du _turtle graphics_
*Turtle graphics* est une façon de réaliser un dessin sans lever le crayon, on imagine une tortue qui se déplace et dessine derrière elle. Pour dessiner, il suffit d'indiquer à la tortue comment se déplacer.

Dans ce projet, on contrôle un "point de dessin" et un "vecteur de dessin" à  l'aide de différentes commandes pour dessiner:

![](https://i.imgur.com/U5wrGE6.png)
> En bleu, le vecteur de dessin. En noir, le point de dessin. En rouge, le segment dessiné par le programme du centre.


## Dépendances
Le projet a été testé sur python 3.6 et 3.9 sur Linux et Windows.
Les modules python suivants doivent être installés afin de lancer chacun des modules du projet:
- `ply`, `pydot`, `tkinter`

De plus, il faut installer `graphviz` si l'on souhaite exécuter le *parser* indépendamment de l'interpéteur. Cette étape peut ne pas marcher sur Windows à cause d'un bug avec `dot`(voir `AST.py:69`).

## Démarrage rapide
### Installation
- Installer les dépendances requises (`pip install ...`)
- Créez un fichier `hello.ds` et y mettre le code suivant:
```javascript
// Define window size
#width(500)
#height(500)

// Set background color
#background(0xF0F0F0)

// Set drawing color
setColor(0x010101)
setLineWidth(2)

// Set drawing vector size
scale(100)

// Make the shape centered
move()
rotate(2 * PI / 3)

// Draw the shape
for(i = 0; i < 6; i = i + 1) {
    draw()
    move()

    rotate(PI / 3)
}

```
### Exécution
- Exécuter `python interpreter.py hello.ds` (remplacer `hello.ds` par le chemin du fichier à interpréter)
- Si tout s'est bien passé, une fenêtre s'affiche avec le résultat ci-dessous:

![](https://i.imgur.com/MY7Tmll.png)

## Référence du langage
Un programme `.ds` est composé de deux parties : l'initialisation et le corps.

### Bloc d'initialisation
Le programme doit commencer par un bloc d'initialisation. Celui-ci doit obligatoirement définir la largeur et la hauteur de l'image. Il peut accessoirement définir la couleur de fond de l'image.

### Corps du programme
C'est ici qu'il faut écrire la suite d'instructions qui décrira la trajectoire du point de dessin.
Les instructions sont séparées par les sauts de lignes, et les blocs sont délimités par des accolades. Les indentations n'ont aucun effet.

#### Types

DesSine n'utilise pas de types. Toutes les variables contiennent des nombres.

Les couleurs sont représentés par des nombres entre 0 et 0xFFFFFF. Il est possible d'utiliser les nombres hexadécimaux en les préfixant de 0x, et de réaliser des opérations dessus. Par exemple, il est tout à fait légitime d'écrire
```js
for (color = 0; color <= 0xFFFFFF; color = color + 0x010101)
```
Il existe deux fonctions built-in qui nécessite une couleur en argument. Il est possible de leur donner des valeurs non entières, celles-ci seront arrondies.

#### Structures de contrôle
DesSine dispose des structures de contrôle `if (else)`, `for` et `while` usuelles. Voici leurs formats exigés respectifs :
```js
if ([comparison]) {
    [instructions]
}
```

```js
if ([comparison]) {
    [instructions]
} else {
    [instructions]
}
```

```js
for ([assignment]; [comparison]; [instruction]) {
    [instructions]
}
```

```js
while ([comparison]) {
    [instructions]
}
```
Il est à noter que les positions des accolades sont strictes ; les accolades ouvrantes doivent se trouver sur la même ligne que le début de la structure, et le else doit suivre l'accolade fermante sans saut de ligne. Les parenthèses sont obligatoires également.
Il faut noter également que les conditions sont obligatoirement sous forme de comparaison. Ainsi, il ne faut pas écrire

```js
if (a) {
    [instructions]
}
```
mais plutôt
```js
if (a != 0) {
    [instructions]
}
```

### Fonctions disponibles

#### Fonctions d'initialisation
Ces fonctions doivent être appellées avant toute autre instruction.
- **`void #height(number height)`**
    - Définit la *hauteur* de la fenêtre en pixels
- **`void #width(number width)`**
    - Définit la *largeur* de la fenêtre en pixels
- **`void #background(color backgroundColor)`**
    - Définit la couleur de fond de la fenêtre.
    - Cette fonction d'initialisation est optionnelle.
    - La couleur de fond par défaut est noire.

#### Gestion du vecteur de dessin
- **`void move()`**
    - Déplace le point de dessin selon le vecteur de dessin sans dessiner
- **`void scale(number coefficient)`**
    - Met à l'échelle le vecteur de dessin selon le coefficient donné.
    - Si le vecteur de dessin atteint une taille nulle, il ne sera plus possible de dessiner, et un warning le fera savoir à l'utilisateur.
- **`void rotate(number angleInRadian)`**
    - Pivote le vecteur de dessin du nombre de radians donné (sens positif).

#### Dessin
- **`void draw()`**
    - Trace un segment depuis le point de dessin, de direction et longueur identique au vecteur de dessin en utilisant la couleur et largeur de trait définies par `setColor()` et `setLineWidth()`. 
    - Cette fonction ne déplace pas le point de dessin (utiliser `move()` pour cela)
- **`void setColor(color color)`**
    - Définit la couleur du trait. La couleur doit se situer entre *0x000000* et *0xFFFFFF*, faute de quoi la couleur ne sera pas changée et un warning le fera savoir à l'utilisateur. 
    - La couleur persiste jusqu'au prochaine appel de `setcolor()`
- **`void setLineWidth(number)`**
    - Définit la largeur du trait en pixels.
#### Utilitaires
- **`number sin(number angleInRadian)`**
    - Retourne le sinus de l'angle donné.
- **`void log(number[, ...])`**
    - Affiche la/les variable(s) dans la console.

## Exemples
Plusieurs exemples sont disponibles dans le dossier `dscript/examples`.

###### tags: `HE-Arc` `Compilateur`