"""Primitivas reutilizables: personas, cajas, iconos, flechas."""
import math, random
from engine import *

def person(p, x, y, s=1.0, pose=None, a=1.0, rgb=INK, kid=False):
    q = dict(hipL=-0.12, kneeL=0, hipR=0.12, kneeR=0, shL=-0.25, elL=0.1, shR=0.25, elR=-0.1, bob=0, tilt=0)
    if pose: q.update(pose)
    c = p.c; c.save(); c.translate(x, y - q['bob'] * s); c.scale(s, s); c.rotate(q['tilt'])
    leg, arm = (55, 40) if kid else (70, 52)
    hip = -2 * leg; neck = hip - (75 if kid else 100)
    limb(p, 0, hip, q['hipL'], q['kneeL'], leg, leg, rgb, 7, a)
    limb(p, 0, hip, q['hipR'], q['kneeR'], leg, leg, rgb, 7, a)
    p.line(0, hip, 0, neck, rgb, 7, a)
    limb(p, 0, neck + 10, q['shL'], q['elL'], arm, arm, rgb, 6, a)
    limb(p, 0, neck + 10, q['shR'], q['elR'], arm, arm, rgb, 6, a)
    p.circle(0, neck - 26, 24 if kid else 26, rgb, 6, a, fill=BG, fa=a)
    c.restore()

def box(p, x, y, w=70, h=55, rgb=AMBER, a=1.0):
    p.rect(x - w / 2, y - h, w, h, rgb, 4, a, r=5, fill=(0.16, 0.13, 0.09), fa=a)
    p.line(x - w / 2, y - h + 14, x + w / 2, y - h + 14, rgb, 3, a * 0.8)
    p.line(x, y - h, x, y - h + 14, rgb, 3, a * 0.8)

def arrow(p, x1, y1, x2, y2, rgb=TEAL, w=4, a=1.0, head=16):
    p.line(x1, y1, x2, y2, rgb, w, a)
    ang = math.atan2(y2 - y1, x2 - x1)
    p.poly([(x2 - head * math.cos(ang - 0.45), y2 - head * math.sin(ang - 0.45)), (x2, y2),
            (x2 - head * math.cos(ang + 0.45), y2 - head * math.sin(ang + 0.45))], rgb, w, a)

def dashed(p, x1, y1, x2, y2, rgb=TEAL, w=3, a=1.0, dash=12, off=0):
    c = p.c; c.set_dash([dash, dash], off); p.line(x1, y1, x2, y2, rgb, w, a); c.set_dash([])

def wheel_robot(p, x, y, s=1.0, a=1.0, ang=0.0, arm=None):
    c = p.c; c.save(); c.translate(x, y); c.scale(s, s)
    p.rect(-70, -90, 140, 62, INK, 5, a, r=14, fill=BG, fa=a)
    p.rect(-40, -78, 80, 20, TEAL, 0, a, r=10, fill=TEAL, fa=a)
    for wx in (-42, 42):
        p.circle(wx, -22, 22, INK, 5, a, fill=BG, fa=a)
        p.line(wx, -22, wx + 16 * math.cos(ang), -22 + 16 * math.sin(ang), INK, 4, a)
    if arm is not None:  # brazo con ventosa: arm = (a1, a2)
        x2, y2 = limb(p, 30, -90, arm[0], arm[1], 70, 60, INK, 7, a)
        p.line(x2 - 14, y2, x2 + 14, y2, TEAL, 6, a)
    c.restore()

