#!/bin/python

import unittest as utest
from libs.lmodem import Modem

class libModemTest(utest.TestCase):
    def test_info(self):
        with open("utest_files/mmcli_sim/sim_modem.txt") as fileSimModem:
            simModem = fileSimModem.read()

            # modem = Modem('0')
            simModemInfo = Modem.extractInfo( simModem )

            # string single key
            self.assertEqual( simModemInfo['modem.generic.access-technologies.length'], '1' )
            # string multiple keys
            self.assertEqual( simModemInfo['modem']['3gpp']['imei'], '358812037638331' )

            '''
            <<Pending Cases to work on>>
            TODO: (broken case): Make this case work without breaking everything -- 
            self.assertEqual( simModemInfo['modem']['generic']['access-technologies']['length'], '1' )
            '''


if __name__ == '__main__':
    utest.main()