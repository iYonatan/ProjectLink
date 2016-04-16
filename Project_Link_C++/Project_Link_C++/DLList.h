#include <string>
#include <Windows.h>
#include <map>
#include "General.h"

using namespace std;

class DLList : public General
{

public:
	DLList();
	// -- Constructor --
	void Create();
	ostream& operator << (ostream& os);

	// -- Variables -- 
	const char PATH[20] = "c:\\Windows\\System32";
	map < string, Info > Dll_list;

	// -- Destructor --
	~DLList();
};

