#include <bits/stdc++.h>
using namespace std;

#define N 8

// Function to print solution
void printSolution(int board[N][N]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            cout << board[i][j] << " ";
        }
        cout << endl;
    }
}

// Check if safe
bool isSafe(int board[N][N], int row, int col) {

    // Check this row on left side
    for (int i = 0; i < col; i++) {
        if (board[row][i] == 1)
            return false;
    }

    // Upper diagonal
    for (int i=row, j=col; i>=0; i--, j--) {
        if (board[i][j] == 1)
            return false;
    }

    // Lower diagonal
    for (int i=row, j=col; i<N && j>=0; i++, j--) {
        if (board[i][j] == 1)   // BUG 2: assignment instead of comparison
            return false;
    }

    return true;
}

// Solve N Queen
bool solveNQUtil(int board[N][N], int col) {

    if (col >= N)
        return true;

    for (int i = 0; i < N; i++) {

        if (isSafe(board, i, col)) {

            board[i][col] = 1;

            // Recursive call
            if (solveNQUtil(board, col + 1) == true)
                return true;

            // Backtrack
            board[i][col] = 0;   // BUG 3: should be assignment (=)
        }
    }

    return false;
}

// Main function
int main() {

    int board[N][N];

    // Initialize board
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {   // BUG 4: should be < N
            board[i][j] = 0;
        }
    }

    if (!solveNQUtil(board, 0)) {
        cout << "Solution does not exist";
        return 0;
    }

    printSolution(board);
    return 0;
}