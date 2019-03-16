#include<iostream>
#include<string>
#include<vector>
#include<fstream>
#include <GL/glew.h>
#include<GL/freeglut.h>
#include<glm/glm.hpp>
#include<glm/ext.hpp>
#include "main.h"
#define MAX_FRAMEBUFFER_WIDTH 1350
#define MAX_FRAMEBUFFER_HEIGHT 700

using std::cout;
using std::string;
using std::ifstream;
using std::ofstream;

/*
Data to render quad
*/

GLuint IBO;
GLuint quad_render_vbo;
GLuint quad_render_vao;
GLuint quad_render_obj_vs;
GLuint quad_render_obj_fs;
GLuint quad_render_prog;
GLuint quad_tex_buffer;
GLuint quad_texture_location;


GLfloat quad_vertexData[] = {
	1.0f,  -1.0f,  0.0f,
	1.0f, 1.0f, 0.0f ,
	-1.0f, -1.0f, 0.0f,
	-1.0f, 1.0f, 0.0f
}; // 4 ve

GLfloat quad_texData[] = {
	1.0f,  0.0f,
	1.0f, 1.0f,
	0.0f, 0.0f,
	0.0f, 1.0f
}; // 

static const GLushort quad_vertex_indices[] =
{
	0,1,2,2,3,1
};

const char* quad_vertex_source[] ={
	"#version 430\n"
	"layout (location = 0) in vec3 vposition;\n"
	"layout (location = 1) in vec2 TexCoord;\n"
	"out vec2 TexCoord0;\n"
	"void main() {\n"
	"TexCoord0     = TexCoord;\n"
	"gl_Position = vec4(vposition,1.0);\n"
	"}\n"};

//texture(tex,TexCoord0)
const char* quad_fragment_source[] ={
	"#version 430\n"
	"in vec2 TexCoord0;\n"
	"layout(binding = 0, r32ui) uniform uimage2D output_image;\n"
	"void main() {\n"
	" gl_FragColor = vec4(imageLoad(output_image, ivec2(gl_FragCoord.xy)).x/32.0,0.0,0.0,1.0);\n"
	"}\n"};

GLuint overdrawImage;
GLuint imageLock;
GLuint imageLockClearBuffer;

glm::mat4 projection;
glm::mat4 view;
glm::mat4 model;
float cameraZoom = 3.0f;
float cameraX = 0.0f;


GLfloat eye_world_pos [] = {0.0,0.0,0.0};
GLfloat light_dir [] = {125.0,125.0,0.0};
GLfloat light_color [] = {0.5,0.5,1.0};

string vertex_source;
string fragment_source;
string tcs_shader_source;
string tes_shader_source;


GLuint vs_shader_object;
GLuint fs_shader_object;

GLuint render_prog;

GLuint MVP_Location;

GLuint VAO;
GLuint VBO[1];

int window_height;
int window_width;

GLuint overdraw_clear_buffer;
glm::vec4 * data;
unsigned int* data1;

