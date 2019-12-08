//#include <opencv2/opencv.hpp>
#include <vector>
#include <iostream>
#include "Board.h"
Board::Board(std::vector<std::vector<int>> b)
{
    board_ = b;
}

std::vector<int> Board::get_row(int row_num)
{
    return board_.at(row_num);
}

std::vector<int> Board::get_col(int col_num)
{
    std::vector<int> col;
    for (auto row : board_)
    {
        col.push_back(row.at(col_num));
    }
    return col;
}

std::vector<std::vector<int>> Board::get_box(int row_num, int col_num)
{
    std::vector<std::vector<int>> box;
    box.push_back(std::vector<int>());
    box.push_back(std::vector<int>());
    box.push_back(std::vector<int>());
    int base_row = 3 * (int)(row_num / 3);
    int base_col = 3 * (int)(col_num / 3);
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            box.at(i).push_back(board_.at(base_row + i).at(base_col + j));
        }
    }
    return box;
}

// a 2 long int vector. 1st is row, 2nd is col
std::vector<int> Board::find_next_empty()
{
    std::vector<int> location;
    location.push_back(-1);
    location.push_back(-1);
    for (int i = 0; i < 9; i++) //row
    {
        for (int j = 0; j < 9; j++) //col
        {
            if (board_.at(i).at(j) == 0) {
                location.at(0) = i;
                location.at(1) = j;
                return location;
            }
        }
    }
    return location;
}

bool Board::valid_option(int row_num, int col_num, int number)
{
    if (board_.at(row_num).at(col_num) != 0)
        return false;
    std::vector<int> row = get_row(row_num);
    for (int num : row)
    {
        if (num == number)
            return false;
    }
    std::vector<int> col = get_col(col_num);
    for (int num : col)
    {
        if (num == number)
            return false;
    }
    std::vector<std::vector<int>> box = get_box(row_num, col_num);
    for (auto row : box)
    {
        for (int num : row)
        {
            if (num == number)
                return false;
        }
    }
    return true;
}

std::vector<std::vector<int>> Board::solve()
{
    std::vector<int> next = find_next_empty();
    //print();
    //std::cout << std::endl << next.at(0) << " " << next.at(1) << std::endl << std::endl;
    // Base case, if nothing is empty so we are done!
    if (next.at(0) == -1)
        return board_;
    if (next.at(1) == -1)
        return board_;
    // Check all valid options in ext empty
    for (int number = 1; number <= 9; number++)
    {
        // If that number is currently valid
        if (valid_option(next.at(0), next.at(1), number))
        {
            std::vector<std::vector<int>> temp = board_;
            temp.at(next.at(0)).at(next.at(1)) = number;
            Board next_board = Board(temp);
            //next_board.print();
            temp = next_board.solve();
            // If it returns the complete puzzle then we are done!
            if (temp.size() == 9)
                return temp;
        }
    }
    // If we didn't find any valid option
    std::vector<std::vector<int>> temp;
    temp.push_back(std::vector<int>());
    temp.at(0).push_back(-1);
    return temp;
}

void Board::print()
{
  for ( auto row : board_ )
  {
    for ( auto num : row )
      std::cout << num << " ";
    std::cout << std::endl;
  }
}
