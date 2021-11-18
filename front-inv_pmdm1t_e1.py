"""
Importamos todos los elementos para pygame para poder usarlos
Sys lo utilizaremos para hacer llamadas del sistema, os.path para rutas de archivos
y random para generar aleatorios
"""

from pygame import *
import sys
from os.path import abspath, dirname
from random import choice

"""
Definimos el directorio base como el directorio en el cual se encuentra el archivo principal
en este caso, este mismo archivo python, mientras el resto de rutas son relativas respecto
a este archivo (fuentes, imagenes y sonidos)
"""

BASE_PATH = abspath(dirname(__file__))
FONT_PATH = BASE_PATH + '/fonts/'
IMAGE_PATH = BASE_PATH + '/images/'
SOUND_PATH = BASE_PATH + '/sounds/'

"""
Definimos los colores que vamos a utilizar en nuestro codigo, principalmente
para rellenar de color tanto los invaders como la nave y otros elementos visuales.
Recordemos que van en clave RGB (Red, Green Blue)
"""

WHITE = (255, 255, 255)
GREEN = (78, 255, 87)
YELLOW = (241, 255, 0)
BLUE = (80, 255, 239)
PURPLE = (203, 0, 255)
RED = (237, 28, 36)

"""
Seguimos definiendo variables, en este caso lass dimensiones de la pantalla (800x600),
el archivo para las fuentes de texto, y un array de elementos de imagenes, con todos los
nombres de las imagenes que vamos a utilizar
"""

SCREEN = display.set_mode((800, 600))
FONT = FONT_PATH + 'space_invaders.ttf'
IMG_NAMES = ['ship', 'mystery',
             'enemy1_1', 'enemy1_2',
             'enemy2_1', 'enemy2_2',
             'enemy3_1', 'enemy3_2',
             'explosionblue', 'explosiongreen', 'explosionpurple',
             'laser', 'enemylaser']

"""
Inicializamos una variable de nombre IMAGES mediante compresion, es decir, vamos cargando los nombres
de las imagenes, definidas en el array de arriba, junto con su formato, .png, y utilizando el metodo convert
alpha para poder crear la transparencia de la imagen
"""

IMAGES = {name: image.load(IMAGE_PATH + '{}.png'.format(name)).convert_alpha()
          for name in IMG_NAMES}

"""
Por ultimo, creamos los tres elementos finales, los blockers, es decir, los escudos que dibujaremos en la 
parte inferior, justo por encima de nuestra nave, la posicion por defecto de los enemigos, en la parte
superior de la pantalla, y la cantidad de pixeles que van a ir bajando cada vez
"""

BLOCKERS_POSITION = 450
ENEMY_DEFAULT_POSITION = 65  # Initial value for a new game
ENEMY_MOVE_DOWN = 35

"""
Al igual que hicimos con el videojuego space invaders en JS, vamos a utilizar lenguaje POO para poder simplificar,
en la medida de lo posible, el diseño del videojuego y hacerlo que contenga la mayor parte de funcionalidad posible
"""

"""
Vamos a definir la clase de la nave, que contendra a su vez dos metodos, init y update.
"""

"""
Clase init, donde dado un objeto de la clase ship, procedemos a construirlo con unos parametros por
defecto.
El sprite que utilizaremos sera el de la imagen que le asignamos (ship), se dibujara en principio
como un rectangulo, que empieza en la posicion 375,540, es decir, la parte inferior de la pantalla
y se le asigna una velocidad inicial de 5
"""

