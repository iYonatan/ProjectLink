#include "stdafx.h"
#include <Windows.h>
#include <iostream>
#include "DLList.h"
#include "dirent.h"
#include "General.h"

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

				if (General::is_PE(dosHeader)) {

					// The offset of NT header is found at 0x3C location in the DOS header specified by e_lfanew
				   //  Get the Base of NT Header(PE Header)  = dosHeader + RVA address of PE header
					ntHeader = PIMAGE_NT_HEADERS(DWORD(dosHeader) + (dosHeader->e_lfanew));

					// Identify for valid PE file
					if (ntHeader->Signature == IMAGE_NT_SIGNATURE) {

						//Get the IMAGE FILE HEADER Structure
						header = ntHeader->FileHeader;
						bool valid_dll = General::is_dll(header);
						int x86_or_amd64 = General::x86_amd64(header);
						if(valid_dll && (x86_or_amd64 == 32 || x86_or_amd64 == 64)){
							//string red [2] = { "asd", "asdasd" };
							//this->dll_list.insert(pair<string, string (*)[2]> (str, &red));

							// Set optional header
							opHeader = ntHeader->OptionalHeader;

							//File size = (Size of code segment(.text) + Size of Initialized data)
							auto fileSize = opHeader.SizeOfCode + opHeader.SizeOfInitializedData;
							// cout << str << "\t" << fileSize << "Bytes" << endl;

							Info dll_info = { to_string(fileSize), "" };
							this->Dll_list.insert(pair<string, Info>(str, dll_info));
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

ostream& DLList::operator<<(ostream& os)
{
	for (map<string, Info>::iterator it = this->Dll_list.begin(); it != this->Dll_list.end(); it++)
	{
		os << it->first << "\t" << it->second.info[0] << endl;
	}
	return os << "";
}

DLList::~DLList()
{
}

