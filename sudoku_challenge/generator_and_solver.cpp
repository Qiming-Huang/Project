#include<iostream>
#include<cstring>
#include<cstdlib>
#include<algorithm>
using namespace std;

int sudoku[9][9];
int show_sudoku[9][9];
bool flag = false;
int num[9] = {1,2,3,4,5,6,7,8,9};
int solution = 0;

bool check(int x,int y,int num){
    for(int i = 0; i < 9; i++){
        if(sudoku[i][y] == num&&i!=x){
            return false;
        }
        if(sudoku[x][i] == num&&i!=y){
            return false;
        }
    }
    int row = x/3;
    int col = y/3;
    for(int i = row*3; i < (row+1)*3; i++){
        for(int j = col*3; j < (col+1)*3; j++){
            if(num==sudoku[i][j]&&x!=i&&y!=j){
                return false;
            }
        }
    }
    return true;
}

void dfs(int step){
    if(flag){
        return ;
    }
    if(step==81){
        for(int i = 0; i < 9; i++){
            for(int j = 0; j < 9; j++) {
                show_sudoku[i][j] = sudoku[i][j];
            }
        }
        flag = true;
        return ;
    }else{
        int x = step/9;
        int y = step%9;
        if(sudoku[x][y]== 0){
            for(int i : num){
                if(check(x,y,i)){
                    sudoku[x][y] = i;
                    dfs(step+1);
                    sudoku[x][y] = 0;
                }
            }
        }else{
            dfs(step+1);
        }
    }
}

void get_randnum(){
    srand(unsigned(time(NULL)));
    random_shuffle(num,num+9);
}

void Dig_hold(){

    for(int i = 0; i < 3; i++){
        for(int j = 0; j < 3; j++){
            int n = rand()%9+1;
            int row = i*3;
            int col = j*3;
            while(n--){
                int  c = rand()%4;
                int  r = rand()%4;
                show_sudoku[row+c][col+r] = 0;
            }
        }
    }
}


bool check1(int x,int y,int num){
    for(int i = 0; i < 9; i++){
        if(show_sudoku[i][y] == num&&i!=x){
            return false;
        }
        if(show_sudoku[x][i] == num&&i!=y){
            return false;
        }
    }
    int row = x/3;
    int col = y/3;
    for(int i = row*3; i < (row+1)*3; i++){
        for(int j = col*3; j < (col+1)*3; j++){
            if(num==show_sudoku[i][j] && x!=i && y!=j ){
                return false;
            }
        }
    }
    return true;
}
void dfs2(int step) {
    if (step == 81) {
        solution++;
    }else{
        int x = step/9;
        int y = step%9;
        if(show_sudoku[x][y]== 0){
            for(int i : num){
                if(check1(x,y,i)){
                    show_sudoku[x][y] = i;
                    dfs2(step+1);
                    show_sudoku[x][y] = 0;
                }
            }
        }else{
            dfs2(step+1);
        }
    }
}

int main(){
    int count;
    cin>>count;
    while(count--){
        get_randnum();
        memset(sudoku,0,sizeof(sudoku));
        flag = false;
        dfs(0);
        Dig_hold();
        get_randnum();
        dfs2(0);
        if(solution !=1) break;
        cout<<"\n";
        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                cout<<show_sudoku[i][j]<<" ";
            }
            cout<<"\n";
        }
    }
    return 0;
}
