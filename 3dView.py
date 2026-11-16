import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from TextureLoader import load_texture
from ObjLoader import ObjLoader

from camera import Camera

# Camera

cam = Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True
left, right, forward, backward, up, down = False, False, False, False, False, False

def key_input_clb(window, key, scancode, action, mode):
    global left, right, forward, backward, up, down

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)

    if key == glfw.KEY_W and action == glfw.PRESS:
        forward = True
    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True
    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True
    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        up = True
    if key in [glfw.KEY_LEFT_SHIFT, glfw.KEY_RIGHT_SHIFT] and action == glfw.PRESS:
        down = True

    if key in [glfw.KEY_W, glfw.KEY_S, glfw.KEY_A, glfw.KEY_D, glfw.KEY_SPACE, glfw.KEY_LEFT_SHIFT, glfw.KEY_RIGHT_SHIFT] and action == glfw.RELEASE:
        forward, backward, left, right, up, down = False, False, False, False, False, False

def do_movement():
    camera_speed = 0.005
    if forward:
        cam.process_keyboard("FORWARD", camera_speed)
    if backward:
        cam.process_keyboard("BACKWARD", camera_speed)
    if left:
        cam.process_keyboard("LEFT", camera_speed)
    if right:
        cam.process_keyboard("RIGHT", camera_speed)
    if up:
        cam.process_keyboard("UP", camera_speed)
    if down:
        cam.process_keyboard("DOWN", camera_speed)

def mouse_look_callback(window, xpos, ypos):
    global lastX, lastY, first_mouse

    if first_mouse:  
        lastX = xpos
        lastY = ypos
        first_mouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)

# Shaders

vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec2 v_texture;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

# Shader used when the model has a texture
fragment_src_textured = """
# version 330

in vec2 v_texture;

out vec4 out_color;

uniform sampler2D s_texture;

void main()
{
    out_color = texture(s_texture, v_texture);
}
"""

# Shader used when the model has NO texture (renders a flat grey colour)
vertex_src_no_tex = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_normal;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
}
"""

fragment_src_no_tex = """
# version 330

out vec4 out_color;

void main()
{
    out_color = vec4(0.8, 0.8, 0.8, 1.0);
}
"""


# GLFW setup

def window_resize(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)


if not glfw.init():
    raise Exception("glfw can not be initialized!")

window = glfw.create_window(WIDTH, HEIGHT, "My OpenGL window", None, None)

if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

glfw.set_window_pos(window, 400, 200)
glfw.set_window_size_callback(window, window_resize)
glfw.set_cursor_pos_callback(window, mouse_look_callback)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.set_key_callback(window, key_input_clb)
glfw.make_context_current(window)


# Load model

has_texture, mesh_index, mesh_buffer = ObjLoader.load_model("meshes/rat.obj")

# Choose shaders based on whether the model has texture coordinates
if has_texture:
    shader = compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src_textured, GL_FRAGMENT_SHADER)
    )
else:
    shader = compileProgram(
        compileShader(vertex_src_no_tex, GL_VERTEX_SHADER),
        compileShader(fragment_src_no_tex, GL_FRAGMENT_SHADER)
    )


# VAO / VBO

VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)

glBindVertexArray(VAO)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, mesh_buffer.nbytes, mesh_buffer, GL_STATIC_DRAW)

if has_texture:
    # Layout: [x y z] [u v] [nx ny nz]  →  stride = 8 floats
    stride = mesh_buffer.itemsize * 8
    # position (loc 0)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    # texture (loc 1)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
    # normal (loc 2)
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(20))
else:
    # Layout: [x y z] [nx ny nz]  →  stride = 6 floats
    stride = mesh_buffer.itemsize * 6
    # position (loc 0)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    # normal (loc 1)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))


# Texture (only when available) 

if has_texture:
    texture = glGenTextures(1)
    load_texture("meshes/rat.png", texture)


# OpenGL state 

glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 100)
mesh_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, -10]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc  = glGetUniformLocation(shader, "projection")
view_loc  = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
glUniformMatrix4fv(model_loc, 1, GL_FALSE, mesh_pos)


# Main loop 

while not glfw.window_should_close(window):
    glfw.poll_events()
    do_movement()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    glBindVertexArray(VAO)
    if has_texture:
        glBindTexture(GL_TEXTURE_2D, texture)

    glDrawArrays(GL_TRIANGLES, 0, len(mesh_index))

    glfw.swap_buffers(window)

glfw.terminate()