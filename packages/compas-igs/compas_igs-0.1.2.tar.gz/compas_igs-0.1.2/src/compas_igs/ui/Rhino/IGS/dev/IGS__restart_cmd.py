from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc


__commandname__ = "IGS__restart"


def RunCommand(is_interactive):

    scene = sc.sticky['IGS']['scene']
    if not scene:
        return

    proxy = sc.sticky['IGS']['proxy']
    if not proxy:
        return

    scene.purge()
    proxy.stop_server()
    proxy.start_server()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
