###########################################
# Created on 1-9-2013. Miguel Angel Astor #
###########################################
import math

PI = 3.14159

def angle_to_vector(angle):
    return [math.cos(angle), math.sin(angle)]

def normalize_vector_2D(vec):
    norm = norm2_2D(vec)
    return (vec[0] / norm, vec[1] / norm)

def dot_product_2D(vec1, vec2):
    return (vec1[0] * vec2[0]) + (vec1[1] * vec2[1])

def norm2_2D(vec):
    return math.sqrt(dot_product_2D(vec, vec))

def angle_vectors_2D(vec1, vec2):
    return math.atan2(vec2[1], vec2[0]) - math.atan2(vec1[1], vec1[0])

def ang_2_radians(ang):
    return (ang * PI) / 180.0

def radians_2_ang(rad):
    return (rad * 180.0) / PI
