# common.py
import omni
from pxr import UsdPhysics

def set_drive_parameters(drive, target_type, target_value, stiffness=None, damping=None, max_force=None):
    """Enable velocity drive for a given joint"""
    if target_type == "position":
        if not drive.GetTargetPositionAttr():
            drive.CreateTargetPositionAttr(target_value)
        else:
            drive.GetTargetPositionAttr().Set(target_value)
    elif target_type == "velocity":
        if not drive.GetTargetVelocityAttr():
            drive.CreateTargetVelocityAttr(target_value)
        else:
            drive.GetTargetVelocityAttr().Set(target_value)

    if stiffness is not None:
        if not drive.GetStiffnessAttr():
            drive.CreateStiffnessAttr(stiffness)
        else:
            drive.GetStiffnessAttr().Set(stiffness)

    if damping is not None:
        if not drive.GetDampingAttr():
            drive.CreateDampingAttr(damping)
        else:
            drive.GetDampingAttr().Set(damping)

    if max_force is not None:
        if not drive.GetMaxForceAttr():
            drive.CreateMaxForceAttr(max_force)
        else:
            drive.GetMaxForceAttr().Set(max_force)
