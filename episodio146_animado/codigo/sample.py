import math, random, sys
sys.path.insert(0, '/home/claude/anim')
from engine import *

def phone_marketing(p, lt, t, d):
    cx, cy = 760, 410
    p.rect(cx - 150, cy - 260, 300, 520, INK, 5, r=36, fill=(0.08, 0.14, 0.15))
    p.rect(cx - 40, cy - 245, 80, 10, DIM, 0, r=5, fill=DIM)
    # robot haciendo una voltereta dentro del móvil
    ph = (lt % 2.4) / 2.4
    c = p.c; c.save(); c.translate(cx, cy + 120)
    hop = math.sin(ph * math.pi) * 110
    c.translate(0, -hop); c.rotate(ease(ph) * 2 * math.pi if ph < 1 else 0); c.translate(0, 150 * 0.55)
    robot(p, 0, 0, 0.55, dict(shL=-2.6, shR=2.6, elL=0, elR=0, kneeL=-0.6 * math.sin(ph * math.pi), kneeR=-0.6 * math.sin(ph * math.pi)))
    c.restore()
    # botón de play y barra de progreso
    p.line(cx - 120, cy + 215, cx + 120, cy + 215, DIM, 4)
    p.line(cx - 120, cy + 215, cx - 120 + 240 * ((lt / 8) % 1), cy + 215, RED, 4)
    # corazones / me gusta que suben
    random.seed(3)
    for i in range(9):
        st = i * 1.7; k = ((lt - st) % 5.0) / 5.0
        if lt < st: continue
        x = cx + 200 + random.uniform(-30, 80) + math.sin(k * 6 + i) * 20; y = cy + 200 - k * 380
        heart(p, x, y, 14 + (i % 3) * 5, a=1 - k)
    # contador de visualizaciones
    views = int(1200 * lt ** 2.2) + 3400
    label(p, f'{views:,} visualizaciones'.replace(',', '.'), cx - 120, cy + 300, lt, 18, DIM)
    caption(p, ['¿REALIDAD', 'o', 'marketing?'], lt - 0.5, 80, 120, 56)

def heart(p, x, y, s, a=1.0):
    c = p.c; c.save(); c.translate(x, y); c.scale(s / 20, s / 20)
    c.move_to(0, 12); c.curve_to(-22, -4, -12, -22, 0, -10); c.curve_to(12, -22, 22, -4, 0, 12)
    p.col(RED, a); c.fill(); c.restore()

def sprint(p, lt, t, d):
    ground = 520
    run_end = d - 7            # cuándo llega a la valla
    speed = 620                # px/s del fondo
    # pista: líneas que se desplazan
    off = (min(lt, run_end) * speed) % 160
    for i in range(-1, 10):
        x = i * 160 - off
        p.line(x, ground + 40, x + 90, ground + 40, DIM, 4, 0.6)
    p.line(0, ground, W, ground, INK, 4)
    if lt < run_end:
        x = 480
        ph = lt * 14
        robot(p, x, ground, 0.95, walk_pose(ph, True))
        for k in range(5):  # líneas de velocidad
            yy = ground - 80 - k * 45
            p.line(x - 120 - k * 25, yy, x - 220 - k * 40, yy, TEAL, 4, 0.7)
        # cronómetro
        sec = min(9.0, lt / run_end * 9.0)
        p.circle(1060, 160, 70, INK, 5)
        p.arc(1060, 160, 70, -math.pi / 2, -math.pi / 2 + 2 * math.pi * sec / 9.58, TEAL, 8)
        p.text(f'{sec:0.2f}'.replace('.', ','), 1060, 175, 40, INK, 1, 'bold', 'center')
        p.text('100 m', 1060, 270, 24, DIM, 1, 'normal', 'center')
        caption(p, ['Más', 'rápido', 'que', 'USAIN', 'BOLT…'], lt - 0.5, 80, 120, 52)
    else:
        k = lt - run_end
        # valla de protección
        bx = 900
        p.rect(bx, ground - 230, 40, 230, AMBER, 5, r=6, fill=(0.2, 0.15, 0.08))
        for j in range(5): p.line(bx, ground - 200 + j * 45, bx + 40, ground - 175 + j * 45, AMBER, 4)
        if k < 0.7:  # último tramo hasta chocar
            x = 480 + (bx - 60 - 480) * ease(k / 0.7)
            robot(p, x, ground, 0.95, walk_pose(lt * 14, True))
        else:
            fall = ease((k - 0.7) / 0.8)
            p.c.save(); p.c.translate(bx - 70, ground); p.c.rotate(-fall * 1.45); robot(p, 0, 0, 0.95, dict(shL=-1.2, shR=1.2, head=0.3 * fall)); p.c.restore()
            if k < 3:
                for j in range(6):
                    ang = j * math.pi / 3 + k * 2; r = 60 + 20 * math.sin(k * 8)
                    star(p, bx - 20 + math.cos(ang) * r, ground - 260 + math.sin(ang) * r * 0.4, 12, AMBER, 1 - k / 3)
        p.text('9,58', 1060, 175, 40, DIM, 1, 'bold', 'center')
        caption(p, ['…pero', 'no', 'sabe', 'FRENAR'], k - 0.6, 80, 120, 52)

