// ColorTutorial.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <opencv2/opencv.hpp>
#include <string>

int main()
{
	std::cout << "Image File: ";
	std::string filename;
	std::cin >> filename;
	cv::Mat image = cv::imread(filename);
	if (!image.data) {
		std::cout << "Could not open the file!" << std::endl;
		return -1;
	}
	cv::Mat grayImage;
	cv::cvtColor(image, grayImage, cv::COLOR_BGR2GRAY);

}
