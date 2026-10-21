"""Episodio 146 · De la mano de los robots — escenas animadas."""
import math, random, sys
sys.path.insert(0, '/home/claude/anim')
from engine import *
from lib import *
import sample as S

CAP_Y = 100
def cap(p, words, lt, delay=0.4, size=48, y=CAP_Y): caption(p, words, lt - delay, 80, y, size)

# ---------------------------------------------------------------- apertura
def title(p, lt, t, d):
    # dos manos que se acercan: humana y robótica
    k = ease((lt - 1) / 5)
    hand(p, 300 + 220 * k, 420, 1.3, 1, INK, 1.0)
    c = p.c; c.save(); c.translate(980 - 220 * k, 420); c.scale(-1, 1)
    p.rect(-60, -35, 70, 70, TEAL, 5, 1, r=10, fill=BG)
    for fy in (-24, 0, 24): p.poly([(10, fy), (48, fy), (72, fy + 8)], TEAL, 9)
    p.poly([(-20, -35), (0, -60), (24, -66)], TEAL, 9)
    c.restore()
    if lt > 6:
        for i in range(8):
            r = (lt - 6) * 60 + i * 6
            p.arc(640, 420, 20 + ((lt - 6) * 50 + i * 30) % 160, 0, 2 * math.pi, TEAL, 2, max(0, 0.5 - ((lt - 6) * 50 + i * 30) % 160 / 320))
    mono(p, 'CARNE DE BIT · EPISODIO 146', 640, 170, 24, TEAL, appear(lt, 0.5), 'center')
    p.text('De la mano de los robots', 640, 245, 64, INK, appear(lt, 1.0), 'bold', 'center')
    p.text('Emilio Sáez Soro conversa con Enric Cervera', 640, 620, 28, DIM, appear(lt, 2.0), 'normal', 'center')

def name_tag(name, role):
    def f(p, lt, t, d):
        k = appear(lt, 0, 0.6)
        w = max(len(name) * 19, len(role) * 11) + 70
        p.rect(60, 590, w, 90, INK, 0, k, r=6, fill=(0.03, 0.06, 0.07), fa=0.9 * k)
        p.rect(60, 590, 7, 90, TEAL, 0, k, r=2, fill=TEAL, fa=k)
        p.text(name, 88, 628, 32, INK, k); p.text(role, 88, 662, 20, DIM, k, 'normal')
    return f

def presentacion(p, lt, t, d):
    # laboratorio: brazo robótico ordenando piezas sobre una mesa
    ph = lt * 0.6
    a1 = 0.5 * math.sin(ph); a2 = 0.9 + 0.4 * math.sin(ph * 1.3); a3 = 0.4 * math.sin(ph * 0.7)
    robot_arm(p, 400, 560, a1, a2, a3, 1.0, 1, 0.5 + 0.5 * math.sin(ph * 2))
    ground(p, 560, 150, 1130)
    for i, col in enumerate((TEAL, AMBER, RED, TEAL, AMBER)):
        p.rect(640 + i * 90, 520, 56, 40, col, 4, 1, r=6, fill=BG)
    mono(p, 'LABORATORIO DE ROBÓTICA INTELIGENTE · UJI', 640, 170, 20, DIM, appear(lt, 1), 'center')
    cap(p, ['Grado', 'en', 'INTELIGENCIA', 'ROBÓTICA'], lt)

def ia_con_cuerpo(p, lt, t, d):
    # 1) burbuja de chat  2) se convierte en robot  3) ciclo percibir-aprender-actuar
    if lt < 14:
        k = appear(lt, 0.5)
        bubble(p, 440, 220, 400, 170, k)
        dots(p, 610, 315, lt, INK, k)
        cap(p, ['La', 'IA', 'puede', 'CONVERSAR…'], lt)
    elif lt < 30:
        k = ease((lt - 14) / 2.5)
        bubble(p, 440, 220, 400, 170, 1 - k)
        robot(p, 640, 600, 0.6 + 0.4 * k, dict(shR=0.15 + 2.4 * ease((lt - 17) / 1.5) * (1 if lt < 24 else 0.0) + 0.35 * math.sin(lt * 5) * (1 if 17 < lt < 24 else 0)), k)
        cap(p, ['…y', 'ahora', 'tiene', 'CUERPO'], lt - 14)
    else:
        lt2 = lt - 30
        labels = [('PERCIBIR', 'eye'), ('APRENDER', 'brain'), ('ACTUAR', 'handi')]
        cx, cy, R = 640, 370, 190
        for i, (lab, ic) in enumerate(labels):
            ang = -math.pi / 2 + i * 2 * math.pi / 3
            x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
            k = appear(lt2, i * 0.8)
            p.circle(x, y, 62, TEAL, 5, k, fill=BG, fa=k)
            draw_icon(p, ic, x, y, k)
            p.text(lab, x, y + 100, 26, INK, k, 'bold', 'center')
            a1 = ang + 0.5; a2 = ang + 2 * math.pi / 3 - 0.5
            p.arc(cx, cy, R, a1, a1 + (a2 - a1) * appear(lt2, i * 0.8 + 0.5, 0.8), DIM, 4, k)
        orb = (lt2 * 0.6) % (2 * math.pi)
        p.circle(cx + R * math.cos(orb - math.pi / 2), cy + R * math.sin(orb - math.pi / 2), 9, AMBER, 0, appear(lt2, 3), fill=AMBER)
        robot(p, cx, cy + 80, 0.32)

def draw_icon(p, ic, x, y, a=1.0):
    if ic == 'eye':
        p.c.save(); p.c.translate(x, y); p.c.scale(1, 0.55); p.circle(0, 0, 34, INK, 5, a); p.c.restore()
        p.circle(x, y, 11, TEAL, 0, a, fill=TEAL, fa=a)
    elif ic == 'brain':
        for dx in (-12, 12): p.circle(x + dx, y - 6, 18, INK, 5, a)
        p.circle(x, y + 12, 18, INK, 5, a)
    elif ic == 'handi':
        hand(p, x + 8, y, 0.45, a, INK, 0.3)

# ---------------------------------------------------------------- spectrum
def spectrum(p, lt, t, d):
    if lt < 38:
        # ordenador de los 80 con franjas de colores y BASIC
        x, y = 360, 230
        p.rect(x, y, 560, 300, INK, 5, 1, r=16, fill=(0.07, 0.07, 0.08))
        for i, col in enumerate((RED, AMBER, (0.95, 0.85, 0.35), TEAL)):
            p.poly([(x + 420 + i * 22, y + 300), (x + 470 + i * 22, y + 250)], col, 10)
        p.rect(x + 40, y + 40, 360, 200, DIM, 3, 1, r=8, fill=(0.05, 0.12, 0.13))
        lines = ['10 PRINT "HOLA"', '20 GOTO 10', 'RUN']
        n = int(lt * 6)
        yy = y + 85
        for ln in lines:
            s = ln[:max(0, n)]; n -= len(ln) + 3
            mono(p, s, x + 60, yy, 24, TEAL); yy += 40
        if lt > 5 and int(lt * 2) % 2: p.rect(x + 60 + 0, yy - 22, 14, 26, TEAL, 0, 1, r=0, fill=TEAL)
        for i in range(10): p.rect(x + 30 + i * 50, y + 320, 40, 26, DIM, 3, 1, r=4)
        mono(p, '1985', 1080, 300, 60, AMBER, appear(lt, 1))
        cap(p, ['Todo', 'empezó', 'con', 'un', 'SPECTRUM'], lt)
    else:
        lt2 = lt - 38
        # carrete de película con robot de ciencia ficción
        for i in range(3):
            x = 240 + i * 280 - (lt2 * 40) % 280
            p.rect(x, 220, 240, 300, INK, 4, 1, r=6, fill=(0.07, 0.07, 0.08))
            for j in range(6):
                p.rect(x + 10, 232 + j * 48, 18, 26, DIM, 0, 1, r=3, fill=DIM); p.rect(x + 212, 232 + j * 48, 18, 26, DIM, 0, 1, r=3, fill=DIM)
            robot(p, x + 120, 480, 0.6, dict(shR=0.9 + 0.3 * math.sin(lt2 * 3 + i)), 1, AMBER)
        mono(p, '30 AÑOS INVESTIGANDO', 640, 620, 24, DIM, appear(lt2, 1.5), 'center')
        cap(p, ['…y', 'con', 'la', 'CIENCIA', 'FICCIÓN'], lt2)

