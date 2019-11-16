#include <iostream>
#include <fstream>
#include <string>
#include <sstream> 

int main() {
	std::ofstream out("data.txt");
	for (int i = 0; i < 1089; i++) {
		std::string filename = "../images/image" + std::to_string(i) + ".dat";
		std::ifstream file(filename);
		if (file.good()) {
			std::string line1;
			std::getline(file, line1);
			std::getline(file, line1);
			std::istringstream str(std::string line);
			for (std::string line; std::getline(file, line);) {
				std::istringstream str(line);
				for (std::string word; str >> word;) {
					if (word.compare("\n") != 0) {
						out << word << ',';
					}
				}
			}
		}
		else {
			continue;
		}
	}
	return 1;
}