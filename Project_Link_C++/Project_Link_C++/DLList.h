#include <string>
#include <Windows.h>
#include <map>

using namespace std;

class DLList
{

private:
	struct Info
	{
		string info[2];
	};

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

