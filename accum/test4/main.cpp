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
		0.0f, -1.0f, 0.0
	};


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

	void run(){ /* goal tonight is to get basics working & cleanup */
		GLuint programID = LoadShaders("vertex.glsl", "atomic-counter1.glsl" );  // Create and compile our GLSL program from the shaders
/*		
	   // Atomic buffer creation
		GLuint atomicsBuffer;
		glGenBuffers(1, &atomicsBuffer);
		// bind buffer and define initial storage capacity
		glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, atomicsBuffer);
		glBufferData(GL_ATOMIC_COUNTER_BUFFER, sizeof(GLuint) * 3, NULL, GL_DYNAMIC_DRAW);
		// unbind buffer 
		glBindBuffer(GL_ATOMIC_COUNTER_BUFFER, 0);
*/
		do{
			//glUseProgram(programID);  // Use shader

			//clear color and depth buffer 
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
			glLoadIdentity();//load identity matrix
			
			glTranslatef(0.0f,0.0f,-4.0f);//move forward 4 units
			
			glColor3f(0.0f,0.0f,1.0f); //blue color
			
			glBegin(GL_POLYGON);//begin drawing of polygon
			glVertex3f(-0.5f,0.5f,0.0f);//first vertex
			glVertex3f(0.5f,0.5f,0.0f);//second vertex
			glVertex3f(1.0f,0.0f,0.0f);//third vertex
			glVertex3f(0.5f,-0.5f,0.0f);//fourth vertex
			glVertex3f(-0.5f,-0.5f,0.0f);//fifth vertex
			glVertex3f(-1.0f,0.0f,0.0f);//sixth vertex
			glEnd();//end drawing of polygon

			// Swap buffers
			glfwSwapBuffers(window);
			glfwPollEvents();

		} // Check if the ESC key was pressed or the window was closed
		while( glfwGetKey(window, GLFW_KEY_ESCAPE ) != GLFW_PRESS &&
			glfwWindowShouldClose(window) == 0 );
	}
};


// pg 581 on atomic adding to a specific coordinate


// Goal is to make atomic buffer that is the size of the image.
// Then for every x,y that gets a pixel written to, the 
// corresponding buffer can also be incremented.

// Currently there is just 3 counters, added to regardless of
// location.

//// Possible issues
// May be the case that the shader isn't binding to the atomic buffer.

//// Goals
// 1. Get the basic counters working.
// 2. Add to counters based on x,y rather than color.
// 3. Increase size of buffer to image size and increment when
// 	  fragment called at pixel
// 4. Output whole vector
// 5. Allow vertex input.

int main(){
  SickOpenGL demo;

  demo.run(); 

  return 0;
}
