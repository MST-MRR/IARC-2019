#version 420 core

layout (r32ui) uniform uimageBuffer image_buffer;  

void main(void){
    int loc = int(mod(gl_FragCoord.y * 1024 + gl_FragCoord.x, 10240 * 7680));
    uint counter = imageAtomicAdd(image_buffer, loc, 1);
}