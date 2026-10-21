"""Motor de animación vectorial para Carne de Bit: dibuja con cairo y envía fotogramas a ffmpeg."""
import cairo, math, subprocess

W, H, FPS = 1280, 720, 25
# Paleta
BG = (0.055, 0.102, 0.110)
GRID = (0.12, 0.19, 0.20)
INK = (0.92, 0.95, 0.94)
DIM = (0.55, 0.64, 0.63)
TEAL = (0.31, 0.76, 0.74)
AMBER = (0.95, 0.65, 0.35)
RED = (0.93, 0.42, 0.38)
FONT = 'Inter Display'

def ease(x):  # suave entrada/salida
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def clamp01(x): return max(0.0, min(1.0, x))

class Pen:
    def __init__(self, ctx): self.c = ctx
    def col(self, rgb, a=1.0): self.c.set_source_rgba(*rgb, a)
    def width(self, w): self.c.set_line_width(w)
    def line(self, x1, y1, x2, y2, rgb=INK, w=4, a=1.0):
        c = self.c; c.set_line_cap(cairo.LINE_CAP_ROUND); self.col(rgb, a); c.set_line_width(w)
        c.move_to(x1, y1); c.line_to(x2, y2); c.stroke()
    def poly(self, pts, rgb=INK, w=4, a=1.0, close=False, fill=None, fa=1.0):
        c = self.c; c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]
        if close: c.close_path()
        if fill is not None: self.col(fill, fa); c.fill_preserve()
        self.col(rgb, a); c.set_line_width(w); c.stroke()
    def rect(self, x, y, w, h, rgb=INK, lw=4, a=1.0, r=10, fill=None, fa=1.0):
        c = self.c; r = min(r, w / 2, h / 2)
        c.new_sub_path(); c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
        c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.close_path()
        if fill is not None: self.col(fill, fa); c.fill_preserve()
        if lw: self.col(rgb, a); c.set_line_width(lw); c.stroke()
        else: c.new_path()
    def circle(self, x, y, r, rgb=INK, w=4, a=1.0, fill=None, fa=1.0):
        c = self.c; c.new_sub_path(); c.arc(x, y, r, 0, 2 * math.pi)
        if fill is not None: self.col(fill, fa); c.fill_preserve()
        if w: self.col(rgb, a); c.set_line_width(w); c.stroke()
        else: c.new_path()
    def arc(self, x, y, r, a1, a2, rgb=INK, w=4, a=1.0):
        c = self.c; c.set_line_cap(cairo.LINE_CAP_ROUND); c.new_sub_path(); c.arc(x, y, r, a1, a2)
        self.col(rgb, a); c.set_line_width(w); c.stroke()
    def text(self, s, x, y, size=40, rgb=INK, a=1.0, weight='bold', align='left', font=FONT):
        c = self.c; c.select_font_face(font, cairo.FONT_SLANT_NORMAL,
                                         cairo.FONT_WEIGHT_BOLD if weight == 'bold' else cairo.FONT_WEIGHT_NORMAL)
        c.set_font_size(size); ext = c.text_extents(s)
        if align == 'center': x -= ext.x_advance / 2
        elif align == 'right': x -= ext.x_advance
        self.col(rgb, a); c.move_to(x, y); c.show_text(s); return ext.x_advance

def background(p, t):
    c = p.c; c.set_source_rgb(*BG); c.paint()
    # rejilla de puntos que deriva lentamente
    off = (t * 6) % 40
    c.set_source_rgba(*GRID, 1)
    for gx in range(-40, W + 40, 40):
        for gy in range(0, H + 40, 40):
            c.arc(gx + off, gy, 1.6, 0, 2 * math.pi); c.fill()

# ---------- personaje robot humanoide ----------
def limb(p, x, y, a1, a2, l1, l2, rgb=INK, w=7, a=1.0):
    """Dos segmentos articulados desde (x,y); ángulos en radianes desde la vertical hacia abajo."""
    x1, y1 = x + l1 * math.sin(a1), y + l1 * math.cos(a1)
    x2, y2 = x1 + l2 * math.sin(a1 + a2), y1 + l2 * math.cos(a1 + a2)
    p.poly([(x, y), (x1, y1), (x2, y2)], rgb, w, a)
    p.circle(x1, y1, w * 0.55, rgb, 0, a, fill=rgb, fa=a)
    return x2, y2