bool PrepareOverDrawImage()
{
	glGenTextures(1,&overdrawImage);
	glBindTexture(GL_TEXTURE_2D, overdrawImage);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_R32UI, MAX_FRAMEBUFFER_WIDTH, MAX_FRAMEBUFFER_HEIGHT, 0, GL_RED_INTEGER, GL_UNSIGNED_INT, NULL);
	glBindTexture(GL_TEXTURE_2D, 0);
	
	glGenBuffers(1, &overdraw_clear_buffer);
    glBindBuffer(GL_PIXEL_UNPACK_BUFFER, overdraw_clear_buffer);
    glBufferData(GL_PIXEL_UNPACK_BUFFER, MAX_FRAMEBUFFER_WIDTH * MAX_FRAMEBUFFER_HEIGHT * sizeof(GLuint), NULL, GL_STATIC_DRAW);

    data = (glm::vec4 *)glMapBuffer(GL_PIXEL_UNPACK_BUFFER, GL_WRITE_ONLY);
    memset(data, 0x00, MAX_FRAMEBUFFER_WIDTH * MAX_FRAMEBUFFER_HEIGHT * sizeof(GLuint));
    glUnmapBuffer(GL_PIXEL_UNPACK_BUFFER);

	glGenTextures(1,&imageLock);
	glBindTexture(GL_TEXTURE_2D, imageLock);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_R32UI, MAX_FRAMEBUFFER_WIDTH, MAX_FRAMEBUFFER_HEIGHT, 0, GL_RED_INTEGER, GL_UNSIGNED_INT, NULL);
	glBindTexture(GL_TEXTURE_2D, 0);
	
	glGenBuffers(1, &imageLockClearBuffer);
    glBindBuffer(GL_PIXEL_UNPACK_BUFFER, imageLockClearBuffer);
    glBufferData(GL_PIXEL_UNPACK_BUFFER, MAX_FRAMEBUFFER_WIDTH * MAX_FRAMEBUFFER_HEIGHT * sizeof(GLuint), NULL, GL_STATIC_DRAW);

    data1 = (unsigned int*)glMapBuffer(GL_PIXEL_UNPACK_BUFFER, GL_WRITE_ONLY);
    memset(data, 0x00, MAX_FRAMEBUFFER_WIDTH * MAX_FRAMEBUFFER_HEIGHT * sizeof(GLuint));
    glUnmapBuffer(GL_PIXEL_UNPACK_BUFFER);

	glBindTexture(GL_TEXTURE_2D, 0);
	glBindBuffer(GL_PIXEL_UNPACK_BUFFER, 0);

	return true;
}

void LoadModel(void) {

    
    std::string inputfile = "low_poly.obj";
    std::vector<tinyobj::shape_t> shapes;
    std::vector<tinyobj::material_t> materials;

    std::string err;
    printf("Loading model: %s", inputfile.c_str() );
    bool ret = tinyobj::LoadObj(shapes, materials, err, inputfile.c_str());

    if (!err.empty()) {
	printf("%s\n", err.c_str() );
    }
    if (!ret) {
	exit(1);
    }

    mesh.vertices = shapes[0].mesh.positions;
    mesh.faces = shapes[0].mesh.indices;
    mesh.normals = shapes[0].mesh.normals;
	    
	glGenVertexArrays(1,&VAO);
	glBindVertexArray(VAO);

    (glGenBuffers(1, &mesh.indexVbo));
    (glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh.indexVbo));
    (glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(GLuint)* mesh.faces.size(), mesh.faces.data(), GL_STATIC_DRAW));

    (glGenBuffers(1, &mesh.vertexVbo));
    (glBindBuffer(GL_ARRAY_BUFFER, mesh.vertexVbo));
    (glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat)*mesh.vertices.size(), mesh.vertices.data() , GL_STATIC_DRAW));


    (glGenBuffers(1, &mesh.normalVbo));
    (glBindBuffer(GL_ARRAY_BUFFER, mesh.normalVbo));
    (glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat)*mesh.normals.size(), mesh.normals.data() , GL_STATIC_DRAW));

    (glEnableVertexAttribArray(0));
    (glBindBuffer(GL_ARRAY_BUFFER, mesh.vertexVbo));
    (glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*)0));

    (glEnableVertexAttribArray(1));
    (glBindBuffer(GL_ARRAY_BUFFER, mesh.normalVbo));
    (glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, (void*)0));

	glBindBuffer(GL_ARRAY_BUFFER,0);
	glBindVertexArray(0);
}

