"""Blender property registration for FrameForge."""

from __future__ import annotations

from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    PointerProperty,
    StringProperty,
)
from bpy.types import Object, Scene

from . import presets

SHOT_PRESET_ITEMS = (("USE_SCENE", "Use Scene Preset", "Follow the preset chosen above"),) + tuple(
    (spec["id"], spec["label"], spec["description"]) for spec in presets.PRESET_SPECS
)


def camera_poll(_self, obj):
    return obj is not None and obj.type == "CAMERA"


def object_poll(_self, obj):
    return obj is not None


def register():
    Scene.frameforge_project_name = StringProperty(
        name="Project Name",
        description="Used as the first part of every exported file name",
        default="",
    )
    Scene.frameforge_camera = PointerProperty(
        name="Camera",
        description="Camera this shot is built for. Falls back to the scene camera",
        type=Object,
        poll=camera_poll,
    )
    Scene.frameforge_focus_object = PointerProperty(
        name="Focus Object",
        description=(
            "What the camera should aim at. Leave empty to use whatever the camera "
            "is already pointing at"
        ),
        type=Object,
        poll=object_poll,
    )

    Scene.frameforge_preset = EnumProperty(
        name="Camera Move",
        description="Preset applied to the selected camera",
        items=presets.preset_items(),
        default="dolly_in",
    )
    Scene.frameforge_strength = FloatProperty(
        name="Amount",
        description="How far the move travels. 1.0 reproduces the current framing at the midpoint",
        default=1.0,
        min=0.05,
        max=3.0,
        soft_min=0.2,
        soft_max=2.0,
        step=10,
        precision=2,
    )
    Scene.frameforge_easing = EnumProperty(
        name="Easing",
        description="How the speed changes over the move",
        items=presets.EASING_ITEMS,
        default=presets.EASING_IN_OUT,
    )
    Scene.frameforge_keyframe_step = IntProperty(
        name="Keyframe Step",
        description="Bake a keyframe every N frames. 1 gives the smoothest result",
        default=1,
        min=1,
        max=10,
    )
    Scene.frameforge_clear_animation = BoolProperty(
        name="Clear Existing Camera Animation",
        description=(
            "Remove animation already on the camera object before baking. "
            "Turn this off to layer a move onto hand-set keys"
        ),
        default=True,
    )

    Scene.frameforge_resolution = EnumProperty(
        name="Resolution",
        description="Output size for the exported frames",
        items=presets.RESOLUTION_ITEMS,
        default=presets.RESOLUTION_SCENE,
    )
    Scene.frameforge_export_first = BoolProperty(
        name="First Frame", description="Export the first frame", default=True
    )
    Scene.frameforge_export_last = BoolProperty(
        name="Last Frame", description="Export the last frame", default=True
    )
    Scene.frameforge_mid_count = IntProperty(
        name="Middle Frames",
        description="Evenly spaced frames between the first and last",
        default=0,
        min=0,
        max=24,
    )
    Scene.frameforge_export_depth = BoolProperty(
        name="Depth Pass",
        description="Export a normalised depth map for the first and last frame",
        default=False,
    )
    Scene.frameforge_export_normal = BoolProperty(
        name="Normal Pass",
        description="Export a normal map for the first and last frame",
        default=False,
    )
    Scene.frameforge_depth_auto = BoolProperty(
        name="Auto Depth Range",
        description=(
            "Normalise the depth map against the surfaces the camera can see. "
            "Turn this off when a distant floor or backdrop eats the range"
        ),
        default=True,
    )
    Scene.frameforge_depth_near = FloatProperty(
        name="Depth Near",
        description="Distance mapped to white when the depth range is manual",
        default=0.0,
        min=0.0,
        soft_max=100.0,
        unit="LENGTH",
    )
    Scene.frameforge_depth_far = FloatProperty(
        name="Depth Far",
        description="Distance mapped to black when the depth range is manual",
        default=0.0,
        min=0.0,
        soft_max=200.0,
        unit="LENGTH",
    )
    Scene.frameforge_export_preview = BoolProperty(
        name="Preview Movie",
        description="Encode an MP4 of the move so you can see the motion before generating",
        default=False,
    )
    Scene.frameforge_preview_quality = IntProperty(
        name="Preview Quality",
        description="Resolution of the preview movie relative to the export size",
        default=50,
        min=25,
        max=100,
        subtype="PERCENTAGE",
    )

    Scene.frameforge_output_dir = StringProperty(
        name="Output Folder",
        description="Where exported packages are written",
        subtype="DIR_PATH",
        default="",
    )
    Scene.frameforge_overwrite = BoolProperty(
        name="Overwrite Existing Files",
        description=(
            "Replace earlier exports of the same shot. Turn this off to keep "
            "every version with a numeric suffix instead"
        ),
        default=True,
    )
    Scene.frameforge_status = StringProperty(name="Status", default="")
    Scene.frameforge_report = StringProperty(name="Report", default="")
    Scene.frameforge_last_output_dir = StringProperty(name="Last Output", default="")

    Object.frameforge_shot_name = StringProperty(
        name="Shot Name",
        description="Override the file name used for this camera",
        default="",
    )
    Object.frameforge_shot_preset = EnumProperty(
        name="Shot Move",
        description="Per-camera preset used by Batch Export",
        items=SHOT_PRESET_ITEMS,
        default="USE_SCENE",
    )


def unregister():
    for owner, name in (
        (Object, "frameforge_shot_preset"),
        (Object, "frameforge_shot_name"),
        (Scene, "frameforge_last_output_dir"),
        (Scene, "frameforge_report"),
        (Scene, "frameforge_status"),
        (Scene, "frameforge_overwrite"),
        (Scene, "frameforge_output_dir"),
        (Scene, "frameforge_preview_quality"),
        (Scene, "frameforge_export_preview"),
        (Scene, "frameforge_export_normal"),
        (Scene, "frameforge_depth_far"),
        (Scene, "frameforge_depth_near"),
        (Scene, "frameforge_depth_auto"),
        (Scene, "frameforge_export_depth"),
        (Scene, "frameforge_mid_count"),
        (Scene, "frameforge_export_last"),
        (Scene, "frameforge_export_first"),
        (Scene, "frameforge_resolution"),
        (Scene, "frameforge_clear_animation"),
        (Scene, "frameforge_keyframe_step"),
        (Scene, "frameforge_easing"),
        (Scene, "frameforge_strength"),
        (Scene, "frameforge_preset"),
        (Scene, "frameforge_focus_object"),
        (Scene, "frameforge_camera"),
        (Scene, "frameforge_project_name"),
    ):
        if hasattr(owner, name):
            delattr(owner, name)
