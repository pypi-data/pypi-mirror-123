from .base import AB_Base

from .control import AB_Control
from .workspace import AB_Workspace
from .region import AB_Region
from .entity import AB_Entity
from .process import AB_Process
from .subprocess import AB_SubProcess
from .risk import AB_Risk
from .assertion import AB_Assertion
from .test_section import AB_TestSection
from .controls_data import AB_Controls_Data
from .effectiveness_option import AB_EffectivenessOption
from .status_option import AB_StatusOption
from .test_type import AB_TestType
from .test import AB_Test
from .file import AB_File

from .continuous_monitoring_systems import AB_Continous_Monitoring_Systems
from .continuous_monitoring_monitors import AB_Continous_Monitoring_Monitors
from .continuous_monitoring_monitor_results import AB_Continous_Monitoring_Monitor_Results

SUBOBJ_LK = {"region_id": {"obj": AB_Region},
             "process_id": {"obj": AB_Process},
             "subprocess_id": {"obj": AB_SubProcess},
             "risk_id": {"obj": AB_Risk},
             "control_id": {"obj": AB_Control},
             "entity_id": {"obj": AB_Entity},
             "controls_datum_id": {"obj": AB_Controls_Data},
             "test_ids": {"obj": AB_Test},
             "file_ids": {"obj": AB_File},
             "continuous_monitoring_system_id": {"obj": AB_Continous_Monitoring_Systems},
             "continuous_monitoring_monitor_id": {"obj": AB_Continous_Monitoring_Monitors}
            }


from .controlrod import AB_ControlRod

USER_AGENT = "control_rod/0.0.0"