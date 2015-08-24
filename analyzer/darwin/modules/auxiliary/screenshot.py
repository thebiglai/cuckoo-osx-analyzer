import os, time
import hashlib
from threading import Thread

from lib.common.results import NetlogFile


class screenshot(Thread):
    def __init__(self, sleeptime=5):
        Thread.__init__(self)
        self.capture = True
        self.imgmd5 = ''
        self.sleeptime = sleeptime

    def stop(self):
        """Stop the screenshots"""
        self.capture = False

    def imgdiff(self, image):
        """Check to see if images are the same.
        This is a very dumbed down check, basically just checking md5sums.
        We should update this to use something like PIL to compare historams.
        Return: True if img is the same
        """
        # TODO: smarter logic.
        # if seconds are enabled to display on the clock, then every image will be different
        with open(image) as fh:
            img = fh.read()

        imghash = hashlib.md5(img).hexdigest()

        if not self.imgmd5:
            self.imgmd5 = imghash
            return False

        if self.imgmd5 == imghash:
            return True

        return False

    def run(self):
        """
        Run the screen shots.
        :return: bool
        """
        img_count = 0

        while self.capture:
            file_name = '/var/tmp/image{0}.jpg'.format(img_count)
            os.system('screencapture -x -t jpg {0}'.format(file_name))
            img_count += 1
            # Upload the images as we go here
            try:
                if not self.imgdiff(file_name):
                    nf = NetlogFile('shots/{0}'.format(file_name))
                    nf.close()
            except:
                pass
            # Clean things up the temp dir so we don't fill the disk on long running processes
            os.remove(file_name)
            time.sleep(self.sleeptime)

        return True