def star(p, x, y, r, rgb, a):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + math.cos(ang) * rr, y + math.sin(ang) * rr))
    p.poly(pts, rgb, 2, a, True, fill=rgb, fa=a)

CODE = ['brazo_izq.subir(90)', 'esperar(0.5)', 'girar(cadera, 30)', 'brazo_der.subir(90)', 'paso(izq)', 'paso(der)',
        'girar(cabeza, -20)', 'repetir(8)', 'brazos.abrir()', 'agacharse(0.4)', 'saltar()', 'fin_bucle']

def choreography(p, lt, t, d):
    ground = 560
    beat = lt * 2.2
    b = math.sin(beat * math.pi)
    pose = dict(shL=-(1.6 + 0.9 * b), elL=0.8 * b, shR=1.6 - 0.9 * b, elR=0.8 * b,
                hipL=-0.25 * b, hipR=0.25 * b, kneeL=-0.2 * abs(b), kneeR=-0.2 * abs(b), bob=abs(b) * 12, head=0.25 * b, tilt=0.08 * b)
    robot(p, 430, ground, 1.0, pose)
    p.line(250, ground, 610, ground, INK, 4)
    # notas musicales
    for i in range(4):
        k = ((lt + i * 0.8) % 3.2) / 3.2
        x = 300 + i * 90 + math.sin(k * 7) * 15; y = 300 - k * 200
        note(p, x, y, 1 - k)
    # panel de instrucciones
    px, py = 720, 170
    p.rect(px, py, 470, 390, DIM, 3, r=14, fill=(0.07, 0.12, 0.13))
    p.text('rutina_baile.py', px + 24, py + 40, 20, DIM, 1, 'normal', 'left', 'DejaVu Sans Mono')
    cur = int(lt * 1.6) % len(CODE)
    for i in range(8):
        j = (cur + i - 3) % len(CODE); y = py + 90 + i * 36
        on = (i == 3)
        if on: p.rect(px + 12, y - 25, 446, 34, TEAL, 0, r=6, fill=TEAL, fa=0.18)
        p.text(f'{j + 1:02d}  ' + CODE[j], px + 24, y, 21, TEAL if on else INK, 1 if on else 0.55, 'normal', 'left', 'DejaVu Sans Mono')
    caption(p, ['Son', 'COREOGRAFÍAS:', 'instrucciones', 'programadas'], lt - 0.5, 80, 120, 50)

def note(p, x, y, a):
    p.circle(x, y, 9, TEAL, 0, a, fill=TEAL, fa=a); p.line(x + 8, y, x + 8, y - 40, TEAL, 4, a); p.line(x + 8, y - 40, x + 26, y - 32, TEAL, 4, a)

if __name__ == '__main__':
    segs = [(0, 22, phone_marketing), (22, 56, sprint), (56, 90, choreography)]
    render(segs, 90, '/home/claude/anim/muestra_146.mp4', '/mnt/user-data/uploads/146_de_la_mano_de_los_robots.mp3', 540)
