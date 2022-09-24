from ovito.io import import_file
from ovito.vis import OpenGLRenderer, Viewport
from ovito.modifiers import ColorCodingModifier, SliceModifier

ouputFname = "fittedOn_ico309-SV_18631-SL_31922-T_300-125-eom"

vp = Viewport()
pipeline = import_file("ico309_ideal.xyz")
pipeline.modifiers.append(
    ColorCodingModifier(
        property="predictionWithNoNoise",
        gradient=ColorCodingModifier.Image(
            "bottomUpCMAP.png"
        ),
    )
)

pipeline.add_to_scene()

vp.type = Viewport.Type.Ortho
vp.camera_pos = (-4.6932, 0, 0)
vp.camera_dir = (-1, 0, 0)
vp.fov = 11.5908  # math.radians(60.0)
# data=pipeline.compute()

# data.cell.vis.enabled =False
tachyon = OpenGLRenderer(antialiasing_level=6)
vp.render_image(
    size=(1000, 1000), filename=f"{ouputFname}_ideal.png", alpha=True, renderer=tachyon
)
pipeline.modifiers.append(
    SliceModifier(
        distance=1,
        normal=(1.0, 0.0, 0.0),
    )
)
vp.render_image(
    size=(1000, 1000),
    filename=f"{ouputFname}_ideal_sliced.png",
    alpha=True,
    renderer=tachyon,
)
