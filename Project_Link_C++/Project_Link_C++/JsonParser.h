#include <iostream>
#include <map>
#include "General.h"
using namespace std;

#pragma once
class JsonParser
{
public:
	JsonParser();

	static string encode(map < string, General::Info > m);

	~JsonParser();
};

