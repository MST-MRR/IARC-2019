#version 430

// https://pixelclear.github.io/technical/post/2017/10/29/Over-Draw-Count.html
// will crash u

layout(binding = 0, r32ui) uniform uimage2D overdraw_count;
layout(binding = 1, r32ui) uniform uimage2D image_lock;

void mutex_lock(ivec2 pos)
{
  uint lock_available;
 do
 {
   lock_available = imageAtomicCompSwap(image_lock, pos, 0, 1);

 }while( lock_available == 0);
}

void mutex_unlock(ivec2 pos)
{
  imageStore(image_lock, pos, uvec4(0));
}

out vec4 color;
void main()                                                                                 
{                  
     mutex_lock(ivec2(gl_FragCoord.xy));           
     uint count = imageLoad(overdraw_count, ivec2(gl_FragCoord.xy)).x;
	 count = count+1;
	 imageStore(overdraw_count, ivec2(gl_FragCoord.xy), uvec4(count));
	 mutex_unlock(ivec2(gl_FragCoord.xy));                                                
}

//Fragment_Shader.fs  // breaks code