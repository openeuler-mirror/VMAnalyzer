
# Copyright (c) 2023. China Mobile (SuZhou) Software Technology Co.,Ltd.
# VMAnalyzer is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of
# the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import unittest

from utils.validators import (
    validate_interval,
    validate_timeout,
    validate_vm_id
)


class TestValidators(unittest.TestCase):

    def test_validate_interval(self):
        """Test validate_interval: positive int -> True, others -> False."""
        self.assertTrue(validate_interval(5))
        self.assertFalse(validate_interval(0))
        self.assertFalse(validate_interval(-1))
        self.assertFalse(validate_interval("5"))
        self.assertFalse(validate_interval(5.5))

    def test_validate_timeout(self):
        """Test validate_timeout: positive int -> True, others -> False."""
        self.assertTrue(validate_timeout(30))
        self.assertFalse(validate_timeout(0))
        self.assertFalse(validate_timeout(-5))
        self.assertFalse(validate_timeout("10"))
        self.assertFalse(validate_timeout(None))

    def test_validate_vm_id(self):
        """Test validate_vm_id: non-negative int -> True, others -> False."""
        self.assertTrue(validate_vm_id(0))
        self.assertTrue(validate_vm_id(100))
        self.assertFalse(validate_vm_id(-1))
        self.assertFalse(validate_vm_id("1"))
        self.assertFalse(validate_vm_id(5.0))
        self.assertFalse(validate_vm_id(None))

if __name__ == '__main__':
    unittest.main()
