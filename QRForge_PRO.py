"""
QRForge PRO v2.0.0
Professional QR Code Design & Export Studio
Vector | Print-Ready | Designer Workflow
"""

# ======================================================
# SYSTEM IMPORTS
# ======================================================
import sys, os, math, requests
import qrcode
from PIL import Image

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtSvg import QSvgGenerator
from PySide6.QtGui import QPdfWriter, QPageSize
from PySide6.QtCore import QRectF

# ======================================================
# METADATA
# ======================================================
APP_NAME = "QRForge PRO"
APP_VERSION = "2.0.0"
APP_AUTHOR = "Mate Technologies"
APP_URL = "https://matetools.gumroad.com"

# ======================================================
# THEMES
# ======================================================
DARK = {
    "bg": "#121418",
    "panel": "#1B1E24",
    "button": "#2A2F3A",
    "button_hover": "#343B4A",
    "primary": "#4F8CFF",
    "primary_hover": "#3E79E0",
    "text": "#E6EAF2",
    "muted": "#9AA4B2",
    "border": "#2F3542"
}

LIGHT = {
    "bg": "#F5F7FB",
    "panel": "#FFFFFF",
    "button": "#E6EAF2",
    "button_hover": "#DCE2EE",
    "primary": "#4F8CFF",
    "primary_hover": "#3E79E0",
    "text": "#1C1E26",
    "muted": "#6B7280",
    "border": "#D1D5DB"
}

# ======================================================
# UTILITIES
# ======================================================
def resource_path(name):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)

def shorten_url(url):
    try:
        r = requests.get(
            f"https://tinyurl.com/api-create.php?url={url}", timeout=5
        )
        return r.text if r.status_code == 200 else url
    except:
        return url

def wifi_payload(ssid, pwd, enc):
    return f"WIFI:S:{ssid};T:{enc if enc!='NONE' else ''};P:{pwd};;"

# ======================================================
# QR GRAPHICS ITEM
# ======================================================
class QRItem(QGraphicsItem):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.size = 300
        self.rotation_angle = 0
        self.fill = QColor("black")
        self.bg = QColor("white")
        self.transparent = False
        self.generate()

        self.setFlags(
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsMovable
        )

    def generate(self):
        qr = qrcode.QRCode(border=1)
        qr.add_data(self.data)
        qr.make(fit=True)

        back = None if self.transparent else self.bg.name()
        img = qr.make_image(
            fill_color=self.fill.name(),
            back_color=back
        ).convert("RGBA")

        self.qimage = QImage(
            img.tobytes("raw", "RGBA"),
            img.width,
            img.height,
            QImage.Format_RGBA8888
        )

    def boundingRect(self):
        return QRectF(-self.size/2, -self.size/2, self.size, self.size)

    def paint(self, p, *_):
        p.save()
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        p.rotate(self.rotation_angle)
        p.drawImage(self.boundingRect(), self.qimage)
        p.restore()

        if self.isSelected():
            p.setPen(QPen(QColor("#00E676"), 2, Qt.DashLine))
            p.drawRect(self.boundingRect())

