#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <string>

int main()
{
	std::cout << "Image File: ";
	//std::string filename;
	//std::cin >> filename;
	std::string  filename = "../images/image19.jpg";
	cv::Mat image = cv::imread(filename);
	cv::Mat grayImage, threshImage, edges;
	if (!image.data) {
		std::cout << "Could not open the file!" << std::endl;
		return -1;
	}

	// Make our image binary and open/close to make readable
	cv::imshow("Monday", image);
	int rad = 1;
	cv::Mat element = cv::getStructuringElement(rad, cv::Size(2*rad+1,2*rad+1), cv::Point(rad,rad));
	cv::cvtColor(image, grayImage, cv::COLOR_BGR2GRAY);
	GaussianBlur(grayImage, grayImage, cv::Size(15, 15), 0);
	cv::adaptiveThreshold(grayImage, threshImage, 255, cv::ADAPTIVE_THRESH_GAUSSIAN_C, cv::THRESH_BINARY_INV, 15, 0);
	//cv::morphologyEx(threshImage, threshImage, cv::MORPH_OPEN, element);
	//cv::morphologyEx(threshImage, threshImage, cv::MORPH_CLOSE, element);
	cv::imshow("Taco", threshImage);

	// Find the outer Barrier and warp to a flat square. Then crop to the full puzzle image
	std::vector<cv::Point2f> squareCorners = { cv::Point2f(0,0), cv::Point2f(225,0), cv::Point2f(225,225) , cv::Point2f(0,225) };
	cv::Canny(threshImage, edges, 10, 100, 5);
	std::vector<std::vector<cv::Point> > contours;
	std::vector<cv::Point> square;
	std::vector<cv::Vec4i> hierarchy;
	cv::findContours(edges, contours, hierarchy, cv::RETR_TREE, cv::CHAIN_APPROX_NONE);
	cv::imshow("Tuesday", edges);
	cv::Scalar color = cv::Scalar(255, 255, 0);
	cv::approxPolyDP(contours.at(hierarchy[0][0]), square, 15, true);
	cv::imshow("Wednesday", image);
	cv::waitKey(0);
}
