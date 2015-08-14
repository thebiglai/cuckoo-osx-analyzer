#!/usr/bin/env python
import os

from lib.core.packages import Package


class Safari(Package):
    """
    Used to open URL's in Safari
    """

    def prepare(self):
        # Set target to open up safari with the target url
        # We can omit the -a if we just want to use the default browser
        self.target = '{0} {1}'.format('/usr/bin/open -F -a safari', self.target)

