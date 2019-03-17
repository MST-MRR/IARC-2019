#version 420 core

// !!!
// Note p577 declaration of strucuted data

// Maybe need to declare structure and edit a specific part of structure


// image to count overdraw
layout (r32ui) uniform uimage2D overdraw_count;

//uniform sampler2D my_texture;

//in vec2 tex_coord;

//layout (location=0) out vec4 fragment_color;

void main(void){
    // read current counter  gl_FragCoord = tex_coord
    uint count = imageLoad(overdraw_count, ivec2(gl_FragCoord.xy));

    count += 1;

    // write to image
    imageStore(output_buffer, ivec2(gl_FragCoord.xy), count);

    /*
    if(True){  // Since not resetting each frame
      fragment_color = vec4(
        1.0,
        0.0, 
        0.0,
        1);
    } else {
      fragment_color = vec4(
        0.0, 0.0, 0.0,
        1);
    }*/
}