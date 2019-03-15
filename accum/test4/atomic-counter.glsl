#version 330 core

// change back to 430

out vec3 color;
void main(){
  color = vec3(1,0,0);
}

/*
//layout (r32ui) uniform uimageBuffer counter_buffer;  // not layout in book

layout (binding=0, offset=0) uniform atomic_uint countboi;
// offset += 4 for next atomic


uniform sampler2D my_texture;

in vec2 tex_coord;

layout (location=0) out vec4 fragment_color;

void main(void){
    vec4 texel_color = texture(my_texture, tex_coord);
    
    uint counter = imageAtomicAdd(countboi, 0, 1);

    //uint counter =  atomicCounterIncrement(countboi);
    // atomic counter returns c's prior value!

    if(counter > 0){
      fragment_color = vec4(
        1.0, // - texel_color.r,
        1.0,// - texel_color.g,
        1.0,// - texel_color.b,
        1);
    } else {
      fragment_color = vec4(
        texel_color.r,
        texel_color.g,
        texel_color.b,
        1);
    }
}

// check book pg 574
*/