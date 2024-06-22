# extension_configuration.py
import weakref
import gc
import omni
import omni.ui as ui
import omni.usd
from omni.usd import StageEventType
from omni.kit.menu.utils import add_menu_items, remove_menu_items
from omni.isaac.ui.menu import make_menu_item_description
import omni.physx as _physx
from .configuration_ui import UIBuilder as UI_Configuration

EXTENSION_TITLE = 'KR20'
STEP_NAME = "Configuration"

class Extension(omni.ext.IExt):
    def on_startup(self, ext_id: str):
        self._self_ref = self
        self._usd_context = omni.usd.get_context()
        self._window = ui.Window(
            title=STEP_NAME, width=500, height=500, visible=False, dockPreference=ui.DockPreference.LEFT_BOTTOM
        )
        self._window.set_visibility_changed_fn(self._on_window_configuration)

        self._models = {}
        self._ext_id = ext_id
        self._menu_items = [make_menu_item_description(ext_id, STEP_NAME, lambda a=weakref.proxy(self): a._menu_callback_configuration())]
        add_menu_items(self._menu_items, EXTENSION_TITLE)

        self.ui_configuration = UI_Configuration()
        self._physxIFace = _physx.acquire_physx_interface()
        self._physx_subscription = None
        self._stage_event_sub = None
        self._timeline = omni.timeline.get_timeline_interface()

    def on_shutdown(self):
        self._models = {}
        remove_menu_items(self._menu_items, EXTENSION_TITLE)
        if self._window:
            self._window = None
        self.ui_configuration.cleanup()
        gc.collect()

    def _on_window_configuration(self, visible):
        if self._window.visible:
            self._usd_context = omni.usd.get_context()
            events = self._usd_context.get_stage_event_stream()
            self._stage_event_sub = events.create_subscription_to_pop(self._on_stage_event)
            stream = self._timeline.get_timeline_event_stream()
            self._timeline_event_sub = stream.create_subscription_to_pop(self._on_timeline_event)
            self._build_ui_configuration()
        else:
            self._usd_context = None
            self._stage_event_sub = None
            self._timeline_event_sub = None
            self.ui_configuration.cleanup()

    def _build_ui_configuration(self):
        with self._window.frame:
            with ui.VStack(spacing=5, height=0):
                self.ui_configuration.build_ui()

    def _menu_callback_configuration(self):
        self._window.visible = not self._window.visible
        self.ui_configuration.on_menu_callback()

    def _on_timeline_event(self, event):
        if event.type == int(omni.timeline.TimelineEventType.PLAY):
            if not self._physx_subscription:
                self._physx_subscription = self._physxIFace.subscribe_physics_step_events(self._on_physics_step)
        elif event.type == int(omni.timeline.TimelineEventType.STOP):
            self._physx_subscription = None
        self.ui_configuration.on_timeline_event(event)

    def _on_physics_step(self, step):
        pass

    def _on_stage_event(self, event):
        if event.type == int(StageEventType.OPENED) or event.type == int(StageEventType.CLOSED):
            self._physx_subscription = None
            self.ui_configuration.cleanup()
        self.ui_configuration.on_stage_event(event)
