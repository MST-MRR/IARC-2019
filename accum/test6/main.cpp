#include <stdio.h>
#include <stdlib.h>
// Include glew before gl.h and glfw3.h
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
using namespace glm;

#include <iostream>
#include <stdexcept>
#include "loader.h"

// pragma debug thing in shaders for debug mode

// shared value in texture is shared between program and shader
static void glfwError(int id, const char* description)
{
  std::cout << description << std::endl;
}


/*

**
*
**
*
*  Goal is to render a texture I create to visualize if atomic
*  add is having any effect
*
*
*
**
*/



class SickOpenGL{
  private:
 	GLFWwindow* window;
	static const GLuint v_count = 14;
  	const GLfloat g_vertex_buffer_data[v_count*3] = {
		-1.0f, -1.0f, 0.0f,
		1.0f, 1.0f, 0.0f,
		-1.0f,  1.0f, 0.0f,
		1.0f, -1.0f, 0.0f,
		-1.0f, 0.5f, 0.0f,
		1.0f,  0.5f, 0.0f,

		0.0f, 1.0f, 0.0f,
		0.0f, -1.0f, 0.0f,

		0.0f, 1.0f, 0.0f,
		0.0f, -1.0f, 0.0f,
		
		0.0f, 1.0f, 0.0f,
		0.0f, -1.0f, 0.0f,
		
		0.0f, 1.0f, 0.0f,
		0.0f, -1.0f, 0.0f
	
	};

	const char* vshader = "vertex.glsl";
	const char* fshader = "fragment.glsl";

  public:
	SickOpenGL(){
		glEnable( GL_DEBUG_OUTPUT );
		glfwSetErrorCallback(&glfwError);

		// Init GLFW
		glewExperimental = true; // Needed for core profile
		if( !glfwInit() )
		{
			fprintf( stderr, "Failed to initialize GLFW\n" );
			throw std::runtime_error("Failed to initialize GLFW.");
		}
	
		glfwWindowHint(GLFW_SAMPLES, 4); // 4x antialiasing
		glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4); // We want OpenGL 3.3
		glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
		glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); // To make MacOS happy
		glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE); // We don't want the old OpenGL 

		// Open window & add OpenGL context
		
		window = glfwCreateWindow( 1024, 768, "Texture Accumulating Arbitrary Values", NULL, NULL);
		if( window == NULL ){
			fprintf( stderr, "Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible.\n" );
			glfwTerminate();
			throw std::runtime_error("Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible.");
		}
		glfwMakeContextCurrent(window); // Initialize GLEW
		
		glewExperimental=true; // Needed in core profile
		if (glewInit() != GLEW_OK) {
			fprintf(stderr, "Failed to initialize GLEW\n");
			throw std::runtime_error("Failed to initialize GLEW");
		}

		// Ensure can capture escape key press
		glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);
	}

	void run(){
		GLuint programID = LoadShaders(vshader, fshader);  // Create and compile our GLSL program from the shaders

		GLuint VertexArrayID;
		glGenVertexArrays(1, &VertexArrayID);
		glBindVertexArray(VertexArrayID);
		
		GLuint vertexbuffer;  // Identifies vertex buffer
		glGenBuffers(1, &vertexbuffer);  // Generate 1 buffer, & store identifier in vertexbuffer
		glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);  // The following commands will talk about our 'vertexbuffer' buffer
		
		// Give vertices to OpenGL.
		glBufferData(GL_ARRAY_BUFFER, sizeof(g_vertex_buffer_data), g_vertex_buffer_data, GL_STATIC_DRAW);

//https://learnopengl.com/Advanced-OpenGL/Framebuffers

unsigned int fbo;
glGenFramebuffers(1, &fbo);

glBindFramebuffer(GL_FRAMEBUFFER, fbo);  

//if(glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE)

glBindFramebuffer(GL_FRAMEBUFFER, 0);

glBindFramebuffer(GL_FRAMEBUFFER, 0);

glDeleteFramebuffers(1, &fbo);  


unsigned int texture;
glGenTextures(1, &texture);
glBindTexture(GL_TEXTURE_2D, texture);
  
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 800, 600, 0, GL_RGB, GL_UNSIGNED_BYTE, NULL);

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);  

glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture, 0);


glTexImage2D(
  GL_TEXTURE_2D, 0, GL_DEPTH24_STENCIL8, 800, 600, 0, 
  GL_DEPTH_STENCIL, GL_UNSIGNED_INT_24_8, NULL
);

glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_TEXTURE_2D, texture, 0);


unsigned int rbo;
glGenRenderbuffers(1, &rbo);

glBindRenderbuffer(GL_RENDERBUFFER, rbo);

glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, 800, 600);

glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, rbo);

unsigned int framebuffer;
glGenFramebuffers(1, &framebuffer);
glBindFramebuffer(GL_FRAMEBUFFER, framebuffer);    

// generate texture
unsigned int texColorBuffer;
glGenTextures(1, &texColorBuffer);
glBindTexture(GL_TEXTURE_2D, texColorBuffer);
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 800, 600, 0, GL_RGB, GL_UNSIGNED_BYTE, NULL);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR );
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
glBindTexture(GL_TEXTURE_2D, 0);

// attach it to currently bound framebuffer object
glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texColorBuffer, 0);

unsigned int rbo;
glGenRenderbuffers(1, &rbo);
glBindRenderbuffer(GL_RENDERBUFFER, rbo); 
glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, 800, 600);  
glBindRenderbuffer(GL_RENDERBUFFER, 0);

glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, rbo);

if(glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE)
	std::cout << "ERROR::FRAMEBUFFER:: Framebuffer is not complete!" << std::endl;
glBindFramebuffer(GL_FRAMEBUFFER, 0);  




		do{
			// Counting is done in texture or associated buffer.
			// TODO Why is it not double counting overlaps

			// Clear screen
			glClear( GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT);
			glClearColor(0.0f, 0.0f, 0.4f, 0.0f) ;

			// Set vertex buffer
			// 1st attribute buffer : vertices
			glEnableVertexAttribArray(0);
			glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);

			glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, (void*)0);

			
/*
			// Draw
			glDrawArrays(GL_LINES, 0, v_count); // Starting from vertex 0; 3 vertices total -> 1 triangle
			glDisableVertexAttribArray(0);

			// Swap buffers
			glfwSwapBuffers(window);
			glfwPollEvents();*/

// first pass
glBindFramebuffer(GL_FRAMEBUFFER, framebuffer);
glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); // we're not using the stencil buffer now
glEnable(GL_DEPTH_TEST);
glfwSwapBuffers(window);// DrawScene();	
  
// second pass
glBindFramebuffer(GL_FRAMEBUFFER, 0); // back to default
glClearColor(1.0f, 1.0f, 1.0f, 1.0f); 
glClear(GL_COLOR_BUFFER_BIT);
  
glUseProgram(programID);  // Use shader   screenShader.use();  
glBindVertexArray(vertexbuffer);
glDisable(GL_DEPTH_TEST);

glActiveTexture(GL_TEXTURE0);
//glBindTexture(GL_TEXTURE_2D, textureColorbuffer);
glDrawArrays(GL_TRIANGLES, 0, 6);  


		} // Check if the ESC key was pressed or the window was closed
		while( glfwGetKey(window, GLFW_KEY_ESCAPE ) != GLFW_PRESS &&
			glfwWindowShouldClose(window) == 0 );
	}
};

int main(){
  SickOpenGL demo;

  demo.run(); 

  return 0;
}
