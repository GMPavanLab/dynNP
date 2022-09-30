from array import array
from ovito.io import *
from ovito.modifiers import *
from ovito.data import *
from ovito.pipeline import *
from ovito.vis import *
from ovito.qt_compat import QtCore
import numpy
from numpy.linalg import norm


def prepareFig3(
    trackedAtom,
    xyzFile,
    OutputName,
    cmapImage="bottomUP.png",
    colorby="bottomUp",
    colorbyInterval=(0.0, 7.0),
    transparentAtoms=None,
    renderer=OpenGLRenderer(antialiasing_level=6),
    camera_pos=(0.5195405958694747, 0.1637907382734865, -0.022509793321067638),
    camera_dir=(0.3822613161499919, -0.7753027203453063, -0.5027742813633606),
    fov=11.779909025058428,
    vpType=Viewport.Type.Ortho,
    visFrame=0,
    transparentDist=2.88,
):
    OutputName = f"{OutputName}_Tracking{trackedAtom}_"
    # Data import:
    pipeline = import_file(xyzFile, multiple_frames=True)

    # Evaluate new pipeline to gain access to visual elements associated with the imported data objects.
    data = pipeline.compute()
    # Visual element initialization:
    data.cell.vis.enabled = False
    # Done accessing input DataCollection of pipeline.
    del data

    pipeline.add_to_scene()
    if transparentAtoms is None:
        transparentAtoms = set()
        pos0 = numpy.array(pipeline.compute(0).particles.positions)

        def distTovisLine(point, pointOnLine, linedir):
            # linedir is normalized
            # see https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
            return norm(numpy.cross(point - pointOnLine, linedir))
            d_pa = point - pointOnLine
            return norm(d_pa - linedir * (d_pa.dot(linedir)))

        """
        for frame in range(pipeline.source.num_frames):
            data = pipeline.compute(frame)
            trackedPos = numpy.array(data.particles.positions[trackedAtom])
            for i in range(len(pos0)):
                d = pos0[i] - trackedPos
                if norm(d) < transparentDist:
                    transparentAtoms.add(i)
        """
        # works not for ortho but camera type is ortho!
        for frame in range(pipeline.source.num_frames):
            data = pipeline.compute(frame)
            trackedPos = numpy.array(data.particles.positions[trackedAtom])
            directionToCamera = trackedPos - numpy.array(camera_pos)
            dFromCamera = norm(directionToCamera)
            # print(dFromCamera)
            directionToCamera /= numpy.linalg.norm(directionToCamera)
            for i in range(len(pos0)):
                dPosToCamera = norm(pos0[i] - numpy.array(camera_pos))
                #   print(i, dPosToCamera)
                if dPosToCamera < dFromCamera:
                    if (
                        distTovisLine(
                            pos0[i], numpy.array(camera_pos), directionToCamera
                        )
                        < transparentDist
                    ):
                        transparentAtoms.add(i)

    transparentAtoms = list(set(transparentAtoms))

    # Assign color:
    pipeline.modifiers.append(
        AssignColorModifier(
            color=[0.8313725590705872, 0.8313725590705872, 0.8313725590705872]
        )
    )

    # Expression selection:
    pipeline.modifiers.append(
        ExpressionSelectionModifier(expression=f"ParticleIndex=={trackedAtom}")
    )

    # Generate trajectory lines:
    mod = GenerateTrajectoryLinesModifier()
    mod.unwrap_trajectories = False
    mod.sample_particle_property = colorby
    mod.vis.width = 0.8
    mod.vis.shading = TrajectoryVis.Shading.Normal
    mod.vis.color_mapping_property = colorby
    mod.vis.color_mapping_interval = colorbyInterval
    mod.vis.color_mapping_gradient = ColorCodingModifier.Image(cmapImage)
    pipeline.modifiers.append(mod)
    mod.generate()

    tranparentAtomsSelection = f"ParticleIndex=={transparentAtoms[0]}"

    for id in transparentAtoms[1:]:
        tranparentAtomsSelection += f"||ParticleIndex=={id}"
    print(tranparentAtomsSelection)
    pipeline.modifiers.append(
        ExpressionSelectionModifier(expression=tranparentAtomsSelection)
    )

    # Compute property:
    pipeline.modifiers.append(
        ComputePropertyModifier(
            expressions=("0.8",),
            output_property="Transparency",
            only_selected=True,
        )
    )

    # Clear selection:
    pipeline.modifiers.append(ClearSelectionModifier())

    # Viewport setup:
    vp = Viewport(
        type=vpType,
        fov=fov,
        camera_dir=camera_dir,
        camera_pos=camera_pos,
    )

    # Rendering:
    vp.render_image(
        filename=f"{OutputName}{colorby}.png",
        size=(1000, 1000),
        alpha=True,
        renderer=renderer,
        frame=visFrame,
    )
    # Generate trajectory lines:
    mod.vis.shading = TrajectoryVis.Shading.Normal
    mod.vis.color_mapping_property = "Time"
    mod.vis.color_mapping_interval = (0.0, pipeline.source.num_frames - 1)
    mod.vis.color_mapping_gradient = ColorCodingModifier.Hot()

    # Rendering:
    vp.render_image(
        filename=f"{OutputName}Time.png",
        size=(1000, 1000),
        alpha=True,
        renderer=renderer,
        frame=visFrame,
    )


if __name__ == "__main__":
    prepareFig3(
        trackedAtom=155,
        xyzFile="ico309_300lastUs@1ns.xyz",
        OutputName="ico309_300",
        transparentAtoms=[119, 155, 232, 236, 250, 251, 253, 291, 294, 295, 296],
        renderer=OpenGLRenderer(antialiasing_level=6),
        visFrame=0,
        camera_pos=(0.5195405958694747, 0.1637907382734865, -0.022509793321067638),
        camera_dir=(0.3822613161499919, -0.7753027203453063, -0.5027742813633606),
        fov=11.779909025058428,
        vpType=Viewport.Type.Ortho,
        # camera_pos=(-11.146021600255509, 26.905564155450673, 18.721812006023814),
        # camera_dir=(0.29885107843047415, -0.8191262059252515, -0.4896123892299345),
        # fov=0.6108652381980153,
        # vpType=Viewport.Type.Perspective,
        cmapImage="bottomUPCMAP.png",
        colorby="bottomUP",
        colorbyInterval=(0.0, 7.0),
        # cmapImage="topDownCMAP.png",
        # colorby="topDown",
        # colorbyInterval=(0.0, 9.0),
        transparentDist=1.44 * 1.5,
    )
