# Compilateurs - _DesSine_
###### tags: `HE-Arc` `Compilateur`
### Exemple de compilation

A point and a vector are always defined

```javascript
// Set default values, must be defined first
#size(120, 200)    // window size
#size(100, 100)

// Methods
// rotate(rads) - Rotate vector by rads
// scale(coeff) - Scale vector by coeff
// move() - Move current point by vector
// draw() - Draw line from point to point + vect
// setColor(int) - Color converted to hexadecimal 
// sin() - Computer sinus and returns it

// Structures
// assignation : variable = 23.0
// controle : for (init, test, cond) { ... }
// tests: if(test) {}

// Operations
// * + - / %

// Exemple

gray = 0x202020
black = 0x000000

for(i = 0; i < 360; i = i + 1) {
    draw()
    
    // We support comments
    if(i > 180) {
        setColor(gray)
    }
    else {
        setColor(black)
    }
    
    rotate(i * pi / 180)
    scale(1.1)
    move()
}

```

Résultat (très schématisé)
![](https://i.imgur.com/Dlm313O.png)
