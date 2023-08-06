import lxml.html
from typing import Union

from . import atserver
from . import atconnect

FTYPE_FILE = 0
FTYPE_DIR = 1

class AternosFile:

	def __init__(
		atserv:atserver.AternosServer,
		path:str, name:str, ftype:int=FTYPE_FILE,
		size:Union[]=0) -> None:

		self.atserv = atserv
		self._name = name
		self._ftype = ftype
		self._size = float(size)

	def delete(self) -> None:

		self.atserv.atserver_request(
			'https://aternos.org/panel/ajax/delete.php',
			atconnect.REQPOST, data={'file': self._name},
			sendtoken=True
		)

	@property
	def text(self) -> str:
		editor = self.atserv.atserver_request(
			f'https://aternos.org/files/{self._name}',
			atconnect.REQGET
		)
		edittree = lxml.html.fromstring(editor.content)

		editfield = edittree.xpath('//div[@class="ace_layer ace_text-layer"]')[0]
		editlines = editfield.xpath('/div[@class="ace_line"]')
		rawlines = []

		for line in editlines:
			rawlines.append(line.text)
		return rawlines

	@text.setter
	def text(self, value:Union[str,bytes]) -> None:
		self.atserv.atserver_request(
			f'https://aternos.org/panel/ajax/save.php',
			atconnect.REQPOST, data={'content': value},
			sendtoken=True
		)

	@property
	def name(self) -> str:
		return self._name

	@property
	def ftype(self) -> int:
		return self._ftype
	
	@property
	def size(self) -> float:
		return self._size
