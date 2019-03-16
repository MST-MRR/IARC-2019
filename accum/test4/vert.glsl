#version 430
layout(location = 0) in vec3 pos;
layout(location = 1) in vec3 normal;

uniform mat4 MVP_matrix;

void main()
{
	gl_Position = MVP_matrix * vec4(pos,1.0);
}