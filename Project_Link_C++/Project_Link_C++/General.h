#include <iostream>
#include <Windows.h>

using namespace std;

#pragma once
class General
{

public:

	// -- Constructor --
	General();

	// -- Structures -- 
	struct Info{ string info[2]; };
	
	// -- Destructor --
	~General();
protected:

	static bool is_PE(PIMAGE_DOS_HEADER  dosHeader);

	static int x86_amd64(IMAGE_FILE_HEADER header);

	static bool is_dll(IMAGE_FILE_HEADER header);

};


