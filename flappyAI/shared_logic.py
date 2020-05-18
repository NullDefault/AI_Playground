import pygame as pg


def load(path):
    return pg.transform.scale2x(pg.image.load(path)).convert()
