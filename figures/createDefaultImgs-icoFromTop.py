from ovito.io import import_file
from ovito.vis import OpenGLRenderer, Viewport
from ovito.modifiers import ColorCodingModifier

trajectories = (
    dict(
        name="ico309-SV_18631-SL_31922-T_300",
        frame=999,
        camera_pos=(-0.023499, 0.0465584, 0.0279121),
        camera_dir=(-0.0182165, -0.372683, -0.92778),
        fov=12.5022,
    ),
    dict(
        name="ico309-SV_18631-SL_31922-T_400",
        frame=999,
        camera_pos=(0.5338502781529455, 0.36405899513418355, -0.45728322467332627),
        camera_dir=(0.8703511215709966, -0.1674509291612136, -0.46308650542113056),
        fov=12.5022,
    ),
    dict(
        name="ico309-SV_18631-SL_31922-T_500",
        frame=998,
        camera_pos=(-0.46736565097827054, -0.5888695021776655, 0.07053023725133135),
        camera_dir=(-0.9296934998773034, -0.28699828374128183, -0.23087221880392866),
        fov=12.5022,
    ),
    dict(
        name="ico309-SV_8899-SL_5536-T_300",
        frame=999,
        camera_pos=(-0.003732204437255861, 0.04805946350097658, -0.21466493606567466),
        camera_dir=(0.03135152789131216, -0.3238487530305299, -0.9455892696406041),
        fov=12.5022,
    ),
    dict(
        name="ico309-SV_8899-SL_5536-T_400",
        frame=999,
        camera_pos=(0.01984540125022433, 0.0966076154346465, 0.16445735068025455),
        camera_dir=(-0.054613050370901306, 0.6265983589710629, 0.777426466788954),
        fov=12.5022,
    ),
    dict(
        name="ico309-SV_8899-SL_5536-T_500",
        frame=0,
        camera_pos=(0.01984540125022433, 0.0966076154346465, 0.16445735068025455),
        camera_dir=(-0.054613050370901306, 0.6265983589710629, 0.777426466788954),
        fov=12.5022,
    ),
)

ouputFname = "fittedOn_ico309-SV_18631-SL_31922-T_300-FromToplast1000ns"

vp = Viewport()
pipeline = import_file(f"{trajectories[0]['name']}_FromToplast1000ns.xyz")
pipeline.modifiers.append(
    ColorCodingModifier(
        property="dendroCutr",
        gradient=ColorCodingModifier.Image("dendroCutr_colors10.png"),
    )
)
pipeline.add_to_scene()

renderer = OpenGLRenderer(antialiasing_level=6)
for myData in trajectories:
    pipeline.source.load(f"{myData['name']}_FromToplast1000ns.xyz")
    data = pipeline.compute()
    data.cell.vis.enabled = False
    vp.type = Viewport.Type.Ortho
    vp.camera_pos = myData["camera_pos"]
    vp.camera_dir = myData["camera_dir"]
    vp.fov = myData["fov"]
    vp.render_image(
        size=(1000, 1000),
        filename=f"{myData['name']}-{ouputFname}.png",
        alpha=True,
        renderer=renderer,
        frame=myData["frame"],
    )
