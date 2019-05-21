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

#include "shader_loader.h"

void GLAPIENTRY MessageCallback( GLenum source, GLenum type, GLuint id, GLenum severity, GLsizei length, const GLchar* message, const void* userParam ){fprintf( stderr, "GL CALLBACK: %s type = 0x%x, severity = 0x%x, message = %s\n", ( type == GL_DEBUG_TYPE_ERROR ? "** GL ERROR **" : "" ), type, severity, message );}
static void glfwError(int id, const char* description){std::cout << description << std::endl;}


class SickOpenGL{
  public:
		GLFWwindow* window;

		const char* vshader = "vertex.glsl";
		const char* fshader = "fragment_accumulator.glsl";

		int WIDTH = 1024, HEIGHT = 768; 

		GLuint BUFF_SIZE = WIDTH * HEIGHT;
		GLsizeiptr BUFF_DATA_SIZE = BUFF_SIZE * sizeof(GLuint);

		GLuint tex, buf;

		GLuint image_unit = 0;

		const int INT_PER_VERTEX = 3;

		GLuint VCOUNT, VSIZE;
		GLsizeiptr VERTEX_DATA_SIZE;
  		GLfloat *g_vertex_buffer_data;

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
	
		glfwWindowHint(GLFW_SAMPLES, 1); // antialiasing
		glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4); // 4.3
		glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
		glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
		glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

		window = glfwCreateWindow(WIDTH, HEIGHT, 
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

		glEnable              ( GL_DEBUG_OUTPUT );
		glDebugMessageCallback( MessageCallback, 0 );
	}

	void set_verticies(const GLuint vertex_count, GLfloat *values){
		/* 3 tuples, 2 sets makes a line. */
		VCOUNT = vertex_count;
		VSIZE = VCOUNT * INT_PER_VERTEX;
		VERTEX_DATA_SIZE = VSIZE * sizeof(GLfloat);

		g_vertex_buffer_data = new GLfloat[VSIZE];
		g_vertex_buffer_data = values;
	}

	void run(){
		/* count lines drawn per pixel */
		// Main data
		GLuint filler[BUFF_SIZE] = {0};

		glGenBuffers(1, &buf);
		glBindBuffer(GL_TEXTURE_BUFFER, buf);
		glBufferData(GL_TEXTURE_BUFFER, BUFF_DATA_SIZE, filler, GL_DYNAMIC_COPY);

		glGenTextures(1, &tex);

		glBindTexture(GL_TEXTURE_BUFFER, tex); 
		glTexBuffer(GL_TEXTURE_BUFFER, GL_R32UI, buf);

		glBindImageTexture(image_unit, tex, 0, GL_FALSE, 0, GL_READ_WRITE, GL_R32UI); 

		// Vertex buffer
		GLuint VertexArrayID;
		glGenVertexArrays(1, &VertexArrayID);
		glBindVertexArray(VertexArrayID);
		
		GLuint vertexbuffer;  
		glGenBuffers(1, &vertexbuffer);
		glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);  
		glBufferData(GL_ARRAY_BUFFER, VERTEX_DATA_SIZE, g_vertex_buffer_data, 
									GL_STATIC_DRAW);
		

		//do{
		// Process
		glClear( GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT);
		glClearColor(0.0f, 0.0f, 0.4f, 0.0f) ;

		glEnableVertexAttribArray(0);
		glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);

		glVertexAttribPointer(0, INT_PER_VERTEX, GL_FLOAT, GL_FALSE, 0, (void*)0);

 		GLuint programID = LoadShaders(vshader, fshader); 
		glUseProgram(programID);
		
		glDrawArrays(GL_LINES, 0, VCOUNT);

		glDisableVertexAttribArray(0);
	
		glfwSwapBuffers(window);


			glfwPollEvents();
		/*} while(glfwGetKey(window, GLFW_KEY_ESCAPE ) != GLFW_PRESS &&
						glfwWindowShouldClose(window) == 0);*/
	}
	
	void convert_output(){
		/* Convert processed data to opencv mat. */
	
		GLuint *initial = new GLuint[BUFF_SIZE];
		glGetNamedBufferSubData(buf, 0, BUFF_DATA_SIZE, initial);

		glfwDestroyWindow(window);


		std::map<GLuint, uint> instance_counter;
		for (uint x = 0; x < BUFF_SIZE; x++){
			GLuint value = initial[x];

			if(instance_counter.find(value) == instance_counter.end())
				instance_counter.insert(std::pair<GLuint, uint>(value, 0));


			instance_counter[value] += 1;

			/*if (value >1)
				std::cout << value << ": " << x << std::endl;*/
				// Proof I need antialiasing

		}
		for(auto elem : instance_counter)
		  std::cout << elem.first << " " << elem.second << std::endl;





	    // Convert to mat
		// vector -> mat
		cv::Mat finish(HEIGHT, WIDTH, CV_32S, cv::Scalar(0));  // S or F
		
		/*for (int i = 0; i < HEIGHT; i++){

			for (int j = 0; j < WIDTH; j++){
				finish.at<GLuint>(i, j) = initial[i*WIDTH + j];
				test.at<GLuint>(i, j) = 255;
			}
		}*
		
	
		cv::Mat one, two;
		cv::normalize(finish, one, 0, 1, cv::NORM_MINMAX);
    	
		std::cout << one.cols << ", " << one.rows << std::endl;
		std::cout << WIDTH << ", " << HEIGHT << std::endl;

		// width and height must be odd
    	//GaussianBlur( one, two, cv::Size(WIDTH - 1, HEIGHT - 1), 0, 0 );

/*
    	cv::imshow("ya boi", finish);
    	cv::waitKey(0);*/
		cv::Mat test(HEIGHT, WIDTH, CV_16UC1, cv::Scalar(65536));

		// pixel values need to be normalized relative to mat map type

    	cv::imshow("test", test);
    	cv::waitKey(0);

	}
};


int main(){
  SickOpenGL demo;

  const GLuint VCOUNT = 14;
  GLfloat verticies[VCOUNT*demo.INT_PER_VERTEX] = {
		-1.0f, -1.0f, 0.0f,
		1.0f, 1.0f, 0.0f,
		-1.0f,  1.0f, 0.0f,
		1.0f, -1.0f, 0.0f,
		-1.0f, 0.5f, 0.0f,
		1.0f,  0.5f, 0.0f,

		0.0f, 1.0f, 0.0f,
		0.0f, -1.0f, 0.0f,
		/*
		0.0f, 1.0f, 0.0f,
		0.0f, -1.0f, 0.0f,

		0.0f, 1.0f, 0.0f,
		0.0f, -1.0f, 0.0f,
		
	 	0.0f, 1.0f, 0.0f,
		0.0f, -1.0f, 0.0f	
		*/
		};
  demo.set_verticies(VCOUNT , verticies);

  demo.run(); 

  demo.convert_output();

  return 0;
}
