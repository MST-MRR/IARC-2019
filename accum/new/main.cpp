#include <stdio.h>
#include <stdlib.h>
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
using namespace glm;

#include <opencv2/opencv.hpp>

#include <iostream>
#include <stdexcept>
#include <vector>
#include <map>
#include <fstream>

#include "loader.h"

void GLAPIENTRY MessageCallback( GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar* message, const void* userParam ){fprintf( stderr, "GL CALLBACK: %s type = 0x%x, severity = 0x%x, message = %s\n", ( type == GL_DEBUG_TYPE_ERROR ? "** GL ERROR **" : "" ), type, severity, message );}
static void glfwError(int id, const char* description){std::cout << description << std::endl;}


class SickOpenGL{
  public:
		GLFWwindow* window;

		const char* vshader = "vertex.glsl";
		const char* fshader = "fragment.glsl";

		int w_width = 1024, w_height = 768; 

		GLuint buff_size = w_width * w_height;
		GLsizeiptr buff_data_size = buff_size * sizeof(GLuint);

		GLuint tex, buf;

		GLuint image_unit = 0;

	SickOpenGL(){
		/* setup opengl */
		glEnable( GL_DEBUG_OUTPUT );
		glfwSetErrorCallback(&glfwError);

		glewExperimental = true; // Needed for core profile
		if( !glfwInit() )
		{
			fprintf( stderr, "Failed to initialize GLFW\n" );
			throw std::runtime_error("Failed to initialize GLFW.");
		}
	
		glfwWindowHint(GLFW_SAMPLES, 4); // antialiasing
		glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4); // 4.3
		glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
		glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
		glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

		window = glfwCreateWindow(w_width, w_height, 
						"Texture Buffer Counting Overlap", NULL, NULL);
		if( window == NULL ){
			fprintf(stderr, "Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible.\n");
			glfwTerminate();
			throw std::runtime_error("Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible.");
		}
		glfwMakeContextCurrent(window); 
		
		glewExperimental=true;
		if (glewInit() != GLEW_OK){
			fprintf(stderr, "Failed to initialize GLEW\n");
			throw std::runtime_error("Failed to initialize GLEW");
		}

		glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);

		glEnable              ( GL_DEBUG_OUTPUT );
		glDebugMessageCallback( MessageCallback, 0 );
	}

	void run(){
		/* count lines drawn per pixel */
		GLuint filler[buff_size] = {0}; // i dont think this is doing for every one lmao

		for(uint i = 0; i < buff_size; i++)
			filler[i] = 6;

		glGenBuffers(1, &buf);
		glBindBuffer(GL_TEXTURE_BUFFER, buf);
		glBufferData(GL_TEXTURE_BUFFER, buff_data_size, filler, GL_DYNAMIC_COPY);

	// just try to read from this buffer, any buffer really


		GLuint *initial = new GLuint[buff_size];
		glGetNamedBufferSubData(buf, 0, buff_data_size, initial);

		std::map<GLuint, uint> instance_counter;
		for (uint x = 0; x < buff_size; x++){
			GLuint value = initial[x];

			if(instance_counter.find(value) == instance_counter.end())
				instance_counter.insert(std::pair<GLuint, uint>(value, 0));


			instance_counter[value] += 1;
		}
		for(auto elem : instance_counter)
		  std::cout << elem.first << " " << elem.second << std::endl;

/*
		glGenTextures(1, &tex);

		glBindTexture(GL_TEXTURE_BUFFER, tex); 
		glTexBuffer(GL_TEXTURE_BUFFER, GL_R32UI, buf);

		glBindImageTexture(image_unit, tex, 0, GL_FALSE, 0, GL_READ_WRITE, GL_R32UI); 

		glfwDestroyWindow(window);*/
	}
	
	void convert_output(){
		/* Convert processed data to opencv mat. */
	// do I want to read the buffer or the whole image? buf/image_unit?
	}
};


int main(){
  SickOpenGL demo;

  demo.run(); 

  demo.convert_output();

  return 0;
}
