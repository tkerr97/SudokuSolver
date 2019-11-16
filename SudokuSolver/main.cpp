#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <string>


cv::Mat performImageActions(cv::Mat image) {
	cv::Mat threshImage;
	int rad = 5;
	cv::Mat element = cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(rad, rad));
	cv::cvtColor(image, threshImage, cv::COLOR_BGR2GRAY);
	GaussianBlur(threshImage, threshImage, cv::Size(13, 13), 0);
	cv::adaptiveThreshold(threshImage, threshImage, 255, cv::ADAPTIVE_THRESH_GAUSSIAN_C, cv::THRESH_BINARY_INV, 15, 0);
	//cv::morphologyEx(threshImage, threshImage, cv::MORPH_OPEN, element);
	cv::morphologyEx(threshImage, threshImage, cv::MORPH_ERODE, element);
	

	return threshImage;
}

cv::Mat warpImageToCorners(cv::Mat threshImage, cv::Mat image) {
	cv::Mat edges;
	std::vector<cv::Point2f> squareCorners = { cv::Point2f(0,0), cv::Point2f(500,0), cv::Point2f(500,500) , cv::Point2f(0,500) };
	cv::Canny(threshImage, edges, 10, 100, 5);
	std::vector<std::vector<cv::Point> > contours;
	std::vector<cv::Point> square;
	std::vector<cv::Vec4i> hierarchy;
	cv::findContours(edges, contours, hierarchy, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_NONE);

	double max = 0;
	std::vector<cv::Point> bigContour;
	for (int i = 0; i < contours.size(); i++) {
		if (cv::contourArea(contours[i]) > max) {
			bigContour = contours[i];
			max = cv::contourArea(bigContour);
		}
	}

	cv::Rect2d border = cv::boundingRect(bigContour);
	cv::Point2f tr = cv::Point2f(border.tl().x + border.width, border.tl().y), bl = cv::Point2f(border.tl().x, border.tl().y + border.height);
	std::vector<cv::Point2f> corners = {border.tl(), tr, border.br(), bl};
	cv::Mat transform = cv::getPerspectiveTransform(corners, squareCorners);
	cv::warpPerspective(image, image, transform, cv::Size(500, 500));
	
	return image;
}

int main()
{
	std::cout << "Image File: ";
	//std::string filename;
	//std::cin >> filename;
	std::string  filename = "../images/image25.jpg";

	cv::Mat image = cv::imread(filename);
	
	if (!image.data) {
		std::cout << "Could not open the file!" << std::endl;
		return -1;
	}

	cv::imshow("Monday", image);

	// Make our image binary and open/close to make readable
	cv::Mat threshImage = performImageActions(image);

	// Find the outer Barrier and warp to a flat square. Then crop to the full puzzle image
	image = warpImageToCorners(threshImage, image);

	cv::imshow("Wednesday", image);
	cv::waitKey(0);
}
