#version 420 core


// Buffer containing palette of colors to mark primitive
layout  (binding = 0, rgba32f) uniform imageBuffer colors;

// Buffer to write
layout (binding = 1, rgba32f) uniform image2D output_buffer;

out vec4 color;


layout (r32ui) uniform uimage2D overdraw_count;

void main(void){
  

  // load color from pallete to mark primitives by image2D
  vec4 col = imageLoad(colors, gl_PrimitiveID & 255);

  // store resulting fragment in 2 locations 
  // fragments window & 
  imageStore(output_buffer, ivec2(gl_FragCoord.xy) - ivec2(200, 0), col);
  
  // location shifted right
  imageStore(output_buffer, ivec2(gl_FragCoord.xy) + ivec2(200, 0), col);



  // Read overdraw counter
  //uint count = imageLoad(overdraw_count, ivec2(gl_FragCoord.xy));
  
  //count = count + 1;

  // Write to image
  //imageStore(output_buffer, ivec2(gl_FragCoord.xy), count);




  imageAtomicAdd(overdraw_count, ivec2(gl_FragCoord.xy), 1);
}