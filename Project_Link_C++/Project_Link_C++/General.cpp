#include "stdafx.h"
#include "General.h"


General::General()
{
}

bool General::is_PE(PIMAGE_DOS_HEADER dosHeader)
{
	if (dosHeader->e_magic == 0x5a4d) {
		return true;
	}
	else {
		return false;
	}
}

int General::x86_amd64(IMAGE_FILE_HEADER header)
{
	switch (header.Machine) {
		//Only few are determined (for remaining refer to the above specification)
	case 0x14c:  return 32; break; // 32 Bit
	case 0x8664: return 64; break; // 64 Bit

	default:     return 0; break;
	}
}

bool General::is_dll(IMAGE_FILE_HEADER header)
{
	if ((header.Characteristics & 0x2000) == 0x2000) return true;

	return false;
}

General::~General()
{
}
