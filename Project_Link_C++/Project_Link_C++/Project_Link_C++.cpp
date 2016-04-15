// Project_Link_C++.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include "DLList.h"


using namespace std;
// Resource http://pastebin.com/LYgVEd5u
int main()
{
	DLList dll_list;
	dll_list.Create();
	dll_list.operator<<(cout);

    return 0;
}

