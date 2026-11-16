import numpy as np


class ObjLoader:
    buffer = []

    @staticmethod
    def search_data(data_values, coordinates, skip, data_type):
        for d in data_values:
            if d == skip:
                continue
            if data_type == 'float':
                coordinates.append(float(d))
            elif data_type == 'int':
                coordinates.append(int(d) - 1)


    @staticmethod  # sorted vertex buffer for use with glDrawArrays function
    def create_sorted_vertex_buffer(indices_data, vertices, textures, normals, has_texture):
        for entry in indices_data:
            if has_texture:
                v_idx, vt_idx, vn_idx = entry
            else:
                v_idx, vn_idx = entry

            # vertex position (3 floats)
            start = v_idx * 3
            ObjLoader.buffer.extend(vertices[start:start + 3])

            # texture coords (2 floats, only when available)
            if has_texture:
                start = vt_idx * 2
                ObjLoader.buffer.extend(textures[start:start + 2])

            # normal (3 floats)
            start = vn_idx * 3
            ObjLoader.buffer.extend(normals[start:start + 3])


    @staticmethod
    def show_buffer_data(buffer):
        stride = 8  # 3 pos + 2 tex + 3 norm
        for i in range(len(buffer) // stride):
            start = i * stride
            end = start + stride
            print(buffer[start:end])


    @staticmethod
    def _parse_face_vertex(token, has_texture):
        """
        Parse a single face token. Handles all OBJ face formats:
            '5'      ->  vertex only
            '5/3'    ->  v/vt
            '5//2'   ->  v//vn
            '5/3/2'  ->  v/vt/vn
        Returns a tuple of zero-based indices.
        """
        parts = token.split('/')
        v_idx  = int(parts[0]) - 1
        vt_raw = parts[1] if len(parts) > 1 else ''
        vn_raw = parts[2] if len(parts) > 2 else ''

        vt_idx = (int(vt_raw) - 1) if vt_raw else 0
        vn_idx = (int(vn_raw) - 1) if vn_raw else 0

        if has_texture:
            return (v_idx, vt_idx, vn_idx)
        else:
            return (v_idx, vn_idx)


    @staticmethod
    def load_model(file):
        vert_coords = []  # all vertex positions
        tex_coords  = []  # all UV coordinates
        norm_coords = []  # all vertex normals

        face_entries = []  # parsed per-vertex tuples
        indices = []       # v_idx list for vertex count

        has_texture = False

        with open(file, 'r') as f:
            line = f.readline()
            while line:
                values = line.split()
                if not values:
                    line = f.readline()
                    continue

                if values[0] == 'v':
                    ObjLoader.search_data(values, vert_coords, 'v', 'float')
                elif values[0] == 'vt':
                    ObjLoader.search_data(values, tex_coords, 'vt', 'float')
                    has_texture = True
                elif values[0] == 'vn':
                    ObjLoader.search_data(values, norm_coords, 'vn', 'float')
                elif values[0] == 'f':
                    for tok in values[1:]:
                        entry = ObjLoader._parse_face_vertex(tok, has_texture)
                        face_entries.append(entry)
                        indices.append(entry[0])

                line = f.readline()

        # Build the interleaved VBO data
        ObjLoader.create_sorted_vertex_buffer(face_entries, vert_coords, tex_coords, norm_coords, has_texture)

        # ObjLoader.show_buffer_data(ObjLoader.buffer)

        buffer = ObjLoader.buffer.copy()
        ObjLoader.buffer = []

        return has_texture, np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')
