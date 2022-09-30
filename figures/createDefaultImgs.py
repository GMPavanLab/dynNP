from ovito.io import import_file
from ovito.vis import OpenGLRenderer, Viewport
from ovito.modifiers import ColorCodingModifier

trajectories = (
    dict(
        name="ico309_Ideal",
        frame=0,
        camera_pos=(-4.6932, 0, 0),
        camera_dir=(-1, 0, 0),
        fov=11.5908,
    ),
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
    dict(
        name="dh348_3_2_3_Ideal",
        frame=0,
        camera_pos=(0.5580883471514578, -0.07135422686409659, -0.813466138672992),
        camera_dir=(0.8052406524866854, 0.10948566179227516, -0.5827524186519731),
        fov=14.727432140208398,
    ),
    dict(
        name="dh348_3_2_3_500",
        frame=992,
        camera_pos=(0.5580883471514578, -0.07135422686409659, -0.813466138672992),
        camera_dir=(0.8052406524866854, 0.10948566179227516, -0.5827524186519731),
        fov=14.727432140208398,
    ),
    dict(
        name="dh348_3_2_3_400",
        frame=993,
        camera_pos=(0.5580883471514578, -0.07135422686409659, -0.813466138672992),
        camera_dir=(0.8052406524866854, 0.10948566179227516, -0.5827524186519731),
        fov=14.727432140208398,
    ),
    dict(
        name="dh348_3_2_3_300",
        frame=998,
        camera_pos=(0.5580883471514578, -0.07135422686409659, -0.813466138672992),
        camera_dir=(0.8052406524866854, 0.10948566179227516, -0.5827524186519731),
        fov=14.727432140208398,
    ),
    dict(
        name="to309_9_4_Ideal",
        frame=0,
        camera_pos=(11.729677498340607, 11.533007442951202, -0.14162683486938477),
        camera_dir=(0.8296772955585443, 0.02056457470792284, 0.5578643952626321),
        fov=12.73897977501983,
    ),
    dict(
        name="to309_9_4_300",
        frame=999,
        camera_pos=(11.729677498340607, 11.533007442951202, -0.14162683486938477),
        camera_dir=(0.8296772955585443, 0.02056457470792284, 0.5578643952626321),
        fov=12.73897977501983,
    ),
    dict(
        name="to309_9_4_400",
        frame=990,
        camera_pos=(10.413795435675127, 11.108086052238065, -0.38886269740025914),
        camera_dir=(0.8165524797707054, -0.10303993812025528, 0.568000720890815),
        fov=12.73897977501983,
    ),
    dict(
        name="to309_9_4_500",
        frame=999,
        camera_pos=(11.82621805728696, 12.354770299192195, -0.8124140273086139),
        camera_dir=(0.03919857077204872, -0.8468106226694496, 0.5304481514564903),
        fov=12.73897977501983,
    ),
)

for (classificationNAME, maxNum) in [("bottomUP", 7.0), ("topDown", 9.0)]:

    vp = Viewport()
    pipeline = import_file(f"{trajectories[0]['name']}lastUs@1ns.xyz")
    pipeline.modifiers.append(
        ColorCodingModifier(
            property=classificationNAME,
            end_value=maxNum,
            start_value=0.0,
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
