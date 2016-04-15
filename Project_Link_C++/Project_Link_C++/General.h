#include <Windows.h>
#pragma once
class General
{
public:
	General();

	static bool is_PE(PIMAGE_DOS_HEADER  dosHeader);
	static int x86_amd64(IMAGE_FILE_HEADER header);
	static bool is_dll(IMAGE_FILE_HEADER header);
	
	~General();
};

