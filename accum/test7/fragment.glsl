#version 420 core

layout (r32ui) uniform uimageBuffer image_buffer;  

// layout (r32ui) uniform uimage2D image_buffer;

uniform sampler2D my_texture;

in vec2 tex_coord;

layout (location=0) out vec4 fragment_color;


void main(void){
    vec4 texel_color = texture(my_texture, tex_coord);

    // do differently for each pixel
    uint counter = imageAtomicAdd(image_buffer, 0, 1);
    
    if(counter > 300000000){  // Since not resetting each frame
      fragment_color = vec4(
        1.0,
        0.0, 
        0.0,
        1);
    } else {
      fragment_color = vec4(
        texel_color.r,
        texel_color.g,
        texel_color.b,
        1);
    }
}