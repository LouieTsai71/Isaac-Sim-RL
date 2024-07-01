import omni.isaac.lab.sim as sim_utils
from omni.isaac.lab.actuators import ImplicitActuatorCfg
from omni.isaac.lab.assets.articulation import ArticulationCfg

KR20_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path="D:\omniverse\IsaacLab\my_code\KR20.usdc",
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True, solver_position_iteration_count=8, solver_velocity_iteration_count=0
        ),
        # collision_props=sim_utils.CollisionPropertiesCfg(contact_offset=0.005, rest_offset=0.0),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        joint_pos={
            "R1": 0.0,
            "R2": 0.0,
            "R3": 0.0,
            "R4": 0.0,
            "R5": 0.0,
            "R6": 0.0,
        },
    ),
    actuators={
        "KR20_base": ImplicitActuatorCfg(
            joint_names_expr=["R1", "R2", "R3"],
            effort_limit=100.0,
            velocity_limit=2.0,
            stiffness=50.0,
            damping=10.0,
        ),
        "KR20_arm": ImplicitActuatorCfg(
            joint_names_expr=["R4", "R5", "R6"],
            effort_limit=100.0,
            velocity_limit=2.0,
            stiffness=50.0,
            damping=10.0,
        ),
    },
    soft_joint_pos_limit_factor=1.0,
)
