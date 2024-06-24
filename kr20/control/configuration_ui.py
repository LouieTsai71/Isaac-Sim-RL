import omni.ui as ui
import omni.timeline
import math,time
from omni.usd import StageEventType
from omni.isaac.ui.element_wrappers import CollapsableFrame, StateButton
from omni.isaac.ui import StringField, Button, IntField, FloatField
from omni.isaac.ui.element_wrappers.core_connectors import LoadButton, ResetButton
from omni.isaac.core.utils.stage import add_reference_to_stage, create_new_stage
from omni.isaac.core.world import World
from omni.isaac.ui.ui_utils import get_style
from omni.client import get_local_file, write_file


from pxr import UsdLux, Sdf, Gf, UsdPhysics, PhysxSchema
from .common import set_drive_parameters
from .your_script import parameters

listener_future = []
data_u_want_to_transfer = []

class UIBuilder:
    def __init__(self):
        #self._arc_status = self.get_txt_from_Nucleus()
        # Frames are sub-windows that can contain multiple UI elements
        self.frames = []
        # UI elements created using a UIElementWrapper instance
        self.wrapped_ui_elements = []
        # Get access to the timeline to control stop/pause/play programmatically
        self._timeline = omni.timeline.get_timeline_interface()
        self._joint_num = 6
   
    def on_menu_callback(self):
        pass

    def on_timeline_event(self, event):
        pass

    def on_stage_event(self, event):
        pass

    def on_physics_step(self, step: float):
        pass
    
    def cleanup(self):
        for ui_elem in self.wrapped_ui_elements:
            ui_elem.cleanup()
    
    def build_ui(self):        
        target_angle_frame = CollapsableFrame("Target Angle", collapsed=False)
        """
        Control the digital robot position, but need to adjust a kinematic solver to allow user give the position directly. 
        """
        with target_angle_frame:
            with ui.VStack(style=get_style(), spacing=5, height=0):
                self._angle_index = []
                for i in range(1, self._joint_num + 1):
                    self._angle = f"_joint_angle_{i}"
                    self._angle = FloatField(
                        label=f"Joint{i} target angle",
                        tooltip="Joint target angle",
                        default_value="0.00",                            
                        on_value_changed_fn = self._on_joint_angle_changed
                    )
                    self._angle_index.append(self._angle)
                    self.wrapped_ui_elements.append(self._angle)
                
                self._load_target_angle_btn = Button(
                    label = "Set the target angle",
                    text = "Setting", 
                    on_click_fn=self._on_config_drives_by_value
                    )
                self.wrapped_ui_elements.append(self._load_target_angle_btn)

                self._test_btn = Button(
                    label = "Propagate value from other scripts",
                    text = "Test", 
                    on_click_fn=self.data_value
                    )
                self.wrapped_ui_elements.append(self._test_btn)

     
########################################################
# Functions Below This Point is joint animation related#
########################################################        
    def _on_joint_angle_changed(self, value):
        self._joint_angle = value

    def _on_config_robot(self):
        """
        Config the robot controller.
        """
        self._joint_path_index = ['/Root/KR20/Robot/A1/node_/mesh_/R1',
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
            self.joint_name = f"R{i}"
            self.joint_name = UsdPhysics.DriveAPI.Get(stage.GetPrimAtPath(f"{self._joint_path_index[i]}"), "angular")
            set_drive_parameters(self.joint_name, "position", math.degrees(0), math.radians(5e3), math.radians(1e4))
            self._joint_name_index.append(self.joint_name)
            # print(self._joint_name_index)

    
    def _on_config_drives_by_value(self):
        self._on_config_robot()
        # print(self._joint_path_index, self._joint_configuration_index)
        for i in range(len(self._joint_name_index)):
           set_drive_parameters(self._joint_name_index[i], "position", self._joint_target_position_index[i])

    def data_value(self):
        Joint_data = 1
        self.data = parameters(Joint_data)
        print(self.data)

        

    
    
