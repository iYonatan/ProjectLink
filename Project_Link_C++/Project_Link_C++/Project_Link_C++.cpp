// Project_Link_C++.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <windows.h>
#include <iostream>

using namespace std;

int main()
{
	
	HANDLE hfile = CreateFileW(
		 L"test.txt",
		GENERIC_READ,
		0,
		NULL,
		CREATE_NEW,
		FILE_ATTRIBUTE_NORMAL,
		NULL);

	cout << "File has been created ! :) " << endl;
    return 0;
}

