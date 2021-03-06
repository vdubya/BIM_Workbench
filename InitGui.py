#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2017 Yorik van Havre <yorik@uncreated.net>              *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************


# main workbench class

class BIMWorkbench(Workbench):


    def __init__(self):
        self.__class__.MenuText = "BIM"
        self.__class__.ToolTip = "BIM workbench"
        self.__class__.Icon = """
/* XPM */
static char * IFC_xpm[] = {
"16 16 9 1",
" 	c None",
".	c #D80742",
"+	c #C20B5E",
"@	c #B11A71",
"#	c #0E4A94",
"$	c #A12288",
"%	c #61398E",
"&	c #983563",
"*	c #1E8BA6",
"                ",
"     #   ..     ",
"    ### ....    ",
"   ## ##+  ..   ",
"  ##  .##   ..  ",
" ##  +. ##   .. ",
" ## $$$+##**..  ",
"  #%$$$%#**&.   ",
"  $$% ##*+..&*  ",
" $$$###*@..  ** ",
" $$  #**$@@  ** ",
"  $$  **%$  **  ",
"   $$  **  **   ",
"    $$$$****    ",
"     $$  **     ",
"                "};
"""

    def Initialize(self):

        # All BIM commands are specified either in BimCommands.py, or
        # in separate files (BimSetup.py, BimProject.py...) that are imported in BimCommands.
        # So importing BimCommands is all that is needed to get all the commands.

        import DraftTools, Arch, BimCommands, PartGui

        draft = ["Draft_Line","Draft_Wire","Draft_Circle","Draft_Arc","Draft_Ellipse",
                 "Draft_Polygon","Draft_Rectangle", "Draft_BSpline", "Draft_BezCurve",
                 "Draft_Point","Draft_Text", "Draft_ShapeString", "Draft_Dimension",
                 "Draft_Label"]

        arch = ["Arch_Floor","Arch_Building","Arch_Site",
                "Arch_Wall","Arch_Structure","Arch_Rebar","Arch_Window","Arch_PipeTools",
                "Arch_Stairs","Arch_Roof","Arch_PanelTools","Arch_Equipment","Arch_Frame",
                "Part_Box","Part_Builder","Draft_Facebinder","Arch_Space",
                "Arch_AxisTools","Arch_SectionPlane","Arch_MaterialTools","Arch_Schedule"]

        # Support v0.18 tools

        try:
            import ArchBuildingPart
        except:
            pass
        else:
            arch[0] = "Arch_BuildingPart"
        try:
            import ArchReference
        except:
            pass
        else:
            arch.insert(4,"Arch_Reference")

        # load rebar tools (Reinforcement addon)

        try:
            import RebarTools
        except:
            pass
        else:
            # create popup group for Rebar tools
            class RebarGroupCommand:

                def GetCommands(self):
                    return tuple(RebarTools.RebarCommands+["Arch_Rebar"])

                def GetResources(self):
                    return { 'MenuText': 'Rebar tools',
                             'ToolTip': 'Rebar tools'
                           }

                def IsActive(self):
                    return not FreeCAD.ActiveDocument is None

            FreeCADGui.addCommand('Arch_RebarTools', RebarGroupCommand())
            arch[arch.index("Arch_Rebar")] = "Arch_RebarTools"

        snap = ['Draft_Snap_Lock','Draft_Snap_Midpoint','Draft_Snap_Perpendicular',
                'Draft_Snap_Grid','Draft_Snap_Intersection','Draft_Snap_Parallel',
                'Draft_Snap_Endpoint','Draft_Snap_Angle','Draft_Snap_Center',
                'Draft_Snap_Extension','Draft_Snap_Near','Draft_Snap_Ortho',
                'Draft_Snap_Special','Draft_Snap_Dimensions','Draft_Snap_WorkingPlane']

        modify = ["Draft_Move","BIM_Copy","Draft_Rotate","BIM_Clone","Draft_Offset", "Part_Offset2D", "Draft_Trimex",
                  "Draft_Scale","Draft_Stretch","Draft_Array","Draft_PathArray",
                  "Draft_Mirror","Part_Extrude","Part_Cut","Part_Fuse","Part_Common",
                  "Part_Compound","Part_SimpleCopy","Draft_Upgrade", "Draft_Downgrade", "Draft_Shape2DView",
                  "Draft_Draft2Sketch","Arch_CutPlane","Arch_Add","Arch_Remove"]

        manage = ["BIM_Setup","BIM_Project","BIM_Levels","BIM_Windows","BIM_IfcElements","BIM_Views",
                  "BIM_Classification"]

        utils = ["BIM_TogglePanels","BIM_Trash",
                 "Draft_VisGroup","Draft_Slope","Draft_SetWorkingPlaneProxy","Draft_AddConstruction",
                 "Arch_Component","Arch_CloneComponent","Arch_SplitMesh","Arch_MeshToShape",
                 "Arch_SelectNonSolidMeshes","Arch_RemoveShape",
                 "Arch_CloseHoles","Arch_MergeWalls","Arch_Check",
                 "Arch_IfcExplorer","Arch_ToggleIfcBrepFlag","Arch_3Views",
                 "Arch_IfcSpreadsheet","Arch_ToggleSubs","Arch_Survey",
                 "queryModel","moveWorkPlane","offsetWorkPlane","rotateWorkPlane"]

        # load webtools

        try:
            import BIMServer, Git, Sketchfab
        except:
            pass
        else:
            utils.extend(["WebTools_Git","WebTools_BimServer","WebTools_Sketchfab"])

        # load flamingo

        try:
            import CommandsPolar,CommandsFrame,CommandsPipe
        except:
            flamingo = None
        else:
            flamingo = ["frameIt","fillFrame","insertPath","insertSection","FrameLineManager","spinSect",
                        "reverseBeam","shiftBeam","pivotBeam","levelBeam","alignEdge","rotJoin","alignFlange",
                        "stretchBeam","extend","adjustFrameAngle","insertPipe","insertElbow","insertReduct",
                        "insertCap","insertFlange","insertUbolt","insertPypeLine","breakPipe","mateEdges",
                        "extend2intersection","extend1intersection","laydown","raiseup"]

        # load fasteners

        try:
            import FastenerBase,FastenersCmd
        except:
            fasteners = None
        else:
            fasteners = [c for c in FastenerBase.FSGetCommands("screws") if not isinstance(c,tuple)]

        # create toolbars

        self.appendToolbar("Draft tools",draft)
        self.appendToolbar("Arch tools",arch)
        self.appendToolbar("Mod tools",modify)
        self.appendToolbar("Manage tools",manage)
        if flamingo:
            self.appendToolbar("Flamingo tools",flamingo)

        # create menus

        def QT_TRANSLATE_NOOP(scope, text): return text # dummy function for the QT translator
        self.appendMenu(QT_TRANSLATE_NOOP("BIM","&2D Drafting"),draft)
        self.appendMenu(QT_TRANSLATE_NOOP("BIM","&3D BIM"),arch)
        if flamingo:
            self.appendMenu(QT_TRANSLATE_NOOP("BIM","&Flamingo"),flamingo)
        if fasteners:
            self.appendMenu(QT_TRANSLATE_NOOP("BIM","&Fasteners"),fasteners)
        self.appendMenu(QT_TRANSLATE_NOOP("BIM","&Snapping"),snap)
        self.appendMenu(QT_TRANSLATE_NOOP("BIM","&Modify"),modify)
        self.appendMenu(QT_TRANSLATE_NOOP("BIM","&Manage"),manage)
        self.appendMenu(QT_TRANSLATE_NOOP("BIM","&Utils"),utils)
        self.appendMenu("&Help",["BIM_Welcome"])

        # load Arch & Draft preference pages

        import Draft_rc,Arch_rc
        FreeCADGui.addPreferencePage(":/ui/preferences-arch.ui","Arch")
        FreeCADGui.addPreferencePage(":/ui/preferences-archdefaults.ui","Arch")
        FreeCADGui.addPreferencePage(":/ui/preferences-draft.ui","Draft")
        FreeCADGui.addPreferencePage(":/ui/preferences-draftsnap.ui","Draft")
        FreeCADGui.addPreferencePage(":/ui/preferences-draftvisual.ui","Draft")
        FreeCADGui.addPreferencePage(":/ui/preferences-drafttexts.ui","Draft")

        Log ('Loading BIM module... done\n')


    def Activated(self):

        if hasattr(FreeCADGui,"draftToolBar"):
            FreeCADGui.draftToolBar.Activated()
        if hasattr(FreeCADGui,"Snapper"):
            FreeCADGui.Snapper.show()
        from DraftGui import todo
        import BimCommands
        if FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/BIM").GetBool("FirstTime",True):
            todo.delay(FreeCADGui.runCommand,"BIM_Welcome")
        todo.delay(BimCommands.setStatusIcons,True)
        if not hasattr(FreeCAD,"BimDocumentObserver"):
            FreeCAD.BimDocumentObserver = BimCommands.BimDocumentObserver()
            FreeCAD.addDocumentObserver(FreeCAD.BimDocumentObserver)
            Log("Adding FreeCAD.BimDocumentObserver\n")

        Log("BIM workbench activated\n")


    def Deactivated(self):

        if hasattr(FreeCADGui,"draftToolBar"):
            FreeCADGui.draftToolBar.Deactivated()
        if hasattr(FreeCADGui,"Snapper"):
            FreeCADGui.Snapper.hide()
        import BimCommands
        BimCommands.setStatusIcons(False)
        if hasattr(FreeCAD,"BimDocumentObserver"):
            FreeCAD.removeDocumentObserver(FreeCAD.BimDocumentObserver)
            del FreeCAD.BimDocumentObserver
            Log("Removing FreeCAD.BimDocumentObserver\n")

        Log("BIM workbench deactivated\n")

    def ContextMenu(self, recipient):
        import BimCommands,DraftTools
        self.appendContextMenu("",["BIM_Trash","Draft_AddConstruction"])

    def GetClassName(self):
        return "Gui::PythonWorkbench"


FreeCADGui.addWorkbench(BIMWorkbench)




