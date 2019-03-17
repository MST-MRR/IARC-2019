#version 420 core

// layout (binding=0, offset=0) uniform atomic_uint countboi;
// uint counter =  atomicCounterIncrement(image_buffer);
// not double counting intersections & middle vertical lines

// Now trying shader buffer storage p576
// do i try overdraw counting with shader buffer or what


layout (r32ui) uniform uimageBuffer image_buffer;  

uniform sampler2D my_texture;

in vec2 tex_coord;

layout (location=0) out vec4 fragment_color;


void main(void){
    vec4 texel_color = texture(my_texture, tex_coord);

    // May change from atomic adding to imageLoad or something meant for texture
    // pg 572
    
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