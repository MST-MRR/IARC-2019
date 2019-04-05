#include <stdio.h>
#include <stdlib.h>
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
using namespace glm;

#include <iostream>
#include <stdexcept>
#include "loader.h"

#include <vector>

#include <opencv2/opencv.hpp>

#include <fstream>




static void glfwError(int id, const char* description)
{
  std::cout << description << std::endl;
}

class SickOpenGL{
  public:
	int w_width = 1024, w_height = 768; // need to change in fragment too

 	GLFWwindow* window;
	
	const int int_per_vertex = 3;

	GLuint v_count;
  	GLfloat *g_vertex_buffer_data;

	const char* vshader = "vertex.glsl";
	const char* fshader = "fragment.glsl";

	GLsizeiptr buff_size = w_width * w_height * 100;
	
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
		glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
		glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
		glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
		glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
		
		window = glfwCreateWindow(w_width, w_height, "Texture Buffer Counting Overlap", NULL, NULL);
		if( window == NULL ){
			fprintf( stderr, "Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible.\n" );
			glfwTerminate();
			throw std::runtime_error("Failed to open GLFW window. If you have an Intel GPU, they are not 3.3 compatible.");
		}
		glfwMakeContextCurrent(window); 
		
		glewExperimental=true;
		if (glewInit() != GLEW_OK) {
			fprintf(stderr, "Failed to initialize GLEW\n");
			throw std::runtime_error("Failed to initialize GLEW");
		}

		glfwSetInputMode(window, GLFW_STICKY_KEYS, GL_TRUE);
	}

	void set_verticies(const GLuint vertex_count, GLfloat *values){
		v_count = vertex_count;

		g_vertex_buffer_data = new GLfloat[v_count*int_per_vertex];
		g_vertex_buffer_data = values;
	}

	void run(){
		GLuint programID = LoadShaders(vshader, fshader);  

		GLuint VertexArrayID;
		glGenVertexArrays(1, &VertexArrayID);
		glBindVertexArray(VertexArrayID);
		
		GLuint vertexbuffer;  
		glGenBuffers(1, &vertexbuffer);
		glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);  
		glBufferData(GL_ARRAY_BUFFER, sizeof(GLfloat) * v_count * int_per_vertex, g_vertex_buffer_data, GL_STATIC_DRAW);

		GLuint tex, buf;

		glGenBuffers(1, &buf); 
		glBindBuffer(GL_TEXTURE_BUFFER, buf); 
		glBufferData(GL_TEXTURE_BUFFER, buff_size, NULL, GL_DYNAMIC_COPY); 

		glGenTextures(1, &tex);  
		glBindTexture(GL_TEXTURE_BUFFER, tex); 
		glTexBuffer(GL_TEXTURE_BUFFER, GL_R32UI, buf);  

		glBindImageTexture(0, tex, 0, GL_FALSE, 0, GL_READ_WRITE, GL_R32UI); 


		//
		do{
			glClear( GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT);
			glClearColor(0.0f, 0.0f, 0.4f, 0.0f) ;

			glEnableVertexAttribArray(0);
			glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);

			glVertexAttribPointer(0, int_per_vertex, GL_FLOAT, GL_FALSE, 0, (void*)0);

			glUseProgram(programID);
			
			glDrawArrays(GL_LINES, 0, v_count);

			glDisableVertexAttribArray(0);
		
			glfwSwapBuffers(window);
			glfwPollEvents();
		} while( glfwGetKey(window, GLFW_KEY_ESCAPE ) != GLFW_PRESS &&
			glfwWindowShouldClose(window) == 0 );
/**/
		
	}
	
	void convert_output(){
		// what data type is the buffer stored as?
		GLuint *data = new GLuint[buff_size];
		
		glGetBufferSubData(GL_TEXTURE_BUFFER, 0, buff_size, data);

		std::vector<std::vector<GLuint>> v;

		// create v as a 2d array from data
		for (int i = 0; i < w_height; i++){
			std::vector<GLuint> x;
			

			for (int j = 0; j < w_width; j++){
				x.push_back(data[i*w_width + w_height]);
			}

			v.push_back(x);
		}
	
		cv::Mat big_ole_mat(w_height, w_width, CV_64FC1);
		for(int i=0; i<big_ole_mat.rows; ++i)
			for(int j=0; j<big_ole_mat.cols; ++j)
				big_ole_mat.at<GLuint>(i, j) = v.at(i).at(j);

		std::cout << big_ole_mat.rows << std::endl;
		
		/*  Nonzero values do exist in the mat
		for(int i=0; i<big_ole_mat.rows; ++i)
			for(int j=0; j<big_ole_mat.cols; ++j){
				GLuint v = big_ole_mat.at<GLuint>(i, j);
				if (v){
					std::cout << v << std::endl;
				}
			}
		*/

		// currently broken
		std::vector<GLuint> ttt;
		 for(int i=0; i<big_ole_mat.rows; ++i){
			for(int j=0; j<big_ole_mat.cols; ++j){
				GLuint v = big_ole_mat.at<GLuint>(i, j);
				if (std::find(ttt.begin(), ttt.end(), v) == ttt.end()){
					std::cout << "\n\n" << v << "\n\n";
				}
				ttt.push_back(v);
			}
			std::cout << std::endl;
	   }
	/*
		cv::Mat dst;
		cv::normalize(big_ole_mat, dst, 0, 1, cv::NORM_MINMAX);
    cv::imshow("test", dst);
    cv::waitKey(0);*/
	
	}
};


int main(){
  SickOpenGL demo;
  
  const GLuint v_count = 14;
  GLfloat x[v_count*demo.int_per_vertex] = {
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
  demo.set_verticies(v_count , x);

  demo.run(); 

  demo.convert_output();

  return 0;
}
