//#include <opencv2/opencv.hpp>
#include <vector>
#include <iostream>
#include "Board.h"

void print(std::vector<std::vector<int>> thing)
{
  for ( auto row : thing )
  {
    for ( auto num : row )
      std::cout << num << " ";
    std::cout << std::endl;
  }
}

int main(int argc, char** argv)
{
  std::vector<std::vector<int>> puzzle, solution;
  puzzle.push_back(std::vector<int> {0,0,6, 0,7,0, 0,0,0});
  puzzle.push_back(std::vector<int> {5,7,0, 1,6,0, 0,0,0});
  puzzle.push_back(std::vector<int> {3,0,0, 0,5,0, 0,0,0});

  puzzle.push_back(std::vector<int> {0,0,0, 0,0,0, 7,0,0});
  puzzle.push_back(std::vector<int> {0,8,5, 0,0,2, 1,0,0});
  puzzle.push_back(std::vector<int> {0,0,0, 0,0,4, 0,6,0});

  puzzle.push_back(std::vector<int> {6,0,9, 0,0,0, 5,0,3});
  puzzle.push_back(std::vector<int> {0,0,0, 0,4,0, 0,8,0});
  puzzle.push_back(std::vector<int> {4,0,0, 0,0,0, 0,0,0});
  print(puzzle);
  Board b = Board(puzzle);
  solution = b.solve();
  print(solution);
}
