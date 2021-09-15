/* Copyright 2013 Simon Opelt and Clemens Birklbauer. All rights reserved.
 * For license and copyright information see license.txt of LFC2013.
 */
#pragma once

#include <string>
#include <vector>
#include <glm/glm.hpp>


// predeclaration
class AOS;

class AOSGenerator // Universal & Unstructured LF Generator: takes care of loading the light field
{
private:
	bool hasVideoData = false;
	std::vector<std::string> cameraNames;
public:
	AOSGenerator(void);
	virtual ~AOSGenerator(void);
	void Generate( AOS *aos, const std::string &jsonPoseFile, const std::string &imgFilePath = "", const std::string& maskFile = "", const bool replaceExtension = false);
	bool isVideoDataAvailable(void) { return hasVideoData; };
	auto getCameraNames(void) const { return cameraNames; };
};


