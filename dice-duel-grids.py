import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white

out = sys.argv[1]
A, A_L = HexColor("#4e79d6"), HexColor("#cfdcf7")
B, B_L = HexColor("#e0812f"), HexColor("#f8dcc2")
GRAY = HexColor("#444444")

W, H = letter
c = canvas.Canvas(out, pagesize=letter)
c.setTitle("Dice Duel worksheet")

c.setFont("Helvetica-Bold", 18); c.setFillColor(GRAY)
c.drawCentredString(W/2, H-42, "Dice Duel")
c.setFont("Helvetica", 9.5)
c.drawCentredString(W/2, H-57, "Faces: whole numbers 0-6 adding to 21. Mark each square A, B, or - (tie). "
                    "Higher number earns 1 point; a tie gives ½ to each.")

cell = 26
cols, rows = 2, 3
top = H - 76
block_h = (top - 24) / rows
col_w = (W - 72) / cols
grid_w = 7 * cell

for k in range(6):
    r, q = divmod(k, cols)
    x0 = 36 + q*col_w + (col_w - grid_w)/2
    y_top = top - r*block_h - 6
    # header row (B faces) and header column (A faces)
    for i in range(7):
        for j in range(7):
            x = x0 + j*cell
            y = y_top - (i+1)*cell
            if i == 0 and j == 0:
                fill, stroke = white, GRAY
            elif i == 0:
                fill, stroke = B_L, B
            elif j == 0:
                fill, stroke = A_L, A
            else:
                fill, stroke = white, GRAY
            c.setFillColor(fill); c.setStrokeColor(stroke); c.setLineWidth(0.8)
            c.rect(x, y, cell, cell, fill=1, stroke=1)
    # corner label
    c.setFillColor(A); c.setFont("Helvetica-Bold", 10)
    c.drawString(x0 + 3, y_top - cell + 4, "A")
    c.setFillColor(GRAY); c.drawCentredString(x0 + cell/2, y_top - cell/2 - 3.5, "\\")
    c.setFillColor(B); c.drawRightString(x0 + cell - 3, y_top - 11, "B")
    # thicker outline around the 6x6 play area
    c.setStrokeColor(GRAY); c.setLineWidth(1.6)
    c.rect(x0 + cell, y_top - 7*cell, 6*cell, 6*cell, fill=0, stroke=1)
    # tally line (wins and ties), then score line
    yt = y_top - 7*cell - 17
    c.setFont("Helvetica", 10)
    c.setFillColor(A); c.drawString(x0, yt, "A wins: ____")
    c.setFillColor(GRAY); c.drawCentredString(x0 + grid_w/2, yt, "Ties: ____")
    c.setFillColor(B); c.drawRightString(x0 + grid_w, yt, "B wins: ____")
    ys = yt - 17
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(A); c.drawString(x0, ys, "A score: ______")
    c.setFillColor(B); c.drawRightString(x0 + grid_w, ys, "B score: ______")

c.save()
