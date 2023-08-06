from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_rhino

import IGS_form_move_cmd
import IGS_form_displaysettings_cmd
import IGS_force_move_cmd
import IGS_force_select_anchor_cmd
import IGS_force_scale_cmd
import IGS_force_displaysettings_cmd


__commandname__ = "IGS_toolbar_display"
"""ATTENTION!
This cmd will be deleted (replaced by toolbar_force_display_cmd, toolbar_form_display_cmd...)
"""


def RunCommand(is_interactive):

    if 'IGS' not in sc.sticky:
        compas_rhino.display_message('IGS has not been initialised yet.')
        return

    scene = sc.sticky['IGS']['scene']
    if not scene:
        return

    if not scene.find_by_name('Form'):
        compas_rhino.display_message("There is no FormDiagram in the scene.")
        return

    if not scene.find_by_name('Force'):
        compas_rhino.display_message("There is no ForceDiagram in the scene.")
        return

    options = ["FormLocation", "FormDisplay", "ForceLocation", "ForceAnchor", "ForceScale", "ForceDisplay"]
    option = compas_rhino.rs.GetString("Display:", strings=options)

    if not option:
        return

    if option == "FormLocation":
        IGS_form_move_cmd.RunCommand(True)

    elif option == "FormDisplay":
        IGS_form_displaysettings_cmd.RunCommand(True)

    elif option == "ForceLocation":
        IGS_force_move_cmd.RunCommand(True)

    elif option == "ForceAnchor":
        IGS_force_select_anchor_cmd.RunCommand(True)

    elif option == "ForceScale":
        IGS_force_scale_cmd.RunCommand(True)

    elif option == "ForceDisplay":
        IGS_force_displaysettings_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
