from python_qt_binding import QtCore
from python_qt_binding import QtWidgets



class AwAbstructWindow(QtWidgets.QMainWindow):

    def __init__(self, guimgr, launch_path):
        super(AwAbstructWindow, self).__init__()
        self.guimgr = guimgr
        self.launch = guimgr.client.launch.mirror(launch_path)

    def load_geomerty(self):
        settings = QtCore.QSettings("Autoware", "AutowareLauncher")
        if settings.contains("geometry"):
            self.restoreGeometry(settings.value("geometry"))

    def save_geometry(self):
        settings = QtCore.QSettings("Autoware", "AutowareLauncher")
        settings.setValue("geometry", self.saveGeometry())



class AwAbstructPanel(QtWidgets.QWidget):

    def __init__(self, guimgr, launch_path):
        super(AwAbstructPanel, self).__init__()
        self.guimgr      = guimgr
        self.launch_path = launch_path

        # Panel Footer
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        layout.addStretch()
        self.footer = QtWidgets.QWidget()
        self.footer.setLayout(layout)

        # Panel Layout
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        layout.addStretch()
        layout.addWidget(self.footer)
        self.setLayout(layout)

    def add_frame(self, frame):
        index = self.layout().count() - 2
        self.layout().insertWidget(index, frame)

    def add_button(self, button):
        self.footer.layout().addWidget(button)

    def add_node_button(self):
        button = QtWidgets.QPushButton("Create")
        self.add_button(button)
        def temp():
            window = AwPluginSelectWindow(self.guimgr, self.launch, self)
            window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            window.setWindowModality(QtCore.Qt.ApplicationModal)
            window.show()
        button.clicked.connect(temp)



class AwAbstructFrame(QtWidgets.QWidget):

    def __init__(self, guimgr, launch_path):
        super(AwAbstructFrame, self).__init__()
        self.guimgr      = guimgr
        self.launch_path = launch_path

        # Frame Header
        self.title = QtWidgets.QLabel("No Title")
        self.title.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        layout = self.guimgr.create_frame_header_hlayout()
        layout.addWidget(self.title)
        self.header = QtWidgets.QWidget()
        self.header.setObjectName("FrameHeader")
        self.header.setLayout(layout)

        # Frame Layout
        layout = self.guimgr.create_frame_entire_vlayout()
        layout.addWidget(self.header)
        self.setLayout(layout)

    def set_title(self, title):
        self.title.setText(title)

    def add_widget(self, widget):
        widget.setObjectName("FrameWidget")
        self.layout().addWidget(widget)

    def add_text_widget(self, text):
        layout = self.guimgr.create_frame_header_hlayout()
        layout.addWidget(QtWidgets.QLabel(text))
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.add_widget(widget)

    def add_button(self, button):
        self.header.layout().addWidget(button)

    def add_config_button(self):

        button = QtWidgets.QPushButton("Config")
        button.clicked.connect(self.guimgr.create_window_open_event(self))
        self.add_button(button)