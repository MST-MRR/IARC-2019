#version 420 core

// should be 2 of the same things separated by 40px but wont shift
// https://stackoverflow.com/questions/14285849/trouble-with-imagestore-opengl-4-3

// test p574
layout (binding = 0, r32ui) uniform uimageBuffer colors;
layout (binding = 1, rgba32f) uniform image2D output_buffer;
out vec4 color;

void main(void){
  vec4 col = imageLoad(colors, gl_PrimitiveID &255);
  imageStore(output_buffer, ivec2(gl_FragCoord.xy) - ivec2(200,0), col);
  imageStore(output_buffer, ivec2(gl_FragCoord.xy) + ivec2(200,0), col);
  color = vec4(1.0,0.0, 0.0,1);
}