# ---------------------------------------------------------------- grado pionero
def grado(p, lt, t, d):
    if lt < 50:
        # equipo de profesores construye el grado con bloques
        names = ['INFORMÁTICA', 'INGENIERÍA', 'MATEMÁTICAS', 'ROBÓTICA']
        for i, n in enumerate(names):
            k = appear(lt, 2 + i * 2.5, 0.8)
            y = 520 - i * 70 - (1 - k) * 200
            p.rect(470, y, 340, 60, [TEAL, AMBER, INK, TEAL][i], 4, k, r=8, fill=BG, fa=k)
            p.text(n, 640, y + 40, 24, INK, k, 'bold', 'center')
        for i, x in enumerate((220, 320, 960, 1060)):
            person(p, x, 580, 0.8, dict(shR=0.4 + 0.5 * math.sin(lt * 2 + i) if i < 2 else 0.25, shL=-0.25 if i < 2 else -0.4 - 0.5 * math.sin(lt * 2 + i)))
        ground(p, 580, 140, 1140)
        cap(p, ['Un', 'EQUIPO', 'que', 'monta', 'un', 'grado', 'PIONERO'], lt)
    else:
        lt2 = lt - 50
        # 2017 → hoy: primera etapa del podcast, IA antes de la explosión de los LLM
        p.line(160, 380, 1120, 380, DIM, 4)
        for i, (yr, lab) in enumerate([('ANTES', 'Primera etapa\ndel podcast'), ('2022', 'Llegan los\nmodelos de lenguaje'), ('HOY', 'Impacto\nbrutal')]):
            x = 260 + i * 380; k = appear(lt2, 1 + i * 2)
            p.circle(x, 380, 14, TEAL if i < 2 else AMBER, 0, k, fill=TEAL if i < 2 else AMBER, fa=k)
            mono(p, yr, x, 340, 30, INK, k, 'center')
            for j, ln in enumerate(lab.split('\n')): p.text(ln, x, 440 + j * 30, 24, DIM, k, 'normal', 'center')
        cap(p, ['Antes', 'de', 'la', 'EXPLOSIÓN', 'de', 'la', 'IA'], lt2)

# ---------------------------------------------------------------- IA y juegos
def ia_juegos(p, lt, t, d):
    if lt < 35:
        # crecimiento: expectativas y fracasos — curva con altibajos
        pts = []
        for i in range(0, 121):
            x = 160 + i * 8; u = i / 120
            y = 520 - (60 * math.sin(u * 9) * (1 - u) + 30 + 360 * u ** 4)
            pts.append((x, y))
        n = int(len(pts) * clamp01(lt / 14))
        if n > 1: p.poly(pts[:n], TEAL, 5)
        for x, lab in ((200, '1956'), (560, '1997'), (900, '2016'), (1110, '2026')):
            mono(p, lab, x, 570, 22, DIM, appear(lt, 1), 'center')
        p.line(160, 540, 1130, 540, DIM, 3)
        cap(p, ['La', 'IA', 'tiene', 'más', 'de', '50', 'AÑOS'], lt)
    else:
        lt2 = lt - 35
        # tablero de ajedrez y Go: la máquina gana
        ox, oy, cs = 300, 180, 50
        for i in range(8):
            for j in range(8):
                if (i + j) % 2: p.rect(ox + i * cs, oy + j * cs, cs, cs, INK, 0, 1, r=0, fill=GRID)
        p.rect(ox, oy, cs * 8, cs * 8, INK, 4, 1, r=2)
        kx = ox + 3.5 * cs + 3 * cs * ease((lt2 - 3) / 2) * 0
        fall = ease((lt2 - 6) / 1.2)
        p.c.save(); p.c.translate(ox + 4.5 * cs, oy + 6.9 * cs); p.c.rotate(fall * 1.4)
        p.poly([(-14, 0), (14, 0), (8, -40), (0, -52), (-8, -40)], INK, 4, 1, True, fill=BG); p.line(-8, -60, 8, -60, INK, 4); p.line(0, -68, 0, -52, INK, 4)
        p.c.restore()
        robot(p, 880, 600, 0.75, dict(shR=2.4 if lt2 > 7 else 0.2, elR=0.2))
        mono(p, 'KASPAROV vs DEEP BLUE · 1997', 500, 640, 22, DIM, appear(lt2, 1), 'center')
        if lt2 > 25:
            p.text('Los robots aún se están adaptando', 640, 680, 26, AMBER, appear(lt2, 25), 'normal', 'center')
        cap(p, ['Los', 'ordenadores', 'ganan', 'al', 'AJEDREZ', 'y', 'al', 'GO'], lt2)

# ---------------------------------------------------------------- donde trabajan
def almacen(p, lt, t, d):
    # estanterías y robot de ruedas que lleva cajas
    for sx in (150, 470, 790):
        p.rect(sx, 230, 260, 280, DIM, 4, 1, r=4)
        for k in range(3):
            p.line(sx, 320 + k * 95, sx + 260, 320 + k * 95, DIM, 4)
            for b in range(3): box(p, sx + 50 + b * 80, 318 + k * 95, 56, 44, AMBER, 0.85)
    ground(p, 600)
    x = (lt * 160) % 1500 - 150
    wheel_robot(p, x, 600, 1.0, 1, lt * 8)
    box(p, x, 510, 80, 60, AMBER)
    cap(p, ['LOGÍSTICA', 'y', 'almacenes'], lt)

def hospital(p, lt, t, d):
    # pasillo de hospital, robot asistente con bandeja
    p.rect(130, 190, 220, 330, DIM, 4, 1, r=8)
    p.rect(215, 250, 50, 140, RED, 0, 1, r=4, fill=RED); p.rect(170, 295, 140, 50, RED, 0, 1, r=4, fill=RED)
    for i in range(3): p.rect(470 + i * 230, 230, 160, 260, DIM, 3, 1, r=6)
    ground(p, 600)
    x = 1180 - lt * 38
    wheel_robot(p, x, 600, 1.0, 1, -lt * 6)
    p.line(x - 60, 505, x + 60, 505, INK, 5)
    p.rect(x - 30, 470, 24, 34, TEAL, 3, 1, r=4); p.circle(x + 20, 488, 14, AMBER, 3)
    cap(p, ['Robots', 'asistentes', 'en', 'HOSPITALES'], lt)

