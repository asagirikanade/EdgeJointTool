import maya.cmds as mc
import maya.app.general.positionAlongCurve as apg


class EdgeJoint:
    def mainmenu(self):

        mc.window('mainmenu', t='Edge Joint Tool')

        mc.columnLayout(adj=True)
        self.name = mc.textFieldGrp(l='Joint Name: ')
        self.joint = mc.intSliderGrp(l='Joint Number: ', v=2, min=2, max=20, f=True)
        self.reverse = mc.checkBoxGrp(l='Reverse: ')
        mc.button(l='Create', c=self.run)
        
        mc.showWindow()

    def run(self,*args):

        name = mc.textFieldGrp(self.name, q=True, tx=True)
        joint = mc.intSliderGrp(self.joint, q=True, v=True)
        obj = mc.ls(sl=True, o=True)

        if name == '':
            print 'ERROR!!'
            return

        for i in obj:
            mc.select(i)
            if mc.objectType(i) == 'mesh':
                mc.hilite(i)
                curves = mc.polyToCurve(usm=False, f=2, dg=1)
            else:
                curves = mc.duplicate(rr=True)
            if mc.checkBoxGrp(self.reverse, q=True, v1=True):
                mc.reverseCurve()
            
            joints = []
            for j in range(joint):
                mc.select(cl=True)
                joints.append(mc.joint(n=name))
            
            mc.select(mc.ls(joints, curves,  tr=True))
            apg.positionAlongCurve()

            for j in range(joint - 1):
                mc.parent(joints[j + 1], joints[j])
                mc.joint(joints[j], e=True, zso=True, oj='xyz', sao='yup')
                if j == joint - 2:
                    mc.rename(joints[j + 1], name + '_end')
            mc.delete(curves)
        mc.select(cl=True)


a = CurveJoint()
a.mainmenu()

        