bool PrepareShaders()
{
	GLint success;
	
	quad_render_obj_vs = glCreateShader(GL_VERTEX_SHADER);
	glShaderSource(quad_render_obj_vs,1,quad_vertex_source,NULL);
	glCompileShader(quad_render_obj_vs);

	
	glGetShaderiv(quad_render_obj_vs, GL_COMPILE_STATUS, &success);

	if (!success) {
		char InfoLog[1024];
		glGetShaderInfoLog(quad_render_obj_vs, 1024, NULL, InfoLog);
		fprintf(stderr, "Error compiling render vs: '%s'\n", InfoLog);
		return false;
	}

	quad_render_obj_fs = glCreateShader(GL_FRAGMENT_SHADER);
	glShaderSource(quad_render_obj_fs,1,quad_fragment_source,NULL);
	glCompileShader(quad_render_obj_fs);

	
	glGetShaderiv(quad_render_obj_fs, GL_COMPILE_STATUS, &success);

	if (!success) {
		char InfoLog[1024];
		glGetShaderInfoLog(quad_render_obj_fs, 1024, NULL, InfoLog);
		fprintf(stderr, "Error compiling : '%s'\n", InfoLog);
		return false;
	}

	quad_render_prog = glCreateProgram();
	glAttachShader(quad_render_prog,quad_render_obj_vs);
	glAttachShader(quad_render_prog,quad_render_obj_fs);
	glLinkProgram(quad_render_prog);

	quad_texture_location = glGetUniformLocation(render_prog, "tex");
	glUniform1i(quad_texture_location, 0);

	glGetShaderiv(render_prog, GL_LINK_STATUS, &success);

	if (!success) {
		char InfoLog[1024];
		glGetShaderInfoLog(render_prog, 1024, NULL, InfoLog);
		fprintf(stderr, "Error linking : '%s'\n", InfoLog);
		return false;
	}
	
	glDetachShader(quad_render_prog,quad_render_obj_vs);
	glDetachShader(quad_render_prog,quad_render_obj_fs);

	return true;
}
bool PrepareQuadVBO()
{
	glGenVertexArrays(1, &quad_render_vao);
	glBindVertexArray(quad_render_vao);
	
	glGenBuffers(1,&IBO);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,IBO);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(quad_vertex_indices), quad_vertex_indices,GL_STATIC_DRAW);

	glGenBuffers(1, &quad_render_vbo);
	glBindBuffer(GL_ARRAY_BUFFER, quad_render_vbo);
	glBufferData(GL_ARRAY_BUFFER,sizeof(quad_vertexData), quad_vertexData, GL_STATIC_DRAW);
	glEnableVertexAttribArray(0);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0);
	
	glGenBuffers(1,&quad_tex_buffer);
	glBindBuffer(GL_ARRAY_BUFFER, quad_tex_buffer);
	glBufferData(GL_ARRAY_BUFFER,sizeof(quad_texData), quad_texData, GL_STATIC_DRAW);
	glEnableVertexAttribArray(1);
	glVertexAttribPointer(1,2,GL_FLOAT, GL_FALSE, 0, 0);
    
	glBindBuffer(GL_ARRAY_BUFFER,0);
	glBindVertexArray(0);
	return true;
}

