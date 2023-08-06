from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import compas_rhino
from compas.geometry import Line


__commandname__ = "IGS_form_constraint_vertex"


def RunCommand(is_interactive):

    if 'IGS' not in sc.sticky:
        compas_rhino.display_message('IGS has not been initialised yet.')
        return

    scene = sc.sticky['IGS']['scene']

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

    while True:
        vertex = form.select_vertex("Select the vertex to constraint")
        if not vertex:
            break

        start = compas_rhino.rs.GetPoint("Start of line constraint")
        if not start:
            break

        end = compas_rhino.rs.GetPoint("End of line constraint")
        if not end:
            break
        if start == end:
            break

        line = Line(start, end)
        form.diagram.vertex_attribute(vertex, 'line_constraint', line)
        force.diagram.constraints_from_dual()

        scene.update()

        answer = compas_rhino.rs.GetString("Continue selecting vertices?", "No", ["Yes", "No"])
        if not answer:
            break
        if answer == "No":
            break
        if answer == 'Yes':
            pass

    scene.update()
    scene.save()


# ==============================================================================
# Main
# ==============================================================================
if __name__ == '__main__':

    RunCommand(True)
