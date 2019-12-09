#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <string>
#include <stdio.h>
#include <fdeep/fdeep.hpp>
#include "Board.h"

cv::Mat performImageActions(cv::Mat image) {
	cv::Mat threshImage;
	int rad = 5;
	cv::Mat element = cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(rad, rad));
	image.copyTo(threshImage);
	GaussianBlur(threshImage, threshImage, cv::Size(13, 13), 0);
	cv::adaptiveThreshold(threshImage, threshImage, 255, cv::ADAPTIVE_THRESH_GAUSSIAN_C, cv::THRESH_BINARY_INV, 15, 2);
	cv::fastNlMeansDenoising(threshImage, threshImage);

	return threshImage;
}

cv::Mat warpImageToCorners(cv::Mat threshImage, cv::Mat image) {
	cv::Mat edges;
	std::vector<cv::Point2f> squareCorners = { cv::Point2f(0,0), cv::Point2f(495,0), cv::Point2f(495,495) , cv::Point2f(0,495) };
	cv::Canny(threshImage, edges, 0, 50, 5);

	std::vector<std::vector<cv::Point> > contours;
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
 	cv::warpPerspective(image, image, transform, cv::Size(495, 495));



	return image;
}

bool checkNumber(cv::Mat image) {
	cv::Mat temp;
	image.copyTo(temp);
	std::vector<std::vector<cv::Point> > contours;
	std::vector<cv::Vec4i> hierarchy;
	
	cv::Canny(temp, temp, 0, 50, 5);
	cv::findContours(temp, contours, hierarchy, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_NONE);
	std::cout << cv::mean(image) << std::endl;
	if (cv::mean(image).val[0] > 10.0) {
		return true;
	}
	return false;
}

std::vector<std::vector<int>> findNumbers(cv::Mat image, fdeep::model model) {
	std::vector<std::vector<int>> board;
	
	for (int i = 0; i < 9; i++) {
		std::vector<int> row;
		for (int j = 0; j < 9; j++) {
			cv::Rect region = cv::Rect((j * 55), (i * 55) , 55, 55);
			cv::Mat number = cv::Mat(image, region);
			std::vector<float> numberVec;
			for (int k = 0; k < 55; k++) {
				for (int l = 0; l < 55; l++) {
					numberVec.push_back(((float)number.at<uchar>(k, l)) / 255);
				}
			}
			const fdeep::shared_float_vec data(fplus::make_shared_ref<fdeep::float_vec>(numberVec));
			fdeep::tensor5 input(fdeep::shape5(1, 1, 55, 55, 1), data);

			auto out = model.predict_class({ input });
			row.push_back(out);
		}
		board.push_back(row);
	}
	return board;
}

int main(){
	std::cout << "OpenCV version : " << CV_VERSION << std::endl;
	fdeep::model model = fdeep::load_model("out.json");

	while (true) {
		std::cout << "Image File: ";
		std::string filename;
		std::cin >> filename;

		cv::Mat image = cv::imread(filename, cv::IMREAD_GRAYSCALE);
		while (!image.data) {
			std::cout << "Could not open the file!" << std::endl;
			std::cout << "Image File: ";
			std::cin >> filename;
			image = cv::imread(filename, cv::IMREAD_GRAYSCALE);
		}

		// Make our image binary and open/close to make readable
		cv::Mat threshImage = performImageActions(image);

		// Find the outer Barrier and warp to a flat square. Then crop to the full puzzle image
		image = warpImageToCorners(threshImage, image);
		
		std::vector<std::vector<int>> sudoku = findNumbers(image, model);
		Board solver(sudoku);
		//std::cout << sudoku << std::endl;
		std::vector<std::vector<int>> solved = solver.solve();
		if (solved.size() == 9) {
			for (int i = 0; i < 9; i++) {
				std::cout << "-------------------" << std::endl;
				std::cout << "|";
				for (int j = 0; j < 9; j++) {
					std::cout << solved[i][j] << "|";
				}
				std::cout << std::endl;
			}
			std::cout << "-------------------" << std::endl;
		}
		else {
			std::cout << "Unable to solve puzzle!" << std::endl;
			std::cout << "This is what I saw" << std::endl;
			for (int i = 0; i < 9; i++) {
				std::cout << "-------------------" << std::endl;
				std::cout << "|";
				for (int j = 0; j < 9; j++) {
					std::cout << sudoku[i][j] << "|";
				}
				std::cout << std::endl;
			}
			std::cout << "-------------------" << std::endl;
		}
		
		cv::waitKey(0);
	}

	
	return 0;
}