void RenderBlendedTeapot()
{
	
	{
		glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT);
		glDisable(GL_DEPTH);
	    glDisable(GL_DEPTH_TEST);
		glDisable(GL_CULL_FACE);
		glEnable(GL_BLEND);
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

		glUseProgram(render_prog);

		glBindBuffer(GL_PIXEL_UNPACK_BUFFER, imageLockClearBuffer);
		glBindTexture(GL_TEXTURE_2D, imageLock);
		glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, MAX_FRAMEBUFFER_WIDTH, MAX_FRAMEBUFFER_HEIGHT, GL_RED_INTEGER, GL_UNSIGNED_INT, NULL);
		glBindTexture(GL_TEXTURE_2D, 0);
		
		glBindBuffer(GL_PIXEL_UNPACK_BUFFER, overdraw_clear_buffer);
		glBindTexture(GL_TEXTURE_2D, overdrawImage);
		glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, MAX_FRAMEBUFFER_WIDTH, MAX_FRAMEBUFFER_HEIGHT, GL_RED_INTEGER, GL_UNSIGNED_INT, NULL);
		glBindTexture(GL_TEXTURE_2D, 0);
		glBindImageTexture(0, overdrawImage, 0, GL_FALSE, 0, GL_READ_WRITE, GL_R32UI);
		glBindImageTexture(1, imageLock, 0, GL_FALSE, 0, GL_READ_WRITE, GL_R32UI);

		for(int i = 0 ; i <20; i ++)
		{
			glBindVertexArray(VAO);
			view = glm::lookAt(glm::vec3(0.0,0.0,0.0),glm::vec3(0.0,0.0,-5.0),glm::vec3(0.0,1.0,0.0));
			model = glm::translate(glm::mat4(1.0),glm::vec3(i-1.0,-2.0,-cameraZoom-i));
			model = glm::rotate(model,cameraX,glm::vec3(0.0,1.0,0.0));
			glm::mat4 MVP = projection*view*model;
			glUniformMatrix4fv(MVP_Location, 1, GL_FALSE , &MVP[0][0]);
			glDrawElements(GL_TRIANGLES,mesh.faces.size(),GL_UNSIGNED_INT, 0);

			glBindVertexArray(0);
		}

		for(int i = 0 ; i <20; i ++)
		{
			glBindVertexArray(VAO);
			view = glm::lookAt(glm::vec3(0.0,0.0,0.0),glm::vec3(0.0,0.0,-5.0),glm::vec3(0.0,1.0,0.0));
			model = glm::translate(glm::mat4(1.0),glm::vec3(i-1.0,0.0,-cameraZoom-i));
			model = glm::rotate(model,cameraX,glm::vec3(0.0,1.0,0.0));
			glm::mat4 MVP = projection*view*model;
			glUniformMatrix4fv(MVP_Location, 1, GL_FALSE , &MVP[0][0]);
			glDrawElements(GL_TRIANGLES,mesh.faces.size(),GL_UNSIGNED_INT, 0);

			glBindVertexArray(0);
		}

		
		for(int i = 0 ; i <20; i ++)
		{
			glBindVertexArray(VAO);
			view = glm::lookAt(glm::vec3(0.0,0.0,0.0),glm::vec3(0.0,0.0,-5.0),glm::vec3(0.0,1.0,0.0));
			model = glm::translate(glm::mat4(1.0),glm::vec3(i-1.0,2.0,-cameraZoom-i));
			model = glm::rotate(model,cameraX,glm::vec3(0.0,1.0,0.0));
			glm::mat4 MVP = projection*view*model;
			glUniformMatrix4fv(MVP_Location, 1, GL_FALSE , &MVP[0][0]);
			glDrawElements(GL_TRIANGLES,mesh.faces.size(),GL_UNSIGNED_INT, 0);

			glBindVertexArray(0);
		}
		glUseProgram(0);
	}
    
}

void RenderQuad()
{
	glUseProgram(quad_render_prog);
	glBindVertexArray(quad_render_vao);
	glBindTexture(GL_TEXTURE_2D, overdrawImage);
	glBindImageTexture(0, overdrawImage, 0, GL_FALSE, 0, GL_READ_WRITE, GL_R32UI);
	glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_SHORT, 0);
	glBindVertexArray(0);
	glUseProgram(0);
}

bool ReadFile(const char* pFileName, string& outFile)
{
    ifstream f(pFileName);
    
    bool ret = false;
    
    if (f.is_open()) {
        string line;
        while (getline(f, line)) {
            outFile.append(line);
            outFile.append("\n");
        }
        
        f.close();
        
        ret = true;
    }
    else {
       cout << "Error Loading file";
    }
    
    return ret;
}



