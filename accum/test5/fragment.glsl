#version 430 core

/*layout(std430, binding=6) buffer layoutname
{
  int data_SSBO[];
};*/

struct ssbo_data
{ //https://stackoverflow.com/questions/18553791/glsl-fragment-shader-struct-out
    int foo;
    float bar[42];
    float baz[20];
};

// uniform means no change for each shader call, no change
ssbo_data testeroni;

out vec3 color;

void main(){
  // goal make data persist across fragments(executing in parallel)
  
  // Idea #1 - struct that is shared across fragments w/ locks
  // Idea #2 - buffer shared across program w/ locks

  // https://stackoverflow.com/questions/21538555/broken-glsl-spinlock-glsl-locks-compendium

  testeroni.baz[10] += 1;

  if(testeroni.baz[10] > 0){// gl_FragCoord.x > 512){
    color = vec3(1,0,0);
  } else {
    color = vec3(0,1,0);
  }
}
