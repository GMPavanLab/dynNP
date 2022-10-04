from array import array
from ovito.io import *
from ovito.modifiers import *
from ovito.data import *
from ovito.pipeline import *
from ovito.vis import *
from ovito.qt_compat import QtCore,QtGui
import numpy
from numpy.linalg import norm

# Parameters:
bar_length = 10   # Simulation units (e.g. Angstroms)
color_black = QtGui.QColor(0,0,0)
label_text = f"{bar_length//10} nm"
#label_color = QtGui.QColor(255,255,255)

def addScale(args: PythonViewportOverlay.Arguments):
    if args.is_perspective:
        raise Exception("This overlay only works with non-perspective viewports.")

    # Compute length of bar in screen space
    screen_length = args.project_size((0,0,0), bar_length)

    # Define geometry of bar in screen space
    height = 0.07 * args.painter.window().height() / 2
    margin = 0.02 * args.painter.window().height()
    left=args.painter.window().width() - screen_length -margin
    top= args.painter.window().height() - height -margin
    lenghtBar = QtCore.QRectF(left, top, screen_length, height)
    fontHeight=2*height
    textBar = QtCore.QRectF(left, top-fontHeight, screen_length, fontHeight)

    # Render bar rectangle
    args.painter.fillRect(lenghtBar, color_black)

    # Render text label
    font = args.painter.font()
    font.setPixelSize(fontHeight)
    args.painter.setFont(font)
    args.painter.setPen(QtGui.QPen(color_black))
    args.painter.drawText(textBar, QtCore.Qt.AlignCenter, label_text)



def prepareFig4(
    xyzFile,
    OutputName,
    colorby,
    cmapImage="topDownFullCMAP.png",
    colorbyInterval=(0.0, 46.0),
    renderer=OpenGLRenderer(antialiasing_level=6),
    camera_pos=(0.5195405958694747, 0.1637907382734865, -0.022509793321067638),
    camera_dir=(0.3822613161499919, -0.7753027203453063, -0.5027742813633606),
    fov=11.779909025058428,
    vpType=Viewport.Type.Ortho,
    visFrame=0
):
    OutputName = f"{OutputName}"
    # Data import:
    pipeline = import_file(xyzFile, multiple_frames=True)

    # Evaluate new pipeline to gain access to visual elements associated with the imported data objects.
    data = pipeline.compute()
    # Visual element initialization:
    data.cell.vis.enabled = False
    # Done accessing input DataCollection of pipeline.
    del data

    pipeline.modifiers.append(
        ColorCodingModifier(
            property=colorby,
            end_value=colorbyInterval[1],
            start_value=colorbyInterval[0],
            gradient=ColorCodingModifier.Image(cmapImage),
        )
    )

    pipeline.add_to_scene()


    # Viewport setup:
    vp = Viewport(
        type=vpType,
        fov=fov,
        camera_dir=camera_dir,
        camera_pos=camera_pos,
    )

    vp.overlays.append(PythonViewportOverlay(function=addScale))

    # Rendering:
    vp.render_image(
        filename=f"{OutputName}.png",
        size=(1000, 1000),
        alpha=True,
        renderer=renderer,
        frame=visFrame,
    )
    pipeline.remove_from_scene()


if __name__ == "__main__":
    prepareToPlot=dict(
                to309_9_4= dict(
    camera_pos=(11.52, 11.52, 0),
    camera_dir=(0,0.836899,-0.547358),
    fov=14.5764,
    colorby="to",),
        to976_12_4 = dict(
    camera_pos=(0, 0, 0),
    camera_dir=(0,0.867423,-0.497571),
    fov=18.9585,
    colorby="to",),
    to807_11_3 = dict(
    camera_pos=(0, 0, 0),
    camera_dir=(0,0.867423,-0.497571),
    fov=16.8147,
    colorby="to",),
        dh1086_7_1_3 = dict(
    camera_pos=(0, 0, 0),
    camera_dir=(-0.268601,0.735836,-0.62161),
    fov=25.1348,
    colorby="dh",),
        dh1734_5_4_4 = dict(
    camera_pos=(0, 0, 0),
    camera_dir=(-0.268601,0.735836,-0.62161),
    fov=22.2925,
    colorby="dh",),
    dh348_3_2_3 = dict(
    camera_pos=(0, 0, 0),
    camera_dir=(-0.268601,0.735836,-0.62161),
    fov=13.7943,
    colorby="dh",),
    ico923_6 = dict(
    camera_pos=(0, 0, 0),
    camera_dir=(0,0.42738,0.904072),
    fov=19.7717,
    colorby="ih",),
        ico309 = dict(
    camera_pos=(0, 0, 0),
    camera_dir=(0,0.42738,0.904072),
    fov=13.7943,
    colorby="ih",),
    )
    for exampleNP in prepareToPlot:
        prepareFig4(
        xyzFile=f"{exampleNP}_topDown.xyz",
        OutputName=f"{exampleNP}_topDown",
        renderer=OpenGLRenderer(antialiasing_level=6),
        **prepareToPlot[exampleNP],
        vpType=Viewport.Type.Ortho,
        
        cmapImage="topDownFullCMAP.png",
        
        colorbyInterval=(0.0, 46.0),
        
    )