def robot(p, x, y, s=1.0, pose=None, a=1.0, eye=TEAL, body=INK):
    """Humanoide sencillo con los pies en (x, y). pose: dict de ángulos."""
    q = dict(hipL=0, kneeL=0, hipR=0, kneeR=0, shL=-0.15, elL=0.2, shR=0.15, elR=-0.2, tilt=0, bob=0, head=0)
    if pose: q.update(pose)
    c = p.c; c.save(); c.translate(x, y - q['bob'] * s); c.scale(s, s); c.rotate(q['tilt'])
    leg = 70
    # piernas
    limb(p, -12, -150, q['hipL'], q['kneeL'], leg, leg, body, 9, a)
    limb(p, 12, -150, q['hipR'], q['kneeR'], leg, leg, body, 9, a)
    # torso
    p.rect(-34, -250, 68, 105, body, 5, a, r=16, fill=BG, fa=a)
    p.circle(0, -205, 10, eye, 4, a)
    # brazos
    limb(p, -38, -238, q['shL'], q['elL'], 55, 55, body, 8, a)
    limb(p, 38, -238, q['shR'], q['elR'], 55, 55, body, 8, a)
    # cabeza
    c.save(); c.translate(0, -282); c.rotate(q['head'])
    p.rect(-30, -28, 60, 50, body, 5, a, r=18, fill=BG, fa=a)
    p.rect(-20, -14, 40, 16, eye, 0, a, r=8, fill=eye, fa=a)
    c.restore()
    c.restore()

def walk_pose(ph, run=False):
    k = 0.9 if run else 0.45
    return dict(hipL=k * math.sin(ph), kneeL=-max(0, k * 1.2 * math.sin(ph + 1.2)),
                hipR=k * math.sin(ph + math.pi), kneeR=-max(0, k * 1.2 * math.sin(ph + math.pi + 1.2)),
                shL=-k * 0.9 * math.sin(ph), elL=-0.9 if run else -0.3,
                shR=-k * 0.9 * math.sin(ph + math.pi), elR=-0.9 if run else -0.3,
                bob=abs(math.sin(ph)) * (12 if run else 5), tilt=0.12 if run else 0)

# ---------- textos ----------
def caption(p, words, lt, x=80, y=640, size=46, rgb=INK, accent=TEAL):
    """Palabras clave que aparecen una a una; lt = tiempo local."""
    xx = x
    for i, w in enumerate(words):
        k = ease((lt - 0.35 * i) / 0.4)
        if k <= 0: break
        p.c.save(); p.c.translate(0, (1 - k) * 18)
        xx += p.text(w + ' ', xx, y, size, accent if w.isupper() else rgb, k)
        p.c.restore()

def label(p, s, x, y, lt, size=22, rgb=DIM, align='left'):
    p.text(s, x, y, size, rgb, ease(lt / 0.5), 'normal', align, 'DejaVu Sans Mono')

# ---------- render ----------
def render(segments, dur, out, audio=None, audio_ss=0.0):
    """segments: lista de (inicio, fin, funcion(p, t_local, t_global, dur_seg))."""
    n = round(dur * FPS)
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-']
    if audio: cmd += ['-ss', str(audio_ss), '-t', str(dur), '-i', audio, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '160k']
    cmd += ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf); p = Pen(ctx)
    segs = sorted(segments, key=lambda s: s[0])
    for f in range(n):
        t = f / FPS
        background(p, t)
        for (a, b, fn) in segs:
            if a - 0.6 <= t < b + 0.6:
                fade = ease((t - a + 0.6) / 0.6) * ease((b + 0.6 - t) / 0.6)
                ctx.push_group(); fn(p, max(0.0, t - a), t, b - a); ctx.pop_group_to_source(); ctx.paint_with_alpha(fade)
        surf.flush(); proc.stdin.write(bytes(surf.get_data()))
    proc.stdin.close(); proc.wait()