def aeropuerto(p, lt, t, d):
    # terminal con avión y carrito autónomo transportando a una persona
    k = (lt * 0.08) % 1
    c = p.c; c.save(); c.translate(200 + k * 1100, 210 - k * 80); c.rotate(-0.08)
    p.poly([(-90, 0), (90, 0), (120, -10), (90, -20), (-70, -20), (-110, -50), (-90, 0)], DIM, 4, 1, True)
    p.poly([(0, -10), (-40, 30), (-10, 30), (40, -10)], DIM, 4, 1, True)
    c.restore()
    for i in range(6): p.rect(120 + i * 180, 300, 140, 200, GRID, 3, 1, r=10)
    ground(p, 600)
    x = (lt * 140) % 1500 - 150
    p.rect(x - 90, 520, 180, 50, INK, 5, 1, r=12, fill=BG)
    for wx in (x - 55, x + 55): p.circle(wx, 580, 20, INK, 5, 1, fill=BG)
    for k2 in range(3): p.arc(x + 100, 540, 18 + k2 * 14, -0.6, 0.6, TEAL, 3, 0.7)
    person(p, x - 10, 520, 0.55, dict(hipL=-1.4, kneeL=1.4, hipR=-1.3, kneeR=1.3))
    cap(p, ['Carritos', 'AUTÓNOMOS', 'en', 'aeropuertos'], lt)

def agricultura(p, lt, t, d):
    for i in range(7):
        y = 330 + i * 40
        p.line(100, y, 1180, y, (0.22, 0.38, 0.3), 6)
        for j in range(14):
            sx = 120 + j * 78 + (i % 2) * 30
            p.line(sx, y, sx, y - 16 - 6 * math.sin(i + j), (0.45, 0.75, 0.5), 4)
    x = 140 + (lt * 70) % 1100
    wheel_robot(p, x, 330, 0.8, 1, lt * 6, arm=(1.8 + 0.3 * math.sin(lt * 3), -0.8))
    for k in range(3): p.arc(x, 210, 30 + k * 20, -2.4, -0.7, TEAL, 3, 0.6)
    cap(p, ['…y', 'también', 'en', 'la', 'AGRICULTURA'], lt)

def demanda(p, lt, t, d):
    # rejilla de plazas que se llenan + cola de espera
    rows, cols = 5, 12
    filled = int(clamp01(lt / 10) * rows * cols)
    for r in range(rows):
        for c in range(cols):
            i = r * cols + c; x = 250 + c * 58; y = 170 + r * 56
            p.rect(x, y, 44, 44, TEAL if i < filled else DIM, 3, 1, r=8, fill=TEAL if i < filled else None, fa=0.35)
    if lt > 11:
        for i in range(9):
            k = appear(lt, 11 + i * 0.4)
            person(p, 280 + i * 85, 660, 0.36, dict(bob=abs(math.sin(lt * 4 + i)) * 4), k)
        mono(p, 'LISTA DE ESPERA', 1080, 600, 22, AMBER, appear(lt, 12), 'center')
    cap(p, ['Todas', 'las', 'PLAZAS', 'cubiertas'], lt)

# ---------------------------------------------------------------- marketing (de la muestra) y patada
def sin_conciencia(p, lt, t, d):
    ground(p, 560)
    ph = lt * 2.2; b = math.sin(ph * math.pi)
    kick = clamp01(math.sin(ph * math.pi / 2)) if lt > 6 else 0
    pose = dict(shL=-1.2, shR=1.2, elL=0.5, elR=-0.5, hipR=-1.3 * kick, kneeR=0.2, bob=4 * abs(b))
    robot(p, 520, 560, 1.0, pose)
    # operario que se acerca y recibe la patada
    hx = 860 - min(1, lt / 6) * 100
    hit = lt > 6.6 and kick > 0.6
    person(p, hx + (40 if hit else 0), 560, 0.9, dict(tilt=0.35 if hit else 0, shL=-1.0, shR=1.0))
    if hit:
        for j in range(5): star(p, hx - 20 + j * 18, 330 - (j % 2) * 20, 10, AMBER, 1)
    mono(p, 'SIN CONCIENCIA DEL ENTORNO', 640, 640, 22, RED, appear(lt, 8), 'center')
    cap(p, ['¿Y', 'si', 'algo', 'CAMBIA', 'en', 'el', 'entorno?'], lt)

# ---------------------------------------------------------------- piernas o ruedas
def piernas_ruedas(p, lt, t, d):
    # izquierda: ruedas en suelo liso (bien) y atascadas en un escalón; derecha: piernas suben
    p.line(640, 170, 640, 640, GRID, 3)
    gL, gR = 560, 560
    ground(p, gL, 60, 600);
    # escalón a la izquierda
    p.poly([(330, gL), (330, gL - 50), (600, gL - 50)], INK, 4)
    xw = min(250, 80 + lt * 30)
    wheel_robot(p, xw, gL, 0.8, 1, lt * 5 if xw < 250 else 0)
    if xw >= 250: p.text('?', 330, 380, 60, AMBER, 1, 'bold', 'center')
    # escaleras a la derecha
    steps = [(680 + i * 90, gR - i * 40) for i in range(6)]
    pts = [(660, gR)]
    for sx, sy in steps: pts += [(sx, sy), (sx, sy - 40)]
    p.poly(pts + [(1220, gR - 240)], INK, 4)
    k = clamp01(lt / 14)
    i = min(5, int(k * 6)); fx = 700 + k * 480; fy = gR - k * 240
    robot(p, fx, fy, 0.65, walk_pose(lt * 6))
    mono(p, 'RUEDAS', 330, 640, 24, DIM, 1, 'center'); mono(p, 'PIERNAS', 950, 640, 24, DIM, 1, 'center')
    cap(p, ['Piernas', 'para', 'el', 'terreno', 'IRREGULAR'], lt)

def pandilla(p, lt, t, d):
    ground(p, 580)
    # niños y robot en fila, saltando
    xs = [260, 410, 560, 760, 910, 1060]
    for i, x in enumerate(xs):
        b = abs(math.sin(lt * 3 + i * 0.7)) * 14
        if i == 3:
            robot(p, x, 580, 0.75, dict(bob=b, shL=-2.6, shR=2.6, elL=0.3, elR=-0.3))
        else:
            person(p, x, 580, 0.85, dict(bob=b, shL=-2.5, shR=2.5), 1, INK, kid=True)
    for i in range(5):
        k = ((lt + i * 1.1) % 4) / 4; heart(p, 760 + math.sin(k * 6 + i) * 60, 300 - k * 160, 18, 1 - k)
    cap(p, ['Uno', 'más', 'de', 'la', 'PANDILLA'], lt)

def semejanza(p, lt, t, d):
    # persona y robot frente a frente: el robot imita los movimientos
    ground(p, 580, 200, 1080)
    s = math.sin(lt * 1.6)
    pose = dict(shL=-1.0 - 0.9 * s, shR=1.0 + 0.9 * s, elL=0.4, elR=-0.4, tilt=0.05 * s)
    person(p, 480, 580, 1.0, pose)
    robot(p, 800, 580, 0.95, dict(shL=-1.0 - 0.9 * math.sin(lt * 1.6 - 0.4), shR=1.0 + 0.9 * math.sin(lt * 1.6 - 0.4), elL=0.4, elR=-0.4))
    for k in range(3): p.arc(640, 360, 20 + k * 16, -0.7, 0.7, TEAL, 3, 0.4 + 0.2 * math.sin(lt * 3 + k))
    cap(p, ['Parecido', 'a', 'nosotros', '=', 'más', 'CONFIANZA'], lt)

