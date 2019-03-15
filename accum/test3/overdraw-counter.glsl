#version 420 core

// image to count overdraw
layout (r32ui) uniform uimage2D overdraw_count;

void main(void){
    // read current counter
    uint cout = imageLoad(overdraw_count, ivec2(gl_FragCoord.xy));

    count += 1;

    // write to image
    imageStore(output_buffer, ivec2(gl_FragCoord.xy), count);
}