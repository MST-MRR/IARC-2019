#version 420 core

// layout (binding=0, offset=0) uniform atomic_uint countboi;
// uint counter =  atomicCounterIncrement(image_buffer);
/*
// should be 2 of the same things separated by 40px but wont shift
// https://stackoverflow.com/questions/14285849/trouble-with-imagestore-opengl-4-3

// test p574
layout (binding = 0, r32ui) uniform uimageBuffer colors;
layout (binding = 1, rgba32f) uniform image2D output_buffer;
out vec4 color;

  vec4 col = imageLoad(colors, gl_PrimitiveID &255);
  imageStore(output_buffer, ivec2(gl_FragCoord.xy) - ivec2(200,0), col);
  imageStore(output_buffer, ivec2(gl_FragCoord.xy) + ivec2(200,0), col);
  color = vec4(1.0,0.0, 0.0,1);
*/

layout (r32ui) uniform uimageBuffer image_buffer;  

uniform sampler2D my_texture;

in vec2 tex_coord;

layout (location=0) out vec4 fragment_color;

// not double counting intersections & middle vertical lines


// Now trying shader buffer storage p576

// do i try overdraw counting with shader buffer or what

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