# ---------------------------------------------------------------- teleoperación y manos
def teleoperado(p, lt, t, d):
    ground(p, 580)
    # operador con gafas de RV y mandos; señal punteada hasta el robot
    s = math.sin(lt * 1.5)
    person(p, 300, 580, 1.0, dict(shR=1.6 + 0.6 * s, elR=-0.6, shL=-1.4 - 0.4 * s, elL=0.6))
    p.rect(278, 296, 46, 18, TEAL, 0, 1, r=6, fill=TEAL)
    dashed(p, 380, 300, 820, 300, TEAL, 3, 0.8, 14, -lt * 40)
    robot(p, 920, 580, 1.0, dict(shR=1.6 + 0.6 * math.sin(lt * 1.5 - 0.3), elR=-0.6, shL=-1.4 - 0.4 * math.sin(lt * 1.5 - 0.3), elL=0.6))
    mono(p, 'CONTROL REMOTO', 600, 280, 20, DIM, appear(lt, 1), 'center')
    cap(p, ['Muchos', 'robots', 'aún', 'se', 'manejan', 'A', 'DISTANCIA'], lt)

def manos(p, lt, t, d):
    if lt < 22:
        # mano humana se abre y cierra frente a pinza robótica
        o = 0.5 + 0.5 * math.sin(lt * 1.8)
        hand(p, 380, 380, 1.6, 1, INK, o)
        robot_arm(p, 900, 600, -0.4, 1.4, 0.4 * math.sin(lt), 1.0, 1, o)
        mono(p, '27 HUESOS', 380, 560, 22, DIM, 1, 'center'); mono(p, '1 PINZA', 900, 650, 22, DIM, 1, 'center')
        cap(p, ['Lo', 'difícil', 'son', 'las', 'MANOS'], lt)
    else:
        lt2 = lt - 22
        # el pulpo: tentáculos con ventosas
        cx, cy = 640, 300
        p.circle(cx, cy, 80, AMBER, 5, 1, fill=BG)
        p.circle(cx - 28, cy - 5, 9, AMBER, 0, 1, fill=AMBER); p.circle(cx + 28, cy - 5, 9, AMBER, 0, 1, fill=AMBER)
        for i in range(8):
            base = -0.4 + i * (math.pi + 0.8) / 7
            pts = []
            for j in range(14):
                u = j / 13
                ang = base + 0.5 * math.sin(lt2 * 2 + i + u * 4) * u
                r = 70 + u * 230
                pts.append((cx + r * math.cos(ang), cy + 40 + r * math.sin(ang) * 0.9))
            p.poly(pts, AMBER, 9 - 0 * 1)
            for j in range(3, 13, 3): p.circle(pts[j][0], pts[j][1], 5, INK, 0, 1, fill=INK)
        cap(p, ['Brazos', 'y', 'VENTOSAS,', 'como', 'un', 'pulpo'], lt2)

# ---------------------------------------------------------------- fascinación
def cine50(p, lt, t, d):
    # proyector y pantalla con robot de película antigua, grano
    p.rect(330, 160, 620, 360, INK, 4, 1, r=4, fill=(0.12, 0.12, 0.11))
    flick = 0.85 + 0.15 * math.sin(lt * 37)
    robot(p, 640, 500, 0.95, dict(shL=-1.2 + 0.5 * math.sin(lt * 1.5), shR=1.2 - 0.5 * math.sin(lt * 1.5), elL=0.8, elR=-0.8), flick, AMBER, (0.85, 0.82, 0.75))
    random.seed(int(lt * 12))
    for _ in range(40): p.circle(random.uniform(340, 940), random.uniform(170, 510), random.uniform(0.6, 1.8), INK, 0, 0.35, fill=INK, fa=0.35)
    p.line(random.uniform(340, 940), 160, random.uniform(340, 940), 520, INK, 1, 0.15)
    mono(p, 'AÑOS 50', 640, 590, 26, AMBER, appear(lt, 1), 'center')
    cap(p, ['Robots', 'en', 'el', 'cine', 'ANTES', 'que', 'en', 'la', 'realidad'], lt)

def expectativas(p, lt, t, d):
    if lt < 60:
        # dos barras: expectativa (sube mucho) y realidad (sube poco)
        e = ease(lt / 6); r = ease((lt - 3) / 6)
        p.rect(400, 560 - 290 * e, 160, 290 * e, TEAL, 4, 1, r=8, fill=TEAL, fa=0.25)
        p.rect(720, 560 - 150 * r, 160, 150 * r, AMBER, 4, 1, r=8, fill=AMBER, fa=0.25)
        ground(p, 560, 300, 980)
        p.text('EXPECTATIVAS', 480, 610, 26, TEAL, 1, 'bold', 'center'); p.text('REALIDAD', 800, 610, 26, AMBER, 1, 'bold', 'center')
        robot(p, 480, 560 - 290 * e, 0.4, dict(shL=-2.6, shR=2.6))
        robot(p, 800, 560 - 150 * r, 0.4, dict(shL=-0.3, shR=0.3, head=0.3 * math.sin(lt)))
        cap(p, ['Distinguir', 'EXPECTATIVAS', 'y', 'REALIDAD'], lt)
    else:
        lt2 = lt - 60
        # estudiante que sueña con un mayordomo y encuentra código
        person(p, 320, 600, 1.0, dict(shR=1.0, elR=-1.4))
        bubble(p, 420, 170, 330, 230, 1, INK, -1)
        robot(p, 585, 380, 0.55, dict(shR=1.2, elR=-1.4))
        p.line(615, 260, 660, 255, INK, 4); p.circle(670, 252, 12, AMBER, 3)  # bandeja con taza
        k = appear(lt2, 4)
        p.rect(800, 220, 380, 300, DIM, 3, k, r=12, fill=(0.07, 0.12, 0.13), fa=k)
        for i in range(7):
            mono(p, ['while True:', '  leer_sensores()', '  calcular_ruta()', '  if obstaculo:', '    frenar()', '  mover(0.2)', '  # ...faltan 3000'][i], 820, 265 + i * 34, 19, TEAL if i else INK, k)
        cap(p, ['No', 'son', 'C3PO:', 'hay', 'que', 'PROGRAMAR', 'mucho'], lt2)

# ---------------------------------------------------------------- en casa
def roomba(p, lt, t, d):
    # planta de una habitación vista desde arriba con el recorrido del aspirador
    ox, oy, w, h = 290, 170, 700, 420
    p.rect(ox, oy, w, h, INK, 5, 1, r=6)
    p.rect(ox + 40, oy + 40, 180, 110, DIM, 3, 1, r=8); p.rect(ox + 460, oy + 260, 200, 120, DIM, 3, 1, r=8)
    path = []; x, y = ox + 260, oy + 60; dx = 1
    for i in range(400):
        x += dx * 6
        if x > ox + w - 40 or x < ox + 40: dx = -dx; y += 34
        path.append((x, min(y, oy + h - 30)))
    n = int(clamp01(lt / 50) * len(path))
    if n > 1: p.poly(path[:n], TEAL, 6, 0.35)
    rx, ry = path[max(0, n - 1)]
    p.circle(rx, ry, 26, INK, 5, 1, fill=BG); p.circle(rx, ry - 10, 6, TEAL, 0, 1, fill=TEAL)
    mono(p, 'MILLONES VENDIDOS', 1140, 640, 20, DIM, appear(lt, 3), 'right')
    cap(p, ['El', 'gran', 'salto:', 'el', 'ROBOT', 'ASPIRADOR'], lt)

