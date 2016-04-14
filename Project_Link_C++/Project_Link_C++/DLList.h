#include <string>
#include <Windows.h>
#include <map>
#include <vector>

using namespace std;

class DLList
{
public:
	DLList();
	// -- Constructor --
	void Create();

	// -- Functions --
	bool is_PE(PIMAGE_DOS_HEADER  dosHeader);
	int x86_amd64(IMAGE_FILE_HEADER header);
	bool is_dll(IMAGE_FILE_HEADER header);
	int dll_size(HANDLE hDll);

	// -- Variables -- 
	const char PATH[20] = "c:\\Windows\\System32";
	map < string, string(*)[] > Dll_list;

	// -- Destructor --
	~DLList();
};

