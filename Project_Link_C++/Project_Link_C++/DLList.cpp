#include "stdafx.h"
#include <Windows.h>
#include <iostream>
#include "DLList.h"
#include "dirent.h"


using namespace std;

DLList::DLList()
{
}

void DLList::Create()
{
	// Variables defination
	struct DIR *dir;
	struct dirent *ent;

	// Folder existence
	if ((dir = opendir(this->PATH)) != nullptr) {

		while ((ent = readdir(dir)) != nullptr) {

			HANDLE hMapObject, hFile;                        //File Mapping Object
			LPVOID lpBase;                                  //Pointer to the base memory of mapped file
			PIMAGE_DOS_HEADER dosHeader;                   //Pointer to DOS Header
			PIMAGE_NT_HEADERS ntHeader;                   //Pointer to NT Header
			IMAGE_FILE_HEADER header;                    //Pointer to image file header of NT Header
			IMAGE_OPTIONAL_HEADER opHeader;             //Optional Header of PE files present in NT Header structure
			PIMAGE_SECTION_HEADER pSecHeader;          //Section Header or Section Table Header

			// Convert from char[] to string 
			string str(ent->d_name);
			string path(this->PATH);

			// Concatenation of full dll's path:  DLL path + \ + DLL name
			string full_path = path + "\\" + ent->d_name;

			// Convert from string to wchar_t
			auto widestr = std::wstring(full_path.begin(), full_path.end());
			auto dll_name = widestr.c_str();

			// Create a file handle in windows API
			hFile = CreateFile(dll_name, GENERIC_READ, FILE_SHARE_READ, nullptr, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);


			// Mapping the given dll file to memory
			hMapObject = CreateFileMapping(hFile, nullptr, PAGE_READONLY, 0, 0, nullptr);
			lpBase = MapViewOfFile(hMapObject, FILE_MAP_READ, 0, 0, 0);

			// Get DOS header
			dosHeader = PIMAGE_DOS_HEADER(lpBase); // 0x040000000

			// Check for valid DOS file
			if (dosHeader != nullptr && dosHeader->e_magic == IMAGE_DOS_SIGNATURE) {

				if (this->is_PE(dosHeader)) {

					// The offset of NT header is found at 0x3C location in the DOS header specified by e_lfanew
				   //  Get the Base of NT Header(PE Header)  = dosHeader + RVA address of PE header
					ntHeader = PIMAGE_NT_HEADERS(DWORD(dosHeader) + (dosHeader->e_lfanew));

					// Identify for valid PE file
					if (ntHeader->Signature == IMAGE_NT_SIGNATURE) {

						//Get the IMAGE FILE HEADER Structure
						header = ntHeader->FileHeader;
						bool valid_dll = this->is_dll(header);
						int x86_or_amd64 = this->x86_amd64(header);
						if(valid_dll && (x86_or_amd64 == 32 || x86_or_amd64 == 64)){
							//string red [2] = { "asd", "asdasd" };
							//this->dll_list.insert(pair<string, string (*)[2]> (str, &red));

							// Set optional header
							opHeader = ntHeader->OptionalHeader;

							//File size = (Size of code segment(.text) + Size of Initialized data)
							auto fileSize = opHeader.SizeOfCode + opHeader.SizeOfInitializedData;
							cout << str << "\t" << fileSize << "Bytes" << endl;
						}
					}
				}
				else {
					printf("\nGiven File is not a valid DOS file\n");

				}
			}
			
		}
		closedir(dir);
	}
}

bool DLList::is_PE(PIMAGE_DOS_HEADER  dosHeader)
{
	if (dosHeader->e_magic == 0x5a4d) {
		return true;
	}
	else {
		return false;
	}
}

int DLList::x86_amd64(IMAGE_FILE_HEADER header)
{
	switch (header.Machine) { 
		//Only few are determined (for remaining refer to the above specification)
		case 0x14c:  return 32; break; // 32 Bit
		case 0x8664: return 64; break; // 64 Bit

		default:     return 0; break;
	}
}

bool DLList::is_dll(IMAGE_FILE_HEADER header)
{
	if ((header.Characteristics & 0x2000) == 0x2000) return true;

	return false;
}


DLList::~DLList()
{
}

