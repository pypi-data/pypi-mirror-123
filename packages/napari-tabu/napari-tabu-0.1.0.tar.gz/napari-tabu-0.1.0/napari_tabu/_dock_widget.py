"""
This module is an example of a barebones QWidget plugin for napari

It implements the ``napari_experimental_provide_dock_widget`` hook specification.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs.
"""
# from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import QWidget, QHBoxLayout, QPushButton
from magicgui import magic_factory


class SendBackWidget(QWidget):
    def __init__(self, napari_viewer, napari_child_viewer):
        super().__init__()
        self.viewer = napari_viewer
        self.child_viewer = napari_child_viewer

        btn = QPushButton("Send current layer back to main napari")
        btn.clicked.connect(self._on_click)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(btn)

    def _on_click(self):
        for l in self.child_viewer.layers.selection:
            self.viewer.add_layer(l)


#@napari_hook_implementation
#def napari_experimental_provide_dock_widget():
#    # you can return either a single widget, or a sequence of widgets
#    return [ExampleQWidget, example_magic_widget]
