#include <bits/stdc++.h>
using namespace std;
vector<long long> arr = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 111, 123, 135, 147, 159, 210, 222, 234, 246, 258, 321, 333, 345, 357, 369, 420, 432, 444, 456, 468, 531, 543, 555, 567, 579, 630, 642, 654, 666, 678, 741, 753, 765, 777, 789, 840, 852, 864, 876, 888, 951, 963, 975, 987, 999, 1111, 1234, 1357, 2222, 2345, 2468, 3210, 3333, 3456, 3579, 4321, 4444, 4567, 5432, 5555, 5678, 6420, 6543, 6666, 6789, 7531, 7654, 7777, 8642, 8765, 8888, 9630, 9753, 9876, 9999, 11111, 12345, 13579, 22222, 23456, 33333, 34567, 43210, 44444, 45678, 54321, 55555, 56789, 65432, 66666, 76543, 77777, 86420, 87654, 88888, 97531, 98765, 99999, 111111, 123456, 222222, 234567, 333333, 345678, 444444, 456789, 543210, 555555, 654321, 666666, 765432, 777777, 876543, 888888, 987654, 999999, 1111111, 1234567, 2222222, 2345678, 3333333, 3456789, 4444444, 5555555, 6543210, 6666666, 7654321, 7777777, 8765432, 8888888, 9876543, 9999999, 11111111, 12345678, 22222222, 23456789, 33333333, 44444444, 55555555, 66666666, 76543210, 77777777, 87654321, 88888888, 98765432, 99999999, 111111111, 123456789, 222222222, 333333333, 444444444, 555555555, 666666666, 777777777, 876543210, 888888888, 987654321, 999999999, 1111111111, 2222222222, 3333333333, 4444444444, 5555555555, 6666666666, 7777777777, 8888888888, 9876543210, 9999999999, 11111111111, 22222222222, 33333333333, 44444444444, 55555555555, 66666666666, 77777777777, 88888888888, 99999999999, 111111111111, 222222222222, 333333333333, 444444444444, 555555555555, 666666666666, 777777777777, 888888888888, 999999999999, 1111111111111, 2222222222222, 3333333333333, 4444444444444, 5555555555555, 6666666666666, 7777777777777, 8888888888888, 9999999999999, 11111111111111, 22222222222222, 33333333333333, 44444444444444, 55555555555555, 66666666666666, 77777777777777, 88888888888888, 99999999999999, 111111111111111, 222222222222222, 333333333333333, 444444444444444, 555555555555555, 666666666666666, 777777777777777, 888888888888888, 999999999999999, 1111111111111111, 2222222222222222, 3333333333333333, 4444444444444444, 5555555555555555, 6666666666666666, 7777777777777777, 8888888888888888, 9999999999999999, 11111111111111111, 22222222222222222, 33333333333333333, 44444444444444444, 55555555555555555, 66666666666666666, 77777777777777777, 88888888888888888, 99999999999999999, 111111111111111111};
int main() {
    long long X;
    cin>>X;
    for (long long& x : arr) {
        if (x>=X) {
            cout<<x<<endl;
            return 0;
        }
    }
}