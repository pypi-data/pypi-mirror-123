from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import compas_rhino


__commandname__ = "IGS_form_update_both"


def RunCommand(is_interactive):

    if 'IGS' not in sc.sticky:
        compas_rhino.display_message('IGS has not been initialised yet.')
        return

    scene = sc.sticky['IGS']['scene']
    proxy = sc.sticky['IGS']['proxy']

    proxy.package = 'compas_ags.ags.graphstatics'

    objects = scene.find_by_name("Form")
    if objects:
        form = objects[0]
    else:
        compas_rhino.display_message('No Form diagram in the scene.')
        return

    objects = scene.find_by_name("Force")
    if objects:
        force = objects[0]
    else:
        compas_rhino.display_message('No Force diagram in the scene.')
        return

    if not scene.settings['IGS']['bi-directional']:
        compas_rhino.display_message('Please turn on the bi-directional to update form and force from constraints.')
        return

    if scene.settings['IGS']['autoupdate']:
        scene.settings['IGS']['autoupdate'] = False

    formdiagram, forcediagram = proxy.update_diagrams_from_constraints(form.diagram, force.diagram)

    form.diagram.data = formdiagram.data
    force.diagram.data = forcediagram.data

    scene.update()
    scene.save()


# ==============================================================================
# Main
# ==============================================================================
if __name__ == '__main__':

    RunCommand(True)
