# configuration_ui.py
import omni.ui as ui
import omni.timeline
from omni.isaac.ui.element_wrappers import CollapsableFrame, FloatField, Button
from omni.isaac.ui.ui_utils import get_style
from pxr import UsdPhysics, PhysxSchema
from .common import set_drive_parameters

class UIBuilder:
    def __init__(self):
        self.frames = []
        self.wrapped_ui_elements = []
        self._timeline = omni.timeline.get_timeline_interface()
        self._joint_num = 6
        self._reward_text = None
        self._episode_text = None

    def build_ui(self):
        target_angle_frame = CollapsableFrame("Target Angle", collapsed=False)
        with target_angle_frame:
            with ui.VStack(style=get_style(), spacing=5, height=0):
                self._angle_index = []
                for i in range(1, self._joint_num + 1):
                    angle_field = FloatField(
                        label=f"Joint{i} target angle",
                        tooltip="Joint target angle",
                        default_value="0.00",
                        on_value_changed_fn=self._on_joint_angle_changed
                    )
                    self._angle_index.append(angle_field)
                    self.wrapped_ui_elements.append(angle_field)

                self._load_target_angle_btn = Button(
                    label="Set the target angle",
                    text="Setting",
                    on_click_fn=self._on_config_drives_by_value
                )
                self.wrapped_ui_elements.append(self._load_target_angle_btn)

                self._reward_text = FloatField(label="Reward", default_value="0.0")
                self.wrapped_ui_elements.append(self._reward_text)
                
                self._episode_text = FloatField(label="Episode", default_value="0")
                self.wrapped_ui_elements.append(self._episode_text)

    def update_training_info(self, reward, episode):
        if self._reward_text:
            self._reward_text.model.set_value(str(reward))
        if self._episode_text:
            self._episode_text.model.set_value(str(episode))

    def _on_joint_angle_changed(self, value):
        self._joint_angle = value

    def _on_config_robot(self):
        self._joint_path_index = [
            '/Root/KR20/Robot/A1/node_/mesh_/R1',
            '/Root/KR20/Robot/A2/node_/mesh_/R2',
            '/Root/KR20/Robot/A3/node_/mesh_/R3',
            '/Root/KR20/Robot/A4/node_/mesh_/R4',
            '/Root/KR20/Robot/A5/node_/mesh_/R5',
            '/Root/KR20/Robot/A6/node_/mesh_/R6'
        ]

        self._joint_target_position_index = []
        for angle in self._angle_index:
            self._joint_target_position_index.append(angle.get_value())

        stage = omni.usd.get_context().get_stage()
        self._joint_name_index = []
        PhysxSchema.PhysxArticulationAPI.Get(stage, '/Root/KR20').CreateSolverPositionIterationCountAttr(64)
        PhysxSchema.PhysxArticulationAPI.Get(stage, '/Root/KR20').CreateSolverVelocityIterationCountAttr(64)
        for i in range(len(self._joint_path_index)):
            joint_name = f"R{i}"
            joint = UsdPhysics.DriveAPI.Get(stage.GetPrimAtPath(f"{self._joint_path_index[i]}"), "angular")
            set_drive_parameters(joint, "position", 0, stiffness=5000, damping=10000)
            self._joint_name_index.append(joint)

    def _on_config_drives_by_value(self):
        self._on_config_robot()
        for i in range(len(self._joint_name_index)):
            set_drive_parameters(self._joint_name_index[i], "position", self._joint_target_position_index[i])