def casa_humanoide(p, lt, t, d):
    if lt < 45:
        # deseo: que recoja, quite el polvo y saque al perro
        ground(p, 580)
        robot(p, 460, 580, 0.95, walk_pose(lt * 4))
        p.c.save(); p.c.translate(640, 580); dog(p, lt); p.c.restore()
        dashed(p, 540, 390, 650, 500, INK, 3, 1, 8, 0)
        items = ['recoger trastos', 'quitar el polvo', 'ordenar la casa', 'sacar al perro']
        for i, it in enumerate(items):
            k = appear(lt, 2 + i * 2)
            yb = 250 + i * 50
            p.rect(860, yb - 24, 26, 26, INK, 3, k, r=4)
            if lt >= 30:
                p.line(864, yb - 20, 882, yb - 2, RED, 4, k); p.line(882, yb - 20, 864, yb - 2, RED, 4, k)
            p.text(it, 902, yb, 28, INK, k, 'normal')
        cap(p, ['¿Un', 'HUMANOIDE', 'en', 'casa?', 'Todavía', 'no'], lt)
    else:
        lt2 = lt - 45
        # coche autónomo con sensores y etiqueta de precio en humanoide
        p.line(0, 520, W, 520, DIM, 4)
        for i in range(10): p.line(i * 160 - (lt2 * 200) % 160, 470, i * 160 + 80 - (lt2 * 200) % 160, 470, DIM, 4, 0.5)
        cx = 420
        p.poly([(cx - 150, 500), (cx - 150, 450), (cx - 90, 410), (cx + 70, 410), (cx + 140, 450), (cx + 150, 500)], INK, 5, 1, True, fill=BG)
        for wx in (cx - 90, cx + 90): p.circle(wx, 505, 26, INK, 5, 1, fill=BG)
        for k in range(4): p.arc(cx + 150, 450, 30 + ((lt2 * 60 + k * 30) % 120), -0.5, 0.5, TEAL, 3, 1 - ((lt2 * 60 + k * 30) % 120) / 120)
        robot(p, 980, 520, 0.6, dict(shL=-1.6 + 0.5 * math.sin(lt2 * 4), shR=1.6 - 0.5 * math.sin(lt2 * 4)))
        p.rect(1060, 230, 160, 60, AMBER, 4, 1, r=8, fill=BG); p.text('20.000 €', 1140, 270, 28, AMBER, 1, 'bold', 'center')
        cap(p, ['Coches', 'AUTÓNOMOS', 'y', 'humanoides', 'para', 'entretener'], lt2)

def dog(p, lt):
    b = math.sin(lt * 8)
    p.rect(-50, -80, 100, 40, INK, 5, 1, r=18, fill=BG)
    p.circle(62, -92, 22, INK, 5, 1, fill=BG)
    for lx in (-35, 35): p.line(lx, -42, lx + 10 * b, 0, INK, 6); p.line(lx + 12, -42, lx + 12 - 10 * b, 0, INK, 6)
    p.line(-50, -70, -78, -96 + 8 * b, INK, 5)

# ---------------------------------------------------------------- autismo
def autismo(p, lt, t, d):
    ground(p, 580, 200, 1080)
    person(p, 450, 580, 0.85, dict(hipL=-1.5, kneeL=1.5, hipR=-1.4, kneeR=1.4, shR=0.9 + 0.2 * math.sin(lt), elR=-0.6), 1, INK, kid=True)
    robot(p, 820, 580, 0.75, dict(head=0.2 * math.sin(lt * 0.8), shL=-0.6, elL=0.5))
    # mirada: línea de contacto que aparece
    k = appear(lt, 5, 1.5)
    dashed(p, 470, 330, 780, 360, TEAL, 3, k, 10, -lt * 20)
    mono(p, 'ESTUDIO PILOTO', 640, 640, 22, DIM, appear(lt, 1), 'center')
    cap(p, ['Robots', 'para', 'apoyar', 'la', 'COMUNICACIÓN'], lt)

def cancion(p, lt, t, d):
    # reloj de 24 h con notas sin fin; robot paciente y padre agotado
    cx, cy = 640, 360
    p.circle(cx, cy, 150, INK, 5)
    for i in range(24):
        ang = i / 24 * 2 * math.pi
        p.line(cx + 135 * math.sin(ang), cy - 135 * math.cos(ang), cx + 150 * math.sin(ang), cy - 150 * math.cos(ang), DIM, 3)
    h = lt * 0.6
    p.line(cx, cy, cx + 100 * math.sin(h), cy - 100 * math.cos(h), TEAL, 6)
    p.line(cx, cy, cx + 70 * math.sin(h / 12), cy - 70 * math.cos(h / 12), INK, 7)
    p.text('24 h', cx, cy + 210, 30, TEAL, 1, 'bold', 'center')
    for i in range(6):
        k = ((lt + i * 0.6) % 3.6) / 3.6
        note(p, cx + 200 + math.sin(k * 6 + i) * 30, cy + 120 - k * 300, 1 - k)
    person(p, 230, 600, 0.8, dict(tilt=0.25, shL=-0.1, shR=0.1, head=0))
    mono(p, 'zzz', 230, 300, 26, DIM, 0.5 + 0.5 * math.sin(lt * 2))
    robot(p, 1050, 600, 0.65, dict(shR=1.6 + 0.4 * math.sin(lt * 3)))
    cap(p, ['La', 'misma', 'canción', 'TODO', 'EL', 'DÍA'], lt)

def dar_la_mano(p, lt, t, d):
    ground(p, 590)
    robot(p, 880, 590, 0.95, dict(shL=-1.3 * appear(lt, 1.5, 1.5), elL=0.1))
    # cola de niños
    for i in range(5):
        x = 640 - i * 120 + (0 if i else 20 * appear(lt, 4))
        person(p, x, 590, 0.75, dict(shR=1.2 * appear(lt, 4) if i == 0 else 0.25, bob=abs(math.sin(lt * 3 + i)) * 4), 1, INK, kid=True)
    if lt > 6:
        for j in range(3): heart(p, 760 + j * 30, 360 - ((lt - 6) * 30 + j * 25) % 120, 14, 0.8)
    mono(p, 'JORNADA DE PUERTAS ABIERTAS', 640, 650, 20, DIM, appear(lt, 1), 'center')
    cap(p, ['Hacen', 'cola', 'para', 'DAR', 'LA', 'MANO', 'al', 'robot'], lt)

def doblar_codo(p, lt, t, d):
    # dos lecturas del mismo gesto
    p.line(640, 170, 640, 620, GRID, 3)
    person(p, 300, 580, 0.9, dict(shR=1.3, elR=-0.1), 1, INK, kid=True)
    hand(p, 440, 400, 0.6, 1, INK, 0.7)
    heart(p, 330, 230, 30, 0.6 + 0.4 * math.sin(lt * 3))
    p.text('Para el niño: un saludo', 320, 650, 26, INK, 1, 'normal', 'center')
    ang = 0.6 + 0.6 * ease((math.sin(lt * 0.9) + 1) / 2)
    robot_arm(p, 900, 560, -0.2, ang, 0.2, 0.9, 1, 0.5)
    mono(p, f'codo = {int(math.degrees(ang))}°', 900, 220, 26, TEAL, 1, 'center')
    p.text('Para el robot: doblar el codo', 960, 650, 26, INK, 1, 'normal', 'center')
    cap(p, ['Un', 'gesto', 'de', 'IGUAL', 'A', 'IGUAL'], lt)

