#Variables
firstFrame = int(nuke.thisGroup()['firstFrame'].value())
lastFrame = int(nuke.thisGroup()['lastFrame'].value())
frequency = int(nuke.thisGroup()['frequency'].value())
frameRange = lastFrame - firstFrame
slices = int(frameRange / frequency)
merge = nuke.thisGroup()['mergeType'].value()

#Inputs
input = nuke.toNode('input')
cam = nuke.toNode('camera')
geo = nuke.toNode('geo')
back = nuke.toNode('background')
output = nuke.toNode('Output1')

for node in nuke.allNodes():

    if node.Class() in ('Input','Output', 'Reformat') or node.name() == 'MergeMatScanline':  
        pass
    else:
        nuke.delete(node) 
      
def projRecursion(input,cam,geo,back,mergeMat,slices):

    for f in range(slices):

        fHoldRGBA = nuke.nodes.FrameHold(inputs = [input], 
        first_frame = firstFrame + range(slices).index(f))
        fHoldCam = nuke.nodes.FrameHold(inputs = [cam], 
        first_frame = firstFrame + range(slices).index(f))    
        proj = nuke.nodes.Project3D(inputs = [fHoldRGBA ,fHoldCam], crop = False)
        projCount = len(nuke.allNodes('Project3D'))

        if merge == 'MergeMat' and projCount <= 1:
            mergeMat = proj
        elif merge == 'MergeMat' and projCount > 1:
            mergeMat = nuke.nodes.MergeMat(inputs = [mergeMat, proj])
        elif merge == 'ScanlineRender':
            applyMat = nuke.nodes.ApplyMaterial(inputs = [geo, proj])
            scan = nuke.nodes.ScanlineRender(inputs = [back,applyMat,cam])
        else:
            pass
    
    if merge == 'MergeMat':
        applyMat = nuke.nodes.ApplyMaterial(inputs = [geo, mergeMat])
        scan = nuke.toNode('MergeMatScanline')
        scan.setInput(0,back)
        scan.setInput(1,applyMat)
        scan.setInput(2,cam)
        output.setInput(0,scan)
    else:
        pass

projRecursion(input,cam,geo,back,mergeMat, slices)