class Ship(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = IMAGES['ship']
        self.rect = self.image.get_rect(topleft=(375, 540))
        self.speed = 5

        """
        Definimos ahora la funcion update, que recibe un objeto, una tecla y los argumentos.
        Dada una tecla que pulsemos de direccion (derecha o izquierda), cambiaremos la velocidad
        de la nave, en una cantidad dada y usaremos el metodo blit para re-dibujar el objeto en pantalla
        """

    def update(self, keys, *args):
        if keys[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 740:
            self.rect.x += self.speed
        game.screen.blit(self.image, self.rect)

"""
Definimos ahora la clase de las balas, que vamos a disparar con la nave, o las que pueden disparar
los invaders. De nuevo, definimos el constructor con el objeto, la posicion (x,y), la direccion, velocidad,
nombre del archivo y lado.
La imagen la obtendremos de nuestro array de imagenes definido al principio, y se le dibujara
como un rectangulo, que empieza desde la posicion superior izquierda (x,y), con una velocidad, direccion, lado
y nombre de archivo.

Lo hacemos de esta manera para poder distinguir entre las balas de los invaders y las de la nave, especialmente,
porque en cierto punto del game, vamos a utilizar power-ups para nuestra nave
"""

class Bullet(sprite.Sprite):
    def __init__(self, xpos, ypos, direction, speed, filename, side):
        sprite.Sprite.__init__(self)
        self.image = IMAGES[filename]
        self.rect = self.image.get_rect(topleft=(xpos, ypos))
        self.speed = speed
        self.direction = direction
        self.side = side
        self.filename = filename

        """
        Funcion de actualizar, donde redibujaremos la imagen y el rectangulo de la misma y se le asignara
        una altura en funcion de la velocidad y la direccion, esto se hace para que cuando los invaders vayan
        bajando de posicion para encontrarse mas cerca de la nave, no tengamos problemas a la hora de 
        actualizar las posiciones de las balas.
        
        Por ultimo, si la bala excede los limites de altura, es decir, desaparece por abajo o arriba del marco
        de la imagen, se destruye, para que no tenga efecto
        """

    def update(self, keys, *args):
        game.screen.blit(self.image, self.rect)
        self.rect.y += self.speed * self.direction
        if self.rect.y < 15 or self.rect.y > 600:
            self.kill()

"""
Ahora definimos la clase de los enemigos, tambien conocidos como invaders, que tendra varias funciones.
De nuevo empezamos con su constructor, esta vez con menos elementos, donde tendremos su objeto y la posicion
en la que se encuentra respecto a un array de elementos de invader, es decir, que posicion ocupa, respecto
a un numero de filas y de columnas y se le cargan las imagenes con un indice y su rectangulo correspondiente 
"""

class Enemy(sprite.Sprite):
    def __init__(self, row, column):
        sprite.Sprite.__init__(self)
        self.row = row
        self.column = column
        self.images = []
        self.load_images()
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        """
        Funcion toggle_image que define que imagen le corresponde al invader de arriba, viene determinado
        por un indice, y si nos salimos de indice del array, se le autoasigna la primera imagen por defecto
        """

    def toggle_image(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

        """
        Queremos que los invaders se vayan redibujando segun van cambiando de posicion, sea altura o valor de X
        """

    def update(self, *args):
        game.screen.blit(self.image, self.rect)

        """
        Queremos cargar las imagenes, como poder defecto vamos a tener 5 filas de invaders, vamos
        a asignarles a cada fila, dos imagenes distintas, que al final entre ambas van a simular el movimiento
        de los invaders cuando van subiendo/bajando o moviendose de forma lateral, para que parezcan que son
        sprite animados y los meteremos en dos variables, de nombre, img1 e img2 utilizando compresion, como
        explicamos en la parte de las variables.
        Por ultimo, una vez hecho todo, redimensionamos las imagenes para que tengan una escala de 40*35 pixeles
        """

    def load_images(self):
        images = {0: ['1_2', '1_1'],
                  1: ['2_2', '2_1'],
                  2: ['2_2', '2_1'],
                  3: ['3_1', '3_2'],
                  4: ['3_1', '3_2'],
                  }
        img1, img2 = (IMAGES['enemy{}'.format(img_num)] for img_num in
                      images[self.row])
        self.images.append(transform.scale(img1, (40, 35)))
        self.images.append(transform.scale(img2, (40, 35)))

"""
Clase que define un grupo de enemigos, donde una vez tenemos todos los enemigos, les asignaremos un grupo a
los mismos. 
Su constructor recive un objeto de tipo EnemiesGroup, filas y columnas.
Los enemigos recibe un array de valoresnulos, que vamos a ir inicializando, mediante el uso de una variable
implicita (_) que no recibe nombre y que actualizamos segun el rango de filas, y las columnas
Definimos al grupo como un movimiento de derecha/izquierda de 0/0, es decir, al principio, en el momento
que se inicializa el juego por primera vez, no estan en movimiento, hasta que se les asigna un tiempo de movimiento
de 600 ms, momento a partir del cual se le asigna una direccion de 1 (derecha), una velocidad de movimiento (30)
un numero de pixeles que se mueven (15), un timer, que hace que se vayan moviendo respecto al tiempo, una
parte inferior dependiendo de la altura a la que se encuentran y una lista de columnas.
"""

class EnemiesGroup(sprite.Group):
    def __init__(self, columns, rows):
        sprite.Group.__init__(self)
        self.enemies = [[None] * columns for _ in range(rows)]
        self.columns = columns
        self.rows = rows
        self.leftAddMove = 0
        self.rightAddMove = 0
        self.moveTime = 600
        self.direction = 1
        self.rightMoves = 30
        self.leftMoves = 30
        self.moveNumber = 15
        self.timer = time.get_ticks()
        self.bottom = game.enemyPosition + ((rows - 1) * 45) + 35
        self._aliveColumns = list(range(columns))
        self._leftAliveColumn = 0
        self._rightAliveColumn = columns - 1

        """
        Funcion que, dado el movimiento del grupo y un timer, si detecta que es hora de moverse, se le asigna
        movimiento lateral o arriba/abajo en funcion de si ha llegado al limite de derecha o abajo.
        En el momento en que direction = -1, en vez de moverse de izquierda a derecha, baja como grupo,
        y se mueve de forma inversa (derecha a izquierda).
        
        En el ultimo else, segun la posicion del movimiento en la que se encuentren, se le asignara
        una de las dos imagenes que tiene dicho sprite para ir haciendo simular el movimiento
        """

    def update(self, current_time):
        if current_time - self.timer > self.moveTime:
            if self.direction == 1:
                max_move = self.rightMoves + self.rightAddMove
            else:
                max_move = self.leftMoves + self.leftAddMove

            if self.moveNumber >= max_move:
                self.leftMoves = 30 + self.rightAddMove
                self.rightMoves = 30 + self.leftAddMove
                self.direction *= -1
                self.moveNumber = 0
                self.bottom = 0
                for enemy in self:
                    enemy.rect.y += ENEMY_MOVE_DOWN
                    enemy.toggle_image()
                    if self.bottom < enemy.rect.y + 35:
                        self.bottom = enemy.rect.y + 35
            else:
                velocity = 10 if self.direction == 1 else -10
                for enemy in self:
                    enemy.rect.x += velocity
                    enemy.toggle_image()
                self.moveNumber += 1

            self.timer += self.moveTime

    """
    Funcion para añadir invaders al grupo, y darle filas/columnas
    """

    def add_internal(self, *sprites):
        super(EnemiesGroup, self).add_internal(*sprites)
        for s in sprites:
            self.enemies[s.row][s.column] = s

    """
    Funcion para eliminar elemento del grupo, si muere dicho elemento, se elimina y se actualiza
    la velocidad de actualizacion de los elementos
    """

    def remove_internal(self, *sprites):
        super(EnemiesGroup, self).remove_internal(*sprites)
        for s in sprites:
            self.kill(s)
        self.update_speed()

        """
        Dada una columna de elementos de invaders, se comprueba si toda la columna esta muerta,
        para hacer que el resto de columnas puedan ocupar su posicion y que sirvan de colision
        al llegar a los extremos, en vez de tener una columna "invisible"
        """

    def is_column_dead(self, column):
        return not any(self.enemies[row][column]
                       for row in range(self.rows))

    """
    Funcion que, dado un elemento aleatorio de los invaders, devuelve el siguiente elemento
    de un iterador, dentro de la lista comprimida que tenemos dentro de las columnas de enemigos,
    mientras no sean null, si no, devuelve null. Esto se hace para evitar como dijimos antes tener columnas
    invisibles    
    """

    def random_bottom(self):
        col = choice(self._aliveColumns)
        col_enemies = (self.enemies[row - 1][col]
                       for row in range(self.rows, 0, -1))
        return next((en for en in col_enemies if en is not None), None)

    """
    Funcion que actualiza la velocidad de los invaders
    """

    def update_speed(self):
        if len(self) == 1:
            self.moveTime = 200
        elif len(self) <= 10:
            self.moveTime = 400

        """
        Funcion que, segun van muriendo los invaders, calcula la ultima columna que no esta viva
        mas cerca del limite para poder actualizar de forma correcta la posicion y la velocidad
        del grupo de invaders, y asi poder actualizar de forma correcta su posicion y todos los elementos
        respecto a su movimiento
        """

    def kill(self, enemy):
        self.enemies[enemy.row][enemy.column] = None
        is_column_dead = self.is_column_dead(enemy.column)
        if is_column_dead:
            self._aliveColumns.remove(enemy.column)

        if enemy.column == self._rightAliveColumn:
            while self._rightAliveColumn > 0 and is_column_dead:
                self._rightAliveColumn -= 1
                self.rightAddMove += 5
                is_column_dead = self.is_column_dead(self._rightAliveColumn)

        elif enemy.column == self._leftAliveColumn:
            while self._leftAliveColumn < self.columns and is_column_dead:
                self._leftAliveColumn += 1
                self.leftAddMove += 5
                is_column_dead = self.is_column_dead(self._leftAliveColumn)


"""
Definimos ahora la clase blocker, es decir, los 4 bloques que tenemos encima de la nave
que podremos usar como escudo.

Recibe un elemento de tipo blocker, un tamaño, color, fila y columna en la que se encuentra.
Se le da una altura, una anchura, una superficie, un color y una imagen.
"""

class Blocker(sprite.Sprite):
    def __init__(self, size, color, row, column):
        sprite.Sprite.__init__(self)
        self.height = size
        self.width = size
        self.color = color
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.column = column

        """
        Funcion que, segun va recibiendo disparos, va actualizandose en pantalla, para mostrar
        como va quedando
        """

    def update(self, keys, *args):
        game.screen.blit(self.image, self.rect)


"""
Definimos ahora la clase powerup, tambien llamada misterio, donde, en cierto momento, en la parte superior
de la pantalla, va a aparecer un invader rojo, que no dispara, pero que nos dara una serie de puntos 
aleatorios, entre dos valores, que hacen que se nos sumen puntos a nuestro marcador, esto lo vamos a hacer
para realizar un powerup mas adelante para nuestra nave, basado en la cantidad de puntos.

Lleva normalmente el mismo tipo de elementos que un invader normal, con la diferencia de que, una vez entra
en pantalla, se lanzara un sonido de un .wav que tenemos en la carpeta de sonidos
"""

class Mystery(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = IMAGES['mystery']
        self.image = transform.scale(self.image, (75, 35))
        self.rect = self.image.get_rect(topleft=(-80, 45))
        self.row = 5
        self.moveTime = 25000
        self.direction = 1
        self.timer = time.get_ticks()
        self.mysteryEntered = mixer.Sound(SOUND_PATH + 'mysteryentered.wav')
        self.mysteryEntered.set_volume(0.3)
        self.playSound = True

        """
        Funcion que actualiza su posicion. Si esta dentro del terreno de juego por primera vez,
        se ejecuta el sonido que definimos arriba, si sale de la pantalla por la derecha o la izquierda,
        en poco tiempo desaparece de la misma
        """

    def update(self, keys, currentTime, *args):
        resetTimer = False
        passed = currentTime - self.timer
        if passed > self.moveTime:
            if (self.rect.x < 0 or self.rect.x > 800) and self.playSound:
                self.mysteryEntered.play()
                self.playSound = False
            if self.rect.x < 840 and self.direction == 1:
                self.mysteryEntered.fadeout(4000)
                self.rect.x += 2
                game.screen.blit(self.image, self.rect)
            if self.rect.x > -100 and self.direction == -1:
                self.mysteryEntered.fadeout(4000)
                self.rect.x -= 2
                game.screen.blit(self.image, self.rect)

        if self.rect.x > 830:
            self.playSound = True
            self.direction = -1
            resetTimer = True
        if self.rect.x < -90:
            self.playSound = True
            self.direction = 1
            resetTimer = True
        if passed > self.moveTime and resetTimer:
            self.timer = currentTime

"""
Definimos la clase enemi explosion, que tiene como explicamos antes dos imagenes, ahora una de las mismas
tiene un tamaño un pelin mayor a la otra, para simular movimiento mientras van moviendose de forma lateral

"""

class EnemyExplosion(sprite.Sprite):
    def __init__(self, enemy, *groups):
        super(EnemyExplosion, self).__init__(*groups)
        self.image = transform.scale(self.get_image(enemy.row), (40, 35))
        self.image2 = transform.scale(self.get_image(enemy.row), (50, 45))
        self.rect = self.image.get_rect(topleft=(enemy.rect.x, enemy.rect.y))
        self.timer = time.get_ticks()

    """
    Definimos un metodo estatico, para poder asignar distintos colores a los invaders,
    la fila superior sera de color purpura, las dos centrales de color azul y las dos inferiores de color verde
    """

    @staticmethod
    def get_image(row):
        img_colors = ['purple', 'blue', 'blue', 'green', 'green']
        return IMAGES['explosion{}'.format(img_colors[row])]

    """
    Funcion que actualiza las explosiones, segun la posicion de los elementos, tanto su x como su y
    """

    def update(self, current_time, *args):
        passed = current_time - self.timer
        if passed <= 100:
            game.screen.blit(self.image, self.rect)
        elif passed <= 200:
            game.screen.blit(self.image2, (self.rect.x - 6, self.rect.y - 6))
        elif 400 < passed:
            self.kill()


"""
Clase la explosion del misterior, donde al principio, una vez el misterio explota, saldra en blanco
con fuente de 20, una cantidad de puntos en pantalla que hemos obtenido y se actualizan los elementos
correspondientes
"""

class MysteryExplosion(sprite.Sprite):
    def __init__(self, mystery, score, *groups):
        super(MysteryExplosion, self).__init__(*groups)
        self.text = Text(FONT, 20, str(score), WHITE,
                         mystery.rect.x + 20, mystery.rect.y + 6)
        self.timer = time.get_ticks()

    def update(self, current_time, *args):
        passed = current_time - self.timer
        if passed <= 200 or 400 < passed <= 600:
            self.text.draw(game.screen)
        elif 600 < passed:
            self.kill()

"""
De igual forma que tenemos que controlar las explosiones de los enemigos, tenemos que controlar las explosiones
de la nave que manejara el jugador, donde, en caso de morir, tenemos que volver a repintar la misma y actualizarla
de forma correcta
"""

class ShipExplosion(sprite.Sprite):
    def __init__(self, ship, *groups):
        super(ShipExplosion, self).__init__(*groups)
        self.image = IMAGES['ship']
        self.rect = self.image.get_rect(topleft=(ship.rect.x, ship.rect.y))
        self.timer = time.get_ticks()

    def update(self, current_time, *args):
        passed = current_time - self.timer
        if 300 < passed <= 600:
            game.screen.blit(self.image, self.rect)
        elif 900 < passed:
            self.kill()

"""
Funcion que define la imagen de la nave viva y la escala de la misma (23x23) y la funcion actualiza correspondiente 
"""

class Life(sprite.Sprite):
    def __init__(self, xpos, ypos):
        sprite.Sprite.__init__(self)
        self.image = IMAGES['ship']
        self.image = transform.scale(self.image, (23, 23))
        self.rect = self.image.get_rect(topleft=(xpos, ypos))

    def update(self, *args):
        game.screen.blit(self.image, self.rect)

"""
Funcion que, dado un objeto de Texto, le añade una fuente, un mensaje, tamaño, color y posicion (x,y)
para poder dibujarlo en la pantalla cuando sea necesario, esto lo usaremos tanto para los puntos que nos dan
los invaders al morir, como el misterio, como los textos de vidas y puntuacion y la funcion draw correspondiente,
para dibujarlo en pantalla
"""

class Text(object):
    def __init__(self, textFont, size, message, color, xpos, ypos):
        self.font = font.Font(textFont, size)
        self.surface = self.font.render(message, True, color)
        self.rect = self.surface.get_rect(topleft=(xpos, ypos))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

"""
Clase spaceinvaders, donde el primer elemento que tenemos, es la inicializacion de un buffer de sonido.
Aunque en Windows normalmente con un buffer de 1024 vamos bien, en Linux, hay veces que si el buffer no es 
superior a dicho tamaño, podemos obtener un error, es por ello que lo hacemos lo suficientemente grande, para que
no de fallo.
de mixer.pre_init los elementos son los siguientes (frecuencia, tamaño, canales, tamaño de buffer)
Mostramos un caption (titulo de la ventana), dibujamos el fondo e inicializamos una serie de elementos
de la ventana, tales como textos.
"""

class SpaceInvaders(object):
    def __init__(self):
        mixer.pre_init(44100, -16, 1, 4096)
        init()
        self.clock = time.Clock()
        self.caption = display.set_caption('Jugando a Front Invaders')
        self.screen = SCREEN
        self.background = image.load(IMAGE_PATH + 'background.jpg').convert()
        self.startGame = False
        self.mainScreen = True
        self.gameOver = False
        # Counter for enemy starting position (increased each new round)
        self.enemyPosition = ENEMY_DEFAULT_POSITION
        self.titleText = Text(FONT, 50, 'Front Invaders', WHITE, 164, 155)
        self.titleText2 = Text(FONT, 25, 'Presiona una tecla para continuar', WHITE,
                               130, 225)
        self.gameOverText = Text(FONT, 50, 'Se acabo', WHITE, 250, 270)
        self.nextRoundText = Text(FONT, 50, 'Siguiente ronda', WHITE, 170, 270)
        self.enemy1Text = Text(FONT, 25, '   =   10 puntos', GREEN, 368, 270)
        self.enemy2Text = Text(FONT, 25, '   =  20 puntos', BLUE, 368, 320)
        self.enemy3Text = Text(FONT, 25, '   =  30 puntos', PURPLE, 368, 370)
        self.enemy4Text = Text(FONT, 25, '   =  ????? puntos', RED, 368, 420)
        self.scoreText = Text(FONT, 20, 'Puntuacion', WHITE, 5, 5)
        self.livesText = Text(FONT, 20, 'Vidas ', WHITE, 640, 5)

        self.life1 = Life(715, 3)
        self.life2 = Life(742, 3)
        self.life3 = Life(769, 3)
        self.livesGroup = sprite.Group(self.life1, self.life2, self.life3)

        """
        Funcion que, llegado un momento podemos utilizar para resetear todos los elementos de la pantalla.
        Por ejemplo, podemos usarla para cuando nos hacen daño en la nave y tenemos que restar una vida, volviendo
        a sacar la nave por pantalla, mientras guardamos el estado actual del resto de elemtnos en la pantalla
        """

    def reset(self, score):
        self.player = Ship()
        self.playerGroup = sprite.Group(self.player)
        self.explosionsGroup = sprite.Group()
        self.bullets = sprite.Group()
        self.mysteryShip = Mystery()
        self.mysteryGroup = sprite.Group(self.mysteryShip)
        self.enemyBullets = sprite.Group()
        self.make_enemies()
        self.allSprites = sprite.Group(self.player, self.enemies,
                                       self.livesGroup, self.mysteryShip)
        self.keys = key.get_pressed()

        self.timer = time.get_ticks()
        self.noteTimer = time.get_ticks()
        self.shipTimer = time.get_ticks()
        self.score = score
        self.create_audio()
        self.makeNewShip = False
        self.shipAlive = True

        """
        Hacemos ahora los escudos blockers, de 4 filas y 9 columans en principio, con lo cual ajustamos
        sus tamaños y posiciones de forma correcta y le asignamos el color verde
        """

    def make_blockers(self, number):
        blockerGroup = sprite.Group()
        for row in range(4):
            for column in range(9):
                blocker = Blocker(10, GREEN, row, column)
                blocker.rect.x = 50 + (200 * number) + (column * blocker.width)
                blocker.rect.y = BLOCKERS_POSITION + (row * blocker.height)
                blockerGroup.add(blocker)
        return blockerGroup

    """
    Creamos los sonidos, que iremos usando a lo largo del videojuego, le damos un volumen por defecto
    y actuamos sobre el mixer necesario 
    """

    def create_audio(self):
        self.sounds = {}
        for sound_name in ['shoot', 'shoot2', 'invaderkilled', 'mysterykilled',
                           'shipexplosion']:
            self.sounds[sound_name] = mixer.Sound(
                SOUND_PATH + '{}.wav'.format(sound_name))
            self.sounds[sound_name].set_volume(0.2)

        self.musicNotes = [mixer.Sound(SOUND_PATH + '{}.wav'.format(i)) for i
                           in range(4)]
        for sound in self.musicNotes:
            sound.set_volume(0.5)

        self.noteIndex = 0

        """
        Cuando llegue el momento oportuno, tal como una explosion de un invader, ejecutaremos
        el sonido correspondiente
        """

    def play_main_music(self, currentTime):
        if currentTime - self.noteTimer > self.enemies.moveTime:
            self.note = self.musicNotes[self.noteIndex]
            if self.noteIndex < 3:
                self.noteIndex += 1
            else:
                self.noteIndex = 0

            self.note.play()
            self.noteTimer += self.enemies.moveTime

    """
    Definimos un metodo estatico para cerrar el videojuego cuando asi lo ordenemos a la pantalla, dandole
    al icono de cerrar la misma
    """

    @staticmethod
    def should_exit(evt):
        # type: (pygame.event.EventType) -> bool
        return evt.type == QUIT or (evt.type == KEYUP and evt.key == K_ESCAPE)

    """
    Controlamos si el usuario presiona alguna tecla, en este caso la de disparo. 
    Si se presiona espacio, la nave debe disparar, siempre y cuando la puntuacion sea menor a 1000
    En caso de tener mas de 1000 puntos, usamos un powerup para disparar dos balas en vez de una, diferenciando
    la bala que va en la parte izquierda y la que va en la parte derecha
    """

    def check_input(self):
        self.keys = key.get_pressed()
        for e in event.get():
            if self.should_exit(e):
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if len(self.bullets) == 0 and self.shipAlive:
                        if self.score < 1000:
                            bullet = Bullet(self.player.rect.x + 23,
                                            self.player.rect.y + 5, -1,
                                            15, 'laser', 'center')
                            self.bullets.add(bullet)
                            self.allSprites.add(self.bullets)
                            self.sounds['shoot'].play()
                        else:
                            leftbullet = Bullet(self.player.rect.x + 8,
                                                self.player.rect.y + 5, -1,
                                                15, 'laser', 'left')
                            rightbullet = Bullet(self.player.rect.x + 38,
                                                 self.player.rect.y + 5, -1,
                                                 15, 'laser', 'right')
                            self.bullets.add(leftbullet)
                            self.bullets.add(rightbullet)
                            self.allSprites.add(self.bullets)
                            self.sounds['shoot2'].play()


    """
    Dibujamos los enemigos en la pantalla, segun un grupo de filas y columnas, en nuestro caso 5 filas y 10
    columnas
    """

    def make_enemies(self):
        enemies = EnemiesGroup(10, 5)
        for row in range(5):
            for column in range(10):
                enemy = Enemy(row, column)
                enemy.rect.x = 157 + (column * 50)
                enemy.rect.y = self.enemyPosition + (row * 45)
                enemies.add(enemy)

        self.enemies = enemies

    """
    Funcion que, hace a los enemigos invaders tambien dispararnos dado un timer, para poder intentar destruir
    nuestra nave.
    """

    def make_enemies_shoot(self):
        if (time.get_ticks() - self.timer) > 700 and self.enemies:
            enemy = self.enemies.random_bottom()
            self.enemyBullets.add(
                Bullet(enemy.rect.x + 14, enemy.rect.y + 20, 1, 5,
                       'enemylaser', 'center'))
            self.allSprites.add(self.enemyBullets)
            self.timer = time.get_ticks()

    """
    Calculamos la puntuacion segun el tipo de enemigo que matemos, dependiendo del color se le asigna
    un valor u otro al invader, a mas arriba se encuentre, mas punto daran, con la excepcion del misterio,
    que tendra un valor aleatorio de 50,100,150 o 300
    """

    def calculate_score(self, row):
        scores = {0: 30,
                  1: 20,
                  2: 20,
                  3: 10,
                  4: 10,
                  5: choice([50, 100, 150, 300])
                  }

        score = scores[row]
        self.score += score
        return score

    """
    Creamos el menu principal, donde tendremos los 4 tipos de enemigos que nos vamos a encontrar
    y luego le asignamos mediante texto su valor en puntos
    """

    def create_main_menu(self):
        self.enemy1 = IMAGES['enemy3_1']
        self.enemy1 = transform.scale(self.enemy1, (40, 40))
        self.enemy2 = IMAGES['enemy2_2']
        self.enemy2 = transform.scale(self.enemy2, (40, 40))
        self.enemy3 = IMAGES['enemy1_2']
        self.enemy3 = transform.scale(self.enemy3, (40, 40))
        self.enemy4 = IMAGES['mystery']
        self.enemy4 = transform.scale(self.enemy4, (80, 40))
        self.screen.blit(self.enemy1, (318, 270))
        self.screen.blit(self.enemy2, (318, 320))
        self.screen.blit(self.enemy3, (318, 370))
        self.screen.blit(self.enemy4, (299, 420))

        """
        Funcion para comprobar las colisiones, tanto de nuestras balas con los invaders, como de las balas
        de los invaders con nuestra nave, asi como cualquier elemento con los borders superior/inferior
        de la pantalla
        """

    def check_collisions(self):
        sprite.groupcollide(self.bullets, self.enemyBullets, True, True)

        for enemy in sprite.groupcollide(self.enemies, self.bullets,
                                         True, True).keys():
            self.sounds['invaderkilled'].play()
            self.calculate_score(enemy.row)
            EnemyExplosion(enemy, self.explosionsGroup)
            self.gameTimer = time.get_ticks()

        for mystery in sprite.groupcollide(self.mysteryGroup, self.bullets,
                                           True, True).keys():
            mystery.mysteryEntered.stop()
            self.sounds['mysterykilled'].play()
            score = self.calculate_score(mystery.row)
            MysteryExplosion(mystery, score, self.explosionsGroup)
            newShip = Mystery()
            self.allSprites.add(newShip)
            self.mysteryGroup.add(newShip)

        for player in sprite.groupcollide(self.playerGroup, self.enemyBullets,
                                          True, True).keys():
            if self.life3.alive():
                self.life3.kill()
            elif self.life2.alive():
                self.life2.kill()
            elif self.life1.alive():
                self.life1.kill()
            else:
                self.gameOver = True
                self.startGame = False
            self.sounds['shipexplosion'].play()
            ShipExplosion(player, self.explosionsGroup)
            self.makeNewShip = True
            self.shipTimer = time.get_ticks()
            self.shipAlive = False

        if self.enemies.bottom >= 540:
            sprite.groupcollide(self.enemies, self.playerGroup, True, True)
            if not self.player.alive() or self.enemies.bottom >= 600:
                self.gameOver = True
                self.startGame = False

        sprite.groupcollide(self.bullets, self.allBlockers, True, True)
        sprite.groupcollide(self.enemyBullets, self.allBlockers, True, True)
        if self.enemies.bottom >= BLOCKERS_POSITION:
            sprite.groupcollide(self.enemies, self.allBlockers, False, True)


        """
        Si ha habido una colision con nuestra nave, debemos de dibujar otra, en este caso en el centro de 
        la fila para dicha nave
        """

    def create_new_ship(self, createShip, currentTime):
        if createShip and (currentTime - self.shipTimer > 900):
            self.player = Ship()
            self.allSprites.add(self.player)
            self.playerGroup.add(self.player)
            self.makeNewShip = False
            self.shipAlive = True


        """
        Funcion de fin de juego, una vez las naves tienen sus vidas a 0, si reciben otra colision, sale
        del juego y pierdes
        """

    def create_game_over(self, currentTime):
        self.screen.blit(self.background, (0, 0))
        passed = currentTime - self.timer
        if passed < 750:
            self.gameOverText.draw(self.screen)
        elif 750 < passed < 1500:
            self.screen.blit(self.background, (0, 0))
        elif 1500 < passed < 2250:
            self.gameOverText.draw(self.screen)
        elif 2250 < passed < 2750:
            self.screen.blit(self.background, (0, 0))
        elif passed > 3000:
            self.mainScreen = True

        for e in event.get():
            if self.should_exit(e):
                sys.exit()


        """
        Ahora si, estamos listos para comenzar el juego, entonces, a menos que el estado del juego sea,
        la salida forzosa, va a ir pintando en pantalla todos los elemenetos poco a poco, hasta que esten
        todos correctos, el usuario le de a una tecla, y comience todo a moverse en el videojuego
        """

    def main(self):
        while True:
            # Dibujamos los enemigos
            if self.mainScreen:
                self.screen.blit(self.background, (0, 0))
                self.titleText.draw(self.screen)
                self.titleText2.draw(self.screen)
                self.enemy1Text.draw(self.screen)
                self.enemy2Text.draw(self.screen)
                self.enemy3Text.draw(self.screen)
                self.enemy4Text.draw(self.screen)
                self.create_main_menu()
                for e in event.get():
                    if self.should_exit(e):
                        sys.exit()
                    if e.type == KEYUP:
                        # Solo se crean los escudos en un nuevo juego, no una nueva ronda
                        self.allBlockers = sprite.Group(self.make_blockers(0),
                                                        self.make_blockers(1),
                                                        self.make_blockers(2),
                                                        self.make_blockers(3))
                        self.livesGroup.add(self.life1, self.life2, self.life3)
                        self.reset(0)
                        self.startGame = True
                        self.mainScreen = False

            # Si comienza la partida, actualiza los textos de score, etc
            elif self.startGame:
                if not self.enemies and not self.explosionsGroup:
                    currentTime = time.get_ticks()
                    if currentTime - self.gameTimer < 3000:
                        self.screen.blit(self.background, (0, 0))
                        # Score text
                        self.scoreText2 = Text(FONT, 20, str(self.score),
                                               GREEN, 180, 5)
                        self.scoreText.draw(self.screen)
                        self.scoreText2.draw(self.screen)
                        self.nextRoundText.draw(self.screen)
                        self.livesText.draw(self.screen)
                        self.livesGroup.update()
                        self.check_input()
                    if currentTime - self.gameTimer > 3000:
                        # Move enemies closer to bottom
                        self.enemyPosition += ENEMY_MOVE_DOWN
                        self.reset(self.score)
                        self.gameTimer += 3000
                else:
                    currentTime = time.get_ticks()
                    self.play_main_music(currentTime)
                    self.screen.blit(self.background, (0, 0))
                    self.allBlockers.update(self.screen)

                    # Score text
                    self.scoreText2 = Text(FONT, 20, str(self.score), GREEN,
                                           180, 5)
                    self.scoreText.draw(self.screen)
                    self.scoreText2.draw(self.screen)
                    self.livesText.draw(self.screen)
                    self.check_input()
                    self.enemies.update(currentTime)
                    self.allSprites.update(self.keys, currentTime)
                    self.explosionsGroup.update(currentTime)
                    self.check_collisions()
                    self.create_new_ship(self.makeNewShip, currentTime)
                    self.make_enemies_shoot()

            elif self.gameOver:
                currentTime = time.get_ticks()
                # Reset enemy starting position
                self.enemyPosition = ENEMY_DEFAULT_POSITION
                self.create_game_over(currentTime)
            # Actualizamos la ventana a 60 fps
            display.update()
            self.clock.tick(60)

# Una vez definidos todos los elementos, que comience el juego llamando a spaceinvaders y a main

if __name__ == '__main__':
    game = SpaceInvaders()
    game.main()
