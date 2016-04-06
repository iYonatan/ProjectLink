// Project_Link_C++.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <windows.h>

using namespace std;
// Resource http://pastebin.com/LYgVEd5u
int main()
{

	HANDLE hMapObject, hFile;                        //File Mapping Object
	LPVOID lpBase;                                  //Pointer to the base memory of mapped file
	PIMAGE_DOS_HEADER dosHeader;                   //Pointer to DOS Header
	PIMAGE_NT_HEADERS ntHeader;                   //Pointer to NT Header
	IMAGE_FILE_HEADER header;                    //Pointer to image file header of NT Header
	IMAGE_OPTIONAL_HEADER opHeader;             //Optional Header of PE files present in NT Header structure
	// ReSharper disable once CppEntityNeverUsed
	PIMAGE_SECTION_HEADER pSecHeader;          //Section Header or Section Table Header

	// Open the DLL file
	hFile = CreateFile(L"AzSqlExt.dll", GENERIC_READ, FILE_SHARE_READ, nullptr, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);
	
	// Mapping the given dll file to memory
	hMapObject = CreateFileMapping(hFile, nullptr, PAGE_READONLY, 0, 0, nullptr);
	lpBase = MapViewOfFile(hMapObject, FILE_MAP_READ, 0, 0, 0);

	// Get DOS header
	dosHeader = PIMAGE_DOS_HEADER(lpBase); // 0x040000000

	// Check for valid DOS file
	if (dosHeader->e_magic == IMAGE_DOS_SIGNATURE) {

		//Dump the Dos Header info
		printf("\nValid Dos Exe File\n------------------\n");
		printf("\nDumping DOS Header Info....\n---------------------------");
		printf("\n%-36s%s ", "Magic number : ", dosHeader->e_magic == 0x5a4d ? "MZ" : "-");
		printf("\n%-36s%#x", "Bytes on last page of file :", dosHeader->e_cblp);
		printf("\n%-36s%#x", "Pages in file : ", dosHeader->e_cp);
		printf("\n%-36s%#x", "Relocation : ", dosHeader->e_crlc);
		printf("\n%-36s%#x", "Size of header in paragraphs : ", dosHeader->e_cparhdr);
		printf("\n%-36s%#x", "Minimum extra paragraphs needed : ", dosHeader->e_minalloc);
		printf("\n%-36s%#x", "Maximum extra paragraphs needed : ", dosHeader->e_maxalloc);
		printf("\n%-36s%#x", "Initial (relative) SS value : ", dosHeader->e_ss);
		printf("\n%-36s%#x", "Initial SP value : ", dosHeader->e_sp);
		printf("\n%-36s%#x", "Checksum : ", dosHeader->e_csum);
		printf("\n%-36s%#x", "Initial IP value : ", dosHeader->e_ip);
		printf("\n%-36s%#x", "Initial (relative) CS value : ", dosHeader->e_cs);
		printf("\n%-36s%#x", "File address of relocation table : ", dosHeader->e_lfarlc);
		printf("\n%-36s%#x", "Overlay number : ", dosHeader->e_ovno);
		printf("\n%-36s%#x", "OEM identifier : ", dosHeader->e_oemid);
		printf("\n%-36s%#x", "OEM information(e_oemid specific) :", dosHeader->e_oeminfo);
		printf("\n%-36s%#x\n", "RVA address of PE header : ", dosHeader->e_lfanew);
	} 
	else {
		printf("\nGiven File is not a valid DOS file\n");
		
	}

	// The offset of NT header is found at 0x3C location in the DOS header specified by e_lfanew
    //  Get the Base of NT Header(PE Header)  = dosHeader + RVA address of PE header
	ntHeader = PIMAGE_NT_HEADERS(DWORD(dosHeader)+(dosHeader->e_lfanew));

	// Identify for valid PE file
	if(ntHeader->Signature == IMAGE_NT_SIGNATURE){

		printf("\nValid PE file \n-------------\n");
		//Dump NT Header Info....
		printf("\nDumping COFF/PE Header Info....\n--------------------------------");
		printf("\n%-36s%s", "Signature :", "PE");


		//Get the IMAGE FILE HEADER Structure
		header = ntHeader->FileHeader;

		//Determine Machine Architechture
		printf("\n%-36s", "Machine Architechture :");
		switch (header.Machine) { //Only few are determined (for remaining refer to the above specification)
			case 0x0:    printf("All "); break;

			case 0x14d:  printf("Intel i860"); break;

			case 0x14c:  printf("Intel i386,i486,i586"); break; // 32 Bit

			case 0x200:  printf("Intel Itanium processor"); break;

			case 0x8664: printf("AMD x64"); break; // 64 Bit

			case 0x162:  printf("MIPS R3000"); break;

			case 0x166:  printf("MIPS R4000"); break;

			case 0x183:  printf("DEC Alpha AXP"); break;


			default:     printf("Not Found"); break;
		}
		//Determine the characteristics of the given file
		printf("\n%-36s", "Characteristics : ");
		if ((header.Characteristics & 0x0002) == 0x0002) printf("Executable Image ,");
		if ((header.Characteristics & 0x0020) == 0x0020) printf("Application can address > 2GB ,");
		if ((header.Characteristics & 0x1000) == 0x1000) printf("System file (Kernel Mode Driver(I think)) ,");
		if ((header.Characteristics & 0x2000) == 0x2000) printf("Dll file \n");
		if ((header.Characteristics & 0x4000) == 0x4000) printf("Application runs only in Uniprocessor ,");

		printf("\n%-36s%d", "Size of optional header :", header.SizeOfOptionalHeader);

		// Set optional header
		opHeader = ntHeader->OptionalHeader;
		printf("\n\nDumping PE Optional Header Info....\n-----------------------------------");
		
		//File size = (Size of code segment(.text) + Size of Initialized data)
		auto fileSize = opHeader.SizeOfCode + opHeader.SizeOfInitializedData;
		printf("\n%-36s%d Bytes\n", "Size of file  : ", fileSize);

	}

	 
	

	/*
	while (getline(reader, line)) {
		cout << line << endl;
	}*/
    return 0;
}