def robot_arm(p, x, y, a1, a2, a3=0.0, s=1.0, a=1.0, grip=0.5, rgb=INK):
    """Brazo industrial anclado en (x,y); ángulos desde la vertical hacia arriba."""
    c = p.c; c.save(); c.translate(x, y); c.scale(s, s)
    p.rect(-55, -30, 110, 30, rgb, 5, a, r=8, fill=BG, fa=a)
    L1, L2 = 150, 120
    x1, y1 = L1 * math.sin(a1), -30 - L1 * math.cos(a1)
    x2, y2 = x1 + L2 * math.sin(a1 + a2), y1 - L2 * math.cos(a1 + a2)
    p.line(0, -30, x1, y1, rgb, 16, a); p.line(x1, y1, x2, y2, rgb, 12, a)
    p.circle(0, -30, 14, rgb, 5, a, fill=BG, fa=a); p.circle(x1, y1, 12, TEAL, 5, a, fill=BG, fa=a)
    g = a1 + a2 + a3
    tx, ty = x2 + 26 * math.sin(g), y2 - 26 * math.cos(g)
    p.line(x2, y2, tx, ty, rgb, 8, a)
    nx, ny = math.cos(g), math.sin(g)
    o = 10 + 14 * grip
    for sgn in (-1, 1):
        bx, by = tx + sgn * o * nx, ty + sgn * o * ny
        p.line(bx, by, bx + 26 * math.sin(g), by - 26 * math.cos(g), rgb, 7, a)
    c.restore()
    return x + s * (tx + 40 * math.sin(g)), y + s * (ty - 40 * math.cos(g))

def bubble(p, x, y, w, h, a=1.0, rgb=INK, tail=-1):
    p.rect(x, y, w, h, rgb, 4, a, r=22, fill=BG, fa=a)
    tx = x + (40 if tail < 0 else w - 40)
    p.poly([(tx - 12, y + h - 1), (tx + tail * -4 + (-20 if tail < 0 else 20), y + h + 26), (tx + 14, y + h - 1)], rgb, 4, a, fill=BG, fa=a)
    p.line(tx - 10, y + h - 2, tx + 12, y + h - 2, BG, 6, a)

def dots(p, x, y, lt, rgb=INK, a=1.0):
    for i in range(3):
        k = 0.5 + 0.5 * math.sin(lt * 6 - i * 0.8)
        p.circle(x + i * 26, y - 6 * k, 7, rgb, 0, a * (0.4 + 0.6 * k), fill=rgb, fa=a * (0.4 + 0.6 * k))

def heart(p, x, y, s, a=1.0, rgb=RED):
    c = p.c; c.save(); c.translate(x, y); c.scale(s / 20, s / 20)
    c.move_to(0, 12); c.curve_to(-22, -4, -12, -22, 0, -10); c.curve_to(12, -22, 22, -4, 0, 12)
    p.col(rgb, a); c.fill(); c.restore()

def star(p, x, y, r, rgb, a):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + math.cos(ang) * rr, y + math.sin(ang) * rr))
    p.poly(pts, rgb, 2, a, True, fill=rgb, fa=a)

def note(p, x, y, a, rgb=TEAL):
    p.circle(x, y, 9, rgb, 0, a, fill=rgb, fa=a); p.line(x + 8, y, x + 8, y - 40, rgb, 4, a); p.line(x + 8, y - 40, x + 26, y - 32, rgb, 4, a)

def ground(p, y=560, x1=0, x2=W, a=1.0): p.line(x1, y, x2, y, INK, 4, a)

def mono(p, s, x, y, size=22, rgb=INK, a=1.0, align='left'):
    p.text(s, x, y, size, rgb, a, 'normal', align, 'DejaVu Sans Mono')

def appear(lt, start, dur=0.5): return ease((lt - start) / dur)

def hand(p, x, y, s=1.0, a=1.0, rgb=INK, open_=1.0, flip=1):
    """Mano humana esquemática (palma + dedos) vista de lado, apuntando a la derecha si flip=1."""
    c = p.c; c.save(); c.translate(x, y); c.scale(s * flip, s)
    p.rect(-60, -35, 70, 70, rgb, 5, a, r=22, fill=BG, fa=a)
    for i, fy in enumerate((-26, -9, 8, 24)):
        ln = 62 - abs(i - 1.3) * 8
        curl = (1 - open_) * 0.9
        x1, y1 = 10, fy
        x2, y2 = x1 + ln * 0.55, fy
        x3, y3 = x2 + ln * 0.45 * math.cos(curl), fy + ln * 0.45 * math.sin(curl)
        p.poly([(x1, y1), (x2, y2), (x3, y3)], rgb, 9, a)
    p.poly([(-20, -35), (0, -62), (26, -70)], rgb, 9, a)  # pulgar
    c.restore()
