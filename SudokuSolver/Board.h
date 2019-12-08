#pragma once
#include <vector>

class Board {
public:
	Board(std::vector<std::vector<int>>);
	std::vector<std::vector<int>> solve();


private:
	std::vector<std::vector<int>> board_;
	std::vector<int> get_row(int row_num);
	std::vector<int> get_col(int col_num);
	std::vector<std::vector<int>> get_box(int row_num, int col_num);
	std::vector<int> find_next_empty();
	bool valid_option(int row_num, int col_num, int number);




};