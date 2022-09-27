from ovito.vis import OpenGLRenderer, Viewport
from ovito.modifiers import ColorCodingModifier
from ovito.data import Particles, DataCollection, ParticleType, SimulationCell
from ovito.pipeline import Pipeline, StaticSource


def CreateLegend(
    cmapFile, legendName, nclasses, renderer=OpenGLRenderer(antialiasing_level=6)
):
    # Create the data collection containing a Particles object:
    particles = Particles()
    data = DataCollection()
    data.objects.append(particles)

    # XYZ coordinates of the three atoms to create:
    pos = [(0.0, 0.0, 0.0)]

    # Create the particle position property:
    particles.create_property("Position", data=pos)

    # Create the particle type property and insert two atom types:
    type_prop = particles.create_property("Particle Type")
    type_prop.types.append(
        ParticleType(
            id=1, name="Au", color=(255 / 255, 209 / 255, 35 / 255), radius=1.44
        )
    )
    type_prop[0] = 1
    particles.create_property("Class", data=[0])

    cell = SimulationCell(pbc=(False, False, False))
    cell[...] = [[10, 0, 0, 0], [0, 10, 0, 0], [0, 0, 10, 0]]

    data.objects.append(cell)
    pipeline = Pipeline(source=StaticSource(data=data))
    pipeline.modifiers.append(
        ColorCodingModifier(
            property="Class",
            end_value=nclasses - 1,
            gradient=ColorCodingModifier.Image(cmapFile),
        )
    )

    pipeline.add_to_scene()
    vp = Viewport()
    vp.type = Viewport.Type.Ortho
    vp.camera_pos = (0, 0, 0)
    vp.camera_dir = (-1, 0, 0)
    vp.fov = 1.44811
    # data=pipeline.compute()

    data.cell.vis.enabled = False

    for c in range(nclasses):
        particles.create_property("Class", data=[c])
        vp.render_image(
            size=(1000, 1000),
            filename=f"{legendName}{c:04}.png",
            renderer=renderer,
            alpha=True,
        )


if __name__ == "__main__":
    # CreateLegend("bottomUpCMAP.png", "bottomUp", 8)
    CreateLegend("topDownCMAP.png", "topDown", 10)
