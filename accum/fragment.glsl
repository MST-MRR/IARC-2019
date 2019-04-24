#version 420 core

layout (r32ui) uniform uimageBuffer image_buffer;  

// uniform sampler2D my_texture;

out vec4 fragment_color;

void main(void){
    int loc = int(mod(gl_FragCoord.y * 1024 + gl_FragCoord.x, 10240 * 7680));
    uint counter = imageAtomicAdd(image_buffer, loc, 1);

    if (counter > 20000){
      fragment_color = vec4(
        1.0,
        0.0, 
        0.0,
        1);
    } else {
      fragment_color = vec4(
        0.0, 
        0.0, 
        0.0,
        1);
    }
}