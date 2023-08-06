from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import math
import compas_rhino
import scriptcontext as sc
from compas_ags.utilities import compute_force_drawinglocation


__commandname__ = "IGS_force_rotate_cmd"


def RunCommand(is_interactive):
    if 'IGS' not in sc.sticky:
        compas_rhino.display_message('IGS has not been initialised yet.')
        return

    scene = sc.sticky['IGS']['scene']

    objects = scene.find_by_name('Form')
    if not objects:
        compas_rhino.display_message("There is no FormDiagram in the scene.")
        return
    form = objects[0]

    objects = scene.find_by_name('Force')
    if not objects:
        compas_rhino.display_message("There is no ForceDiagram in the scene.")
        return
    force = objects[0]

    force.rotation = [0, 0, -math.pi/2]
    force.location = compute_force_drawinglocation(form, force)

    scene.update()
    scene.save()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
