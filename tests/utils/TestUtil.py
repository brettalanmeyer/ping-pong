from BaseTest import BaseTest
from datetime import datetime
from pingpong.utils import util
import json

class TestUtil(BaseTest):

	def test_param(self):
		with self.request:
			test1 = util.param("test1")
			assert test1 == None

			test2 = util.param("test2", "A Value")
			assert test2 == "A Value"

			test3 = util.param("test3", "7")
			assert test3 == "7"
			assert test3 != 7

			test4 = util.param("test4", "9", "int")
			assert test4 == 9
			assert test4 != "9"

			test5 = util.param("test5", "9", "str")
			assert test5 == "9"
			assert test5 != 9

	def test_paramForm(self):
		with self.request:
			test1 = util.paramForm("test1")
			assert test1 == None

			test2 = util.paramForm("test2", "A Value")
			assert test2 == "A Value"

			test3 = util.paramForm("test3", "7")
			assert test3 == "7"
			assert test3 != 7

			test4 = util.paramForm("test4", "9", "int")
			assert test4 == 9
			assert test4 != "9"

			test5 = util.paramForm("test5", "9", "str")
			assert test5 == "9"
			assert test5 != 9

	def test_jsonSerial(self):
		assert json.dumps({}) == "{}"
		assert json.dumps({ "key": "value" }) == '{"key": "value"}'

		data = {
			"time": datetime(2016, 01, 01, 01, 01, 01)
		}

		with self.assertRaises(Exception) as context:
			json.dumps(data)
		assert "is not JSON serializable" in str(context.exception)

		serialized = json.dumps(data, default = util.jsonSerial)
		assert serialized == '{"time": "2016-01-01 01:01:01"}'

	def test_shuffle(self):
		array1 = [1]
		array2 = util.shuffle(array1)
		assert array1 == array2

		array3 = [1,2]
		array4 = util.shuffle(array3)
		assert array3[0] == array4[1]
		assert array3[1] == array4[0]

		array5 = [1,2,3]
		array6 = util.shuffle(array5)
		assert array5 != array6
		assert len(array5) == 3
		assert len(array6) == 3

		array7 = [1,2,3,4]
		for i in range(0, 100):
			array8 = util.shuffle(array7)
			assert array7 != array8

	def test_hasConfig(self):
		with self.ctx:
			assert util.hasConfig("TESTING")
			assert util.hasConfig("DEBUG")
			assert util.hasConfig("ADMIN_USERNAME")
			assert util.hasConfig("ADMIN_PASSWORD")
			assert not util.hasConfig("TEST_CONFIG")
			assert not util.hasConfig("asdf")
			assert not util.hasConfig("qwer")

	def test_date(self):
		now = datetime.now()
		assert str(now) == util.date(now)
		assert None == util.date(None)

	def test_generateUUID(self):
		uuid1 = util.generateUUID()
		uuid2 = util.generateUUID()
		assert uuid1 != None
		assert len(uuid1) == 36
		assert uuid1 != uuid2

	def test_formatTime(self):
		assert util.formatTime(0) == "00:00:00"
		assert util.formatTime(100) == "00:01:40"
		assert util.formatTime(120) == "00:02:00"
		assert util.formatTime(3600) == "01:00:00"
		assert util.formatTime(49813) == "13:50:13"
		assert util.formatTime(359999) == "99:59:59"

	def test_hash(self):
		assert util.hash("some string") == "21bc225587d8768058837b68fe7e0341e87b972f02fd8fb0c236d1d3"
