#version 430 core

/* Notes 
* uniform means no change for each shader call, no change
* p577
* https://stackoverflow.com/questions/18553791/glsl-fragment-shader-struct-out
* https://stackoverflow.com/questions/21538555/broken-glsl-spinlock-glsl-locks-compendium
*/

/*
// single data item
struct ssbo_data
{ 
    int foo;
    float bar[42];
    float baz[20];
};

// buffer block
layout(std430, binding=6) buffer layoutname
{
  ssbo_data data_SSBO[]; // render time sized array
};
*/
layout (r32ui) uniform uimage2D overdraw_count;

out vec3 color;

void main(){
  // goal make data persist across fragments(executing in parallel)
  
  // Idea #1 - struct that is shared across fragments w/ locks
  // Idea #2 - buffer shared across program w/ locks


//GLuint count = 0;
imageAtomicAdd(overdraw_count, ivec2(gl_FragCoord.xy), 1);

  
  //layoutname.baz[10] += 1;

  /*if(count > 1){   // layoutname.baz[10] > 1){// gl_FragCoord.x > 512){
    color = vec3(1,0,0);
  } else {
    color = vec3(0,1,0);
  }*/
}