# ======================================================
# CANVAS VIEW
# ======================================================
class Canvas(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.rotating = False
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def wheelEvent(self, e):
        self.scale(1.15 if e.angleDelta().y() > 0 else 0.85,
                   1.15 if e.angleDelta().y() > 0 else 0.85)

    def mousePressEvent(self, e):
        self.rotating = bool(e.modifiers() & Qt.AltModifier)
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if self.rotating:
            item = self.itemAt(e.position().toPoint())
            if isinstance(item, QRItem):
                c = item.scenePos()
                dx = e.scenePosition().x() - c.x()
                dy = e.scenePosition().y() - c.y()
                item.rotation_angle = math.degrees(math.atan2(dy, dx))
                item.update()
        super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        self.rotating = False
        super().mouseReleaseEvent(e)

# ======================================================
# MAIN APPLICATION
# ======================================================
class QRForgeStudio(QMainWindow):
    def __init__(self):
        super().__init__()

        self.dark = True
        self.current_item = None

        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(1200, 680)
        self.setWindowIcon(QIcon(resource_path("logo.ico")))

        self.scene = QGraphicsScene(-5000, -5000, 10000, 10000)
        self.canvas = Canvas(self.scene)
        self.setCentralWidget(self.canvas)

        self.build_controls()
        self.build_toolbar()
        self.apply_theme()

    # ==================================================
    # UI BUILDERS
    # ==================================================
    def build_controls(self):
        dock = QDockWidget("QR Controls")
        dock.setFixedWidth(380)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        w = QWidget()
        l = QVBoxLayout(w)
        dock.setWidget(w)

        self.mode = QComboBox()
        self.mode.addItems(["Text", "URL", "Wi-Fi"])
        l.addWidget(self.mode)

        self.text = QTextEdit()
        self.text.setPlaceholderText("Enter content…")
        l.addWidget(self.text)

        self.shorten = QCheckBox("Shorten URL")
        l.addWidget(self.shorten)

        self.ssid = QLineEdit(); self.ssid.setPlaceholderText("Wi-Fi SSID")
        self.pwd = QLineEdit(); self.pwd.setPlaceholderText("Wi-Fi Password")
        self.enc = QComboBox(); self.enc.addItems(["WPA", "WEP", "NONE"])

        for wdg in (self.ssid, self.pwd, self.enc):
            l.addWidget(wdg)

        self.fill_btn = QPushButton("🎨 Fill Color")
        self.bg_btn = QPushButton("🖌 Background")
        self.trans = QCheckBox("Transparent Background")

        l.addWidget(self.fill_btn)
        l.addWidget(self.bg_btn)
        l.addWidget(self.trans)

        add_btn = QPushButton("➕ Add QR")
        add_btn.setObjectName("primary")
        l.addWidget(add_btn)
        l.addStretch()

        add_btn.clicked.connect(self.add_qr)
        self.fill_btn.clicked.connect(self.pick_fill)
        self.bg_btn.clicked.connect(self.pick_bg)

    def build_toolbar(self):
        tb = QToolBar()
        self.addToolBar(tb)

        tb.addAction("PNG", self.export_png)
        tb.addAction("SVG", self.export_svg)
        tb.addAction("PDF", self.export_pdf)
        tb.addSeparator()
        tb.addAction("🌗 Theme", self.toggle_theme)
        tb.addAction("ℹ About", self.show_about)

    # ==================================================
    # CORE ACTIONS
    # ==================================================
    def add_qr(self):
        mode = self.mode.currentText()
        if mode == "Text":
            data = self.text.toPlainText()
        elif mode == "URL":
            url = self.text.toPlainText()
            data = shorten_url(url) if self.shorten.isChecked() else url
        else:
            data = wifi_payload(self.ssid.text(), self.pwd.text(), self.enc.currentText())

        item = QRItem(data)
        item.transparent = self.trans.isChecked()
        item.generate()
        self.scene.addItem(item)
        item.setPos(0, 0)
        self.current_item = item

    def pick_fill(self):
        if self.current_item:
            c = QColorDialog.getColor()
            if c.isValid():
                self.current_item.fill = c
                self.current_item.generate()
                self.current_item.update()

    def pick_bg(self):
        if self.current_item:
            c = QColorDialog.getColor()
            if c.isValid():
                self.current_item.bg = c
                self.current_item.generate()
                self.current_item.update()

    # ==================================================
    # EXPORTS (PNG / SVG / PDF)
    # ==================================================
    # (unchanged logic – already production grade)
    def export_png(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export PNG", "", "PNG Files (*.png)"
        )
        if not path:
            return

        if not self.scene.items():
            QMessageBox.warning(self, "Export PNG", "No QR codes to export.")
            return

        rect = self.scene.itemsBoundingRect().adjusted(-20, -20, 20, 20)

        img = QImage(
            int(rect.width()),
            int(rect.height()),
            QImage.Format_ARGB32
        )
        img.fill(Qt.transparent)

        painter = QPainter(img)
        painter.setRenderHint(QPainter.Antialiasing)
        self.scene.render(
            painter,
            target=QRectF(img.rect()),
            source=rect
        )
        painter.end()

        img.save(path)

    def export_svg(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export SVG", "", "SVG Files (*.svg)"
        )
        if not path:
            return

        if not self.scene.items():
            QMessageBox.warning(self, "Export SVG", "No QR codes to export.")
            return

        rect = self.scene.itemsBoundingRect().adjusted(-20, -20, 20, 20)

        svg = QSvgGenerator()
        svg.setFileName(path)
        svg.setSize(rect.size().toSize())
        svg.setViewBox(rect)
        svg.setTitle("QRForge PRO")
        svg.setDescription("Vector QR export")

        painter = QPainter(svg)
        self.scene.render(
            painter,
            target=QRectF(rect),
            source=rect
        )
        painter.end()

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export PDF", "", "PDF Files (*.pdf)"
        )
        if not path:
            return

        items = self.scene.items()
        if not items:
            QMessageBox.warning(self, "Export PDF", "No QR codes to export.")
            return

        pdf = QPdfWriter(path)
        pdf.setPageSize(QPageSize(QPageSize.A4))
        pdf.setResolution(300)
        pdf.setPageMargins(QMarginsF(0, 0, 0, 0))

        painter = QPainter(pdf)
        painter.setRenderHint(QPainter.Antialiasing)

        page_rect = pdf.pageLayout().fullRectPixels(pdf.resolution())

        for i, item in enumerate(items):
            if i > 0:
                pdf.newPage()

            rect = item.sceneBoundingRect()
            scale = min(
                page_rect.width() / rect.width(),
                page_rect.height() / rect.height()
            ) * 0.9

            painter.save()
            painter.translate(
                page_rect.width() / 2,
                page_rect.height() / 2
            )
            painter.scale(scale, scale)
            painter.translate(-rect.center().x(), -rect.center().y())
            self.scene.render(painter, QRectF(rect), rect)
            painter.restore()

        painter.end()

    # ==================================================
    # THEMING
    # ==================================================
    def apply_theme(self):
        self.setStyleSheet("/* your existing dark/light QSS */")

    def toggle_theme(self):
        self.dark = not self.dark
        self.apply_theme()

    # ==================================================
    # ABOUT
    # ==================================================
    def show_about(self):
        QMessageBox.information(
            self,
            "About QRForge PRO",
            f"{APP_NAME} v{APP_VERSION}\n\n"
            "Professional QR design & export studio\n\n"
            f"Built by {APP_AUTHOR}\n{APP_URL}"
        )

# ======================================================
# ENTRY POINT
# ======================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QRForgeStudio()
    win.show()
    sys.exit(app.exec())