# ---------------------------------------------------------------- generalista vs especializado
def generalista(p, lt, t, d):
    p.line(640, 170, 640, 620, GRID, 3)
    ground(p, 580, 60, 600); ground(p, 580, 680, 1220)
    # humanoide cargando cajas
    x = 120 + (lt * 50) % 380
    robot(p, x, 580, 0.8, {**walk_pose(lt * 5), 'shL': -0.9, 'shR': 0.9, 'elL': -1.0, 'elR': 1.0})
    box(p, x, 480, 80, 60)
    for i in range(3): box(p, 540, 580 - i * 58, 70, 55)
    # carrito con brazo y ventosa cogiendo objetos
    ph = lt * 1.2
    wheel_robot(p, 860, 580, 0.9, 1, 0, arm=(1.6 + 0.6 * math.sin(ph), -1.2 + 0.4 * math.sin(ph)))
    for i in range(4): box(p, 1040 + (i % 2) * 70, 580 - (i // 2) * 52, 60, 48, TEAL)
    mono(p, 'GENERALISTA', 330, 650, 24, DIM, 1, 'center'); mono(p, 'ESPECIALIZADO', 950, 650, 24, DIM, 1, 'center')
    cap(p, ['¿HUMANOIDE', 'o', 'carrito', 'con', 'brazo?'], lt)

def impresora3d(p, lt, t, d):
    # impresora 3D construyendo una pieza capa a capa
    x0, y0 = 430, 180
    p.rect(x0, y0, 420, 400, INK, 5, 1, r=10)
    p.line(x0 + 20, y0 + 60, x0 + 400, y0 + 60, DIM, 5)
    layers = int(clamp01(lt / 40) * 22)
    for i in range(layers):
        y = y0 + 360 - i * 10; w = 160 - abs(i - 11) * 4
        p.line(640 - w / 2, y, 640 + w / 2, y, TEAL, 8, 0.9)
    hx = 640 + 80 * math.sin(lt * 5)
    hy = y0 + 350 - layers * 10
    p.line(hx, y0 + 60, hx, hy - 30, DIM, 4)
    p.poly([(hx - 22, hy - 40), (hx + 22, hy - 40), (hx, hy - 12)], INK, 4, 1, True, fill=BG)
    p.rect(x0 + 60, y0 + 370, 300, 14, DIM, 0, 1, r=4, fill=DIM)
    cap(p, ['Con', 'IMPRESORAS', '3D', 'diseñamos', 'a', 'medida'], lt)

def espana(p, lt, t, d):
    if lt < 50:
        # cadena de suministro: barcos/cajas llegando, frente a software propio
        p.line(100, 420, 1180, 420, DIM, 3)
        for i in range(6):
            x = (lt * 90 + i * 220) % 1400 - 100
            box(p, x, 420, 70, 50, AMBER)
        mono(p, 'MOTORES · SENSORES · COMPONENTES', 640, 470, 22, DIM, 1, 'center')
        p.text('China', 140, 360, 30, AMBER, 1, 'bold'); p.text('España', 1140, 360, 30, TEAL, 1, 'bold', 'right')
        cap(p, ['No', 'podemos', 'competir', 'en', 'COSTE…'], lt)
    else:
        lt2 = lt - 50
        robot(p, 380, 590, 0.95, dict(head=0.25 * math.sin(lt2)), 1 if lt2 > 6 else 0.35)
        p.rect(620, 200, 560, 340, DIM, 3, 1, r=14, fill=(0.07, 0.12, 0.13))
        code = ['class Robot:', '  def percibir(self): ...', '  def planificar(self): ...', '  def actuar(self): ...', '', 'robot.integrar(cliente)']
        n = int(lt2 * 4)
        for i, ln in enumerate(code):
            mono(p, ln[:max(0, n - i * 8)], 645, 250 + i * 44, 22, TEAL if i == 5 else INK)
        cap(p, ['…pero', 'sí', 'en', 'SOFTWARE'], lt2)

# ---------------------------------------------------------------- IA generativa
def vision(p, lt, t, d):
    if lt < 38:
        # escena con objetos detectados por cajas etiquetadas
        ground(p, 560, 120, 1160)
        box(p, 300, 560, 110, 90); p.circle(560, 510, 50, INK, 5); person(p, 820, 560, 0.85); wheel_robot(p, 1040, 560, 0.6)
        dets = [(230, 455, 140, 115, 'caja 0,97'), (500, 450, 120, 120, 'pelota 0,91'), (760, 250, 120, 320, 'persona 0,99'), (990, 490, 100, 80, 'robot 0,88')]
        for i, (x, y, w, h, lab) in enumerate(dets):
            k = appear(lt, 2 + i * 1.2)
            p.rect(x, y, w, h, TEAL, 3, k, r=2)
            p.rect(x, y - 28, len(lab) * 13 + 14, 28, TEAL, 0, k, r=2, fill=TEAL, fa=k)
            mono(p, lab, x + 7, y - 8, 18, BG, k)
        cap(p, ['VISIÓN', 'artificial', 'con', 'IA'], lt)
    else:
        lt2 = lt - 38
        # orden en lenguaje natural y ruta en un plano
        bubble(p, 70, 160, 520, 120, 1)
        msg = 'Vete por el pasillo, gira la segunda a la derecha y coge la caja'
        n = int(lt2 * 18)
        cut = msg.rfind(' ', 0, 36); lines = [msg[:cut], msg[cut + 1:]]
        mono(p, lines[0][:n], 95, 210, 21, INK); mono(p, lines[1][:max(0, n - cut - 1)], 95, 245, 21, INK)
        ox, oy = 680, 170
        walls = [(ox, oy, ox + 520, oy), (ox, oy + 120, ox + 300, oy + 120), (ox + 380, oy + 120, ox + 520, oy + 120),
                 (ox + 300, oy + 120, ox + 300, oy + 420), (ox + 380, oy + 120, ox + 380, oy + 420)]
        for w_ in walls: p.line(*w_, DIM, 6)
        path = [(ox + 40, oy + 60), (ox + 340, oy + 60), (ox + 340, oy + 380)]
        k = clamp01((lt2 - 4) / 10)
        seg = path[:1]; tot = k * 600
        for (x1, y1), (x2, y2) in zip(path, path[1:]):
            L = math.hypot(x2 - x1, y2 - y1)
            if tot <= 0: break
            u = min(1, tot / L); seg.append((x1 + (x2 - x1) * u, y1 + (y2 - y1) * u)); tot -= L
        if len(seg) > 1: dashed(p, *seg[0], *seg[0], TEAL); p.poly(seg, TEAL, 5)
        p.circle(*seg[-1], 14, TEAL, 0, 1, fill=TEAL)
        box(p, ox + 340, oy + 420, 50, 40)
        cap(p, ['Órdenes', 'en', 'LENGUAJE', 'NATURAL'], lt2, y=110)

# ---------------------------------------------------------------- sustitución
def puerta(p, lt, t, d):
    ground(p, 590)
    # puerta cerrada; el humanoide la empuja sin éxito
    p.rect(760, 210, 200, 380, INK, 5, 1, r=4, fill=(0.1, 0.16, 0.17))
    p.circle(790, 410, 10, AMBER, 4)
    k = clamp01(lt / 6)
    x = 360 + 280 * ease(k)
    tries = max(0, lt - 6)
    push = 0.5 + 0.5 * math.sin(tries * 4) if tries > 0 else 0
    robot(p, x + 18 * push, 590, 0.95, walk_pose(lt * 5) if k < 1 else dict(shR=1.4 + 0.2 * push, elR=-0.2, shL=-0.2, head=0.2 * math.sin(tries)))
    if tries > 4:
        p.text('?', x, 240, 64, AMBER, 1, 'bold', 'center')
    cap(p, ['Baila', 'y', 'corre…', 'pero', 'no', 'abre', 'una', 'PUERTA'], lt)

def fabrica(p, lt, t, d):
    if lt < 50:
        # cadena de montaje: coches avanzando, brazos soldando, personas en otras fases
        p.line(80, 520, 1200, 520, DIM, 6)
        for i in range(5):
            x = (lt * 60 + i * 280) % 1400 - 120
            p.poly([(x - 90, 510), (x - 90, 470), (x - 50, 440), (x + 50, 440), (x + 90, 470), (x + 90, 510)], INK, 4, 1, True, fill=BG)
        for j, ax in enumerate((380, 760)):
            ph = lt * 2 + j
            tx, ty = robot_arm(p, ax, 300, 2.6 + 0.25 * math.sin(ph), 0.9, 0.3, 0.8, 1, 0.3)
            if math.sin(ph * 3) > 0.3:
                for s_ in range(6):
                    a_ = random.uniform(0, 2 * math.pi); p.line(tx, ty, tx + 22 * math.cos(a_), ty + 22 * math.sin(a_), AMBER, 3)
        person(p, 1170, 660, 0.6, dict(shR=1.0 + 0.4 * math.sin(lt * 3), elR=-0.8))
        cap(p, ['Robots', 'en', 'la', 'industria…', 'y', 'también', 'PERSONAS'], lt)
    elif lt < 120:
        lt2 = lt - 50
        # robot cocinero batiendo huevos: «demo de feria»
        p.rect(300, 470, 680, 30, INK, 4, 1, r=6)
        robot(p, 520, 470, 0.7, dict(shR=1.4, elR=-0.6 + 0.5 * math.sin(lt2 * 9), hipL=0, hipR=0))
        p.arc(700, 440, 50, 0.1, math.pi - 0.1, INK, 5)
        for i in range(2): p.circle(680 + i * 40, 440, 16, (0.95, 0.85, 0.35), 0, 1, fill=(0.95, 0.85, 0.35))
        p.rect(820, 380, 140, 50, AMBER, 3, 1, r=6); mono(p, 'DEMO', 890, 413, 22, AMBER, 1, 'center')
        cap(p, ['¿El', 'COCINERO', 'robot?', 'De', 'momento,', 'demo', 'de', 'feria'], lt2)
    else:
        lt2 = lt - 120
        # fontanero: tubería con fuga, «un par de décadas»
        p.poly([(200, 260), (600, 260), (600, 460), (1000, 460)], INK, 18)
        for i in range(8):
            k = ((lt2 * 1.5 + i * 0.3) % 2) / 2
            p.circle(600 + 20, 360 + k * 220, 6, TEAL, 0, 1 - k, fill=TEAL, fa=1 - k)
        person(p, 820, 640, 0.75, dict(shL=-1.8, shR=1.8, elL=0.6, elR=-0.6))
        p.rect(950, 160, 220, 90, AMBER, 4, 1, r=10, fill=BG); p.text('≈ 20 años', 1060, 220, 32, AMBER, 1, 'bold', 'center')
        cap(p, ['El', 'FONTANERO', 'robot', 'no', 'llegará', 'pronto'], lt2)

# ---------------------------------------------------------------- deporte
def deporte(p, lt, t, d):
    if lt < 45:
        # fútbol de robots
        p.rect(140, 220, 1000, 380, (0.22, 0.38, 0.3), 4, 1, r=6, fill=(0.07, 0.14, 0.11))
        p.line(640, 220, 640, 600, (0.22, 0.38, 0.3), 4); p.circle(640, 410, 70, (0.22, 0.38, 0.3), 4)
        bx = 640 + 300 * math.sin(lt * 0.9); by = 470 + 60 * math.sin(lt * 1.7)
        for i, (x0, col) in enumerate([(400, TEAL), (520, TEAL), (760, AMBER), (880, AMBER)]):
            x = x0 + (bx - x0) * 0.3
            robot(p, x, 560, 0.45, walk_pose(lt * 6 + i), 1, col)
        p.circle(bx, by, 14, INK, 4, 1, fill=BG)
        cap(p, ['Jugar', 'en', 'EQUIPO', 'es', 'mucho', 'más', 'difícil'], lt)
    else:
        lt2 = lt - 45
        # tenis: robot con raqueta y pelota que va y vuelve
        ground(p, 580)
        p.line(640, 580, 640, 470, INK, 4); p.line(600, 470, 680, 470, INK, 4)
        u = (lt2 % 2.4) / 2.4; to_r = int(lt2 / 2.4) % 2 == 0
        x = 330 + (620 * u if to_r else 620 * (1 - u)); y = 520 - 220 * math.sin(math.pi * u)
        p.circle(x, y, 12, (0.85, 0.95, 0.35), 0, 1, fill=(0.85, 0.95, 0.35))
        sw = 1 - abs(u - (0 if to_r else 1)) * 6
        robot(p, 260, 580, 0.8, dict(shR=1.2 + 1.0 * clamp01(sw), elR=-0.2))
        person(p, 1020, 580, 0.9, dict(shL=-1.2 - 1.0 * clamp01(1 - abs(u - (1 if to_r else 0)) * 6)))
        cap(p, ['Ya', 'devuelven', 'la', 'PELOTA', 'al', 'campo', 'contrario'], lt2)

def seguir_corriendo(p, lt, t, d):
    if lt < 40:
        ground(p, 560)
        x = (lt * 500) % 1700 - 200
        p.poly([(x - 120, 540), (x - 120, 500), (x - 70, 470), (x + 60, 470), (x + 120, 500), (x + 120, 540)], DIM, 4, 1, True, fill=BG)
        for wx in (x - 70, x + 70): p.circle(wx, 545, 18, DIM, 4, 1, fill=BG)
        person(p, 640, 560, 1.0, walk_pose(lt * 9, True))
        cap(p, ['Hay', 'coches', 'más', 'rápidos…', 'y', 'SEGUIMOS', 'CORRIENDO'], lt)
    else:
        lt2 = lt - 40
        # avatar de profesor en una pantalla con estudiantes
        p.rect(380, 170, 520, 320, INK, 5, 1, r=14, fill=(0.07, 0.12, 0.13))
        person(p, 640, 470, 0.7, dict(shR=1.4 + 0.3 * math.sin(lt2 * 2), elR=-0.6), 1, TEAL)
        mono(p, 'AVATAR', 640, 210, 20, TEAL, 1, 'center')
        for i in range(5): person(p, 300 + i * 170, 680, 0.42, dict(shR=2.6 if i == 2 and int(lt2) % 4 < 2 else 0.25))
        cap(p, ['¿PROFESORES', 'avatar?', 'Otra', 'guerra'], lt2)

# ---------------------------------------------------------------- ilusión y uso dual
def ilusion(p, lt, t, d):
    robot(p, 400, 600, 1.0, dict(shR=2.5, elR=-0.2, shL=-0.3))
    price = 2_000_000 * (1 - ease(lt / 12)) + 15_000 * ease(lt / 12)
    s = f'{int(price):,} €'.replace(',', '.')
    p.text(s, 880, 380, 64, AMBER, 1, 'bold', 'center')
    mono(p, 'HACE 10 AÑOS → HOY', 880, 440, 22, DIM, 1, 'center')
    cap(p, ['Humanoides', 'al', 'alcance', 'de', 'la', 'INVESTIGACIÓN'], lt)

def drones(p, lt, t, d):
    if lt < 70:
        # drones sobrevolando un campo, mira telescópica
        p.line(0, 560, W, 560, DIM, 4)
        for i in range(4):
            x = (lt * (90 + i * 25) + i * 330) % 1500 - 100; y = 230 + i * 50 + 15 * math.sin(lt * 2 + i)
            drone(p, x, y, lt, 0.9 - i * 0.1)
        cx = 640 + 120 * math.sin(lt * 0.5); cy = 450
        p.circle(cx, cy, 60, RED, 3, 0.8); p.line(cx - 80, cy, cx + 80, cy, RED, 2, 0.8); p.line(cx, cy - 80, cx, cy + 80, RED, 2, 0.8)
        mono(p, 'TECNOLOGÍA DE USO DUAL', 640, 640, 22, RED, appear(lt, 2), 'center')
        cap(p, ['Los', 'DRONES', 'han', 'cambiado', 'la', 'guerra'], lt)
    else:
        lt2 = lt - 70
        # documento de regulación con sello
        p.rect(440, 170, 400, 460, INK, 5, 1, r=10, fill=(0.07, 0.12, 0.13))
        for i in range(8): p.line(480, 240 + i * 40, 800 - (i % 3) * 60, 240 + i * 40, DIM, 4)
        k = ease((lt2 - 2) / 0.4)
        if lt2 > 2:
            p.c.save(); p.c.translate(740, 540); p.c.rotate(-0.2); p.c.scale(1.6 - 0.6 * k, 1.6 - 0.6 * k)
            p.rect(-110, -40, 220, 80, RED, 6, k, r=10); p.text('REGULAR', 0, 14, 38, RED, k, 'bold', 'center'); p.c.restore()
        drone(p, 1050, 320, lt2, 0.8)
        p.line(990, 260, 1110, 380, RED, 8); p.line(1110, 260, 990, 380, RED, 8)
        cap(p, ['Como', 'las', 'MINAS', 'ANTIPERSONA:', 'regular'], lt2)

def drone(p, x, y, lt, s=1.0):
    c = p.c; c.save(); c.translate(x, y); c.scale(s, s)
    p.rect(-30, -12, 60, 24, INK, 4, 1, r=8, fill=BG)
    for sx in (-1, 1):
        p.line(sx * 30, -4, sx * 70, -18, INK, 4)
        w = 30 * abs(math.sin(lt * 40 + sx))
        p.line(sx * 70 - w, -24, sx * 70 + w, -24, TEAL, 4)
    p.circle(0, 14, 6, RED, 0, 1, fill=RED)
    c.restore()

# ---------------------------------------------------------------- cierre y créditos
def cierre(p, lt, t, d):
    # grano que cae y se separa de la paja
    random.seed(7)
    for i in range(70):
        sx = random.uniform(420, 860); sp = random.uniform(0.6, 1.2); chaff = i % 3 == 0
        y = 150 + ((lt * 140 * sp + i * 37) % 420)
        x = sx + (y - 150) * (0.9 if chaff else 0) * 0.5
        if chaff: p.line(x, y, x + 14, y - 6, DIM, 3, 0.7)
        else: p.circle(x, y, 5, AMBER, 0, 1, fill=AMBER)
    p.poly([(400, 570), (880, 570), (840, 610), (440, 610)], INK, 4, 1, True)
    cap(p, ['Separar', 'el', 'GRANO', 'de', 'la', 'paja'], lt)

def creditos(p, lt, t, d):
    robot(p, 640, 660, 0.55, dict(shR=2.4 + 0.4 * math.sin(lt * 5), elR=-0.3))
    lines = [('Carne de Bit · Episodio 146', 40, INK, 'bold'), ('De la mano de los robots', 30, DIM, 'normal'),
             ('Emilio Sáez Soro conversa con Enric Cervera (UJI)', 24, DIM, 'normal'), ('', 20, DIM, 'normal'),
             ('Animación generada con código, sin imágenes externas', 22, TEAL, 'normal'),
             ('Realizada con ayuda de Claude', 20, DIM, 'normal')]
    y = 120
    for s, size, col, wt in lines:
        p.text(s, 640, y, size, col, appear(lt, 0.5), wt, 'center'); y += size + 18

# ---------------------------------------------------------------- guion
SEGMENTS = [
    (0, 32, title),
    (32, 62, presentacion), (40, 48.5, name_tag('Emilio Sáez Soro', 'Sociólogo · Presentador de Carne de Bit')),
    (50, 58.5, name_tag('Enric Cervera', 'Director del Grado en Inteligencia Robótica · UJI')),
    (62, 132, ia_con_cuerpo),
    (132, 210, spectrum), (140, 148.5, name_tag('Enric Cervera', 'Laboratorio de Robótica Inteligente · UJI')),
    (210, 305, grado),
    (305, 395, ia_juegos),
    (395, 432, almacen), (432, 460, hospital), (460, 487, aeropuerto), (487, 510, agricultura), (510, 540, demanda),
    (540, 584, S.phone_marketing), (584, 628, S.sprint), (628, 692, S.choreography), (692, 722, sin_conciencia),
    (722, 790, piernas_ruedas), (790, 840, pandilla), (840, 892, semejanza),
    (892, 958, teleoperado), (958, 1035, manos),
    (1035, 1100, cine50), (1100, 1232, expectativas),
    (1232, 1295, roomba), (1295, 1385, casa_humanoide),
    (1385, 1440, autismo), (1440, 1505, cancion), (1505, 1560, dar_la_mano), (1560, 1605, doblar_codo),
    (1605, 1690, generalista), (1690, 1745, impresora3d), (1745, 1865, espana),
    (1865, 1955, vision),
    (1955, 2050, puerta), (2050, 2155, fabrica),
    (2155, 2235, deporte), (2235, 2295, seguir_corriendo),
    (2295, 2370, ilusion), (2370, 2462, drones),
    (2462, 2502, cierre), (2502, 2621.78, creditos),
]

if __name__ == '__main__':
    import engine
    dur = 2621.78
    if len(sys.argv) > 1:  # render parcial: inicio fin
        a, b = float(sys.argv[1]), float(sys.argv[2])
        segs = [(s - a, e - a, f) for s, e, f in SEGMENTS if e > a and s < b]
        engine.render(segs, b - a, f'/home/claude/anim/parte_{int(a)}.mp4', '/mnt/user-data/uploads/146_de_la_mano_de_los_robots.mp3', a)
    else:
        engine.render(SEGMENTS, dur, '/home/claude/anim/CarneDeBit_146_animado.mp4', '/mnt/user-data/uploads/146_de_la_mano_de_los_robots.mp3', 0)