bool InitShaders()
{
	int success;

	ReadFile("shader.vs",vertex_source);
	ReadFile("shader.fs",fragment_source);

	const char* p[1];
	p[0] = vertex_source.c_str();
	GLint Lengths[1] = { (GLint)vertex_source.size() };

	vs_shader_object = glCreateShader(GL_VERTEX_SHADER);
	glShaderSource(vs_shader_object,1,p,NULL);
	glCompileShader(vs_shader_object);
	glGetShaderiv(vs_shader_object, GL_COMPILE_STATUS, &success);
	
    if (!success) {
        char InfoLog[1024];
        glGetShaderInfoLog(vs_shader_object, 1024, NULL, InfoLog);
        std::cout <<"Error compiling : '%s'\n" <<InfoLog;
        return false;
    }

	const char* p1[1];
	p1[0] = fragment_source.c_str();
	GLint Lengths1[1] = { (GLint)fragment_source.size() };

	fs_shader_object = glCreateShader(GL_FRAGMENT_SHADER);
	glShaderSource(fs_shader_object,1,p1,NULL);
	glCompileShader(fs_shader_object);
	glGetShaderiv(fs_shader_object, GL_COMPILE_STATUS, &success);
	
    if (!success) {
        char InfoLog[1024];
        glGetShaderInfoLog(fs_shader_object, 1024, NULL, InfoLog);
        std::cout <<"Error compiling : '%s'\n" <<InfoLog;
        return false;
    }


	render_prog = glCreateProgram();
	glAttachShader(render_prog,vs_shader_object);
	glAttachShader(render_prog,fs_shader_object);

	glLinkProgram(render_prog);
	std::cout<<"\nError: '%s'\n"<<glewGetErrorString(glGetError());
	glGetProgramiv(render_prog, GL_LINK_STATUS, &success);
	
    if (!success) {
        char InfoLog[1024];
        glGetProgramInfoLog(render_prog, 1024, NULL, InfoLog);
        std::cout <<"Error Linking: '%s'\n" <<InfoLog;
        return false;
    }

	glValidateProgram(render_prog);
	glGetProgramiv(render_prog, GL_VALIDATE_STATUS, &success);
    if (!success) {
		char InfoLog[1024];
		glGetProgramInfoLog(render_prog, 1024, NULL, InfoLog);
        fprintf(stderr, "Invalid shader program: '%s'\n", InfoLog);
     return false;
    }

	glDetachShader(render_prog,vs_shader_object);
	glDetachShader(render_prog,fs_shader_object);

	glUseProgram(render_prog);

	MVP_Location = glGetUniformLocation(render_prog, "MVP_matrix");

return true;
}

void Key(unsigned char key, int x, int y)
{
	switch(key)
	{
	case 'a' :
		cameraZoom -= 0.1;
		break;
	case 'z':
		cameraZoom +=0.1;
		break;
	case 'r':
		cameraX +=0.1;
		break;
	case 'w':
		cameraX -= 0.1;
		break;
	}

}

void Display()
{
	RenderBlendedTeapot();
	RenderQuad();
	glutSwapBuffers();
	glutPostRedisplay();
}

void ChangeSize(int w, int h)
{
	glClearColor(0.0,0.0,0.0,1.0);
	glViewport(0,0,w,h);
	projection = glm::perspective(45.0f,w/(float)h,0.1f, 100.0f);
	window_width = w;
	window_height = h;
}

void Clear()
{
	glDeleteVertexArrays(1,&quad_render_vao);
	glDeleteBuffers(1,&quad_render_vbo);
	glDeleteShader(quad_render_obj_vs);
	glDeleteShader(quad_render_obj_fs);
	glDeleteProgram(quad_render_prog);
	glDeleteBuffers(1, &quad_tex_buffer);
	glDeleteTextures(1,&overdrawImage);
	glDeleteBuffers(1, &imageLockClearBuffer);
	glDeleteTextures(1, &imageLock);
	glDeleteShader(vs_shader_object);
	glDeleteShader(fs_shader_object);
	glDeleteProgram(render_prog);
	glDeleteVertexArrays(1, &VAO);
	glDeleteBuffers(1, VBO);
}

int main(int argc, char* argv[])
{
	glutInit(&argc,argv);
	glutInitDisplayMode(GLUT_RGBA|GLUT_DEPTH|GLUT_DOUBLE);
	
	glutInitWindowPosition(0,0);
	glutInitWindowSize(MAX_FRAMEBUFFER_WIDTH,MAX_FRAMEBUFFER_HEIGHT);
	glutCreateWindow("TeslaOverDraw");

	GLenum res = glewInit();
    if (res != GLEW_OK) {
       std::cout<<"Error: '%s'\n"<<glewGetErrorString(res);
        return false;
    }

	glutDisplayFunc(Display);
	glutKeyboardFunc(Key);
	glutReshapeFunc(ChangeSize);
	
	InitShaders();
	LoadModel();
	PrepareOverDrawImage();
	PrepareQuadVBO();
	PrepareShaders();
	
	glutMainLoop();
	Clear();
	return 0;
}
