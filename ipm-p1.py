#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import locale
import gettext
import pathlib
from pathlib import Path

from controlador import Controlador

if __name__ == '__main__':
	LOCALE_DIR = Path(__file__).parent / "locale"
	locale.bindtextdomain('ipm-p1', LOCALE_DIR)
	gettext.bindtextdomain('ipm-p1', LOCALE_DIR)
	gettext.textdomain('ipm-p1')

	controlador = Controlador()
	controlador.run()