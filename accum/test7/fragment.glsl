#version 420 core

layout (r32ui) uniform uimageBuffer image_buffer;  

//layout (r32ui) uniform uimage2D image_buffer;

uniform sampler2D my_texture;

in vec2 tex_coord;

layout (location=0) out vec4 fragment_color;


void main(void){
    vec4 texel_color = texture(my_texture, tex_coord);

    // do differently for each pixel

    int loc = int(mod(gl_FragCoord.y * 1024 + gl_FragCoord.x, 10240 * 7680));
    uint counter = imageAtomicAdd(image_buffer, loc, 1);
    //uint count = imageAtomicAdd(my_texture, ivec2(gl_FragCoord.xy), 1);


    if (counter > 20000){  // Since not resetting each frame
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