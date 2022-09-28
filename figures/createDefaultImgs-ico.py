from ovito.io import import_file
from ovito.vis import OpenGLRenderer, Viewport
from ovito.modifiers import ColorCodingModifier

trajectories = (
    dict(
        name="ico309_300",
        frame=999,
        camera_pos=(-0.023499, 0.0465584, 0.0279121),
        camera_dir=(-0.0182165, -0.372683, -0.92778),
        fov=12.5022,
    ),
    dict(
        name="ico309_400",
        frame=999,
        camera_pos=(0.5338502781529455, 0.36405899513418355, -0.45728322467332627),
        camera_dir=(0.8703511215709966, -0.1674509291612136, -0.46308650542113056),
        fov=12.5022,
    ),
    dict(
        name="ico309_500",
        frame=998,
        camera_pos=(-0.46736565097827054, -0.5888695021776655, 0.07053023725133135),
        camera_dir=(-0.9296934998773034, -0.28699828374128183, -0.23087221880392866),
        fov=12.5022,
    ),
)

for classificationNAME in ["bottomUP", "topDown"]:

    vp = Viewport()
    pipeline = import_file(f"{trajectories[0]['name']}lastUs@1ns.xyz")
    pipeline.modifiers.append(
        ColorCodingModifier(
            property=classificationNAME,
            gradient=ColorCodingModifier.Image(f"{classificationNAME}CMAP.png"),
        )
    )
    pipeline.add_to_scene()

    renderer = OpenGLRenderer(antialiasing_level=6)
    for myData in trajectories:
        pipeline.source.load(f"{myData['name']}lastUs@1ns.xyz")
        data = pipeline.compute()
        data.cell.vis.enabled = False
        vp.type = Viewport.Type.Ortho
        vp.camera_pos = myData["camera_pos"]
        vp.camera_dir = myData["camera_dir"]
        vp.fov = myData["fov"]
        vp.render_image(
            size=(1000, 1000),
            filename=f"{myData['name']}-{classificationNAME}.png",
            alpha=True,
            renderer=renderer,
            frame=myData["frame"],
        )
    pipeline.remove_from_scene()
