#!/usr/bin/env python3

import sys
import textwrap
from collections import namedtuple
import time

import gi
gi.require_version('Atspi', '2.0')
from gi.repository import Atspi

import e2e

# Funciones de ayuda

def show(text):
    print(textwrap.dedent(text))

def show_passed():
    print('\033[92m', "    Passed", '\033[0m')

def show_not_passed(e):
    print('\033[91m', "    Not passed", '\033[0m')
    print(textwrap.indent(str(e), "    "))


# Contexto de las pruebas

Ctx = namedtuple("Ctx", "path process app")


# Implementacion de los pasos

def given_he_lanzado_la_aplicacion(ctx):
    process, app = e2e.run(ctx.path)
    assert app is not None
    return Ctx(path=ctx.path, process=process, app=app)

def when_pulso_la_pagina_3M(ctx):
    gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'page tab list')
    item = next(gen, None)
    assert item is not None
    item.select_child(2)
    return ctx

def when_pulso_asc(ctx):
    gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'push button' and node.get_name() == 'Ascendente')
    boton = next(gen, None)
    assert boton is not None
    e2e.do_action(boton, 'click')
    return ctx

def then_veo_lista_canciones(ctx):
    gen = (node for _path, node in e2e.tree(ctx.app) if node.get_role_name() == 'table cell' and node.get_text(0, -1).startswith("La primavera"))
    label = next(gen, None)
    assert label and label.get_text(0, -1) == "La primavera (Vivaldi)"
    return ctx

if __name__ == '__main__':
    sut_path = sys.argv[1]
    initial_ctx = Ctx(path = sut_path, process = None, app = None)

    show("""
    GIVEN he lanzado la aplicacion
    WHEN pulso la página 3M
    WHEN pulso el botón Ascendente
    THEN veo la lista de canciones
    """)
    ctx = initial_ctx
    try:
        ctx = given_he_lanzado_la_aplicacion(ctx)
        ctx = when_pulso_la_pagina_3M(ctx)
        ctx = when_pulso_asc(ctx)
        ctx = then_veo_lista_canciones(ctx)
        show_passed()
    except  Exception as e:
        show_not_passed(e)
    e2e.stop(ctx.process)
